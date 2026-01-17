import os
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from django.conf import settings

# Global variables
_model = None
_class_names = None # <--- New Global for the names

def load_resources():
    """
    Loads both the Model and the Class Indices (Singleton).
    """
    global _model, _class_names
    
    # 1. Load Model
    if _model is None:
        try:
            print(f"Loading AI Model from: {settings.MODEL_PATH}...")
            _model = load_model(settings.MODEL_PATH)
            print("Model loaded!")
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    # 2. Load Class Indices
    if _class_names is None:
        json_path = os.path.join(settings.BASE_DIR, 'ml_engine', 'models', 'class_indices.json')
        try:
            print(f"Loading Class Indices from: {json_path}...")
            with open(json_path, 'r') as f:
                indices = json.load(f)
                # Convert {"Benign": 0, "Malignant": 1} -> ["Benign", "Malignant"]
                # We sort by value (0, 1, 2) to ensure the list order matches the model output
                _class_names = [k for k, v in sorted(indices.items(), key=lambda item: item[1])]
            print(f"Class Labels Loaded: {_class_names}")
        except Exception as e:
            print(f"Error loading class_indices.json: {e}")
            return False
            
    return True

def predict_image(img_path):
    # Ensure resources are loaded
    if not load_resources():
        return {"error": "AI Resources failed to load"}

    try:
        # 1. Preprocess
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        
        # 2. Predict
        predictions = _model.predict(img_array)
        
        # 3. Decode
        predicted_index = np.argmax(predictions)
        confidence = float(np.max(predictions)) * 100
        
        # Get the name safely
        diagnosis = _class_names[predicted_index]
        
        return {
            "diagnosis": diagnosis,
            "confidence": round(confidence, 2)
        }
    except Exception as e:
        return {"error": str(e)}