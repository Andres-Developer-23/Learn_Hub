// ============================================
// LEARNHUB - ENROLLMENT FUNCTIONALITY
// Global function definitions
// ============================================

console.log('LearnHub: script.js parsing...');

let currentCourseData = null;

// These functions are defined at the global scope so they can be called from onclick attributes

function scrollToSection(sectionId) {
    console.log('LearnHub: scrollToSection called with:', sectionId);
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        console.log('LearnHub: Scrolled to section:', sectionId);
    } else {
        console.log('LearnHub: Section not found:', sectionId);
    }
}

function showEnrollmentForm() {
    console.log('LearnHub: showEnrollmentForm called');
    const modal = document.getElementById('enrollment-modal');
    
    if (!modal) {
        console.log('LearnHub: ERROR - Modal not found!');
        // Try to find any enrollment modal
        const allModals = document.querySelectorAll('[id*="enrollment"]');
        console.log('LearnHub: Found enrollment elements:', allModals.length);
        return;
    }
    
    // Check if modal was just created with innerHTML
    if (!modal.querySelector('.modal-content')) {
        console.log('LearnHub: Modal exists but has no content, creating...');
        createModalHTML(modal);
    }
    
    modal.style.display = 'flex';
    modal.style.zIndex = '9999';
    document.body.style.overflow = 'hidden';
    
    // Force a reflow
    modal.offsetHeight;
    
    console.log('LearnHub: Modal should be visible now');
    console.log('LearnHub: Modal display:', modal.style.display);
    console.log('LearnHub: Modal bounding rect:', JSON.stringify(modal.getBoundingClientRect()));
    
    setTimeout(function() {
        const nameInput = document.getElementById('enroll-name');
        if (nameInput) {
            nameInput.focus();
            console.log('LearnHub: Name input focused');
        } else {
            console.log('LearnHub: Name input still not found after modal creation');
        }
    }, 150);
}

function openEnrollmentModal() {
    console.log('LearnHub: openEnrollmentModal called');
    showEnrollmentForm();
}

function openCourseSummary(courseId) {
    console.log('LearnHub: openCourseSummary called with courseId:', courseId);
    const modal = document.getElementById('enrollment-modal');
    if (!modal) return;

    modal.style.display = 'flex';
    modal.style.zIndex = '9999';
    document.body.style.overflow = 'hidden';

    modal.innerHTML = `
        <div class="modal-content course-summary-modal">
            <button onclick="closeEnrollmentForm()" class="modal-close-btn">&times;</button>
            <div class="course-summary-loading">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Cargando información del curso...</p>
            </div>
        </div>
    `;

    if (courseId === 0) {
        setTimeout(function () {
            renderCourseSummary(modal, getMockCourseData());
        }, 300);
        return;
    }

    fetch('/api/course/' + courseId + '/')
        .then(function (res) {
            if (!res.ok) throw new Error('HTTP error ' + res.status);
            return res.json();
        })
        .then(function (data) {
            currentCourseData = data;
            renderCourseSummary(modal, data);
        })
        .catch(function (err) {
            console.error('LearnHub: Error fetching course:', err);
            modal.querySelector('.course-summary-loading').innerHTML =
                '<p style="color: var(--rose);">Error al cargar la información del curso. Intenta de nuevo.</p>';
        });
}

function getSectionTypeLabel(type) {
    var labels = { explicacion: '📖 Explicación', ejemplo: '💡 Ejemplo', demo: '🎯 Demo' };
    return labels[type] || '📌 ' + type;
}

function getInitials(name) {
    if (!name) return '?';
    return name.split(' ').map(function (w) { return w[0]; }).join('').substring(0, 2).toUpperCase();
}

