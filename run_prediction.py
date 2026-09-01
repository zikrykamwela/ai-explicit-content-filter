import sys

from src.predict import predict_image


image_path = sys.argv[1] if len(sys.argv) > 1 else "data/test.jpg"

if not image_path:
    raise ValueError("Please provide an image path, for example: ./run.sh data/test.jpg")

result = predict_image(image_path)

print("Prediction Result")
print("-----------------")
print(f"Object: {result['class_name']}")
print(f"Class ID: {result['class_id']}")
print(f"Explicitness: {result['explicitness']}")
print(f"Confidence: {result['confidence']:.2%}")