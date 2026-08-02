{%- if site.search_enabled != false -%}
// Lazy-load the search index.
//
// Just the Docs requests assets/js/search-data.json from initSearch() as soon
// as the DOM is ready (see the theme's assets/js/just-the-docs.js), so every
// visitor downloads the whole index - over 1 MB of JSON for this site - and
// pays for building the lunr index, on every page, even if they never search.
//
// The theme has no hook for deferring that request (just-the-docs#1210), but
// it does include this file at the end of just-the-docs.js: late enough that
// initSearch() is already scheduled, early enough that it has not run yet. So
// the request is held back here until the visitor reaches for the search box,
// and is then sent unchanged, leaving the theme's own search code untouched.
(function () {
  var searchDataUrl = {{ "assets/js/search-data.json" | relative_url | jsonify }};
  var nativeOpen = XMLHttpRequest.prototype.open;
  var nativeSend = XMLHttpRequest.prototype.send;
  var deferredRequest = null;

  // Requests other than the search index are passed straight through, and the
  // patch is removed again once the theme has initialised (see below), so it
  // is only in place for the initial page setup.
  XMLHttpRequest.prototype.open = function (method, url) {
    if (url === searchDataUrl) {
      this.isSearchIndexRequest = true;
    }
    return nativeOpen.apply(this, arguments);
  };

  XMLHttpRequest.prototype.send = function () {
    if (!this.isSearchIndexRequest) {
      return nativeSend.apply(this, arguments);
    }
    deferredRequest = { xhr: this, args: arguments };
  };

  function loadSearchIndex() {
    if (!deferredRequest) return;

    var xhr = deferredRequest.xhr;
    var args = deferredRequest.args;
    deferredRequest = null;

    // initSearch() assigned request.onload before this listener was added, so
    // it runs first: by the time this fires, the index is built and the
    // theme's own input handlers are live. Re-fire 'focus' so that anything
    // typed while the index was still loading is searched immediately,
    // instead of only on the next keystroke.
    xhr.addEventListener('load', function () {
      var searchInput = document.getElementById('search-input');
      if (searchInput && searchInput.value !== '' &&
          document.activeElement === searchInput) {
        searchInput.dispatchEvent(new Event('focus'));
      }
    });

    nativeSend.apply(xhr, args);
  }

  function themeReady() {
    // initSearch() has run by now - the theme registered its DOMContentLoaded
    // handler before this one - so stop intercepting requests.
    XMLHttpRequest.prototype.open = nativeOpen;
    XMLHttpRequest.prototype.send = nativeSend;

    var searchInput = document.getElementById('search-input');
    if (!searchInput) {
      // No search box to wait for: send whatever was held back, if anything.
      loadSearchIndex();
      return;
    }

    // 'mouseenter' and 'touchstart' give the download a head start on the
    // click or tap that is about to focus the search box.
    ['focus', 'mouseenter', 'touchstart'].forEach(function (type) {
      searchInput.addEventListener(type, loadSearchIndex, { once: true, passive: true });
    });
    {%- if site.search.focus_shortcut_key %}

    // The theme's focus shortcut only starts working once the index has
    // loaded, which now requires focusing the search box first. Focus it here
    // too, so the shortcut keeps working from the first key press.
    document.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === '{{ site.search.focus_shortcut_key }}') {
        e.preventDefault();

        var mainHeader = document.getElementById('main-header');
        if (mainHeader) mainHeader.classList.add('nav-open');
        searchInput.focus();
      }
    });
    {%- endif %}
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', themeReady);
  } else {
    // just-the-docs.js was loaded after the document was parsed, so
    // initSearch() already ran and nothing was intercepted.
    themeReady();
  }
})();
{%- endif -%}
