# AI-Based Adaptive Learning System for Dyslexia Support

A portfolio/academic prototype built with Python, Flask, Hugging Face Transformers, GPT-2, image preprocessing, OCR, and adaptive difficulty logic.

## Architecture

1. Content Generation
   - Flask requests a practice sentence.
   - Hugging Face Transformers loads pretrained GPT-2.
   - The application creates a difficulty/topic prompt.
   - GPT-2 generates a sentence.

2. Handwriting Evaluation
   - User uploads a handwriting image.
   - OpenCV/Pillow preprocess the image.
   - Tesseract OCR extracts machine-readable text.
   - The evaluator compares expected vs OCR text.

3. Adaptive Learning
   - A similarity score is calculated.
   - High performance increases difficulty.
   - Low performance can reduce difficulty.
   - The next exercise uses the updated level.

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

Install Tesseract separately because `pytesseract` is a Python wrapper around the Tesseract executable.

On Windows, install Tesseract and add its installation directory to PATH. If it is not on PATH, set:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Path\To\tesseract.exe"
```

inside `services/ocr_service.py`.

### 4. Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

The first GPT-2 generation may take longer because the pretrained model needs to be downloaded and loaded.

## Important project/interview notes

- GPT-2 is the pretrained language model.
- Hugging Face Transformers is the library used to load/tokenize/run GPT-2.
- GPT-2 is used for text generation, not handwriting recognition.
- OCR converts the uploaded handwriting image into text.
- The evaluation layer compares the OCR output with the expected sentence.
- The adaptive layer changes difficulty based on the evaluation score.

## Limitations

This is a learning/demo prototype. OCR quality depends heavily on handwriting, image quality, and the installed OCR engine. GPT-2 is an older generative model and can produce awkward or irrelevant text, so generated sentences should be validated/filtered in a production system.

## Suggested improvements

- Store learner history in a database.
- Add user authentication.
- Add a better handwriting-specific OCR model.
- Add spelling-aware error categories.
- Add a curated sentence dataset and validate generated sentences.
- Add a dashboard showing progress over time.
- Add accessibility features and human evaluation with target learners.