function renderCourseSummary(modal, data) {
    currentCourseData = data;

    var contentsHtml = '';
    if (data.contents && data.contents.length > 0) {
        for (var i = 0; i < data.contents.length; i++) {
            var c = data.contents[i];
            contentsHtml += '<div class="content-item">' +
                '<span class="content-type-badge">' + getSectionTypeLabel(c.section_type) + '</span>' +
                '<span class="content-title">' + escapeHtml(c.title) + '</span>' +
                '</div>';
        }
    } else {
        contentsHtml = '<p class="no-contents">El contenido del curso estará disponible próximamente.</p>';
    }

    var examsHtml = '';
    if (data.exams && data.exams.length > 0) {
        var passing = data.exams[0].passing_score || 70;
        examsHtml = '<p><i class="fas fa-file-alt"></i> ' + data.exams_count + ' examen(es) · <i class="fas fa-check-circle"></i> ' + passing + '% mínimo para aprobar</p>';
    } else {
        examsHtml = '<p>No hay evaluaciones disponibles aún.</p>';
    }

    var instructorInitials = getInitials(data.instructor_name);

    modal.innerHTML = `
        <div class="modal-content course-summary-modal">
            <button onclick="closeEnrollmentForm()" class="modal-close-btn">&times;</button>

            <div class="course-summary-header">
                <span class="course-summary-icon">${data.icon || '📚'}</span>
                <h2>${escapeHtml(data.title)}</h2>
                <div class="course-summary-meta">
                    <span class="badge badge-level"><i class="fas fa-signal"></i> ${escapeHtml(data.level)}</span>
                    <span class="badge badge-duration"><i class="fas fa-clock"></i> ${escapeHtml(data.duration)}</span>
                </div>
            </div>

            <div class="course-summary-body">
                <div class="course-summary-section">
                    <h3><i class="fas fa-info-circle"></i> Descripción</h3>
                    <p class="course-description">${escapeHtml(data.description)}</p>
                </div>

                <div class="course-summary-section">
                    <h3><i class="fas fa-chalkboard-teacher"></i> Instructor</h3>
                    <div class="course-summary-instructor">
                        <div class="instructor-avatar">${instructorInitials}</div>
                        <div class="instructor-info">
                            <h4>${escapeHtml(data.instructor_name)}</h4>
                            <p>${escapeHtml(data.instructor_bio || 'Instructor profesional con amplia experiencia en la industria.')}</p>
                        </div>
                    </div>
                </div>

                <div class="course-summary-section">
                    <h3><i class="fas fa-list"></i> Contenido del curso</h3>
                    <div class="course-summary-contents">
                        ${contentsHtml}
                    </div>
                </div>

                <div class="course-summary-section">
                    <h3><i class="fas fa-file-alt"></i> Evaluaciones</h3>
                    ${examsHtml}
                </div>
            </div>

            <div class="course-summary-footer">
                <button class="cta-final-btn" onclick="transitionToEnrollment()">
                    <i class="fas fa-graduation-cap"></i> Inscribirme ahora
                </button>
            </div>
        </div>
    `;

    modal.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function getMockCourseData() {
    return {
        icon: '📚',
        title: 'Curso de ejemplo',
        description: 'Este curso cubre los fundamentos y conceptos avanzados de la materia. A través de lecciones prácticas y proyectos reales, desarrollarás las habilidades necesarias para aplicar lo aprendido en situaciones del mundo real. Ideal para estudiantes que buscan una formación completa y actualizada.',
        duration: '12 semanas',
        level: 'Principiante',
        instructor_name: 'Instructor Profesional',
        instructor_bio: 'Experto en la materia con años de experiencia formando a nuevos talentos.',
        contents: [
            { section_type: 'explicacion', title: 'Introducción a los conceptos fundamentales', content: '', order: 1 },
            { section_type: 'ejemplo', title: 'Ejercicios prácticos y aplicaciones', content: '', order: 2 },
            { section_type: 'demo', title: 'Proyecto integrador final', content: '', order: 3 },
        ],
        exams: [{ id: 1, title: 'Evaluación final', passing_score: 70, time_limit_minutes: 30 }],
        exams_count: 1,
    };
}

function escapeHtml(text) {
    if (!text) return '';
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function transitionToEnrollment() {
    console.log('LearnHub: transitionToEnrollment called');
    var modal = document.getElementById('enrollment-modal');
    if (modal) {
        modal.innerHTML = '';
    }
    showEnrollmentForm();
}

function goBackToSummary() {
    console.log('LearnHub: goBackToSummary called');
    var modal = document.getElementById('enrollment-modal');
    if (!modal || !currentCourseData) {
        closeEnrollmentForm();
        return;
    }
    renderCourseSummary(modal, currentCourseData);
}

function closeEnrollmentForm() {
    console.log('LearnHub: closeEnrollmentForm called');
    const modal = document.getElementById('enrollment-modal');
    if (!modal) {
        console.log('LearnHub: ERROR - Modal not found!');
        return;
    }
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
    const form = document.getElementById('enrollment-form');
    if (form) form.reset();
    const message = document.getElementById('enrollment-message');
    if (message) {
        message.style.display = 'none';
        message.textContent = '';
    }
    console.log('LearnHub: Modal closed');
}

function submitEnrollmentForm(event) {
    console.log('LearnHub: submitEnrollmentForm called');
    if (event) event.preventDefault();

    const nameInput = document.getElementById('enroll-name');
    const emailInput = document.getElementById('enroll-email');
    const levelSelect = document.getElementById('enroll-level');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoading = document.getElementById('btn-loading');
    const message = document.getElementById('enrollment-message');

    const name = nameInput ? nameInput.value.trim() : '';
    const email = emailInput ? emailInput.value.trim() : '';
    const level = levelSelect ? levelSelect.value : '';

    console.log('LearnHub: Form data - Name:', name, 'Email:', email, 'Level:', level);

    if (!name) {
        showMessage(message, 'Por favor ingresa tu nombre completo.', 'error');
        if (nameInput) nameInput.focus();
        return;
    }
    if (!email) {
        showMessage(message, 'Por favor ingresa tu correo electrónico.', 'error');
        if (emailInput) emailInput.focus();
        return;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        showMessage(message, 'Por favor ingresa un correo electrónico válido.', 'error');
        if (emailInput) emailInput.focus();
        return;
    }
    if (!level) {
        showMessage(message, 'Por favor selecciona tu nivel de experiencia.', 'error');
        if (levelSelect) levelSelect.focus();
        return;
    }

    if (submitBtn) submitBtn.disabled = true;
    if (btnText) btnText.style.display = 'none';
    if (btnLoading) btnLoading.style.display = 'inline';

    console.log('LearnHub: Sending enrollment request...');

    const data = { name: name, email: email, level: level };
    const csrfToken = getCsrfToken();
    console.log('LearnHub: CSRF Token:', csrfToken ? 'Present' : 'Missing');

    // Create the fetch request
    const request = new Request('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest',
            'Accept': 'application/json'
        },
        body: JSON.stringify(data),
        mode: 'same-origin',
        credentials: 'include'
    });

    fetch(request)
    .then(function(response) {
        console.log('LearnHub: Response status:', response.status);
        if (!response.ok) {
            console.log('LearnHub: Response not OK');
            throw new Error('HTTP error! status: ' + response.status);
        }
        return response.json();
    })
    .then(function(result) {
        console.log('LearnHub: Response result:', result);
        if (result.status === 'success') {
            showMessage(message, result.message, 'success');
            const form = document.getElementById('enrollment-form');
            if (form) form.reset();
            setTimeout(function() { closeEnrollmentForm(); }, 2000);
        } else {
            showMessage(message, result.message || 'Error al enviar la solicitud.', 'error');
        }
    })
    .catch(function(error) {
        console.error('LearnHub: Error:', error);
        showMessage(message, 'Error de conexión. Por favor intenta de nuevo.', 'error');
    })
    .finally(function() {
        if (submitBtn) submitBtn.disabled = false;
        if (btnText) btnText.style.display = 'inline';
        if (btnLoading) btnLoading.style.display = 'none';
    });
}

