document.addEventListener("DOMContentLoaded", function () {
  const elements = document.querySelectorAll("h1, p, button");
  elements.forEach((el) => {
    el.style.opacity = 0;
    el.style.transform = "translateY(20px)";
  });

  setTimeout(() => {
    elements.forEach((el, index) => {
      setTimeout(() => {
        el.style.transition = "all 0.6s ease";
        el.style.opacity = 1;
        el.style.transform = "translateY(0)";
      }, 300 * index);
    });
  }, 500);
});
