from flask import Flask, render_template_string, request

from src.predict import predict_image

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Explicit Content Filter</title>
    <style>
      body { font-family: Arial, sans-serif; padding: 30px; }
      form { margin-bottom: 20px; }
      input { margin-top: 10px; }
      .result { margin-top: 20px; }
    </style>
  </head>
  <body>
    <h1>Explicit Content Filter</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="image" accept="image/*" required>
      <br>
      <input type="submit" value="Predict">
    </form>

    {% if result %}
      <div class="result">
        <h2>Prediction Result</h2>
        <p><strong>Image:</strong> {{ image_name }}</p>
        <p><strong>Object:</strong> {{ result['class_name'] }}</p>
        <p><strong>Class ID:</strong> {{ result['class_id'] }}</p>
        <p><strong>Explicitness:</strong> {{ result['explicitness'] }}</p>
        <p><strong>Confidence:</strong> {{ '%.2f' % (result['confidence'] * 100) }}%</p>
      </div>
    {% endif %}
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_name = None

    if request.method == "POST":
        uploaded_file = request.files.get("image")

        if uploaded_file and uploaded_file.filename:
            image_name = uploaded_file.filename
            temp_path = f"/tmp/{uploaded_file.filename}"
            uploaded_file.save(temp_path)
            result = predict_image(temp_path)

    return render_template_string(HTML, result=result, image_name=image_name)


if __name__ == "__main__":
    app.run(debug=True)