function getCsrfToken() {
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) return metaToken.getAttribute('content');
    
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, 10) === 'csrftoken=') {
            return cookie.substring(10);
        }
    }
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) return csrfInput.value;
    return '';
}

function showMessage(element, text, type) {
    if (!element) {
        console.log('LearnHub: Message element not found');
        return;
    }
    element.textContent = text;
    element.style.display = 'block';
    if (type === 'success') {
        element.style.backgroundColor = 'rgba(34, 197, 94, 0.15)';
        element.style.borderColor = '#22c55e';
        element.style.color = '#4ade80';
    } else {
        element.style.backgroundColor = 'rgba(244, 63, 94, 0.15)';
        element.style.borderColor = '#ef4444';
        element.style.color = '#f87171';
    }
    setTimeout(function() { element.style.display = 'none'; }, 5000);
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('LearnHub: Page loaded, initializing...');

    // Initialize navbar scroll effect
    const navbar = document.querySelector('nav');
    if (navbar) {
        window.addEventListener('scroll', function() {
            navbar.classList.toggle('scrolled', window.scrollY > 50);
        }, { passive: true });
    }

    // Initialize modal backdrop close
    const modal = document.getElementById('enrollment-modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) closeEnrollmentForm();
        });
    }

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('enrollment-modal');
            if (modal && modal.style.display === 'flex') {
                closeEnrollmentForm();
            }
        }
    });

    // Initialize smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#') {
                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    // Check modal structure and create if missing
    const modalEl = document.getElementById('enrollment-modal');
    if (modalEl && !modalEl.querySelector('.modal-content')) {
        createModalHTML(modalEl);
    }
    
    // Also add click listener to CTA button as backup
    const ctaBtn = document.getElementById('btn-open-modal');
    if (ctaBtn) {
        ctaBtn.addEventListener('click', function() {
            console.log('LearnHub: CTA button clicked via event listener');
            showEnrollmentForm();
        });
        console.log('LearnHub: CTA button click listener attached');
    }

    console.log('LearnHub: Initialization complete');
});

