# AI Explicit Content Filter

AI-powered system for detecting and filtering explicit content using Python and computer vision with ResNet18 deep learning model.

## Features

- 🖼️ **Image Classification** — Predicts object labels using ResNet18 (ImageNet pretrained)
- 🔍 **Explicitness Detection** — Classifies images as explicit or non-explicit based on detected objects
- 💻 **Command-line Interface** — Run predictions from the terminal with dynamic image selection
- 🌐 **Web Interface** — Upload images through a browser and get predictions instantly
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

### Option 2: Web Interface (Flask App)

Start the web application for interactive image uploading:

```bash
python app.py
```

Then open your browser to:
```
http://localhost:5000
```

**How to use:**
1. Click the file upload button
2. Select an image from your computer
3. Click "Predict"
4. View the result on the page
5. Upload another image or refresh to predict again

## Project Structure

```
├── app.py                 # Flask web server for image upload
├── run.sh                 # Command-line runner with dynamic image selection
├── run_prediction.py      # Entry point for prediction script
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── src/
│   ├── predict.py         # Main prediction logic with explicitness classification
│   ├── model.py           # Model loading (ResNet18)
│   └── image_processor.py # Image loading and preprocessing
├── data/
│   └── test.jpg           # Sample test image
├── models/                # Model weights storage
└── tests/
    ├── test_model.py      # Tests for model and classification
    ├── test_image_processor.py
    └── test_app.py        # Tests for Flask app
```

## How It Works

1. **Image Input** — Upload or select an image file
2. **Preprocessing** — Image is resized to 224×224 and normalized for the model
3. **Model Inference** — ResNet18 predicts the object class (1000 ImageNet categories)
4. **Classification** — Detected object label is checked against explicit-content keywords
5. **Output** — Returns object name, class ID, explicitness label, and confidence score

## Requirements

- torch >= 2.0.0
- torchvision >= 0.15.0
- opencv-python >= 4.8.0
- flask >= 2.3.0

See `requirements.txt` for full list.

## Examples

### Test from command line:
```bash
./run.sh data/test.jpg
```

### Test from web interface:
1. Start: `python app.py`
2. Go to: `http://localhost:5000`
3. Upload any image
4. Get instant prediction

## Notes

- The model uses ImageNet categories, not custom explicit-content labels
- Explicitness detection uses keyword matching on object names
- Confidence is the model's prediction confidence (0-1)
- For best results, use clear, well-lit images

## License

MIT License

## Author

zikrykamwela
