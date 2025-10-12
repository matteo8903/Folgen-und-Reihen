

import sympy as sp


def folge(f, eps):
    
    result = []
    n = 1
    while True:
        wert = eval(f, {"n": n, "__builtins__": {}})
        result.append(wert)
        print(f"a_{{{n}}} = {wert}")
        if wert <= eps:
            break
        n += 1
    return result, n


def berechne_folge(folge_string: str, epsilon: float):
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(folge_string), n_sym, sp.oo)
    
    if limes == sp.oo:
        return {
            'divergent': True,
            'limes': limes,
            'message': f"Da der Limes gegen {limes} geht ist er Divergent."
        }
    else:
        ergebnis, anzahl = folge(folge_string, epsilon)
        
        return {
            'divergent': False,
            'limes': limes,
            'message': f"Der Limes geht gegen {limes} und ist deshalb konvergent",
            'anzahl': anzahl,
            'letzter_wert': ergebnis[-1],
            'alle_werte': ergebnis
        }


# Dein originaler Code bleibt hier für direktes Ausführen
if __name__ == "__main__":
    import sympy as sp

    f = input("Gib eine Gleichung ein:")
    eps = float(input("Gib eine ε-Wert ein:"))

    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(f), n_sym, sp.oo)

    def folge(f,eps):
        result = []
        n = 1
        while True:
            wert = eval(f, {"n": n, "__builtins__": {}})
            result.append(wert)
            print(f"a_{{{n}}} = {wert}")
            if wert <= eps:
                break
            n += 1
        return result, n

    if limes == sp.oo:
        print(f"Da der Limes gegen {limes} geht ist er Divergent.")
    else:
        ergebnis, anzahl = folge(f, eps)
        print(f"Der Limes geht gegen {limes} und ist deshalb konvergent")
        print(f"\n✅ Die Folge wurde {anzahl} mal berechnet")
        print(f"📊 Letzter Wert: {ergebnis[-1]}")
        print(f"📈 Alle Werte: {ergebnis}")