// Animasi sederhana
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.querySelector('.order-btn');
  if (btn) {
    btn.addEventListener('mouseover', () => {
      btn.style.transform = 'scale(1.05)';
    });
    btn.addEventListener('mouseout', () => {
      btn.style.transform = 'scale(1)';
    });
  }
});
