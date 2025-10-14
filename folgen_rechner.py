import sympy as sp


def folge(f, eps, max_iter=10000):
    result = []
    n = 1
    while n <= max_iter:
        wert = eval(f, {"n": n, "__builtins__": {}})
        result.append(wert)
        print(f"a_{{{n}}} = {wert}")
        if wert <= eps:
            break
        n += 1
    return result, n


def berechne_folge(folge_string: str, epsilon: float, max_iterations: int = 10000):
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(folge_string), n_sym, sp.oo)
    
    if limes == sp.oo:
        return {
            'divergent': True,
            'limes': limes,
            'message': f"Da der Limes gegen {limes} geht ist er Divergent."
        }
    else:
        ergebnis, anzahl = folge(folge_string, epsilon, max_iterations)
        
        # Prüfe ob max_iterations erreicht wurde
        if anzahl >= max_iterations:
            message = f"Der Limes geht gegen {limes}. WARNUNG: Maximale Iterationen ({max_iterations}) erreicht!"
        else:
            message = f"Der Limes geht gegen {limes} und ist deshalb konvergent"
        
        return {
            'divergent': False,
            'limes': limes,
            'message': message,
            'anzahl': anzahl,
            'letzter_wert': ergebnis[-1],
            'alle_werte': ergebnis,
            'max_reached': anzahl >= max_iterations
        }


# Dein originaler Code bleibt hier für direktes Ausführen
if __name__ == "__main__":
    import sympy as sp

    f = input("Gib eine Gleichung ein: ")
    eps = float(input("Gib eine ε-Wert ein: "))
    max_iter = int(input("Maximale Anzahl Berechnungen (z.B. 10000): "))

    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(f), n_sym, sp.oo)

    def folge(f, eps, max_iter):
        result = []
        n = 1
        while n <= max_iter:
            wert = eval(f, {"n": n, "__builtins__": {}})
            result.append(wert)
            print(f"a_{{{n}}} = {wert}")
            if wert <= eps:
                break
            n += 1
        return result, n

    if limes == sp.oo:
        print(f"Da der Limes gegen {limes} geht ist diese Folge Divergent.")
    else:
        ergebnis, anzahl = folge(f, eps, max_iter)
        print(f"Diese Folge konvergiert gegen {limes}.")
        print(f"\n✅ Die Folge wurde {anzahl} mal berechnet")
        
        if anzahl >= max_iter:
            print(f"⚠️ WARNUNG: Maximale Iterationen erreicht!")
        
        print(f"📊 Letzter Wert: {ergebnis[-1]}")
        print(f"📈 Alle Werte: {ergebnis}")

