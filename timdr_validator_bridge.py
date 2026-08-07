import json
import math

class TIMDRValidatorBridge:
    def __init__(self):
        # Kanoniczne parametry i stałe modelu GIA & TIMDR
        self.valid_states = {"λ", "τ", "ρ"}
        self.critical_angles = {36.0, 30.0, 5.625, 720.0}
        
    def verify_lambda_layer(self, json_data):
        """[Warstwa Łambda] Walidacja spójności grafu i formatu wejściowego FAI"""
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            
            # Weryfikacja sekcji krytycznych dla sztucznej inteligencji
            if "MODEL" not in data or "STATES" not in data or "TRANSITIONS" not in data:
                return {"layer": "Λ", "status": "FAIL", "error": "Brak kompletnej struktury modelu FAI."}
                
            symbols = [s["SYMBOL"] for s in data["STATES"] if "SYMBOL" in s]
            if not set(symbols).issubset(self.valid_states):
                return {"layer": "Λ", "status": "FAIL", "error": f"Niedozwolone symbole stanów: {set(symbols) - self.valid_states}"}
                
            return {"layer": "Λ", "status": "VERIFIED", "details": f"Liczba zweryfikowanych stanów: {len(symbols)}"}
        except Exception as e:
            return {"layer": "Λ", "status": "ERROR", "error": str(e)}

    def verify_tau_layer(self, angle, current_state, next_state):
        """[Warstwa Tau] Walidacja transformacji, map kątowych i przesunięć izometrycznych"""
        if angle not in self.critical_angles:
            return {"layer": "τ", "status": "FAIL", "error": f"Kąt {angle}° poza kanoniczną mapą obiegów TIMDR."}
            
        # Każda transformacja musi poprawnie opuszczać stan początkowy lub pośredni
        if current_state == "λ" and next_state != "τ":
            return {"layer": "τ", "status": "FAIL", "error": "Złamanie liniowości: ze stanu λ dopuszczalne jest tylko przejście do τ."}
            
        return {"layer": "τ", "status": "VERIFIED", "details": f"Transformacja {current_state} -> {next_state} pomyślna przy {angle}°"}

    def verify_rho_layer_and_singularity(self, num_faces, curvature, initial_entropy, final_entropy):
        """[Warstwa Rho] Obliczanie dywergencji ΔS, stabilizacji oraz warunków brzegowych Tetroidy i domknięcia M²"""
        # 1. Walidacja Tetroidy (Osobliwość Möbiusa)
        if num_faces != 3:
            return {"layer": "ρ", "status": "FAIL", "error": f"Tetroida wymaga dokładnie 3 ścian (podano: {num_faces})."}
        if curvature <= 0:
            return {"layer": "ρ", "status": "FAIL", "error": "Krzywizna Tetroidy musi być dodatnia, by zapobiegać zapadaniu."}
            
        # 2. Wyliczenie dywergencji ΔS (Różnica entropii informacyjnej)
        delta_S = final_entropy - initial_entropy
        
        # Interpretacja statusu stabilizacji pola rezonansowego
        stabilization = "DODATNIA (Emergencja nowej struktury)" if delta_S > 0 else "UJEMNA (Redukcja i stabilizacja stanu)"
        
        return {
            "layer": "ρ",
            "status": "VERIFIED",
            "metrics": {
                "tetroida_boundary": "ZACHOWANE",
                "delta_S_divergence": round(delta_S, 4),
                "resonance_stabilization": stabilization
            }
        }

# =====================================================================
# PIPELINE INTEGRACYJNY - SYMULACJA PEŁNEGO PASZPORTU WALIDACYJNEGO
# =====================================================================
if __name__ == "__main__":
    bridge = TIMDRValidatorBridge()
    print("=== URUCHAMIANIE ZINTEGROWANEGO WALIDATORA GIA & TIMDR ===\n")
    
    # Dane wejściowe pobrane bezpośrednio ze specyfikacji model.html
    fai_json_source = {
        "MODEL": {"STATES": ["λ", "τ", "ρ"], "TRANSITIONS": "MIXED", "VERSION": 1},
        "STATES": [
            {"SYMBOL": "λ", "NAME": "lambda", "ROLE": "start", "CODE": "00"},
            {"SYMBOL": "τ", "NAME": "tau", "ROLE": "change", "CODE": "01"},
            {"SYMBOL": "ρ", "NAME": "rho", "ROLE": "effect", "CODE": "10"}
        ],
        "TRANSITIONS": []
    }
    
    # 1. Uruchomienie testu dla warstwy strukturalnej (Λ)
    res_lambda = bridge.verify_lambda_layer(fai_json_source)
    print(f"[{res_lambda['layer']}] Status: {res_lambda['status']} | {res_lambda.get('details', res_lambda.get('error'))}")
    
    # 2. Uruchomienie testu dla warstwy transformacji (τ) - Cykl obrotu 720° przy inicjacji procesu
    res_tau = bridge.verify_tau_layer(angle=720.0, current_state="λ", next_state="τ")
    print(f"[{res_tau['layer']}] Status: {res_tau['status']} | {res_tau.get('details', res_tau.get('error'))}")
    
    # 3. Uruchomienie testu dla warstwy stabilizacji rezonansu (ρ) - Przejście ΔS i parametry Tetroidy
    res_rho = bridge.verify_rho_layer_and_singularity(num_faces=3, curvature=0.618, initial_entropy=1.442, final_entropy=0.854)
    print(f"[{res_rho['layer']}] Status: {res_rho['status']}")
    if res_rho['status'] == "VERIFIED":
        print(f"     -> Dywergencja ΔS: {res_rho['metrics']['delta_S_divergence']}")
        print(f"     -> Status pola: {res_rho['metrics']['resonance_stabilization']}")
