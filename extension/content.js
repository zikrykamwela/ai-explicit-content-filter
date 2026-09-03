const analyzedImages = new WeakSet();
const blockedImages = new WeakSet();
let enabled = true;

chrome.storage.local.get({ enabled: true }).then((settings) => {
  enabled = settings.enabled;
  if (enabled) scanImages();
});

chrome.storage.onChanged.addListener((changes) => {
  if (!changes.enabled) return;
  enabled = changes.enabled.newValue;
  if (enabled) scanImages();
});

const observer = new MutationObserver(() => {
  if (enabled) scanImages();
});
observer.observe(document.documentElement, { childList: true, subtree: true });

function scanImages() {
  document.querySelectorAll("img").forEach((image) => {
    if (!analyzedImages.has(image) && image.src) analyze(image);
  });
}

function analyze(image) {
  analyzedImages.add(image);
  chrome.runtime.sendMessage({ type: "analyze-image", url: image.currentSrc || image.src }, (result) => {
    if (chrome.runtime.lastError || !result || result.error) return;
    if (result.explicitness === "explicit") block(image);
  });
}

function block(image) {
  if (blockedImages.has(image)) return;
  blockedImages.add(image);
  image.style.setProperty("filter", "blur(28px)", "important");
  image.style.setProperty("background", "#17191d", "important");
  image.setAttribute("alt", "Image hidden by ClearView");
  image.setAttribute("title", "Image hidden by ClearView content filter");
}
