from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

class InputData(BaseModel):
    data: str

@app.post("/validate")
def validate_structure(payload: InputData):
    raw = payload.data.strip()

    # TEXT VALIDATION
    if not raw.startswith("{") and not raw.startswith("["):
        return {
            "type": "text",
            "status": "ok" if len(raw.split()) > 3 else "error",
            "hint": "Tekst jest zbyt krótki, dodaj więcej treści aby był zrozumiały."
                    if len(raw.split()) <= 3 else
                    "Tekst wygląda spójnie — zdania są wystarczająco rozwinięte."
        }

    # JSON / LIST VALIDATION
    try:
        parsed = json.loads(raw)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="To nie jest poprawny JSON — sprawdź nawiasy i przecinki."
        )

    # LIST VALIDATION
    if isinstance(parsed, list):
        if len(parsed) == 0:
            return {
                "type": "list",
                "status": "error",
                "hint": "Lista jest pusta — dodaj elementy, aby miała sens."
            }
        if len(parsed) != len(set(parsed)):
            return {
                "type": "list",
                "status": "warning",
                "hint": "Lista zawiera powtórzenia — usuń duplikaty, jeśli nie są potrzebne."
            }
        return {
            "type": "list",
            "status": "ok",
            "hint": "Lista wygląda poprawnie — elementy są unikalne i uporządkowane."
        }

    # JSON OBJECT VALIDATION
    if isinstance(parsed, dict):
        if len(parsed.keys()) == 0:
            return {
                "type": "json",
                "status": "error",
                "hint": "JSON jest pusty — dodaj pola, aby struktura była kompletna."
            }

        missing = []
        required = ["name", "type", "value"]  # przykładowe pola dla laika

        for r in required:
            if r not in parsed:
                missing.append(r)

        if missing:
            return {
                "type": "json",
                "status": "warning",
                "hint": f"Brakuje pól: {', '.join(missing)} — dodaj je, aby struktura była pełna."
            }

        return {
            "type": "json",
            "status": "ok",
            "hint": "JSON jest kompletny — wszystkie podstawowe pola są obecne."
        }

    return {
        "type": "unknown",
        "status": "error",
        "hint": "Nie rozpoznano struktury — użyj tekstu, listy lub JSON."
    }
