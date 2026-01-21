import os
import json
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input
from django.conf import settings

# ===================== CONFIGURATION =====================

# ✅ Correct last convolutional layer for EfficientNet
LAST_CONV_LAYER = "top_conv"

# Singleton resources
_model = None
_class_names = None

# ===================== RESOURCE LOADER =====================

def load_resources():
    global _model, _class_names

    if _model is None:
        try:
            print(f"Loading AI Model from: {settings.MODEL_PATH}")
            _model = load_model(settings.MODEL_PATH)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Model loading failed: {e}")
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
                    k for k, v in sorted(indices.items(), key=lambda item: item[1])
                ]
        except Exception as e:
            print(f"❌ class_indices.json loading failed: {e}")
            return False

    return True

# ===================== GRAD-CAM =====================

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    try:
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(last_conv_layer_name).output,
                model.output
            ]
        )
    except ValueError:
        print("❌ Invalid Grad-CAM layer name")
        return None

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        pred_index = tf.argmax(predictions[0])
        class_channel = predictions[:, pred_index]

    grads = tape.gradient(class_channel, conv_outputs)

    # Global Average Pooling
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]

    # Weighted feature maps
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    # ReLU + numerical stability
    heatmap = tf.maximum(heatmap, 0)
    max_val = tf.reduce_max(heatmap) + 1e-8
    heatmap /= max_val

    return heatmap.numpy()

# ===================== HEATMAP SAVING =====================

def save_heatmap_image(original_img_path, heatmap, filename):
    img = cv2.imread(original_img_path)  # BGR
    if img is None:
        return None

    # ✅ Resize heatmap FIRST
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Overlay
    superimposed_img = cv2.addWeighted(
        img, 0.6,
        heatmap, 0.4,
        0
    )

    save_dir = os.path.join(settings.MEDIA_ROOT, "heatmaps")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, f"heatmap_{filename}")
    cv2.imwrite(save_path, superimposed_img)

    return f"/media/heatmaps/heatmap_{filename}"

# ===================== MAIN PREDICTION =====================

def predict_image(img_path):
    if not load_resources():
        return {"error": "AI resources failed to load"}

    try:
        # ---------- Preprocessing ----------
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)

        # ---------- Prediction ----------
        predictions = _model.predict(img_array)
        predicted_index = np.argmax(predictions)
        confidence = float(predictions[0][predicted_index]) * 100
        diagnosis = _class_names[predicted_index]

        # ---------- Explainability ----------
        heatmap_url = None
        heatmap = make_gradcam_heatmap(
            img_array,
            _model,
            LAST_CONV_LAYER
        )

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
