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
            pre { background: #000; color: #0f0; padding: 15px; border-radius: 10px; margin-top: 20px; font-size: 15px; }
        </style>
    </head>

    <body>
        <div id="box">
            <h2>Math Validator — Pro Formula Editor</h2>
            <p>Wpisz formułę matematyczną (pełne wsparcie nawiasów, operatorów, skrótów):</p>

            <textarea id="editor">2*x^2</textarea>
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
