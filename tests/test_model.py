import sys
from pathlib import Path

# Add parent directory to path so we can import src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import load_model
from src.predict import classify_explicitness


def test_load_model():
    """Test load_model returns a valid model."""
    model = load_model()

    assert model is not None
    assert model.training is False


def test_classify_explicitness():
    """Test explicit/non-explicit classification helper."""
    assert classify_explicitness("tobacco shop", 0.41) == "non-explicit"
    assert classify_explicitness("bikini", 0.78) == "explicit"
    assert classify_explicitness("lingerie", 0.52) == "explicit"
    assert classify_explicitness("person", 0.92) == "non-explicit"