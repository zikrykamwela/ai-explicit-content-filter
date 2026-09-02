import sys

from src.predict import predict_image


image_path = sys.argv[1] if len(sys.argv) > 1 else "data/test.jpg"

if not image_path:
    raise ValueError("Please provide an image path, for example: python run_prediction.py data/test.jpg")

print(f"Image path: {image_path}")
print("-" * 50)

result = predict_image(image_path)

print("Prediction Result")
print("-" * 50)
print(f"Classification: {result['class_name'].upper()}")
print(f"Explicitness: {result['explicitness'].upper()}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Class ID: {result['class_id']}")
print()
print("All Predictions:")
print("-" * 50)
for pred in result['all_predictions']:
    print(f"  {pred['label']:15} - {pred['score']:.2%}")