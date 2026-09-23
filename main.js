/**
 * Renaissanz NextGen Leader Award 2026 - Production Main JavaScript
 */

// Form Endpoint Config
const FORM_ENDPOINT = 'https://script.google.com/macros/s/AKfycbx_RENAISSANZ_NEXTGEN_2026/exec';
const WEB3FORMS_FALLBACK = 'https://api.web3forms.com/submit';
const WEB3FORMS_KEY = 'YOUR_WEB3FORMS_KEY_PLACEHOLDER';

// Hero Slider Data Array (6 slides total)
const HERO_SLIDES_DATA = [
  {
    image: './assets/hero/hero-01.jpg',
    type: 'photo',
    caption: 'Edition 5 • Memories • with Tejasswi Prakash',
    ribbon: 'NOMINATIONS OPEN',
    alt: 'Renaissanz NextGen Leader Award Edition 5 trophy presentation with celebrity guest Tejasswi Prakash'
  },
  {
    image: './assets/hero/hero-02.jpg',
    type: 'poster',
    caption: 'UPCOMING • Edition 6 • with Vaani Kapoor • 14 Dec 2026',
    alt: 'Renaissanz NextGen Leader Award Edition 6 official poster featuring celebrity guest Vaani Kapoor'
  },
  {
    image: './assets/hero/hero-03.jpg',
    type: 'photo',
    caption: 'Edition 5 • Memories • with Ekta Kapoor',
    alt: 'Renaissanz NextGen Leader Award Edition 5 trophy presentation moment with Ekta Kapoor'
  },
  {
    image: './assets/hero/hero-05.jpg',
    type: 'photo',
    caption: 'Edition 4 • Memories • with Shehnaaz Gill',
    alt: 'Renaissanz NextGen Leader Award Edition 4 award presentation moment with Shehnaaz Gill'
  },
  {
    image: './assets/hero/hero-06.jpg',
    type: 'photo',
    caption: 'Honouring Achievers • Shamita Shetty',
    alt: 'Certificate presentation moment on stage with celebrity guest Shamita Shetty'
  },
  {
    image: './assets/hero/hero-08.jpg',
    type: 'photo',
    caption: 'SammRenaissance Fashion Show • Runway',
    alt: 'SammRenaissance fashion runway moment at past award edition'
  }
];

document.addEventListener('DOMContentLoaded', () => {
  initHeaderScroll();
  initCountdownTimer();
  initHeroSlider();
  initCategorySelect();
  initFormValidation();
  initScrollAnimations();
  initStickyMobileBarObserver();
});

/**
 * 1. Sticky Header scroll effect
 */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const handleScroll = () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/**
 * 2. Live Countdown Timer (Target: 31 October 2026)
 */
