from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from validator import validate
import json

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def ui():
    return """
    <html>
    <head>
        <title>Math Validator UI</title>
        <style>
            body { font-family: Arial; background: #f2f2f2; padding: 30px; }
            #box { background: white; padding: 20px; border-radius: 10px; width: 600px; margin: auto; box-shadow: 0 0 10px #aaa; }
            input { width: 400px; padding: 8px; font-size: 16px; }
            button { padding: 8px 16px; font-size: 16px; cursor: pointer; }
            pre { background: #222; color: #0f0; padding: 15px; border-radius: 10px; margin-top: 20px; }
        </style>
    </head>
    <body>
        <div id="box">
            <h2>Math Validator — UI</h2>
            <p>Wpisz wyrażenie i kliknij Validate:</p>
            <input id="expr" placeholder="1/(x-1)">
            <button onclick="run()">Validate</button>

            <pre id="out">{ wynik pojawi się tutaj }</pre>
        </div>

        <script>
            async function run() {
                const expr = document.getElementById("expr").value;
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
