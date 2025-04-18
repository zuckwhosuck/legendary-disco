import torch
import numpy as np
import os
import json
import requests
from safetensors.torch import load_file
from transformers import AutoModelForImageClassification

# Paths to local model and config
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "deepfake_detector.safetensors")
CONFIG_PATH = os.path.join(MODEL_DIR, "config.json")

# GitHub release direct download URLs
MODEL_URL = "https://github.com/zuckwhosuck/DeepDetectPrevious/releases/download/v1.0/deepfake_detector.safetensors"
CONFIG_URL = "https://github.com/zuckwhosuck/DeepDetectPrevious/releases/download/v1.0/config.json"

def download_file(url, path):
    """Download a file from a URL to a local path."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        print(f"Downloading from {url}...")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded to {path}")
    else:
        print(f"{path} already exists.")

def load_model():
    """Load and return the deepfake detection model."""
    try:
        # Step 1: Ensure model and config are present
        download_file(MODEL_URL, MODEL_PATH)
        download_file(CONFIG_URL, CONFIG_PATH)

        # Step 2: Load config
        print("Loading model configuration...")
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        # Step 3: Build model from config
        model = build_model(config)

        # Step 4: Load weights from safetensors
        print("Loading model weights...")
        state_dict = load_file(MODEL_PATH)
        model.load_state_dict(state_dict, strict=False)

        model.eval()
        print("Model loaded successfully!")
        return model

    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def build_model(config):
    """Build a model dynamically based on config.json."""
    try:
        model = AutoModelForImageClassification.from_pretrained(
            config["_name_or_path"],
            num_labels=2,
            ignore_mismatched_sizes=True
        )
        return model
    except Exception as e:
        print(f"Error building model: {e}")
        return None

def preprocess_image(image, target_size=(224, 224)):
    """Preprocess the image for model input."""
    image = image.resize(target_size)
    img_array = np.array(image) / 255.0
    img_array = np.transpose(img_array, (2, 0, 1))  # Change to (C, H, W)
    img_tensor = torch.tensor(img_array, dtype=torch.float32).unsqueeze(0)
    return img_tensor

def predict_image(model, image):
    """Predict whether an image is a deepfake or not."""
    if model is None:
        return {"error": "Model not loaded"}

    try:
        processed_img = preprocess_image(image)

        with torch.no_grad():
            outputs = model(processed_img)
            logits = outputs.logits
            prediction_score = torch.softmax(logits, dim=-1)[0, 1].item()

        is_deepfake = prediction_score < 0.5
        confidence = prediction_score if not is_deepfake else (1 - prediction_score)

        prediction_data = {
            "prediction": "Deepfake" if is_deepfake else "Authentic",
            "confidence": confidence,
            "all_scores": {
                "Deepfake": 1 - prediction_score,
                "Authentic": prediction_score
            }
        }
        return prediction_data

    except Exception as e:
        return {"error": f"Error during prediction: {str(e)}"}
