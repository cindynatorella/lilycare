// Handle all show/hide buttons for inline editors and optional history panels.
document.addEventListener("DOMContentLoaded", () => {
  const toggleButtons = document.querySelectorAll("[data-toggle-target]");

  toggleButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.getAttribute("data-toggle-target");
      const panel = document.getElementById(targetId);

      if (!panel) {
        return;
      }

      const isHidden = panel.hasAttribute("hidden");
      if (isHidden) {
        panel.removeAttribute("hidden");
      } else {
        panel.setAttribute("hidden", "");
      }

      const relatedButtons = document.querySelectorAll(`[data-toggle-target="${targetId}"]`);
      relatedButtons.forEach((relatedButton) => {
        relatedButton.setAttribute("aria-expanded", String(isHidden));
        const openLabel = relatedButton.getAttribute("data-open-label");
        const closedLabel = relatedButton.getAttribute("data-closed-label");
        if (openLabel && closedLabel) {
          relatedButton.textContent = isHidden ? openLabel : closedLabel;
        }
      });
    });
  });
});