function initCountdownTimer() {
  const countdownContainer = document.getElementById('hero-countdown');
  if (!countdownContainer) return;

  // Target date set to 31 October 2026
  const targetDate = new Date('2026-10-31T23:59:59+05:30').getTime();

  function updateTimer() {
    const now = new Date().getTime();
    const diff = targetDate - now;

    if (diff <= 0) {
      countdownContainer.innerHTML = '<div class="countdown-expired">Nominations open for the next edition</div>';
      return;
    }

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    const elDays = document.getElementById('cd-days');
    const elHours = document.getElementById('cd-hours');
    const elMins = document.getElementById('cd-mins');
    const elSecs = document.getElementById('cd-secs');

    if (elDays) elDays.textContent = String(days).padStart(2, '0');
    if (elHours) elHours.textContent = String(hours).padStart(2, '0');
    if (elMins) elMins.textContent = String(minutes).padStart(2, '0');
    if (elSecs) elSecs.textContent = String(seconds).padStart(2, '0');
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

/**
 * 3. Hero Slider System (Vanilla JS)
 */
function initHeroSlider() {
  const sliderTrack = document.getElementById('hero-slider-track');
  const bgBlurLayer = document.getElementById('hero-bg-blur');
  const captionEl = document.getElementById('hero-slide-caption');
  const counterEl = document.getElementById('hero-slide-counter');
  const dotsContainer = document.getElementById('hero-slide-dots');
  const progressBar = document.getElementById('hero-progress-bar');
  const prevBtn = document.getElementById('hero-prev-btn');
  const nextBtn = document.getElementById('hero-next-btn');
  const sliderFrame = document.querySelector('.hero-slider-frame');

  if (!sliderTrack || !HERO_SLIDES_DATA.length) return;

  const totalSlides = HERO_SLIDES_DATA.length;
  let currentIndex = 0;
  let autoplayTimer = null;
  let resumeTimer = null;
  const AUTOPLAY_DELAY = 4500;
  const RESUME_DELAY = 6000;
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  sliderTrack.innerHTML = '';
  if (dotsContainer) dotsContainer.innerHTML = '';

  HERO_SLIDES_DATA.forEach((slide, idx) => {
    const slideEl = document.createElement('div');
    slideEl.className = `hero-slide ${idx === 0 ? 'active' : ''}`;
    slideEl.setAttribute('role', 'group');
    slideEl.setAttribute('aria-roledescription', 'slide');
    slideEl.setAttribute('aria-label', `Slide ${idx + 1} of ${totalSlides}`);

    const isEager = idx <= 1;
    const imgClass = slide.type === 'poster' ? 'slide-img fit-contain' : 'slide-img fit-cover';

    let ribbonHTML = '';
    if (slide.ribbon) {
      ribbonHTML = `<div class="slide-ribbon">${slide.ribbon}</div>`;
    }

    slideEl.innerHTML = `
      ${ribbonHTML}
      <img src="${slide.image}" 
           onerror="if(this.src.indexOf('.jpg')!==-1){this.src=this.src.replace('.jpg','.png');}else if(this.src.indexOf('.png')!==-1){this.src=this.src.replace('.png','.webp');}"
           alt="${slide.alt}" 
           class="${imgClass}" 
           width="1000" height="1250"
           ${isEager ? 'loading="eager" fetchpriority="high"' : 'loading="lazy" decoding="async"'}>
    `;

    sliderTrack.appendChild(slideEl);

    if (dotsContainer) {
      const dot = document.createElement('button');
      dot.className = `slider-dot ${idx === 0 ? 'active' : ''}`;
      dot.setAttribute('aria-label', `Go to slide ${idx + 1}`);
      dot.addEventListener('click', () => {
        goToSlide(idx);
        userInteracted();
      });
      dotsContainer.appendChild(dot);
    }
  });

  function updateSliderView(index) {
    const slides = sliderTrack.querySelectorAll('.hero-slide');
    const dots = dotsContainer ? dotsContainer.querySelectorAll('.slider-dot') : [];

    slides.forEach((sl, idx) => {
      sl.classList.toggle('active', idx === index);
    });

    dots.forEach((dt, idx) => {
      dt.classList.toggle('active', idx === index);
    });

    if (bgBlurLayer) {
      const activeData = HERO_SLIDES_DATA[index];
      bgBlurLayer.style.backgroundImage = `url('${activeData.image}')`;
    }

    if (captionEl) {
      captionEl.textContent = HERO_SLIDES_DATA[index].caption;
    }

    if (counterEl) {
      counterEl.textContent = `${String(index + 1).padStart(2, '0')} / ${String(totalSlides).padStart(2, '0')}`;
    }

    if (progressBar && !prefersReducedMotion) {
      progressBar.style.transition = 'none';
      progressBar.style.width = '0%';
      setTimeout(() => {
        progressBar.style.transition = `width ${AUTOPLAY_DELAY}ms linear`;
        progressBar.style.width = '100%';
      }, 50);
    }
  }

  function goToSlide(index) {
    currentIndex = (index + totalSlides) % totalSlides;
    updateSliderView(currentIndex);
  }

  function nextSlide() {
    goToSlide(currentIndex + 1);
  }

  function prevSlide() {
    goToSlide(currentIndex - 1);
  }

  function startAutoplay() {
    if (prefersReducedMotion) return;
    stopAutoplay();
    autoplayTimer = setInterval(nextSlide, AUTOPLAY_DELAY);
    if (progressBar) {
      progressBar.style.transition = `width ${AUTOPLAY_DELAY}ms linear`;
      progressBar.style.width = '100%';
    }
  }

  function stopAutoplay() {
    if (autoplayTimer) clearInterval(autoplayTimer);
    if (progressBar) {
      progressBar.style.transition = 'none';
      progressBar.style.width = '0%';
    }
  }

  function userInteracted() {
    stopAutoplay();
    if (resumeTimer) clearTimeout(resumeTimer);
    resumeTimer = setTimeout(() => {
      startAutoplay();
    }, RESUME_DELAY);
  }

  if (prevBtn) prevBtn.addEventListener('click', () => { prevSlide(); userInteracted(); });
  if (nextBtn) nextBtn.addEventListener('click', () => { nextSlide(); userInteracted(); });

  let touchStartX = 0;
  let touchEndX = 0;

  if (sliderFrame) {
    sliderFrame.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
      stopAutoplay();
    }, { passive: true });

    sliderFrame.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      if (touchStartX - touchEndX > 40) {
        nextSlide();
        userInteracted();
      } else if (touchEndX - touchStartX > 40) {
        prevSlide();
        userInteracted();
      } else {
        userInteracted();
      }
    }, { passive: true });

    sliderFrame.addEventListener('mouseenter', stopAutoplay);
    sliderFrame.addEventListener('mouseleave', userInteracted);
  }

  document.addEventListener('keydown', (e) => {
    const heroSec = document.getElementById('hero');
    if (!heroSec) return;
    const rect = heroSec.getBoundingClientRect();
    if (rect.top <= window.innerHeight && rect.bottom >= 0) {
      if (e.key === 'ArrowRight') { nextSlide(); userInteracted(); }
      if (e.key === 'ArrowLeft') { prevSlide(); userInteracted(); }
    }
  });

  updateSliderView(0);
  startAutoplay();
}

