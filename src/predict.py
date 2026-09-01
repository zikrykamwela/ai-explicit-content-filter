import torch
from torchvision.models import ResNet18_Weights

from src.image_processor import load_image, preprocess_image
from src.model import load_model


EXPLICIT_KEYWORDS = {
    "nude",
    "naked",
    "sexy",
    "bikini",
    "lingerie",
    "underwear",
    "breast",
    "genital",
    "porn",
    "adult",
    "erotic",
    "sexual",
    "swimsuit",
    "bra",
    "thong",
    "striptease",
    "seductive",
    "topless",
    "provocative",
    "lingerie",
    "bodypaint",
}


def classify_explicitness(class_name: str, confidence: float) -> str:
    """Return a simple explicit/non-explicit label from the predicted object name."""
    normalized = class_name.lower().replace("_", " ")

    if any(keyword in normalized for keyword in EXPLICIT_KEYWORDS):
        return "explicit"

    if confidence >= 0.95 and normalized in {"person", "woman", "man", "girl", "boy"}:
        return "explicit"

    return "non-explicit"


def predict_image(image_path: str):
    """Run the pre-trained model on an image and return the predicted class label."""
    image = load_image(image_path)
    tensor = preprocess_image(image)
    model = load_model()

    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, class_id = torch.max(probabilities, dim=0)

    confidence_value = confidence.item()
    class_id_value = class_id.item()
    class_name = "unknown"

    weights = ResNet18_Weights.DEFAULT
    categories = weights.meta.get("categories", [])

    if 0 <= class_id_value < len(categories):
        class_name = categories[class_id_value]

    explicitness = classify_explicitness(class_name, confidence_value)

    return {
        "class_id": class_id_value,
        "class_name": class_name,
        "confidence": confidence_value,
        "explicitness": explicitness,
    }