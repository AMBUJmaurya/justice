// Mobile Menu Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger
        const spans = hamburger.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close menu when clicking on a link
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
            const spans = hamburger.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });
}

// Pricing Toggle (Monthly/Yearly)
const pricingToggle = document.getElementById('pricingToggle');
const pricingGrid = document.getElementById('pricingGrid');

if (pricingToggle && pricingGrid) {
    pricingToggle.addEventListener('change', function() {
        const pricingCards = pricingGrid.querySelectorAll('.pricing-card');
        
        if (this.checked) {
            // Yearly pricing
            const yearlyPrices = [29, 49, 89];
            pricingCards.forEach((card, index) => {
                const amountElement = card.querySelector('.amount');
                if (amountElement) {
                    amountElement.textContent = yearlyPrices[index];
                }
                const periodElement = card.querySelector('.period');
                if (periodElement) {
                    periodElement.textContent = 'Per Year';
                }
            });
        } else {
            // Monthly pricing
            const monthlyPrices = [39, 59, 99];
            pricingCards.forEach((card, index) => {
                const amountElement = card.querySelector('.amount');
                if (amountElement) {
                    amountElement.textContent = monthlyPrices[index];
                }
                const periodElement = card.querySelector('.period');
                if (periodElement) {
                    periodElement.textContent = 'Per Year';
                }
            });
        }
    });
}

// Tab Functionality
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('[data-tab-content]');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        tabBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        
        // Get the tab data attribute
        const tabId = btn.getAttribute('data-tab');
        
        // You can add logic here to show/hide tab contents if needed
        console.log('Tab clicked:', tabId);
    });
});

// Smooth Scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Header Scroll Effect
let lastScroll = 0;
const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        header.style.boxShadow = '0 4px 20px rgba(0,0,0,0.15)';
    } else {
        header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
    }
    
    lastScroll = currentScroll;
});

// Scroll Animations (Fade in on scroll)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for scroll animation
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll('.feature-card, .service-card, .expertise-item, .news-card, .testimonial-card, .pricing-card, .practice-area-card, .court-card, .advocate-card, .blog-card, .office-card, .contact-info-card, .award-card, .mv-card, .timeline-item, .process-step, .stat-item');
    
    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Client-side validation for demo forms only
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        if (this.id === 'aiChatForm') {
            return;
        }
        const isServerForm = (this.getAttribute('method') || '').toLowerCase() === 'post';
        if (isServerForm) {
            return;
        }

        e.preventDefault();

        let isValid = true;
        const requiredFields = this.querySelectorAll('[required]');
        requiredFields.forEach(field => {
            const value = field.type === 'checkbox' ? field.checked : field.value.trim();
            if (!value) {
                isValid = false;
                field.style.borderColor = 'red';
            } else {
                field.style.borderColor = '';
            }
        });

        if (isValid) {
            alert('Thank you for your message! We will get back to you soon.');
            this.reset();
        } else {
            alert('Please fill in all required fields.');
        }
    });
});

// Dropdown menu close on outside click
document.addEventListener('click', (e) => {
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        if (!dropdown.contains(e.target)) {
            const menu = dropdown.querySelector('.dropdown-menu');
            if (menu) {
                menu.style.opacity = '0';
                menu.style.visibility = 'hidden';
            }
        }
    });
});

// Login Toggle for Contact Page
const loginToggle = document.querySelector('.login-toggle');
const loginForm = document.getElementById('loginForm');

if (loginToggle && loginForm) {
    loginToggle.addEventListener('click', function(e) {
        e.preventDefault();
        if (loginForm.style.display === 'none') {
            loginForm.style.display = 'block';
        } else {
            loginForm.style.display = 'none';
        }
    });
}

// Booking Form Loading State
const bookingForm = document.getElementById('bookingForm');
if (bookingForm) {
    bookingForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const submitBtn = this.querySelector('.btn-submit');
        
        // Show loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Simulate form submission
        setTimeout(() => {
            alert('Booking submitted successfully! We will contact you soon.');
            this.reset();
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
        }, 2000);
    });
}

// Card Number Formatting
const cardInput = document.getElementById('card-number');
if (cardInput) {
    cardInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\s/g, '');
        let formattedValue = value.match(/.{1,4}/g)?.join(' ') || value;
        e.target.value = formattedValue;
    });
}

// Circular Text Animation
const circleTextSvg = document.querySelector('.circle-text-svg');
if (circleTextSvg) {
    let rotation = 0;
    setInterval(() => {
        rotation += 0.5;
        circleTextSvg.style.transform = `rotate(${rotation}deg)`;
    }, 50);
}

// Set background images for expertise items
document.addEventListener('DOMContentLoaded', () => {
    const expertiseItems = document.querySelectorAll('.expertise-item[data-bg-image]');
    expertiseItems.forEach(item => {
        const bgImage = item.getAttribute('data-bg-image');
        if (bgImage) {
            item.style.setProperty('--bg-img', `url('${bgImage}')`);
        }
    });
});

console.log('ByLaw Site - Script loaded successfully');

// AI Chat Widget
const initAiChat = () => {
    const widget = document.getElementById('aiChatWidget');
    if (!widget) return;

    const fab = document.getElementById('aiChatFab');
    const panel = document.getElementById('aiChatPanel');
    const closeBtn = document.getElementById('aiChatClose');
    const form = document.getElementById('aiChatForm');
    const input = document.getElementById('aiChatInput');
    const messages = document.getElementById('aiChatMessages');

    const getCookie = (name) => {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return '';
    };

    const addMsg = (text, who) => {
        const div = document.createElement('div');
        div.className = `ai-chat-msg ai-chat-msg--${who}`;
        div.textContent = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
        return div;
    };

    const open = () => {
        panel.hidden = false;
        widget.classList.add('ai-chat--open');
        setTimeout(() => input?.focus(), 50);
    };

    const close = () => {
        panel.hidden = true;
        widget.classList.remove('ai-chat--open');
    };

    fab?.addEventListener('click', () => {
        if (panel.hidden) open();
        else close();
    });
    closeBtn?.addEventListener('click', close);

    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = (input.value || '').trim();
        if (!question) return;

        addMsg(question, 'user');
        input.value = '';

        const typing = addMsg('Typing…', 'bot');

        try {
            const resp = await fetch('/ai/ask/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ question }),
            });
            const data = await resp.json().catch(() => ({}));
            typing.remove();
            if (!resp.ok) {
                addMsg(data?.answer || `Request failed (HTTP ${resp.status}).`, 'bot');
                return;
            }
            addMsg(data?.answer || 'Sorry, I could not answer that right now.', 'bot');
        } catch (err) {
            typing.remove();
            addMsg('Network error. Please try again.', 'bot');
        }
    });
};

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAiChat);
} else {
    initAiChat();
}

