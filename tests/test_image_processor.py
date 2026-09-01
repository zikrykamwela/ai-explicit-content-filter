import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.image_processor import get_image_info, preprocess_image
import numpy as np


def test_image_info():
    """Test get_image_info with a sample image array."""
    image = np.zeros((100, 200, 3), dtype=np.uint8)

    info = get_image_info(image)

    assert info["width"] == 200
    assert info["height"] == 100
    assert info["channels"] == 3


def test_preprocess_image():
    """Test preprocess_image converts and resizes correctly."""
    image = np.zeros((500, 500, 3), dtype=np.uint8)

    tensor = preprocess_image(image)

    assert tensor.shape == (1, 3, 224, 224)