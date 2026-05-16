// Python Console - REPL persistente en el navegador
(function () {
    'use strict';

    var history = [];
    var historyIndex = -1;
    var pyPromise = null;
    var packagesLoaded = {};

    function getPy() {
        if (window.__pyodideReady) return window.__pyodideReady;
        if (pyPromise) return pyPromise;
        pyPromise = new Promise(function (resolve, reject) {
            var s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
            s.onload = function () {
                loadPyodide({ indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/' })
                    .then(function (py) {
                        window.__pyodide = py;
                        window.__pyodideReady = Promise.resolve(py);
                        resolve(py);
                    }).catch(reject);
            };
            s.onerror = function () { reject(Error('No se pudo cargar Python.')); };
            document.head.appendChild(s);
        });
        return pyPromise;
    }

    function esc(t) {
        if (!t) return '';
        var d = document.createElement('div');
        d.appendChild(document.createTextNode(t));
        return d.innerHTML;
    }

    function build() {
        var panel = document.createElement('div');
        panel.id = 'py-console';

        var out = document.createElement('div');
        out.id = 'py-console-output';
        out.innerHTML = '';

        var inp = document.createElement('textarea');
        inp.id = 'py-console-input';
        inp.rows = 1;
        inp.placeholder = 'Escribe c\u00f3digo Python...';
        inp.spellcheck = false;

        var runBtn = document.createElement('button');
        runBtn.id = 'py-console-run';
        runBtn.innerHTML = '<i class="fas fa-play"></i>';
        runBtn.title = 'Ejecutar (Enter)';

        var clearBtn = document.createElement('button');
        clearBtn.id = 'py-console-clear';
        clearBtn.innerHTML = '<i class="fas fa-trash-alt"></i>';
        clearBtn.title = 'Limpiar';

        var closeBtn = document.createElement('button');
        closeBtn.id = 'py-console-close';
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        closeBtn.title = 'Cerrar (Esc)';

        var prompt = document.createElement('span');
        prompt.id = 'py-console-prompt';
        prompt.textContent = '>>>';

        var hdr = document.createElement('div');
        hdr.id = 'py-console-header';
        hdr.innerHTML = '<i class="fab fa-python" style="color:var(--accent)"></i> Python Console';
        hdr.appendChild(clearBtn);
        hdr.appendChild(closeBtn);

        var row = document.createElement('div');
        row.id = 'py-console-row';
        row.appendChild(prompt);
        row.appendChild(inp);
        row.appendChild(runBtn);

        panel.appendChild(hdr);
        panel.appendChild(out);
        panel.appendChild(row);
        document.body.appendChild(panel);

        window.togglePythonConsole = function () {
            if (panel.style.display === 'flex') {
                panel.style.display = 'none';
            } else {
                panel.style.display = 'flex';
                inp.focus();
            }
        };
        window.openPythonConsole = function () {
            panel.style.display = 'flex';
            inp.focus();
        };
        closeBtn.onclick = function () {
            panel.style.display = 'none';
        };
        clearBtn.onclick = function () {
            out.innerHTML = '';
        };

        inp.addEventListener('input', function () {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        function exec() {
            var code = inp.value.trim();
            if (!code) return;
            out.innerHTML += '<div style="color:var(--success);padding:0.2rem 0">&gt;&gt;&gt; ' + esc(code) + '</div>';
            out.scrollTop = out.scrollHeight;
            history.push(code);
            historyIndex = history.length;
            inp.value = '';
            inp.style.height = 'auto';
            run(code, out);
        }

        runBtn.onclick = exec;

        inp.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); exec(); return; }
            if (e.key === 'ArrowUp' && !e.shiftKey) {
                e.preventDefault();
                if (historyIndex > 0) { historyIndex--; inp.value = history[historyIndex]; }
                inp.style.height = 'auto';
                inp.style.height = Math.min(inp.scrollHeight, 120) + 'px';
            }
            if (e.key === 'ArrowDown' && !e.shiftKey) {
                e.preventDefault();
                if (historyIndex < history.length - 1) { historyIndex++; inp.value = history[historyIndex]; }
                else { historyIndex = history.length; inp.value = ''; }
                inp.style.height = 'auto';
                inp.style.height = Math.min(inp.scrollHeight, 120) + 'px';
            }
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && panel.style.display === 'flex' && document.activeElement !== inp) {
                panel.style.display = 'none';
                btn.style.display = 'flex';
            }
        });
    }

    async function run(code, out) {
        try {
            var py = await getPy();

            // Install needed packages automatically
            var checks = {pandas:'pandas',numpy:'numpy','sklearn':'scikit-learn','sklearn.':'scikit-learn',matplotlib:'matplotlib',seaborn:'seaborn',PIL:'pillow'};
            for (var k in checks) {
                if (code.indexOf(k) >= 0 && !packagesLoaded[checks[k]]) {
                    out.innerHTML += '<div style="color:var(--amber);padding:0.1rem 0;font-size:0.75rem"><i class="fas fa-spinner fa-spin"></i> Instalando ' + checks[k] + '...</div>';
                    out.scrollTop = out.scrollHeight;
                    try { await py.loadPackage(checks[k]); packagesLoaded[checks[k]] = true; } catch (e) {}
                }
            }

            // Redirect stdout/stderr to a buffer
            await py.runPython('import sys,io; _buf=io.StringIO(); sys.stdout=_buf; sys.stderr=_buf; _has_err=False');

            var output = '';
            try {
                await py.runPython(code);
                output = await py.runPython('_buf.getvalue()');
            } catch (pyErr) {
                // Get partial output before error
                try { output = await py.runPython('_buf.getvalue()'); } catch (e2) {}
                var msg = pyErr.message || String(pyErr);
                // Remove Pyodide wrapper noise if present
                msg = msg.replace(/^PythonError: /, '');
                output += '\n' + msg;
            }

            // Restore stdout/stderr
            try { await py.runPython('sys.stdout=sys.__stdout__; sys.stderr=sys.__stderr__; _buf.close()'); } catch (e) {}

            // Display output
            if (output && output.trim()) {
                var lines = output.split('\n');
                for (var i = 0; i < lines.length; i++) {
                    var l = lines[i];
                    if (!l.trim()) continue;
                    var isErr = l.indexOf('Error') >= 0 || l.indexOf('Traceback') >= 0 || l.indexOf('Exception') >= 0;
                    out.innerHTML += '<div style="padding:0.1rem 0 0.1rem 1rem;white-space:pre-wrap;color:' +
                        (isErr ? 'var(--rose)' : '#e2e8f0') + '">' + esc(l) + '</div>';
                }
            } else {
                out.innerHTML += '<div style="color:var(--text-muted);padding:0.1rem 0 0.1rem 1rem;font-style:italic">(sin salida)</div>';
            }
        } catch (err) {
            out.innerHTML += '<div style="color:var(--rose);padding:0.2rem 0">' + esc(err.message || String(err)) + '</div>';
        }
        out.scrollTop = out.scrollHeight;
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
    else build();
})();
