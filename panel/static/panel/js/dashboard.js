document.addEventListener('DOMContentLoaded', function() {
    // WARNING: This file is NOT currently loaded by any template.
// The inline <script> in dashboard.html contains the active code.
// If you enable this file, ensure Django template syntax is removed
// and use a meta tag or cookie-based CSRF approach.
const CSRF = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    let curId = null;

    function updateActiveSidebar() {
        const hash = window.location.hash || '#sec-overview';
        document.querySelectorAll('a.ni').forEach(function(n) { n.classList.remove('active'); });
        const link = document.querySelector('a.ni[href="' + hash + '"]');
        if (link) link.classList.add('active');
    }
    window.addEventListener('hashchange', updateActiveSidebar);
    updateActiveSidebar();

    (function initCharts() {
        try {
            const chartDona = document.getElementById('chartDona');
            const chartStatus = document.getElementById('chartStatus');

            if (typeof Chart === 'undefined') {
                return;
            }

            if (chartDona) {
                new Chart(chartDona.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Principiante', 'Intermedio', 'Avanzado'],
                        datasets: [{
                            // TODO: These values must be passed from the template (e.g., via data attributes or inline JSON)
data: [0, 0, 0],
                            backgroundColor: ['#4ade80', '#fbbf24', '#a78bfa'],
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { color: '#94a3b8', padding: 20 }
                            }
                        }
                    }
                });
            }

            if (chartStatus) {
                new Chart(chartStatus.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: ['Pendientes', 'Aceptados', 'Rechazados'],
                        datasets: [{
                            data: [{{ pending|default:0 }}, {{ accepted|default:0 }}, {{ rejected|default:0 }}],
                            backgroundColor: ['#fbbf24', '#4ade80', '#f87171'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: { beginAtZero: true, ticks: { color: '#94a3b8' } },
                            x: { ticks: { color: '#94a3b8' } }
                        }
                    }
                });
            }
        } catch (err) {
            // Charts not available
        }
    })();

    document.querySelectorAll('.btn-ed').forEach(function(btn) {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            curId = this.getAttribute('data-ed');
            document.getElementById('en').value = this.getAttribute('data-name');
            document.getElementById('ee').value = this.getAttribute('data-email');
            document.getElementById('el').value = this.getAttribute('data-level');
            document.getElementById('edit-mo').classList.add('open');
        });
    });

    document.querySelectorAll('.del-form').forEach(function(form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            curId = this.querySelector('[name=csrfmiddlewaretoken]').value;
            const row = this.closest('tr');
            if (row) curId = row.getAttribute('data-id');
            document.getElementById('del-mo').classList.add('open');
            window._delForm = this;
        });
    });

    document.querySelector('.save-edit-btn').addEventListener('click', function() {
        fetch('/panel/estudiante/' + curId + '/editar/', {
            method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':CSRF},
            body:JSON.stringify({
                name:document.getElementById('en').value,
                email:document.getElementById('ee').value,
                level:document.getElementById('el').value
            })
        })
        .then(function(r) { return r.json(); })
        .then(function(d) {
            if(d.status==='success'){ showToast('✅ Estudiante actualizado'); setTimeout(function() { location.reload(); }, 900); }
        });
    });

    document.querySelector('.confirm-del-btn').addEventListener('click', function() {
        const delForm = window._delForm;
        if (!delForm) { closeMo(); return; }
        const url = delForm.getAttribute('action');
        const csrf = delForm.querySelector('[name=csrfmiddlewaretoken]').value;
        const row = delForm.closest('tr');
        const sid = row ? row.getAttribute('data-id') : null;
        fetch(url, {method:'POST', headers:{'X-CSRFToken':csrf, 'X-Requested-With':'XMLHttpRequest'}})
        .then(function(r) { return r.json(); })
        .then(function(d) {
            if(d.status==='success'){
                closeMo();
                if (row) row.remove();
                showToast('🗑️ Estudiante eliminado');
            }
        });
    });

    document.querySelector('.copy-creds-btn').addEventListener('click', function() {
        const u = document.getElementById('cred-user').value;
        const p = document.getElementById('cred-pw').value;
        navigator.clipboard.writeText('Usuario: ' + u + '\nContraseña: ' + p + '\nPortal: /estudiante/login/')
            .then(function() { showToast('📋 Credenciales copiadas al portapapeles'); });
    });

    document.querySelectorAll('.close-btn').forEach(function(btn) {
        btn.addEventListener('click', function() { closeMo(); });
    });
    document.querySelectorAll('.mo').forEach(function(m) {
        m.addEventListener('click', function(e) { if(e.target===m) closeMo(); });
    });

    function closeMo() { document.querySelectorAll('.mo').forEach(function(m) { m.classList.remove('open'); }); curId=null; }

    function showToast(msg,type){
        if (!type) type='ok';
        const t=document.getElementById('toast');
        t.textContent=msg;
        t.className='toast ' + type + ' show';
        setTimeout(function() { t.className='toast'; }, 3000);
    }

    document.getElementById('srch').addEventListener('input',function(){
        const q=this.value.toLowerCase();
        document.querySelectorAll('#stb tr[data-id]').forEach(function(r){
            r.style.display=(r.getAttribute('data-name').toLowerCase().indexOf(q)!==-1||r.getAttribute('data-email').toLowerCase().indexOf(q)!==-1)?'':'none';
        });
    });
});