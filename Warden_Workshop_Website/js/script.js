// ============================================
// MOBILE NAVIGATION TOGGLE
// ============================================
const mobileMenu = document.getElementById('mobile-menu');
const mobileDrawer = document.querySelector('.mobile-drawer');

if (mobileMenu) {
    mobileMenu.addEventListener('click', () => {
        mobileMenu.classList.toggle('active-menu');
        if (mobileDrawer) mobileDrawer.classList.toggle('active-menu');
    });
}

// Close mobile menu when any non-dropdown nav link is clicked
document.querySelectorAll('.mobile-drawer a:not(.dropdown-toggle)').forEach(link => {
    link.addEventListener('click', () => {
        if (mobileMenu) mobileMenu.classList.remove('active-menu');
        if (mobileDrawer) mobileDrawer.classList.remove('active-menu');
    });
});


// ============================================
// DROPDOWN — Desktop hover is CSS-only.
// JS handles click-to-toggle, mobile accordion,
// outside-click close, and Escape key close.
// ============================================
const dropdownParents = document.querySelectorAll('.has-dropdown');

dropdownParents.forEach(parent => {
    const toggle = parent.querySelector('.dropdown-toggle');

    if (toggle) {
        toggle.addEventListener('click', (e) => {
            e.preventDefault();

            const isOpen = parent.classList.contains('open');

            // Close all other dropdowns first
            dropdownParents.forEach(p => {
                p.classList.remove('open');
                const t = p.querySelector('.dropdown-toggle');
                if (t) t.setAttribute('aria-expanded', 'false');
            });

            if (!isOpen) {
                parent.classList.add('open');
                toggle.setAttribute('aria-expanded', 'true');
            }
        });
    }
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.has-dropdown')) {
        dropdownParents.forEach(p => {
            p.classList.remove('open');
            const t = p.querySelector('.dropdown-toggle');
            if (t) t.setAttribute('aria-expanded', 'false');
        });
    }
});

// Close dropdown on Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        dropdownParents.forEach(p => {
            p.classList.remove('open');
            const t = p.querySelector('.dropdown-toggle');
            if (t) t.setAttribute('aria-expanded', 'false');
        });
    }
});


// ============================================
// SCROLL REVEAL ANIMATION
// ============================================
const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, observerOptions);

document.querySelectorAll('.reveal').forEach((el) => {
    observer.observe(el);
});


// ============================================
// DYNAMIC NAVBAR SHADOW ON SCROLL
// ============================================
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (!nav) return;
    if (window.scrollY > 50) {
        nav.style.boxShadow = '0 5px 20px rgba(0,0,0,0.08)';
    } else {
        nav.style.boxShadow = 'none';
    }
});
