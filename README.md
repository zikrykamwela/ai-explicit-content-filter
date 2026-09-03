# AI Explicit Content Filter

AI-powered system for detecting and filtering explicit visual content with a local Python model, Django website, and Chrome/Chromium browser extension.

## Features

- 🖼️ **Image Classification** — Classifies images with the `Falconsai/nsfw_image_detection` model
- 🔍 **Explicitness Detection** — Returns explicit/non-explicit status and confidence
- 💻 **Command-line Interface** — Run predictions from the terminal with dynamic image selection
- 🌐 **Django Web Interface** — Upload, preview, and analyze images with responsive feedback
- 🧩 **Browser Extension** — Hide explicit images found on web pages
- 📊 **Detailed Results** — Object name, Class ID, Explicitness label, and Confidence score

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/zikrykamwela/ai-explicit-content-filter.git
   cd ai-explicit-content-filter
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Command-line Interface

Run predictions on images from the terminal:

```bash
./run.sh data/test.jpg
```

**Output:**
```
Image path: data/test.jpg
Prediction Result
-----------------
Object: gown
Class ID: 578
Explicitness: non-explicit
Confidence: 47.85%
```

You can use any image file in the `data/` folder or provide any path:
```bash
./run.sh /path/to/your/image.jpg
```

### Option 2: Web Interface (Django)

Start the web application for interactive image uploading:

```bash
python manage.py runserver
```

Then open your browser to:
```
http://localhost:8000
```

**How to use:**
1. Drop an image into the analysis area or browse for one
2. Review the preview and choose **Analyze image**
3. View the classification, confidence, and recommendation
4. Choose **Analyze another image** to continue

### Option 3: Browser Extension

The `extension/` directory contains a Chrome/Chromium Manifest V3 extension. It
uses the local Django model service to inspect images in browser pages and blur images
classified as explicit.

1. Start the prediction service:
   ```bash
   python manage.py runserver
   ```
2. Open `chrome://extensions` (or the equivalent extensions page in your browser).
3. Enable **Developer mode**, choose **Load unpacked**, and select this repository's `extension/` folder.
4. Open the ClearView extension popup to enable protection and confirm the API URL.

The extension needs access to page content and image URLs to perform its job.
It only controls content rendered inside the browser. A browser extension cannot
reliably control the whole device, other applications, or bypass operating-system
parental controls. For device-wide filtering, use a managed DNS, operating-system
parental-control policy, or a dedicated device-management application alongside
this extension.

The extension API accepts an image form field named `image` at `POST /api/predict`.
It immediately returns a job ID with `202 processing`; poll
`GET /api/predict/<job_id>` until the status is `completed` or `failed`.

## Project Structure

```
├── manage.py              # Django development server entry point
├── content_filter/        # Django project configuration and URLs
├── filter_site/           # Website views and prediction API
├── templates/             # Django HTML templates
├── static/                # Website CSS and JavaScript
├── extension/             # Chrome/Chromium Manifest V3 extension
├── app.py                 # Legacy Flask upload server
├── run.sh                 # Command-line runner with dynamic image selection
├── run_prediction.py      # Entry point for prediction script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── src/
│   ├── predict.py         # Main prediction logic with explicitness classification
│   ├── model.py           # Cached NSFW model loading
│   └── image_processor.py # Image loading and preprocessing
├── data/
│   └── test.jpg           # Sample test image
├── models/                # Model weights storage
└── tests/
    ├── test_model.py      # Tests for model and classification
    ├── test_image_processor.py
      └── test_app.py        # Tests for the legacy Flask app
```

## How It Works

1. **Image Input** — Upload an image through Django or the browser extension
2. **Temporary Storage** — The upload is written to a temporary file for inference
3. **Model Inference** — The NSFW image classification model analyzes the image
4. **Classification** — The top model label is mapped to explicit/non-explicit status
5. **Cleanup** — The temporary upload is removed after the prediction job finishes
6. **Output** — The client receives the label, confidence, and explicitness status

## Requirements

- torch >= 2.0.0
- torchvision >= 0.15.0
- opencv-python >= 4.8.0
- Flask >= 3.0.0
- Django >= 5.0.0
- transformers >= 4.30.0
- pillow >= 9.0.0

See `requirements.txt` for full list.

## Examples

### Test from command line:
```bash
./run.sh data/test.jpg
```

### Test from web interface:
```bash
python manage.py runserver
```

Open `http://localhost:8000`, upload an image, and choose **Analyze image**.

## Notes

- The first prediction may take several minutes while Hugging Face downloads and initializes the model.
- The model is cached in memory after its first load, so later predictions are faster.
- The API uses a background worker and polling to avoid gateway `504` timeouts.
- Confidence is the model's prediction confidence from 0 to 1.
- For best results, use clear images in JPG, PNG, or WEBP format.
- The browser extension only filters content rendered in the browser; it cannot control other apps or the entire device.

## Troubleshooting

### Analysis is still loading

Keep the Django server running and wait for the first model download to finish.
Check the terminal running `manage.py runserver` for download or model errors.

### The browser shows a 504 error

Restart the Django server so it is using the asynchronous API implementation:

```bash
Ctrl+C
python manage.py runserver
```

The upload request should return `202 processing` immediately, followed by polling
until the result is ready.

### The extension cannot connect

Confirm the Django server is running at `http://localhost:8000`, then open the
extension popup and verify the prediction service URL is:

```text
http://localhost:8000/api/predict
```

## License

MIT License

## Author

zikrykamwela
