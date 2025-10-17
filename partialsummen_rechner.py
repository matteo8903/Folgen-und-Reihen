import sympy as sp


def folge(f, ntes_glied):
    """
    Berechnet Partialsumme bis zu einem bestimmten Glied.
    """
    partialsumme = 0
    n = 1
    terme = []
    partialsummen = []
    
    while True:
        wert = eval(f, {"n": n, "__builtins__": {}})
        partialsumme += wert
        terme.append(wert)
        partialsummen.append(partialsumme)
        print(f"a_{{{n}}} = {wert}")
        if n == ntes_glied:
            break
        n += 1
    
    return partialsumme, n, terme, partialsummen


def berechne_partialsumme(folge_string: str, n_max: int):
    """
    Berechnet die Partialsumme einer Folge von n=1 bis n=n_max.
    
    Args:
        folge_string: Die Folge als String (z.B. "1/n**2")
        n_max: Bis zu welchem n summiert werden soll
    
    Returns:
        Dictionary mit Ergebnissen
    """
    # Berechne Partialsumme
    partialsumme, anzahl, terme, partialsummen = folge(folge_string, n_max)
    
    return {
        'partialsumme': partialsumme,
        'anzahl_terme': anzahl,
        'terme': terme,
        'partialsummen': partialsummen
    }


# Direktes Ausführen - Dein originaler Code-Stil
if __name__ == "__main__":
    import sympy as sp
    
    f = input("Gib eine Gleichung ein: ")
    ntes_glied = float(input("Welche Partialsumme soll berechnet werden (BIS ZU WELCHEM GLIED): "))
    
    def folge(f, ntes_glied):
        partialsumme = 0
        n = 1
        while True:
            wert = eval(f, {"n": n, "__builtins__": {}})
            partialsumme += wert
            print(f"a_{{{n}}} = {wert}")
            if n == ntes_glied:
                break
            n += 1
        return partialsumme, n
    
    ergebnis, anzahl = folge(f, ntes_glied)
    print(f"\n📊 Die Summe der {anzahl} Gliedern ist: {ergebnis}")
