import torch
from transformers import pipeline


def load_model():
    """
    Load a pre-trained NSFW image detection model from Hugging Face.
    Uses the Falconsai/nsfw_image_detection model for accurate content classification.
    """
    # Initialize the image classification pipeline with NSFW model
    classifier = pipeline(
        "image-classification",
        model="Falconsai/nsfw_image_detection",
        device=0 if torch.cuda.is_available() else -1  # Use GPU if available
    )
    
    return classifier