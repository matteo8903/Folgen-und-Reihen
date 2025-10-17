import sympy as sp


def berechne_limes(folge_string: str):
    """
    Berechnet den Limes einer Folge für n → ∞
    
    Args:
        folge_string: Die Folge als String (z.B. "1/n")
    
    Returns:
        Dictionary mit Ergebnissen
    """
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(folge_string), n_sym, sp.oo)
    
    if limes == sp.oo:
        divergent = True
        message = f"Da der Limes gegen {limes} geht ist er Divergent."
    else:
        divergent = False
        message = f"Der Limes geht gegen {limes} und ist deshalb konvergent"
    
    return {
        'limes': limes,
        'divergent': divergent,
        'message': message
    }


# Direktes Ausführen
if __name__ == "__main__":
    f = input("Gib eine Gleichung ein: ")
    
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(f), n_sym, sp.oo)
    
    if limes == sp.oo:
        print(f"Da der Limes gegen {limes} geht ist er Divergent.")
    else:
        print(f"Der Limes geht gegen {limes} und ist deshalb konvergent")