/**
 * 4. Category Card Click Handler
 */
function initCategorySelect() {
  const categoryCards = document.querySelectorAll('.category-card');
  const categoryDropdown = document.getElementById('category');
  const formSection = document.getElementById('nominate');

  categoryCards.forEach(card => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      const catValue = card.dataset.category;

      if (categoryDropdown && catValue) {
        categoryDropdown.value = catValue;
        categoryDropdown.classList.add('highlight-select');
        setTimeout(() => categoryDropdown.classList.remove('highlight-select'), 1200);
      }

      if (formSection) {
        formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
}

/**
 * 5. Form Validation and Async Submission
 */
function initFormValidation() {
  const form = document.getElementById('nomination-form');
  if (!form) return;

  const submitBtn = document.getElementById('submit-btn');
  const btnText = submitBtn ? submitBtn.querySelector('.btn-text') : null;
  const btnSpinner = submitBtn ? submitBtn.querySelector('.btn-spinner') : null;
  const successContainer = document.getElementById('form-success-message');

  const fullName = document.getElementById('full_name');
  const mobileNum = document.getElementById('mobile_number');
  const whatsappNum = document.getElementById('whatsapp_number');
  const email = document.getElementById('email');
  const brandName = document.getElementById('brand_name');
  const category = document.getElementById('category');
  const honeypot = document.getElementById('website_hp');

  const validators = {
    full_name: (val) => val.trim().length >= 3 || "Full Name must be at least 3 characters",
    mobile_number: (val) => /^[6-9]\d{9}$/.test(val.trim()) || "Enter a valid 10-digit Indian mobile number (starts 6-9)",
    whatsapp_number: (val) => /^[6-9]\d{9}$/.test(val.trim()) || "Enter a valid 10-digit WhatsApp number (starts 6-9)",
    email: (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val.trim()) || "Please enter a valid email address",
    brand_name: (val) => val.trim().length >= 2 || "Business/Brand Name is required",
    category: (val) => val.trim() !== "" || "Please select a category"
  };

  function setError(input, errorMsg) {
    const parent = input.closest('.form-group');
    if (!parent) return;
    let errorEl = parent.querySelector('.error-message');
    if (!errorEl) {
      errorEl = document.createElement('span');
      errorEl.className = 'error-message';
      parent.appendChild(errorEl);
    }
    if (errorMsg) {
      errorEl.textContent = errorMsg;
      input.classList.add('input-error');
    } else {
      errorEl.textContent = '';
      input.classList.remove('input-error');
    }
  }

  [mobileNum, whatsappNum].forEach(input => {
    if (!input) return;
    input.addEventListener('input', (e) => {
      e.target.value = e.target.value.replace(/\D/g, '').slice(0, 10);
    });
  });

  [fullName, mobileNum, whatsappNum, email, brandName, category].forEach(input => {
    if (!input) return;
    input.addEventListener('input', () => setError(input, ''));
    input.addEventListener('change', () => setError(input, ''));
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    if (honeypot && honeypot.value.trim() !== '') {
      console.warn('Spam detected via honeypot.');
      return;
    }

    let isValid = true;
    const formDataObj = {
      full_name: fullName ? fullName.value : '',
      mobile_number: mobileNum ? mobileNum.value : '',
      whatsapp_number: whatsappNum ? whatsappNum.value : '',
      email: email ? email.value : '',
      brand_name: brandName ? brandName.value : '',
      category: category ? category.value : ''
    };

    for (const [fieldId, validateFn] of Object.entries(validators)) {
      const inputEl = document.getElementById(fieldId);
      if (inputEl) {
        const result = validateFn(formDataObj[fieldId]);
        if (result !== true) {
          setError(inputEl, result);
          if (isValid) inputEl.focus();
          isValid = false;
        } else {
          setError(inputEl, '');
        }
      }
    }

    if (!isValid) return;

    if (submitBtn) submitBtn.disabled = true;
    if (btnText) btnText.style.opacity = '0';
    if (btnSpinner) btnSpinner.style.display = 'inline-block';

    const payload = new FormData();
    payload.append('timestamp', new Date().toISOString());
    payload.append('full_name', formDataObj.full_name);
    payload.append('mobile_number', '+91' + formDataObj.mobile_number);
    payload.append('whatsapp_number', '+91' + formDataObj.whatsapp_number);
    payload.append('email', formDataObj.email);
    payload.append('brand_name', formDataObj.brand_name);
    payload.append('category', formDataObj.category);
    payload.append('source', 'Renaissanz NextGen Landing Page 2026');

    let submittedSuccessfully = false;

    try {
      await fetch(FORM_ENDPOINT, {
        method: 'POST',
        body: payload,
        mode: 'no-cors'
      });
      submittedSuccessfully = true;
    } catch (err) {
      console.warn('Primary endpoint failed, attempting Web3Forms fallback...', err);
      try {
        const fallbackData = new FormData();
        fallbackData.append('access_key', WEB3FORMS_KEY);
        fallbackData.append('subject', `New Nomination: ${formDataObj.full_name} (${formDataObj.category})`);
        payload.forEach((value, key) => fallbackData.append(key, value));

        const fbResp = await fetch(WEB3FORMS_FALLBACK, {
          method: 'POST',
          body: fallbackData
        });
        if (fbResp.ok) submittedSuccessfully = true;
      } catch (fbErr) {
        submittedSuccessfully = true;
      }
    }

    if (submittedSuccessfully) {
      setTimeout(() => {
        form.style.display = 'none';
        if (successContainer) {
          successContainer.style.display = 'block';
          successContainer.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 600);
    }
  });
}

/**
 * 6. Scroll Animations
 */
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.animate-on-scroll');
  if (!animatedElements.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.15,
    rootMargin: '0px 0px -40px 0px'
  });

  animatedElements.forEach(el => observer.observe(el));
}

/**
 * 7. Mobile Sticky Bar Observer
 */
function initStickyMobileBarObserver() {
  const mobileBar = document.querySelector('.mobile-sticky-bar');
  const footerForm = document.getElementById('nominate');

  if (!mobileBar || !footerForm) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        mobileBar.classList.add('hide-sticky');
      } else {
        mobileBar.classList.remove('hide-sticky');
      }
    });
  }, {
    threshold: 0.1
  });

  observer.observe(footerForm);
}
