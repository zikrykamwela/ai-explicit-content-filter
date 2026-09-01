import torch
from torchvision.models import resnet18, ResNet18_Weights


def load_model():
    """Load a pre-trained ResNet18 model."""
    weights = ResNet18_Weights.DEFAULT

    model = resnet18(weights=weights)

    model.eval()

    return model