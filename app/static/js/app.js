document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }
  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Checkbox Listener
   */
  class CheckboxListener {
    constructor(selector, onChangeCallback) {
      this.$checkboxes = document.querySelectorAll(selector);
      this.checkedValues = [];
      this.onChangeCallback = onChangeCallback;
      this.init();
    }

    init() {
      this.$checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
          this.checkedValues.push(checkbox.value);
        }
        checkbox.addEventListener("change", (event) => {
          if (event.target.checked) {
            this.checkedValues.push(event.target.value);
          } else {
            const index = this.checkedValues.indexOf(event.target.value);
            if (index !== -1) {
              this.checkedValues.splice(index, 1);
            }
          }
          this.onChangeCallback();
        });
      });
    }
  }
  const toggleInstitutionVisibility = function () {
    document.querySelectorAll(".form-group--checkbox-step3").
    forEach(function (institutionDiv) {
      const institutionCategories = institutionDiv.dataset.categories
          ? institutionDiv.dataset.categories.split(','):[];
      if (institutionCategories.some(category => checkboxListener.checkedValues.includes(category))) {
        institutionDiv.style.display = "block";
      } else {
        institutionDiv.style.display = "none";
      }
    });
  };
  const checkboxListener = new CheckboxListener("input[name='categories']",
      toggleInstitutionVisibility);
  toggleInstitutionVisibility()

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }
  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function(e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
    constructor(form) {
      this.$form = form;
      this.$next = form.querySelectorAll(".next-step");
      this.$prev = form.querySelectorAll(".prev-step");
      this.$step = form.querySelector(".form--steps-counter span");
      this.currentStep = 1;

      this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
      const $stepForms = form.querySelectorAll("form > div");
      this.slides = [...this.$stepInstructions, ...$stepForms];
      this.formData = {}
      this.init();
    }

    /**
     * Init all methods
     */
    init() {
      this.events();
      this.updateForm();
    }

    /**
     * All events that are happening in form
     */
    events() {
      // Next step
      this.$next.forEach(btn => {
        btn.addEventListener("click", e => {
            e.preventDefault();
            this.currentStep++;
          if (this.currentStep === 2) {
            let selectedCategories = this.$form.querySelectorAll("input[name='categories']:checked");
            this.formData.categories = selectedCategories.length > 0 ?
                Array.from(selectedCategories).map(checkbox => checkbox.value).join(", ") : "";
            }
          if (this.currentStep === 3) {
            this.formData.bags = this.$form.querySelector("input[name='bags']").value;
          }
         if (this.currentStep === 4) {
            let selectedOrganization = document.querySelector("input[name='organization']:checked");
            if (selectedOrganization) {
              let selectedInstitutionDiv = selectedOrganization.parentNode;
              let institutionName = selectedInstitutionDiv.querySelector(".title").innerText;
              this.formData.institution = institutionName;
            } else {
              this.formData.institution = "";
            }
          }
          if (this.currentStep === 5) {
            this.formData.street = this.$form.querySelector("input[name='address']").value;
            this.formData.city = this.$form.querySelector("input[name='city']").value;
            this.formData.postcode = this.$form.querySelector("input[name='postcode']").value;
            this.formData.phone = this.$form.querySelector("input[name='phone']").value;
            this.formData.date = this.$form.querySelector("input[name='data']").value;
            this.formData.time = this.$form.querySelector("input[name='time']").value;
            this.formData.info = this.$form.querySelector("textarea[name='more_info']").value;

            let bagsText = "";
            switch (true) {
              case this.formData.bags == 1:
                bagsText = " worek";
                break;
              case this.formData.bags >= 2 && this.formData.bags <= 4:
                bagsText = " worki";
                break;
              default:
                bagsText = " worków";
            }
            document.getElementById("bags-summary").innerHTML =
                "Oddajesz: " + this.formData.categories + " - " + this.formData.bags + bagsText;
            document.getElementById("institution-summary").innerHTML =
                "Odbiorca: " + this.formData.institution;
            document.getElementById("pick-up-street").innerHTML = this.formData.street;
            document.getElementById("pick-up-city").innerHTML = this.formData.city;
            document.getElementById("pick-up-postcode").innerHTML = this.formData.postcode;
            document.getElementById("pick-up-phone").innerHTML = this.formData.phone;
            document.getElementById("pick-up-date").innerHTML = this.formData.date;
            document.getElementById("pick-up-time").innerHTML = this.formData.time;
            document.getElementById("pick-up-info").innerHTML = this.formData.info;
          }
          this.updateForm();
        });
      });

      // Previous step
      this.$prev.forEach(btn => {
        btn.addEventListener("click", e => {
          e.preventDefault();
          this.currentStep--;
          if (this.currentStep === 1) {
            let selectedCategories = this.$form.querySelectorAll("input[name='categories']:checked");
            this.formData.categories = selectedCategories.length > 0 ?
                Array.from(selectedCategories).map(checkbox => checkbox.value).join(", ") : "";
            }
          if (this.currentStep === 2) {
            this.formData.bags = this.$form.querySelector("input[name='bags']").value;
          }
          if (this.currentStep === 3) {
            let selectedOrganization = document.querySelector("input[name='organization']:checked")
            if (selectedOrganization) {
              let selectedInstitutionDiv = selectedOrganization.parentNode;
              let institutionName = selectedInstitutionDiv.querySelector(".title").innerText;
              this.formData.institution = institutionName;
            } else {
              this.formData.institution = "";
            }
          }
          if (this.currentStep === 4) {
            this.formData.street = this.$form.querySelector("input[name='address']").value;
            this.formData.city = this.$form.querySelector("input[name='city']").value;
            this.formData.postcode = this.$form.querySelector("input[name='postcode']").value;
            this.formData.phone = this.$form.querySelector("input[name='phone']").value;
            this.formData.date = this.$form.querySelector("input[name='data']").value;
            this.formData.time = this.$form.querySelector("input[name='time']").value;
            this.formData.info = this.$form.querySelector("textarea[name='more_info']").value;
          }
          this.updateForm();
        });
      });
      // Form submit
      this.$form.querySelector("form").addEventListener("submit", e => {
        if (this.currentStep < 5) {
          e.preventDefault();
          this.currentStep++;
          this.updateForm();
        }
      });
    }

    /**
     * Update form front-end
     * Show next or previous section etc.
     */
    updateForm() {
      this.$step.innerText = this.currentStep;

      // TODO: Validation

      this.slides.forEach(slide => {
        slide.classList.remove("active");

        if (slide.dataset.step == this.currentStep) {
          slide.classList.add("active");
        }
      });

      this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
      this.$step.parentElement.hidden = this.currentStep >= 6;

    }

    /**
     * Submit form
     *
     * TODO: validation
     */
    submit(e) {
      e.preventDefault();
      this.currentStep++;
      this.updateForm();
    }
  }
  const form = document.querySelector(".form--steps");
  if (form !== null) {
    new FormSteps(form);
  }
});

