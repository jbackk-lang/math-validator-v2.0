from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from validator import validate

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>Math Validator — Pro Editor</title>

        <!-- CodeMirror -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/matchbrackets.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/addon/edit/closebrackets.min.js"></script>

        <style>
            body { font-family: Arial; background: #0d0d0d; color: #eee; padding: 30px; }
            #box { background: #1a1a1a; padding: 25px; border-radius: 12px; width: 900px; margin: auto; box-shadow: 0 0 20px #00ffcc55; }
            button { padding: 10px 20px; font-size: 18px; cursor: pointer; background: #0f0; color: #000; border: none; margin-top: 15px; }
            button:hover { background: #0c0; }
            pre { background: #000; color: #0f0; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 15px; white-space: pre-wrap; }

            #keypad { margin-top: 18px; }
            .keyrow { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 6px; }
            .keyrow:first-of-type { margin-top: 10px; }
            .key {
                padding: 8px 0;
                width: 46px;
                font-size: 16px;
                font-family: monospace;
                cursor: pointer;
                background: #222;
                color: #0ff;
                border: 1px solid #333;
                border-radius: 6px;
                margin-top: 0;
                text-align: center;
            }
            .key:hover { background: #333; border-color: #0ff; }
            .key.op   { color: #ff0; }
            .key.fn   { width: auto; padding: 8px 12px; color: #f0f; }
            .key.wide { width: auto; padding: 8px 14px; color: #999; }
            .keypad-label { color: #666; font-size: 12px; margin: 10px 0 4px; text-transform: uppercase; letter-spacing: 1px; }
        </style>
    </head>

    <body>
        <div id="box">
            <h2>Math Validator — Pro Formula Editor</h2>
            <p>Wpisz formułę matematyczną (pełne wsparcie nawiasów, operatorów, skrótów):</p>

            <textarea id="editor">2*x^2</textarea>

            <div id="keypad">
                <div class="keypad-label">Cyfry</div>
                <div class="keyrow" id="digits"></div>

                <div class="keypad-label">Operatory i nawiasy</div>
                <div class="keyrow" id="operators"></div>

                <div class="keypad-label">Zmienne i stałe</div>
                <div class="keyrow" id="variables"></div>

                <div class="keypad-label">Funkcje</div>
                <div class="keyrow" id="functions"></div>

                <div class="keyrow">
                    <span class="key wide" onclick="clearEditor()">Wyczyść</span>
                    <span class="key wide" onclick="backspace()">⌫ Usuń</span>
                </div>
            </div>

            <button onclick="run()">Validate</button>

            <pre id="out">{ wynik pojawi się tutaj }</pre>
        </div>

        <script>
            var editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
                lineNumbers: true,
                mode: "python",
                theme: "default",
                indentUnit: 4,
                smartIndent: true,
                matchBrackets: true,
                autoCloseBrackets: true
            });

            function insertAtCursor(text) {
                editor.replaceSelection(text);
                editor.focus();
            }

            function clearEditor() {
                editor.setValue("");
                editor.focus();
            }

            function backspace() {
                var cursor = editor.getCursor();
                if (cursor.ch > 0) {
                    editor.replaceRange(
                        "",
                        { line: cursor.line, ch: cursor.ch - 1 },
                        cursor
                    );
                } else if (cursor.line > 0) {
                    var prevLineLen = editor.getLine(cursor.line - 1).length;
                    editor.replaceRange(
                        "",
                        { line: cursor.line - 1, ch: prevLineLen },
                        cursor
                    );
                }
                editor.focus();
            }

            function buildKeys(containerId, keys) {
                var container = document.getElementById(containerId);
                keys.forEach(function (k) {
                    var el = document.createElement("span");
                    el.className = "key" + (k.cls ? " " + k.cls : "");
                    el.textContent = k.label;
                    el.onclick = function () { insertAtCursor(k.insert !== undefined ? k.insert : k.label); };
                    container.appendChild(el);
                });
            }

            // Cyfry 0-9
            buildKeys("digits", "0123456789".split("").map(function (d) { return { label: d }; }));

            // Operatory matematyczne i nawiasy
            buildKeys("operators", [
                { label: "+", cls: "op" },
                { label: "−", cls: "op", insert: "-" },
                { label: "×", cls: "op", insert: "*" },
                { label: "÷", cls: "op", insert: "/" },
                { label: "^", cls: "op" },
                { label: "=", cls: "op" },
                { label: "(" },
                { label: ")" },
                { label: "." },
                { label: "√", insert: "sqrt(" },
                { label: "π", insert: "pi" },
            ]);

            // Zmienne i stałe
            buildKeys("variables", [
                { label: "x" },
                { label: "y" },
                { label: "z" },
                { label: "e" },
                { label: "∞", insert: "oo" },
                { label: "Λ=", insert: "Lambda=" },
                { label: "τ=", insert: "Tau=" },
                { label: "ρ=", insert: "Rho=" },
            ]);

            // Funkcje
            buildKeys("functions", [
                { label: "sin(", cls: "fn" },
                { label: "cos(", cls: "fn" },
                { label: "tan(", cls: "fn" },
                { label: "log(", cls: "fn" },
                { label: "exp(", cls: "fn" },
                { label: "abs(", cls: "fn" },
            ]);

            async function run() {
                const expr = editor.getValue();
                const res = await fetch("/validate?expr=" + encodeURIComponent(expr));
                const data = await res.json();
                document.getElementById("out").textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """


@app.get("/validate")
def validate_expr(expr: str):
    return validate(expr)
