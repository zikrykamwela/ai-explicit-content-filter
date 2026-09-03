const enabledInput = document.querySelector("#enabled");
const apiUrlInput = document.querySelector("#api-url");
const status = document.querySelector("#status");

chrome.storage.local.get({
  enabled: true,
  apiUrl: "http://localhost:8000/api/predict"
}).then((settings) => {
  enabledInput.checked = settings.enabled;
  apiUrlInput.value = settings.apiUrl;
});

document.querySelector("#save").addEventListener("click", async () => {
  const apiUrl = apiUrlInput.value.trim();
  if (!apiUrl) {
    status.textContent = "Enter a prediction service URL.";
    return;
  }

  await chrome.storage.local.set({ enabled: enabledInput.checked, apiUrl });
  status.textContent = "Settings saved.";
});
