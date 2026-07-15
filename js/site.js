(function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".primary-nav");

  function setNavOpen(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNavOpen(false);
      });
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setNavOpen(false);
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 840) setNavOpen(false);
    });
  }

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
