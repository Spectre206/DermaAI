# Create a file named 'check_layers.py' in the root folder and run it
import os
from tensorflow.keras.models import load_model

model_path = r"D:\DermaAI\ml_engine\models\skin_model_v1.h5"
model = load_model(model_path)
model.summary()