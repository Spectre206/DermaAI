import os
import json
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.conf import settings
from django.core.files.storage import default_storage

# --- CONFIGURATION ---

LAST_CONV_LAYER = "top_activation"  

# Global variables
_model = None
_class_names = None

def load_resources():
    """Loads Model and Class Indices (Singleton Pattern)"""
    global _model, _class_names
    
    if _model is None:
        try:
            print(f"Loading AI Model from: {settings.MODEL_PATH}...")
            _model = load_model(settings.MODEL_PATH)
            print("Model loaded!")
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    if _class_names is None:
        json_path = os.path.join(settings.BASE_DIR, 'ml_engine', 'models', 'class_indices.json')
        try:
            print(f"Loading Class Indices from: {json_path}...")
            with open(json_path, 'r') as f:
                indices = json.load(f)
                _class_names = [k for k, v in sorted(indices.items(), key=lambda item: item[1])]
            print(f"Class Labels: {_class_names}")
        except Exception as e:
            print(f"Error loading class_indices.json: {e}")
            return False
            
    return True

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    """Generates the heatmap tensor"""
    try:
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[model.get_layer(last_conv_layer_name).output, model.output]
        )
    except ValueError:
        print(f"Layer '{last_conv_layer_name}' not found. Cannot generate Heatmap.")
        return None

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_heatmap_image(original_img_path, heatmap, filename):
    """Overlays heatmap on original image and saves it"""
    # 1. Read original image
    img = cv2.imread(original_img_path)
    if img is None: return None
    
    # 2. Resize heatmap to match image
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # 3. Overlay (0.4 is transparency intensity)
    superimposed_img = heatmap * 0.4 + img
    
    # 4. Save to 'media/heatmaps/'
    save_dir = os.path.join(settings.MEDIA_ROOT, 'heatmaps')
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, f"heatmap_{filename}")
    cv2.imwrite(save_path, superimposed_img)
    
    # Return relative URL for the API
    return f"/media/heatmaps/heatmap_{filename}"

def predict_image(img_path):
    if not load_resources():
        return {"error": "AI Resources failed to load"}

    try:
        # 1. Preprocess
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        # 2. Predict
        predictions = _model.predict(img_array)
        predicted_index = np.argmax(predictions)
        confidence = float(np.max(predictions)) * 100
        diagnosis = _class_names[predicted_index]
        
        # 3. Generate Explainability (Grad-CAM)
        heatmap_url = None
        heatmap = make_gradcam_heatmap(img_array, _model, LAST_CONV_LAYER)
        
        if heatmap is not None:
            # Get original filename to name the heatmap
            filename = os.path.basename(img_path)
            heatmap_url = save_heatmap_image(img_path, heatmap, filename)

        return {
            "diagnosis": diagnosis,
            "confidence": round(confidence, 2),
            "heatmap_url": heatmap_url  
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}