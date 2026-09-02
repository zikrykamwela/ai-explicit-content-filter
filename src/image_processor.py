from pathlib import Path
import cv2
from PIL import Image


def load_image(image_path: str):
    """Load an image from disk using OpenCV."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    return image


def load_image_pil(image_path: str):
    """Load an image from disk using PIL."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = Image.open(str(path)).convert("RGB")

    return image


def get_image_info(image):
    """Return basic information about an image."""
    if isinstance(image, Image.Image):
        width, height = image.size
        return {
            "width": width,
            "height": height,
            "channels": 3 if image.mode == "RGB" else len(image.mode),
        }
    else:
        height, width, channels = image.shape
        return {
            "width": width,
            "height": height,
            "channels": channels,
        }


import torch
from torchvision import transforms


def preprocess_image(image):
    """
    Prepare an OpenCV image for an AI model.
    """
    # OpenCV uses BGR, while most AI models expect RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        ),
    ])
    tensor = transform(image_rgb)

    # Add batch dimension: [C, H, W] → [1, C, H, W]
    tensor = tensor.unsqueeze(0)

    return tensor