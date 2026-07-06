function showToast(message) {
  const toastEl = document.getElementById('toast');
  if (!toastEl) return;
  toastEl.textContent = message;
  toastEl.classList.add('show');
  setTimeout(() => toastEl.classList.remove('show'), 2200);
}

function showAlert(message, type) {
  const alertEl = document.getElementById('page-alert');
  if (!alertEl) return;
  alertEl.className = 'alert alert-' + (type || 'error');
  alertEl.textContent = message;
  alertEl.hidden = false;
  alertEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function hideAlert() {
  const alertEl = document.getElementById('page-alert');
  if (alertEl) alertEl.hidden = true;
}