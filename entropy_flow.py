class EntropyFlowValidator:
    """
    Sprawdza stabilność dynamiczną i zachowanie monotoniczności czasu tau
    w funkcji zmian entropii Delta S.
    """
    def __init__(self, tolerance=1e-6):
        self.tolerance = tolerance

    def validate_causality_guard(self, entropy_stream, tau_function):
        """
        Musi zachodzić: d(tau)/d(t) > 0 dla każdego kroku wzdłuż osi Delta S.
        Eliminuje anomalie 'wymijania się' stanów.
        """
        for i in range(1, len(entropy_stream)):
            ds_prev = entropy_stream[i-1]
            ds_curr = entropy_stream[i]
            
            tau_prev = tau_function(ds_prev)
            tau_curr = tau_function(ds_curr)
            
            # Zapobieganie ujemnemu czasowi lokalnemu
            if tau_curr < tau_prev:
                raise ArithmeticError(f"Causality Violation: Ujemny przyrost czasu tau przy przejściu stanu {i-1} -> {i}")
                
            # Zapobieganie punktom osobliwym (zamrożenie czasu przy niezerowej entropii)
            if abs(tau_curr - tau_prev) < self.tolerance and abs(ds_curr - ds_prev) > self.tolerance:
                raise ZeroDivisionError(f"Singularity Detected: Czas tau zablokowany w punkcie osobliwym stanu {i}.")
                
        return True
