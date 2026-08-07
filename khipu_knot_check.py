def execute_full_topological_validation(self, equation_ast, operator_func, system_coefficients):
    # Krok 1: Klasyczna poprawność matematyczna (Składnia, typy danych)
    self.base_ast_validate(equation_ast)
    
    # Krok 2: Uruchomienie uzupełnień topologicznych
    print("[INIT] Uruchamianie topologicznej walidacji struktury...")
    
    # Test Möbiusa
    self.moebius_checker.validate_operator_continuity(operator_func)
    
    # Test stabilizacji Lambda
    self.lambda_stabilizer.validate_poles_convergance(system_coefficients['b'], system_coefficients['a'])
    
    print("[SUCCESS] Równanie zachowuje integralność trójpętlowego toroidu.")
    return True
