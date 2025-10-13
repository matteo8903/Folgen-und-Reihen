import sympy as sp


def berechne_glied(folge_string: str, glied_nr: int):
    """
    Berechnet ein bestimmtes Glied einer Folge.
    
    Args:
        folge_string: Die Folge als String (z.B. "1/n")
        glied_nr: Welches Glied berechnet werden soll
    
    Returns:
        Dictionary mit Ergebnissen
    """
    result = []
    n = 1
    while True:
        wert = eval(folge_string, {"n": n, "__builtins__": {}})
        result.append(wert)
        print(f"a_{{{n}}} = {wert}")
        if n == glied_nr:
            break
        n += 1
    
    return {
        'anzahl': n,
        'letzter_wert': result[-1],
        'alle_werte': result
    }


# Direktes Ausführen - Dein originaler Code
if __name__ == "__main__":
    f = input("Gib eine Gleichung ein: ")
    Glied = int(input("Welches Glied willst du ausrechnen?: "))
    
    result = []
    n = 1
    
    print("\n=== Berechnung ===\n")
    
    while True:
        wert = eval(f, {"n": n, "__builtins__": {}})
        result.append(wert)
        print(f"a_{{{n}}} = {wert}")
        if n == Glied:
            break
        n += 1
    
    print(f"\n✅ Das {n}. Glied wurde berechnet.")
    print(f"📊 Das {n}. Glied ist: {result[-1]}")
    print(f"📈 Alle Werte: {result}")
    
