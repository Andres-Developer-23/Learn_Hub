// Code Runner - ejecuta Python en el navegador via Pyodide
(function () {
    'use strict';

    var pyodide = null;
    var loadingPromise = null;
    var packagesLoaded = {};

    function getPyodide() {
        if (pyodide) return Promise.resolve(pyodide);
        if (loadingPromise) return loadingPromise;

        loadingPromise = new Promise(function (resolve, reject) {
            var script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
            script.onload = function () {
                loadPyodide({
                    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
                }).then(function (py) {
                    pyodide = py;
                    window.__pyodide = py;
                    window.__pyodideReady = Promise.resolve(py);
                    resolve(py);
                }).catch(reject);
            };
            script.onerror = function () { reject(new Error('No se pudo cargar Pyodide. Revisa tu conexión.')); };
            document.head.appendChild(script);
        });

        return loadingPromise;
    }

    function extractCode(preEl) {
        var code = preEl.querySelector('code');
        return code ? code.textContent : preEl.textContent;
    }

    function escapeHtml(t) {
        if (!t) return '';
        var d = document.createElement('div');
        d.appendChild(document.createTextNode(t));
        return d.innerHTML;
    }

    function getIconForResult(text) {
        if (text.indexOf('Error') >= 0 || text.indexOf('Traceback') >= 0) return 'fa-exclamation-circle';
        return 'fa-check-circle';
    }

    function createRunnerUI(preEl) {
        if (preEl.parentNode && preEl.parentNode.classList.contains('code-runner-wrapper')) return;

        var wrapper = document.createElement('div');
        wrapper.className = 'code-runner-wrapper';
        wrapper.style.cssText = 'margin:0.8rem 0;border:1px solid var(--card-border);border-radius:10px;overflow:hidden;';

        var header = document.createElement('div');
        header.className = 'code-runner-header';
        header.style.cssText = 'display:flex;align-items:center;justify-content:space-between;padding:0.5rem 1rem;background:var(--card-bg);border-bottom:1px solid var(--card-border);';

        var badge = document.createElement('span');
        badge.className = 'code-runner-badge';
        badge.style.cssText = 'font-size:0.75rem;font-weight:600;color:var(--accent);display:flex;align-items:center;gap:0.4rem;';
        badge.innerHTML = '<i class="fab fa-python"></i> Python';

        var runBtn = document.createElement('button');
        runBtn.className = 'code-runner-btn';
        runBtn.style.cssText = 'padding:0.35rem 0.85rem;border-radius:6px;border:1px solid var(--accent);background:transparent;color:var(--accent);font-size:0.75rem;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:0.4rem;transition:all 0.2s;';
        runBtn.innerHTML = '<i class="fas fa-play" style="font-size:0.65rem"></i> Ejecutar';

        var output = document.createElement('div');
        output.className = 'code-runner-output';
        output.style.cssText = 'display:none;';

        runBtn.addEventListener('mouseenter', function () {
            runBtn.style.cssText = runBtn.style.cssText + 'background:var(--accent);color:white;';
        });
        runBtn.addEventListener('mouseleave', function () {
            runBtn.style.cssText = 'padding:0.35rem 0.85rem;border-radius:6px;border:1px solid var(--accent);background:transparent;color:var(--accent);font-size:0.75rem;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:0.4rem;transition:all 0.2s;';
        });

        header.appendChild(badge);
        header.appendChild(runBtn);
        wrapper.appendChild(header);

        preEl.parentNode.insertBefore(wrapper, preEl);
        wrapper.appendChild(preEl);
        wrapper.appendChild(output);

        runBtn.addEventListener('click', function () { runCode(preEl, output, runBtn); });
    }

    function needsPackage(code) {
        var pkgs = {
            'pandas': 'pandas',
            'numpy': 'numpy',
            'sklearn': 'scikit-learn',
            'sklearn.': 'scikit-learn',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'PIL': 'pillow',
            'cv2': 'opencv-python',
            'requests': 'requests',
            'beautifulsoup': 'beautifulsoup4',
        };
        for (var key in pkgs) {
            if (code.indexOf(key) >= 0) return pkgs[key];
        }
        return null;
    }

    async function runCode(preEl, outputEl, btnEl) {
        var code = extractCode(preEl);

        outputEl.style.display = 'block';
        outputEl.innerHTML = '<div style="padding:1rem;text-align:center;color:var(--text-secondary);font-size:0.82rem"><i class="fas fa-spinner fa-spin"></i> Cargando Python...</div>';
        btnEl.disabled = true;
        btnEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Cargando...';

        try {
            var py = await getPyodide();

            outputEl.innerHTML = '<div style="padding:1rem;text-align:center;color:var(--text-secondary);font-size:0.82rem"><i class="fas fa-spinner fa-spin"></i> Ejecutando...</div>';
            btnEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Ejecutando...';

            // Install needed packages
            var pkg = needsPackage(code);
            if (pkg && !packagesLoaded[pkg]) {
                outputEl.innerHTML = '<div style="padding:1rem;text-align:center;color:var(--text-secondary);font-size:0.82rem"><i class="fas fa-spinner fa-spin"></i> Instalando ' + pkg + '...</div>';
                try {
                    await py.loadPackage(pkg);
                    packagesLoaded[pkg] = true;
                } catch (e) {
                    // package not available in Pyodide, continue anyway
                    console.warn('Package not available:', pkg);
                }
            }

            // Capture stdout
            await py.runPython(
                'import sys, io\n' +
                '_stdout = io.StringIO()\n' +
                'sys.stdout = _stdout\n' +
                'sys.stderr = _stdout\n'
            );

            await py.runPython(code);

            var result = await py.runPython(
                'sys.stdout = sys.__stdout__\n' +
                'sys.stderr = sys.__stderr__\n' +
                '_output = _stdout.getvalue()\n' +
                '_stdout.close()\n' +
                '_output'
            );

            if (result && result.trim()) {
                var html = '<div class="code-runner-header" style="padding:0.5rem 1rem;background:rgba(34,197,94,0.08);border-bottom:1px solid rgba(34,197,94,0.15);display:flex;align-items:center;gap:0.5rem;font-size:0.75rem;color:var(--success);font-weight:600">';
                html += '<i class="fas fa-check-circle"></i> Salida</div>';
                html += '<pre class="code-runner-output-text">' + escapeHtml(result) + '</pre>';
                outputEl.innerHTML = html;
            } else {
                outputEl.innerHTML = '<div style="padding:0.8rem 1rem;color:var(--success);font-size:0.8rem;display:flex;align-items:center;gap:0.4rem;background:rgba(34,197,94,0.05)"><i class="fas fa-check-circle"></i> Código ejecutado sin errores</div>';
            }
        } catch (err) {
            var msg = err.message || String(err);
            outputEl.innerHTML = '<div style="padding:0.5rem 1rem;background:rgba(244,63,94,0.08);border-bottom:1px solid rgba(244,63,94,0.15);display:flex;align-items:center;gap:0.5rem;font-size:0.75rem;color:var(--rose);font-weight:600"><i class="fas fa-exclamation-circle"></i> Error</div>' +
                '<pre class="code-runner-output-text code-runner-error-text">' + escapeHtml(msg) + '</pre>';
        } finally {
            btnEl.disabled = false;
            btnEl.innerHTML = '<i class="fas fa-play" style="font-size:0.65rem"></i> Ejecutar';
        }
    }

    function init() {
        document.querySelectorAll('.content-text pre').forEach(function (pre) {
            var code = pre.querySelector('code');
            if (code && code.textContent.trim()) {
                createRunnerUI(pre);
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
