const DEFAULT_API_URL = "http://localhost:8000/api/predict";

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== "analyze-image") {
    return false;
  }

  analyzeImage(message.url)
    .then(sendResponse)
    .catch((error) => sendResponse({ error: error.message }));

  return true;
});

async function analyzeImage(imageUrl) {
  const response = await fetch(imageUrl, { credentials: "omit" });
  if (!response.ok) {
    throw new Error(`Image request failed (${response.status})`);
  }

  const blob = await response.blob();
  const formData = new FormData();
  formData.append("image", blob, "page-image");

  const settings = await chrome.storage.local.get({ apiUrl: DEFAULT_API_URL });
  const prediction = await fetch(settings.apiUrl, {
    method: "POST",
    body: formData
  });
  const result = await prediction.json();

  if (!prediction.ok) {
    throw new Error(result.error || "Prediction request failed");
  }

  let status;
  do {
    await new Promise((resolve) => setTimeout(resolve, 1000));
    status = await fetch(`${settings.apiUrl}/${encodeURIComponent(result.job_id)}`);
    result.status = await status.json();
  } while (result.status.status === "processing");

  if (!status.ok || result.status.status === "failed") {
    throw new Error(result.status.error || "Prediction request failed");
  }
  return result.status.result;
}
