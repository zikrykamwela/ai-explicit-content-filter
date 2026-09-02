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
    # Model is a Hugging Face pipeline, not a PyTorch module
    assert hasattr(model, "__call__") or callable(model)


def test_classify_explicitness():
    """Test explicit/non-explicit classification helper for NSFW model."""
    # NSFW model outputs: "normal", "safe", "porn", "sexy", "hentai"
    assert classify_explicitness("normal", 0.95) == "non-explicit"
    assert classify_explicitness("safe", 0.90) == "non-explicit"
    assert classify_explicitness("porn", 0.85) == "explicit"
    assert classify_explicitness("sexy", 0.75) == "explicit"
    assert classify_explicitness("hentai", 0.80) == "explicit"