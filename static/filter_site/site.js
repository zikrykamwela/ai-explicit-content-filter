const form = document.querySelector('#analyze-form');
const input = document.querySelector('#image-input');
const dropzone = document.querySelector('#dropzone');
const preview = document.querySelector('#preview');
const previewImage = document.querySelector('#preview-image');
const fileName = document.querySelector('#file-name');
const fileSize = document.querySelector('#file-size');
const analyzeButton = document.querySelector('#analyze-button');
const loading = document.querySelector('#loading');
const loadingText = document.querySelector('#loading-text');
const message = document.querySelector('#message');
const result = document.querySelector('#result');

function setFile(file) {
  if (!file || !file.type.startsWith('image/')) {
    showMessage('Please choose a JPG, PNG, or WEBP image.');
    return;
  }
  input.files = new DataTransfer().files;
  const transfer = new DataTransfer();
  transfer.items.add(file);
  input.files = transfer.files;
  previewImage.src = URL.createObjectURL(file);
  fileName.textContent = file.name;
  fileSize.textContent = `${(file.size / 1024 / 1024).toFixed(2)} MB`;
  preview.hidden = false;
  dropzone.hidden = true;
  analyzeButton.disabled = false;
  message.hidden = true;
  result.hidden = true;
}

input.addEventListener('change', () => setFile(input.files[0]));
['dragenter', 'dragover'].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropzone.classList.add('dragover');
}));
['dragleave', 'drop'].forEach((eventName) => dropzone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropzone.classList.remove('dragover');
}));
dropzone.addEventListener('drop', (event) => setFile(event.dataTransfer.files[0]));

document.querySelector('#remove-file').addEventListener('click', reset);
document.querySelector('#new-check').addEventListener('click', reset);

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  loading.hidden = false;
  loadingText.textContent = 'Loading the AI model. The first check may take a few minutes...';
  analyzeButton.disabled = true;
  message.hidden = true;
  result.hidden = true;
  try {
    const response = await fetch('/api/predict', { method: 'POST', body: new FormData(form) });
    const payload = await readJson(response);
    if (!response.ok) throw new Error(payload.error || `Analysis failed (${response.status}).`);
    const completed = await waitForPrediction(payload.job_id);
    showResult(completed.result);
  } catch (error) {
    showMessage(error.name === 'TypeError' ? 'Unable to reach the prediction service. Is Django running?' : error.message);
  } finally {
    loading.hidden = true;
    loadingText.textContent = 'Reading the image securely...';
    analyzeButton.disabled = false;
  }
});

async function readJson(response) {
  const body = await response.text();
  if (!body.trim()) throw new Error(`The server returned an empty response (${response.status}).`);
  try {
    return JSON.parse(body);
  } catch {
    throw new Error(`The server returned an unexpected response (${response.status}).`);
  }
}

async function waitForPrediction(jobId) {
  if (!jobId) throw new Error('The server did not create an analysis job.');
  for (;;) {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    const response = await fetch(`/api/predict/${encodeURIComponent(jobId)}`);
    const payload = await readJson(response);
    if (payload.status === 'completed') return payload;
    if (payload.status === 'failed' || !response.ok) throw new Error(payload.error || 'Analysis failed.');
    loadingText.textContent = 'The AI model is analyzing your image...';
  }
}

function showResult(data) {
  const explicit = data.explicitness === 'explicit';
  result.classList.toggle('explicit', explicit);
  document.querySelector('#result-title').textContent = explicit ? 'Content flagged' : 'Looks clear';
  document.querySelector('#result-symbol').textContent = explicit ? '!' : '✓';
  document.querySelector('#result-class').textContent = data.class_name;
  document.querySelector('#result-confidence').textContent = `${(data.confidence * 100).toFixed(1)}%`;
  document.querySelector('#result-recommendation').textContent = explicit ? 'Keep protected' : 'Safe to view';
  document.querySelector('#confidence-fill').style.width = `${data.confidence * 100}%`;
  result.hidden = false;
}

function showMessage(text) {
  message.textContent = text;
  message.hidden = false;
}

function reset() {
  form.reset();
  preview.hidden = true;
  dropzone.hidden = false;
  analyzeButton.disabled = true;
  result.hidden = true;
  message.hidden = true;
  URL.revokeObjectURL(previewImage.src);
}
