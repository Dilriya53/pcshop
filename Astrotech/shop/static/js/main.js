/* =========================
    ASTRO TECH - main.js
========================== */

document.addEventListener('DOMContentLoaded', function () {

    /* --------------------------
        CART FUNCTIONALITY
    -------------------------- */

    let cart = [];

    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const productCard = btn.closest('.product-card');
            const productName = productCard.querySelector('h3').textContent;
            const productPrice = productCard.querySelector('.price').textContent;

            cart.push({ name: productName, price: productPrice });

            showToast(productName + ' added to cart!');
            updateCartCount();
        });
    });

    function updateCartCount() {
        const cartBadge = document.getElementById('cart-count');
        if (cartBadge) {
            cartBadge.textContent = cart.length;
        }
    }

    /* --------------------------
        TOAST NOTIFICATION
    -------------------------- */

    function showToast(message) {
        let toast = document.getElementById('toast');

        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'toast';
            toast.style.cssText = `
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: #3b82f6;
                color: white;
                padding: 14px 24px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 600;
                z-index: 9999;
                opacity: 0;
                transition: opacity 0.3s ease;
                box-shadow: 0 0 20px rgba(59,130,246,0.5);
            `;
            document.body.appendChild(toast);
        }

        toast.textContent = message;
        toast.style.opacity = '1';

        setTimeout(function () {
            toast.style.opacity = '0';
        }, 2500);
    }

    /* --------------------------
        NAVBAR SCROLL EFFECT
    -------------------------- */

    const navbar = document.querySelector('nav');

    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(11,15,25,0.98)';
            navbar.style.boxShadow = '0 4px 20px rgba(0,0,0,0.5)';
        } else {
            navbar.style.background = 'rgba(17,24,39,0.95)';
            navbar.style.boxShadow = 'none';
        }
    });

    /* --------------------------
        SCROLL REVEAL ANIMATION
    -------------------------- */

    const revealElements = document.querySelectorAll(
        '.category-card, .product-card, .feature-card, .builder'
    );

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    /* --------------------------
        SMOOTH SCROLL FOR NAV LINKS
    -------------------------- */

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

});
