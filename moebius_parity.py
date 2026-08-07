import numpy as np

class MoebiusParityValidator:
    """
    Weryfikuje, czy operator J poprawnie obsługuje transformację parzystości
    po pełnym obrocie (2pi) oraz pełne domknięcie cyklu (6pi).
    """
    def __init__(self, theta_step=np.pi/12):
        self.theta_step = theta_step

    def validate_operator_continuity(self, operator_matrix_func, dimensions=3):
        """
        Sprawdza warunek brzegowy: J(theta + 2pi) = P * J(theta)
        gdzie P to macierz odbicia przestrzennego (parzystości).
        """
        # Macierz permutacji/odbicia P dla struktury Möbiusa
        P = np.eye(dimensions)
        P[0, 0] = -1  # Odwrócenie orientacji na pierwszej osi profilu
        
        theta_0 = 0
        theta_1 = 2 * np.pi
        theta_final = 6 * np.pi
        
        J_0 = operator_matrix_func(theta_0)
        J_1 = operator_matrix_func(theta_1)
        J_final = operator_matrix_func(theta_final)
        
        # Test 2pi (Warunek Möbiusa)
        expected_J_1 = np.dot(P, J_0)
        if not np.allclose(J_1, expected_J_1, rtol=1e-5):
            raise ValueError("Topological Continuity Fault: Naruszenie symetrii nieorientowalnej przy 2pi.")
            
        # Test 6pi (Warunek domknięcia trójpętlowego)
        if not np.allclose(J_final, J_0, rtol=1e-5):
            raise ValueError("Triloop Closure Fault: Układ nie domyka się po 3 pełnych obrotach (6pi).")
            
        return True