function createModalHTML(modal) {
    console.log('LearnHub: Creating modal HTML structure...');
    modal.style.display = 'none';
    modal.style.position = 'fixed';
    modal.style.top = '0';
    modal.style.left = '0';
    modal.style.width = '100%';
    modal.style.height = '100%';
    modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    modal.style.zIndex = '9999';
    modal.style.alignItems = 'center';
    modal.style.justifyContent = 'center';

    modal.innerHTML = `
        <div class="modal-content" style="
            background: #0f1528;
            padding: 2.5rem;
            border-radius: 20px;
            max-width: 480px;
            width: 90%;
            border: 1px solid rgba(255, 255, 255, 0.08);
            position: relative;
            box-shadow: 0 25px 80px rgba(0, 0, 0, 0.6);
        ">
            <button onclick="closeEnrollmentForm()" style="
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.08);
                color: #94a3b8;
                font-size: 1.3rem;
                width: 36px;
                height: 36px;
                border-radius: 8px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
            ">&times;</button>

            <h2 style="font-size: 1.7rem; margin-bottom: 0.4rem; color: #f1f5f9;">Formulario de Inscripción</h2>
            <p style="color: #94a3b8; margin-bottom: 2rem; font-size: 0.9rem;">Completa tus datos para comenzar tu prueba gratuita</p>

            <form id="enrollment-form" onsubmit="submitEnrollmentForm(event)">
                <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''}">
                <div class="form-group" style="margin-bottom: 1.1rem;">
                    <label for="enroll-name" style="display: block; margin-bottom: 0.4rem; color: #94a3b8; font-weight: 600; font-size: 0.82rem;">Nombre completo</label>
                    <input type="text" id="enroll-name" name="name" placeholder="Ej: Juan Pérez" required style="
                        width: 100%;
                        padding: 0.75rem 1rem;
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        background: #060917;
                        color: white;
                        font-size: 0.95rem;
                    ">
                </div>

                <div class="form-group" style="margin-bottom: 1.1rem;">
                    <label for="enroll-email" style="display: block; margin-bottom: 0.4rem; color: #94a3b8; font-weight: 600; font-size: 0.82rem;">Correo electrónico</label>
                    <input type="email" id="enroll-email" name="email" placeholder="Ej: juan@ejemplo.com" required style="
                        width: 100%;
                        padding: 0.75rem 1rem;
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        background: #060917;
                        color: white;
                        font-size: 0.95rem;
                    ">
                </div>

                <div class="form-group" style="margin-bottom: 1.1rem;">
                    <label for="enroll-level" style="display: block; margin-bottom: 0.4rem; color: #94a3b8; font-weight: 600; font-size: 0.82rem;">Nivel de experiencia</label>
                    <select id="enroll-level" name="level" required style="
                        width: 100%;
                        padding: 0.75rem 1rem;
                        border-radius: 10px;
                        border: 1px solid rgba(255, 255, 255, 0.08);
                        background: #060917;
                        color: white;
                        font-size: 0.95rem;
                    ">
                        <option value="">Selecciona tu nivel</option>
                        <option value="principiante">Principiante</option>
                        <option value="intermedio">Intermedio</option>
                        <option value="avanzado">Avanzado</option>
                    </select>
                </div>

                <button type="submit" id="submit-btn" class="cta-final-btn" style="
                    width: 100%;
                    padding: 1rem;
                    background: linear-gradient(135deg, #22c55e, #16a34a);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    font-size: 1.05rem;
                    font-weight: 700;
                    cursor: pointer;
                    margin-top: 0.5rem;
                ">
                    <span id="btn-text">Enviar solicitud</span>
                    <span id="btn-loading" style="display: none;"><i class="fas fa-spinner fa-spin"></i> Enviando...</span>
                </button>
            </form>

            <div id="enrollment-message" class="message" style="
                margin-top: 1rem;
                padding: 0.85rem 1rem;
                border-radius: 10px;
                text-align: center;
                font-size: 0.85rem;
                display: none;
            "></div>
        </div>
    `;
    console.log('LearnHub: Modal HTML created');
}

