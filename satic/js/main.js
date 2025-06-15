// V Mart Inventory System - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
  initializeFormValidation();
  initializeAlerts();
  initializeTooltips();
  initializeStockLevelFeedback();
  console.log('✅ V Mart Inventory JS loaded');
});

// -------------------------------
// 1️⃣ Form Validation
// -------------------------------
function initializeFormValidation() {
  const forms = document.querySelectorAll('form[novalidate]');
  forms.forEach(form => {
    form.addEventListener('submit', function(e) {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add('was-validated');
    });
  });
}

// -------------------------------
// 2️⃣ Bootstrap Alerts Auto-Dismiss
// -------------------------------
function initializeAlerts() {
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    if (alert.classList.contains('alert-success')) {
      setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
      }, 4000);
    }
  });
}

// -------------------------------
// 3️⃣ Tooltips (Bootstrap)
// -------------------------------
function initializeTooltips() {
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach(t => {
    new bootstrap.Tooltip(t);
  });
}

// -------------------------------
// 4️⃣ Stock Level Feedback
//    - Highlights stock input color based on value
// -------------------------------
function initializeStockLevelFeedback() {
  const stockInput = document.querySelector('input[name="stock_quantity"]');
  const minStockInput = document.querySelector('input[name="min_stock_level"]');

  if (stockInput && minStockInput) {
    stockInput.addEventListener('input', updateFeedback);
    minStockInput.addEventListener('input', updateFeedback);

    // Initial check on load
    updateFeedback();
  }

  function updateFeedback() {
    const stock = parseInt(stockInput.value) || 0;
    const minStock = parseInt(minStockInput.value) || 0;

    stockInput.classList.remove('border-success', 'border-warning', 'border-danger');

    if (stock === 0) {
      stockInput.classList.add('border-danger');
    } else if (stock <= minStock) {
      stockInput.classList.add('border-warning');
    } else {
      stockInput.classList.add('border-success');
    }
  }
}

// -------------------------------
// 5️⃣ Optional: Keyboard Shortcut for Search
// -------------------------------
document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    const searchInput = document.getElementById('search');
    if (searchInput) {
      searchInput.focus();
      searchInput.select();
    }
  }
});

// -------------------------------
// 6️⃣ Utility: Format currency (optional for future use)
// -------------------------------
function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
}
