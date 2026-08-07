import scipy.signal as signal

class LambdaStabilizerValidator:
    """
    Analizuje bieguny układu dyskretnego (Z-transformata) pod kątem
    ich intersekcji z geometryczną osią stabilizacji Lambda.
    """
    def __init__(self, lambda_radius=1.0):
        # W strukturze toroidalnej promień stabilności krytycznej zależy od geometrii rdzenia
        self.lambda_radius = lambda_radius 

    def validate_poles_convergance(self, b_coefficients, a_coefficients):
        """
        Oblicza bieguny transmitancji H(z) = B(z)/A(z) i sprawdza,
        czy nie pokrywają się nieliniowo z potrójną symetrią obrotową toroidu.
        """
        poles = signal.ZerosPolesGain(b_coefficients, a_coefficients).poles
        
        for pole in poles:
            magnitude = np.abs(pole)
            angle = np.angle(pole)
            
            # Test stabilności ogólnej (wewnątrz okręgu jednostkowego / promienia Lambda)
            if magnitude > self.lambda_radius:
                raise ValueError(f"System Unstable: Biegun {pole} poza obszarem zbieżności Lambda.")
                
            # Specyficzny test dla trójpętlowego toroidu: 
            # Rezonanse pasożytnicze na stykach fazowych (krok co 120 stopni)
            for k in [0, 1, 2]:
                critical_phase = (2 * np.pi * k) / 3
                if np.isclose(angle, critical_phase, atol=1e-3) and np.isclose(magnitude, self.lambda_radius, atol=1e-2):
                    raise ValueError(f"Phase Intersecion Fault: Biegun w strefie krytycznej sprzężenia pętli (Faza: {np.degrees(angle)} deg).")
                    
        return True
