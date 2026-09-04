(function () {
  function init() {
    var article = document.querySelector(".md-content__inner");
    if (!article || article.querySelector(".digna-feedback")) return;

    var wrap = document.createElement("div");
    wrap.className = "digna-feedback";
    wrap.innerHTML =
      '<span class="digna-feedback__label">Was this page helpful?</span>' +
      '<button type="button" class="digna-feedback__btn" data-value="yes" aria-label="Yes, this page was helpful">Yes</button>' +
      '<button type="button" class="digna-feedback__btn" data-value="no" aria-label="No, this page was not helpful">No</button>' +
      '<span class="digna-feedback__thanks" hidden>Thanks for your feedback!</span>';
    article.appendChild(wrap);

    var buttons = wrap.querySelectorAll(".digna-feedback__btn");
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        if (window.clarity) {
          window.clarity("event", "docs_feedback_" + btn.dataset.value);
        }
        buttons.forEach(function (b) {
          b.disabled = true;
        });
        btn.classList.add("digna-feedback__btn--selected");
        wrap.querySelector(".digna-feedback__thanks").hidden = false;
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  if (window.document$) {
    window.document$.subscribe(init);
  }
})();
