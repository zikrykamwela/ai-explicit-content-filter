from PIL import Image
from src.model import load_model

# NSFW classification labels
NSFW_LABELS = {"normal", "safe"}


def classify_explicitness(class_name: str, confidence: float) -> str:
    """
    Classify if content is explicit or non-explicit based on NSFW model output.
    
    Args:
        class_name: The predicted label (e.g., "porn", "sexy", "normal", "hentai")
        confidence: The confidence score (0.0 to 1.0)
    
    Returns:
        "explicit" or "non-explicit"
    """
    class_lower = class_name.lower().strip()
    
    # Check if the label is in the safe/normal category
    if class_lower in NSFW_LABELS:
        return "non-explicit"
    
    return "explicit"


def predict_image(image_path: str):
    """
    Run the pre-trained NSFW detection model on an image.
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Dictionary with class_name, confidence, explicitness, and class_id
    """
    # Load the model
    model = load_model()
    
    # Open the image using PIL (required by Hugging Face pipeline)
    image = Image.open(image_path)
    
    # Run inference
    results = model(image)
    
    # Get the top prediction
    top_result = results[0]
    class_name = top_result["label"]
    confidence = top_result["score"]
    
    # Classify as explicit or not
    explicitness = classify_explicitness(class_name, confidence)
    
    return {
        "class_id": 0,  # Not used with pipeline model
        "class_name": class_name,
        "confidence": confidence,
        "explicitness": explicitness,
    }