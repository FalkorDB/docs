/**
 * FalkorDB Documentation Enhanced UX Script
 * Provides smooth interactions and improved user experience
 */

(function() {
  'use strict';

  // ===== Back to Top Button =====
  function initBackToTop() {
    // Create back-to-top button
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '↑';
    backToTop.setAttribute('aria-label', 'Back to top');
    backToTop.setAttribute('title', 'Back to top');
    document.body.appendChild(backToTop);

    // Show/hide button based on scroll position
    let scrollTimeout;
    window.addEventListener('scroll', function() {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(function() {
        if (window.pageYOffset > 300) {
          backToTop.classList.add('visible');
        } else {
          backToTop.classList.remove('visible');
        }
      }, 100);
    });

    // Scroll to top on click
    backToTop.addEventListener('click', function() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // ===== Enhanced Copy Button Feedback =====
  function initCopyFeedback() {
    document.addEventListener('click', function(e) {
      if (e.target.classList.contains('copy-btn')) {
        const btn = e.target;
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        btn.style.background = 'linear-gradient(135deg, #4ade80, #22c55e)';
        
        setTimeout(function() {
          btn.textContent = originalText;
          btn.style.background = '';
        }, 2000);
      }
    });
  }

  // ===== Smooth Anchor Scrolling =====
  function initSmoothAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
      anchor.addEventListener('click', function(e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        
        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
          
          // Update URL without jumping
          if (history.pushState) {
            history.pushState(null, null, href);
          }
        }
      });
    });
  }

  // ===== Enhanced External Link Indicators =====
  function initExternalLinks() {
    const domain = window.location.hostname;
    document.querySelectorAll('.main-content a').forEach(function(link) {
      const href = link.getAttribute('href');
      if (href && (href.startsWith('http') || href.startsWith('//'))) {
        const linkDomain = link.hostname;
        if (linkDomain && linkDomain !== domain) {
          link.setAttribute('target', '_blank');
          link.setAttribute('rel', 'noopener noreferrer');
          
          // Add external link indicator
          if (!link.querySelector('.external-link-icon')) {
            const icon = document.createElement('span');
            icon.className = 'external-link-icon';
            icon.innerHTML = ' ↗';
            icon.style.fontSize = '0.8em';
            icon.style.opacity = '0.6';
            link.appendChild(icon);
          }
        }
      }
    });
  }

  // ===== Code Block Enhancements =====
  function initCodeEnhancements() {
    document.querySelectorAll('pre code').forEach(function(codeBlock) {
      // Add language label if available
      const classes = codeBlock.className.split(' ');
      const langClass = classes.find(c => c.startsWith('language-'));
      if (langClass) {
        const lang = langClass.replace('language-', '').toUpperCase();
        const pre = codeBlock.parentElement;
        
        if (!pre.querySelector('.code-lang-label')) {
          const label = document.createElement('div');
          label.className = 'code-lang-label';
          label.textContent = lang;
          label.style.cssText = `
            position: absolute;
            top: 8px;
            left: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            color: #FDE900;
            background: rgba(253, 233, 0, 0.15);
            padding: 2px 8px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
          `;
          pre.style.position = 'relative';
          pre.insertBefore(label, pre.firstChild);
        }
      }
    });
  }

  // ===== Table of Contents Highlighting =====
  function initTocHighlighting() {
    const observer = new IntersectionObserver(
      function(entries) {
        entries.forEach(function(entry) {
          if (entry.isIntersecting) {
            const id = entry.target.getAttribute('id');
            if (id) {
              // Remove active class from all TOC links
              document.querySelectorAll('.nav-list-link').forEach(function(link) {
                link.classList.remove('active');
              });
              
              // Add active class to current section
              const activeLink = document.querySelector(`.nav-list-link[href="#${id}"]`);
              if (activeLink) {
                activeLink.classList.add('active');
              }
            }
          }
        });
      },
      {
        rootMargin: '-20% 0px -80% 0px'
      }
    );

    // Observe all headings
    document.querySelectorAll('h1[id], h2[id], h3[id], h4[id]').forEach(function(heading) {
      observer.observe(heading);
    });
  }

  // ===== Keyboard Navigation Enhancement =====
  function initKeyboardNav() {
    document.addEventListener('keydown', function(e) {
      // Alt + Arrow Up: Scroll to top
      if (e.altKey && e.key === 'ArrowUp') {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      
      // Alt + Arrow Down: Scroll to bottom
      if (e.altKey && e.key === 'ArrowDown') {
        e.preventDefault();
        window.scrollTo({ 
          top: document.body.scrollHeight, 
          behavior: 'smooth' 
        });
      }
    });
  }

  // ===== Search Enhancement =====
  function initSearchEnhancement() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
      searchInput.setAttribute('placeholder', 'Search documentation...');
      
      // Add keyboard shortcut hint
      searchInput.addEventListener('focus', function() {
        this.setAttribute('placeholder', 'Type to search...');
      });
      
      searchInput.addEventListener('blur', function() {
        this.setAttribute('placeholder', 'Search documentation... (Ctrl+K)');
      });
      
      // Ctrl/Cmd + K to focus search
      document.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
          e.preventDefault();
          searchInput.focus();
        }
      });
    }
  }

  // ===== Loading Animation =====
  function initLoadingEffects() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
      mainContent.style.opacity = '0';
      mainContent.style.transform = 'translateY(20px)';
      mainContent.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      
      setTimeout(function() {
        mainContent.style.opacity = '1';
        mainContent.style.transform = 'translateY(0)';
      }, 100);
    }
  }

  // ===== Initialize All Enhancements =====
  function init() {
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function() {
        initBackToTop();
        initCopyFeedback();
        initSmoothAnchors();
        initExternalLinks();
        initCodeEnhancements();
        initTocHighlighting();
        initKeyboardNav();
        initSearchEnhancement();
        initLoadingEffects();
      });
    } else {
      // DOM already loaded
      initBackToTop();
      initCopyFeedback();
      initSmoothAnchors();
      initExternalLinks();
      initCodeEnhancements();
      initTocHighlighting();
      initKeyboardNav();
      initSearchEnhancement();
      initLoadingEffects();
    }
  }

  // Start initialization
  init();
})();
