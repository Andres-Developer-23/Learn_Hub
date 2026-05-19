// WARNING: This file is NOT currently loaded by any template.
// The inline <script> in notifications.html contains the active code.
// If you enable this file, ensure Django template syntax is removed
// and use a meta tag or cookie-based CSRF approach.
const CSRF = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
        btn.classList.add('active');
        document.getElementById('tab-' + btn.dataset.tab).classList.remove('hidden');
    });
});

function handleAction(action, pk) {
    // TODO: Use {% url %} via data attribute when this file is activated
const url = action === 'accept'
    ? '/notificaciones/notificacion/' + pk + '/aceptar/'
    : '/notificaciones/notificacion/' + pk + '/rechazar/';
    
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(r => r.json())
    .then(d => {
        if (d.status === 'success') {
            showToast(action === 'accept' ? '✅ Estudiante aceptado' : '❌ Estudiante rechazado', 'ok');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast('❌ Error al procesar solicitud', 'er');
        }
    })
    .catch(err => {
        showToast('❌ Error de conexión', 'er');
    });
}

function handleEnrollment(pk, action) {
    const url = action === 'accept' 
        ? '/panel/inscripcion/' + pk + '/aceptar/'
        : '/panel/inscripcion/' + pk + '/rechazar/';
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(r => r.json())
    .then(d => {
        if (d.status === 'success') {
            showToast(action === 'accept' ? '✅ Inscripción aceptada' : '❌ Inscripción rechazada', 'ok');
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast('❌ Error al procesar solicitud', 'er');
        }
    })
    .catch(err => {
        showToast('❌ Error de conexión', 'er');
    });
}

function markRead(pk) {
    fetch('/notificaciones/notificacion/' + pk + '/leer/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(r => r.json())
    .then(d => {
        if (d.status === 'success') {
            showToast('📖 Notificación marcada como leída', 'ok');
            setTimeout(() => location.reload(), 1000);
        }
    });
}

function markUnread(pk) {
    fetch('/notificaciones/notificacion/' + pk + '/desleer/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': CSRF,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(r => r.json())
    .then(d => {
        if (d.status === 'success') {
            showToast('📌 Notificación marcada como no leída', 'ok');
            setTimeout(() => location.reload(), 1000);
        }
    });
}

function showToast(msg, type) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'toast ' + type + ' show';
    setTimeout(() => t.className = 'toast', 3000);
}