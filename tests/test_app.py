import io
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app


def test_upload_image_page_and_prediction():
    """A valid uploaded image should return the prediction page."""
    client = app.test_client()

    image = np.zeros((32, 32, 3), dtype=np.uint8)
    encoded_image = cv2.imencode(".png", image)[1].tobytes()

    response = client.post(
        "/",
        data={"image": (io.BytesIO(encoded_image), "test.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Prediction Result" in body
