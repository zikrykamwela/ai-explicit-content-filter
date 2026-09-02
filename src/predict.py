import torch

from src.image_processor import load_image, preprocess_image
from src.model import load_model


def predict_image(image_path: str):
    """Run the pre-trained model on an image."""
    image = load_image(image_path)
    tensor = preprocess_image(image)
    model = load_model()

    with torch.no_grad():
        outputs = model(tensor)

        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)

        confidence, class_id = torch.max(probabilities, dim=0)

    return {
        "class_id": class_id.item(),
        "confidence": confidence.item(),
    }