// Debug function
window.debugEnrollment = function() {
    console.log('=== LearnHub Debug ===');
    console.log('CTA Button:', document.getElementById('btn-open-modal'));
    console.log('Modal:', document.getElementById('enrollment-modal'));
    console.log('Form:', document.getElementById('enrollment-form'));
    console.log('scrollToSection:', typeof scrollToSection);
    console.log('showEnrollmentForm:', typeof showEnrollmentForm);
    console.log('openEnrollmentModal:', typeof openEnrollmentModal);
};

console.log('LearnHub: script.js loaded');

// ============================================
// FUTURISTIC ANIMATIONS
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    
    // Create particles container
    createParticles();
    
    // Create orb elements in hero
    createHeroOrbs();
    
    // Initialize scroll-triggered animations
    initScrollAnimations();
    
    // Add reveal classes to elements
    addRevealClasses();
    
    // Initialize navbar scroll effect
    initNavbarScroll();
});

// Create dynamic particles
function createParticles() {
    // Check if container exists
    let container = document.getElementById('particles-bg');
    if (!container) {
        container = document.createElement('div');
        container.id = 'particles-bg';
        document.body.insertBefore(container, document.body.firstChild);
    }
    
    // Create 25 particles
    const particleCount = 25;
    const colors = ['particle-accent', 'particle-purple', 'particle-teal', 'particle-white'];
    const sizes = ['particle-small', 'particle-medium', 'particle-large'];
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = `particle ${sizes[Math.floor(Math.random() * sizes.length)]} ${colors[Math.floor(Math.random() * colors.length)]}`;
        
        // Random positioning
        particle.style.left = Math.random() * 100 + '%';
        
        // Random animation parameters
        const duration = 15 + Math.random() * 20;
        const delay = Math.random() * -duration;
        const drift = (Math.random() - 0.5) * 100;
        
        particle.style.animationDuration = duration + 's';
        particle.style.animationDelay = delay + 's';
        particle.style.setProperty('--drift', drift + 'px');
        particle.style.setProperty('--particle-opacity', (0.3 + Math.random() * 0.5).toString());
        
        container.appendChild(particle);
    }
    
    // Add mouse interaction - particles follow cursor slightly
    document.addEventListener('mousemove', function(e) {
        const particles = document.querySelectorAll('.particle');
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        particles.forEach((particle, index) => {
            const moveX = (x - 0.5) * 30 * (index % 3 + 1);
            const moveY = (y - 0.5) * 20 * (index % 2 + 1);
            particle.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });
}

function createParticles() {
    const container = document.createElement('div');
    container.className = 'particles-container';
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = (15 + Math.random() * 10) + 's';
        
        if (Math.random() > 0.5) {
            particle.style.background = 'var(--purple)';
        } else if (Math.random() > 0.5) {
            particle.style.background = 'var(--teal)';
        }
        
        container.appendChild(particle);
    }
    
    document.body.appendChild(container);
}

function createHeroOrbs() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const orb1 = document.createElement('div');
    orb1.className = 'hero-orb orb-1';
    
    const orb2 = document.createElement('div');
    orb2.className = 'hero-orb orb-2';
    
    hero.appendChild(orb1);
    hero.appendChild(orb2);
}

function initScrollAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, observerOptions);
    
    // Observe all reveal elements
    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .reveal-scale, .section-header').forEach(el => {
        observer.observe(el);
    });
}

function addRevealClasses() {
    // Add reveal classes to sections
    const sections = document.querySelectorAll('.section-header');
    sections.forEach((section, index) => {
        section.classList.add('reveal');
        section.style.transitionDelay = (index * 0.1) + 's';
    });
    
    // Add reveal classes to category cards
    document.querySelectorAll('.category-card').forEach((card, index) => {
        card.classList.add('reveal');
        card.style.transitionDelay = (index * 0.1) + 's';
    });
    
    // Add reveal classes to course cards
    document.querySelectorAll('.course-card').forEach((card, index) => {
        card.classList.add('reveal-scale');
        card.style.transitionDelay = (index * 0.15) + 's';
    });
    
    // Add reveal classes to benefit cards
    document.querySelectorAll('.benefit-card').forEach((card, index) => {
        card.classList.add('reveal-left');
        card.style.transitionDelay = (index * 0.1) + 's';
    });
    
    // Add reveal classes to testimonial cards
    document.querySelectorAll('.testimonial-card').forEach((card, index) => {
        card.classList.add('reveal-right');
        card.style.transitionDelay = (index * 0.1) + 's';
    });
}

function initNavbarScroll() {
    const navbar = document.querySelector('nav');
    if (!navbar) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}