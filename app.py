from flask import Flask, render_template_string, request, jsonify
import os
import tempfile
from src.predict import predict_image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Explicit Content Filter</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --light: #f9fafb;
            --dark: #111827;
            --border: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 900px;
            background: white;
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .upload-section {
            margin-bottom: 30px;
        }

        .dropzone {
            border: 3px dashed var(--primary);
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: var(--light);
            position: relative;
            overflow: hidden;
        }

        .dropzone:hover {
            border-color: var(--primary-dark);
            background: #f0f4ff;
        }

        .dropzone.dragover {
            border-color: var(--success);
            background: #f0fdf4;
            box-shadow: inset 0 0 0 2px var(--success);
        }

        .dropzone-icon {
            font-size: 3em;
            margin-bottom: 15px;
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }

        .dropzone-text h3 {
            color: var(--dark);
            margin-bottom: 5px;
            font-size: 1.3em;
        }

        .dropzone-text p {
            color: #6b7280;
            font-size: 0.95em;
        }

        .file-input {
            display: none;
        }

        .image-preview {
            margin: 30px 0;
            display: none;
            text-align: center;
        }

        .image-preview.show {
            display: block;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .image-preview img {
            max-width: 100%;
            max-height: 400px;
            border-radius: 12px;
            box-shadow: var(--shadow);
            margin-bottom: 15px;
        }

        .image-info {
            text-align: left;
            background: var(--light);
            padding: 15px;
            border-radius: 8px;
            font-size: 0.95em;
            color: #6b7280;
        }

        .button-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        button {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            min-width: 150px;
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.3);
        }

        .btn-primary:active {
            transform: translateY(0);
        }

        .btn-secondary {
            background: var(--light);
            color: var(--dark);
            border: 2px solid var(--border);
        }

        .btn-secondary:hover {
            background: var(--border);
        }

        .btn-primary:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 30px;
        }

        .loading.show {
            display: block;
        }

        .spinner {
            border: 4px solid var(--light);
            border-top: 4px solid var(--primary);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .loading-text {
            color: #6b7280;
            font-size: 1.1em;
        }

        .result-section {
            display: none;
            margin-top: 40px;
            padding-top: 40px;
            border-top: 2px solid var(--border);
        }

        .result-section.show {
            display: block;
            animation: slideIn 0.3s ease;
        }

        .result-card {
            background: var(--light);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            border-left: 5px solid var(--primary);
        }

        .result-card.explicit {
            border-left-color: var(--danger);
        }

        .result-card.non-explicit {
            border-left-color: var(--success);
        }

        .result-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }

        .result-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-badge.explicit {
            background: #fee2e2;
            color: var(--danger);
        }

        .result-badge.non-explicit {
            background: #dcfce7;
            color: var(--success);
        }

        .result-icon {
            font-size: 1.5em;
        }

        .result-details {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }

        .detail-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid var(--border);
        }

        .detail-label {
            color: #6b7280;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .detail-value {
            color: var(--dark);
            font-size: 1.3em;
            font-weight: 700;
        }

        .confidence-bar {
            margin-top: 10px;
            background: var(--border);
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--primary-dark));
            border-radius: 4px;
            transition: width 0.5s ease;
        }

        .predictions-list {
            margin-top: 20px;
        }

        .prediction-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: white;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid var(--border);
        }

        .prediction-label {
            font-weight: 600;
            color: var(--dark);
            text-transform: capitalize;
        }

        .prediction-score {
            color: var(--primary);
            font-weight: 700;
            font-size: 1.1em;
        }

        .error-message {
            background: #fee2e2;
            color: var(--danger);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            border: 1px solid #fecaca;
            display: none;
        }

        .error-message.show {
            display: block;
        }

        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }

            .content {
                padding: 20px;
            }

            .dropzone {
                padding: 30px 20px;
            }

            .result-details {
                grid-template-columns: 1fr;
            }
        }

        .upload-progress {
            display: none;
            margin-top: 20px;
        }

        .upload-progress.show {
            display: block;
        }

        .progress-bar {
            width: 100%;
            height: 6px;
            background: var(--border);
            border-radius: 3px;
            overflow: hidden;
            margin-bottom: 10px;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--primary-dark));
            width: 0%;
            transition: width 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class=\"header\">
            <h1>🔒 Explicit Content Filter</h1>
            <p>Advanced AI-powered content moderation system</p>
        </div>

        <div class="content">
            <!-- Error Message -->\n            <div class=\"error-message\" id=\"errorMessage\"></div>

            <!-- Upload Section -->
            <div class="upload-section">
                <div class=\"dropzone\" id=\"dropzone\">
                    <div class=\"dropzone-icon\">📸</div>
                    <div class=\"dropzone-text\">
                        <h3>Drag & Drop Your Image</h3>
                        <p>Or click to browse (PNG, JPG, WebP - Max 16MB)</p>
                    </div>
                </div>
                <input type=\"file\" id=\"fileInput\" class=\"file-input\" accept=\"image/*\">

                <!-- Image Preview -->
                <div class=\"image-preview\" id=\"imagePreview\">
                    <img id=\"previewImage\" alt=\"Preview\">
                    <div class=\"image-info\">
                        <p><strong>File:</strong> <span id=\"fileName\"></span></p>
                        <p><strong>Size:</strong> <span id=\"fileSize\"></span></p>
                    </div>
                </div>

                <!-- Upload Progress -->
                <div class=\"upload-progress\" id=\"uploadProgress\">
                    <div class=\"progress-bar\">
                        <div class=\"progress-fill\" id=\"progressFill\"></div>
                    </div>
                    <p id=\"progressText\">Uploading...</p>
                </div>

                <!-- Loading Indicator -->
                <div class=\"loading\" id=\"loading\">
                    <div class=\"spinner\"></div>
                    <p class=\"loading-text\">Analyzing image with AI...</p>
                </div>

                <!-- Button Group -->
                <div class=\"button-group\">
                    <button class=\"btn-primary\" id=\"predictBtn\" onclick=\"predictImage()\" disabled>
                        Analyze Image
                    </button>
                    <button class=\"btn-secondary\" id=\"resetBtn\" onclick=\"resetForm()\" style=\"display: none;\">
                        Upload Another
                    </button>
                </div>
            </div>

            <!-- Results Section -->
            <div class=\"result-section\" id=\"resultSection\">
                <div class=\"result-card\" id=\"resultCard\">
                    <div class=\"result-header\">
                        <div class=\"result-badge\" id=\"resultBadge\">
                            <span class=\"result-icon\" id=\"resultIcon\"></span>
                            <span id=\"resultText\"></span>
                        </div>
                    </div>

                    <div class=\"result-details\">
                        <div class=\"detail-item\">
                            <div class=\"detail-label\">Classification</div>
                            <div class=\"detail-value\" id=\"className\"></div>
                        </div>
                        <div class=\"detail-item\">
                            <div class=\"detail-label\">Confidence Score</div>
                            <div class=\"detail-value\" id=\"confidence\"></div>
                            <div class=\"confidence-bar\">
                                <div class=\"confidence-fill\" id=\"confidenceFill\"></div>
                            </div>
                        </div>
                        <div class=\"detail-item\">
                            <div class=\"detail-label\">Status</div>
                            <div class=\"detail-value\" id=\"explicitness\"></div>
                        </div>
                    </div>

                    <div class=\"predictions-list\" id=\"predictionsList\">
                        <h4 style=\"margin-bottom: 12px; color: var(--dark);\">All Predictions</h4>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        const dropzone = document.getElementById('dropzone');
        const fileInput = document.getElementById('fileInput');
        const imagePreview = document.getElementById('imagePreview');
        const previewImage = document.getElementById('previewImage');
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        const predictBtn = document.getElementById('predictBtn');
        const resetBtn = document.getElementById('resetBtn');
        const loading = document.getElementById('loading');
        const resultSection = document.getElementById('resultSection');
        const errorMessage = document.getElementById('errorMessage');
        const uploadProgress = document.getElementById('uploadProgress');
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');

        let selectedFile = null;

        // Drag and drop events
        dropzone.addEventListener('click', () => fileInput.click());

        dropzone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropzone.classList.add('dragover');
        });

        dropzone.addEventListener('dragleave', () => {
            dropzone.classList.remove('dragover');
        });

        dropzone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropzone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                handleFileSelect(files[0]);
            }
        });

        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleFileSelect(e.target.files[0]);
            }
        });

        function handleFileSelect(file) {
            // Validate file type
            if (!file.type.startsWith('image/')) {
                showError('Please select a valid image file (PNG, JPG, WebP, etc.)');
                return;
            }

            // Validate file size (16MB)
            if (file.size > 16 * 1024 * 1024) {
                showError('File size exceeds 16MB limit');
                return;
            }

            selectedFile = file;
            clearError();

            // Show preview
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImage.src = e.target.result;
                fileName.textContent = file.name;
                fileSize.textContent = formatFileSize(file.size);
                imagePreview.classList.add('show');
                predictBtn.disabled = false;
            };
            reader.readAsDataURL(file);
        }

        function formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
        }

        function predictImage() {
            if (!selectedFile) {
                showError('Please select an image first');
                return;
            }

            const formData = new FormData();
            formData.append('image', selectedFile);

            loading.classList.add('show');
            resultSection.classList.remove('show');
            predictBtn.disabled = true;
            clearError();

            fetch('/', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                loading.classList.remove('show');
                displayResults(data.result);
                resultSection.classList.add('show');
                resetBtn.style.display = 'inline-block';
                predictBtn.style.display = 'none';
            })
            .catch(error => {
                loading.classList.remove('show');
                showError('Error analyzing image: ' + error.message);
                predictBtn.disabled = false;
            });
        }

        function displayResults(result) {
            const resultCard = document.getElementById('resultCard');
            const isExplicit = result.explicitness === 'explicit';
            
            resultCard.classList.toggle('explicit', isExplicit);
            resultCard.classList.toggle('non-explicit', !isExplicit);

            // Result badge
            const resultBadge = document.getElementById('resultBadge');
            const resultIcon = document.getElementById('resultIcon');
            const resultText = document.getElementById('resultText');
            
            resultBadge.classList.toggle('explicit', isExplicit);
            resultBadge.classList.toggle('non-explicit', !isExplicit);
            resultIcon.textContent = isExplicit ? '⚠️' : '✅';
            resultText.textContent = result.explicitness.toUpperCase();

            // Details
            document.getElementById('className').textContent = result.class_name.toUpperCase();
            document.getElementById('confidence').textContent = (result.confidence * 100).toFixed(2) + '%';
            document.getElementById('explicitness').textContent = result.explicitness;
            
            // Confidence bar
            document.getElementById('confidenceFill').style.width = (result.confidence * 100) + '%';

            // Predictions list
            const predictionsList = document.getElementById('predictionsList');
            predictionsList.innerHTML = '<h4 style=\"margin-bottom: 12px; color: var(--dark);\">All Predictions</h4>';
            
            if (result.all_predictions && result.all_predictions.length > 0) {
                result.all_predictions.forEach((pred, index) => {
                    const item = document.createElement('div');
                    item.className = 'prediction-item';
                    const score = (pred.score * 100).toFixed(2);
                    item.innerHTML = `
                        <span class=\"prediction-label\">${pred.label}</span>
                        <span class=\"prediction-score\">${score}%</span>
                    `;
                    predictionsList.appendChild(item);
                });
            }
        }

        function resetForm() {
            selectedFile = null;
            fileInput.value = '';
            imagePreview.classList.remove('show');
            resultSection.classList.remove('show');
            loading.classList.remove('show');
            uploadProgress.classList.remove('show');
            clearError();
            
            predictBtn.disabled = true;
            predictBtn.style.display = 'inline-block';
            resetBtn.style.display = 'none';
        }

        function showError(message) {
            errorMessage.textContent = message;
            errorMessage.classList.add('show');
        }

        function clearError() {
            errorMessage.classList.remove('show');
        }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return predict_uploaded_image()

    return render_template_string(HTML)


@app.route("/api/predict", methods=["POST"])
def predict_api():
    """Classify an image for browser extensions and other clients."""
    return predict_uploaded_image()


def predict_uploaded_image():
    uploaded_file = request.files.get("image")

    if not uploaded_file or not uploaded_file.filename:
        return jsonify({"error": "No file provided"}), 400

    try:
        suffix = os.path.splitext(uploaded_file.filename)[1] or ".img"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temp_file:
            uploaded_file.save(temp_file)
            temp_path = temp_file.name

        result = predict_image(temp_path)
        return jsonify({"result": result}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500
    finally:
        if "temp_path" in locals() and os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(debug=True)
