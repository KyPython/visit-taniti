(function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      const open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Lodging budget filters (guerrilla testing feedback)
  const filterBtns = document.querySelectorAll("[data-filter]");
  const items = document.querySelectorAll("[data-budget]");
  if (filterBtns.length && items.length) {
    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        const value = btn.getAttribute("data-filter");
        filterBtns.forEach(function (b) {
          b.classList.toggle("is-active", b === btn);
          b.setAttribute("aria-pressed", b === btn ? "true" : "false");
        });
        items.forEach(function (item) {
          const budget = item.getAttribute("data-budget");
          item.hidden = value !== "all" && budget !== value;
        });
      });
    });
  }

  // Booking inquiry form (prototype interaction)
  const form = document.getElementById("booking-form");
  const status = document.getElementById("form-status");
  if (form && status) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      status.textContent =
        "Thanks! Your trip inquiry was recorded in this prototype. A Taniti tourism advisor would follow up with lodging and activity options.";
      status.classList.add("is-visible");
      form.reset();
      status.focus();
    });
  }
})();
