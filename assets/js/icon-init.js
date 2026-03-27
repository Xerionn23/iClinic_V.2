(function () {
  function debounce(fn, wait) {
    let t;
    return function () {
      const ctx = this;
      const args = arguments;
      clearTimeout(t);
      t = setTimeout(function () {
        fn.apply(ctx, args);
      }, wait);
    };
  }

  function refreshIcons() {
    try {
      if (typeof feather !== 'undefined' && feather && typeof feather.replace === 'function') {
        feather.replace();
      }
    } catch (e) {
      // noop
    }

    try {
      const svgs = document.querySelectorAll('svg.feather');
      svgs.forEach(function (svg) {
        if (!svg) return;
        if (!svg.style.display) svg.style.display = 'inline-block';
        if (!svg.style.flexShrink) svg.style.flexShrink = '0';
        if (!svg.style.verticalAlign) svg.style.verticalAlign = 'middle';
      });
    } catch (e) {
      // noop
    }

    try {
      if (typeof lucide !== 'undefined' && lucide && typeof lucide.createIcons === 'function') {
        lucide.createIcons();
      }
    } catch (e) {
      // noop
    }
  }

  const refreshIconsDebounced = debounce(refreshIcons, 50);

  function startObservers() {
    refreshIcons();

    try {
      const target = document.body;
      if (!target || typeof MutationObserver === 'undefined') return;

      const observer = new MutationObserver(function () {
        refreshIconsDebounced();
      });

      observer.observe(target, {
        childList: true,
        subtree: true,
        attributes: true,
        attributeFilter: ['class', 'style', 'x-show', 'x-cloak', 'aria-hidden'],
      });
    } catch (e) {
      // noop
    }

    window.addEventListener('resize', refreshIconsDebounced);
    window.addEventListener('orientationchange', refreshIconsDebounced);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startObservers);
  } else {
    startObservers();
  }

  document.addEventListener('alpine:initialized', refreshIconsDebounced);
})();
