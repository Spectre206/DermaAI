import os
import json
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.efficientnet import preprocess_input 
from django.conf import settings

# --- CONFIGURATION ---
LAST_CONV_LAYER = "top_activation"  

# Global variables
_model = None
_class_names = None

def load_resources():
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
            with open(json_path, 'r') as f:
                indices = json.load(f)
                _class_names = [k for k, v in sorted(indices.items(), key=lambda item: item[1])]
        except Exception as e:
            print(f"Error loading class_indices.json: {e}")
            return False     
    return True

def make_gradcam_heatmap(img_array, model, last_conv_layer_name):
    try:
        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[model.get_layer(last_conv_layer_name).output, model.output]
        )
    except ValueError:
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
    # 1. Read original image
    img = cv2.imread(original_img_path)
    if img is None: return None
    
    # 2. Resize heatmap to match image
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    
    # 3. Overlay (CRITICAL FIX HERE)
    # We force the math result to be an integer (uint8) immediately
    combined = heatmap * 0.4 + img
    superimposed_img = np.uint8(combined)
    
    # 4. Save
    save_dir = os.path.join(settings.MEDIA_ROOT, 'heatmaps')
    os.makedirs(save_dir, exist_ok=True)
    
    save_path = os.path.join(save_dir, f"heatmap_{filename}")
    
    # Debug Check
    success = cv2.imwrite(save_path, superimposed_img)
    if success:
        print(f"Heatmap Saved Successfully: {save_path}")
    else:
        print(f"FAILED to Save Heatmap: {save_path}")
    
    return f"/media/heatmaps/heatmap_{filename}"

def predict_image(img_path):
    if not load_resources():
        return {"error": "AI Resources failed to load"}

    try:
        # 1. Preprocess
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = preprocess_input(img_array) 
        img_array = np.expand_dims(img_array, axis=0)

        # 2. Predict
        predictions = _model.predict(img_array)
        predicted_index = np.argmax(predictions)
        confidence = float(np.max(predictions)) * 100
        diagnosis = _class_names[predicted_index]
        
        # 3. Generate Explainability
        heatmap_url = None
        heatmap = make_gradcam_heatmap(img_array, _model, LAST_CONV_LAYER)
        
        if heatmap is not None:
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