import os
import json
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from django.conf import settings

# =====================================================
# CONFIGURATION
# =====================================================

LAST_CONV_LAYER = "top_conv"  # Correct for EfficientNet

_model = None
_class_names = None

# =====================================================
# LOAD MODEL & CLASSES (Singleton)
# =====================================================

def load_resources():
    global _model, _class_names

    if _model is None:
        try:
            _model = load_model(settings.MODEL_PATH)
            print("✅ Model loaded")
        except Exception as e:
            print("❌ Model load failed:", e)
            return False

    if _class_names is None:
        try:
            json_path = os.path.join(
                settings.BASE_DIR,
                "ml_engine",
                "models",
                "class_indices.json"
            )
            with open(json_path, "r") as f:
                indices = json.load(f)
                _class_names = [
                    k for k, v in sorted(indices.items(), key=lambda x: x[1])
                ]
        except Exception as e:
            print("❌ Class index load failed:", e)
            return False

    return True

# =====================================================
# GRAD-CAM++ (STABLE TENSORFLOW VERSION)
# =====================================================

def make_gradcam_plus_plus(img_array, model, last_conv_layer_name):
    """
    TensorFlow-safe Grad-CAM++ (no higher-order gradients)
    """

    grad_model = tf.keras.models.Model(
        inputs=model.inputs,
        outputs=[
            model.get_layer(last_conv_layer_name).output,
            model.output
        ]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        pred_index = tf.argmax(predictions[0])
        class_score = predictions[:, pred_index]

        # Explicitly watch conv feature maps
        tape.watch(conv_outputs)

        grads = tape.gradient(class_score, conv_outputs)

    # Remove batch dimension
    conv_outputs = conv_outputs[0]
    grads = grads[0]

    # Positive gradients
    positive_grads = tf.maximum(grads, 0)

    # Grad-CAM++ weights (stable approximation)
    weights = tf.reduce_sum(
        positive_grads,
        axis=(0, 1)
    )

    # Weighted sum
    cam = tf.reduce_sum(
        weights * conv_outputs,
        axis=-1
    )

    # Normalize
    cam = tf.maximum(cam, 0)
    cam /= tf.reduce_max(cam) + 1e-8

    return cam.numpy()

# =====================================================
# HEATMAP GENERATION & SAVE
# =====================================================

def save_heatmap_image(original_img_path, heatmap, filename):
    img = cv2.imread(original_img_path)  # BGR
    if img is None:
        return None

    # Resize heatmap FIRST
    heatmap = cv2.resize(
        heatmap,
        (img.shape[1], img.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    # Overlay
    superimposed_img = cv2.addWeighted(
        img, 0.6,
        heatmap, 0.4,
        0
    )

    save_dir = os.path.join(settings.MEDIA_ROOT, "heatmaps")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(
        save_dir,
        f"heatmap_{filename}"
    )

    cv2.imwrite(save_path, superimposed_img)

    return f"/media/heatmaps/heatmap_{filename}"

# =====================================================
# MAIN PREDICTION FUNCTION
# =====================================================

def predict_image(img_path):
    if not load_resources():
        return {"error": "AI resources failed to load"}

    try:
        # -------- Preprocess --------
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # -------- Prediction --------
        preds = _model.predict(img_array)
        pred_idx = np.argmax(preds)
        confidence = float(preds[0][pred_idx]) * 100
        diagnosis = _class_names[pred_idx]

        # -------- Grad-CAM++ --------
        heatmap = make_gradcam_plus_plus(
            img_array,
            _model,
            LAST_CONV_LAYER
        )

        heatmap_url = None
        if heatmap is not None:
            filename = os.path.basename(img_path)
            heatmap_url = save_heatmap_image(
                img_path,
                heatmap,
                filename
            )

        return {
            "diagnosis": diagnosis,
            "confidence": round(confidence, 2),
            "heatmap_url": heatmap_url
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
