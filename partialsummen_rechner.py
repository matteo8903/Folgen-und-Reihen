import sympy as sp


def berechne_partialsumme(folge_string: str, n_max: int):
    """
    Berechnet die Partialsumme einer Folge von n=1 bis n=n_max.
    
    Args:
        folge_string: Die Folge als String (z.B. "1/n**2")
        n_max: Bis zu welchem n summiert werden soll
    
    Returns:
        Dictionary mit Ergebnissen
    """
    terme = []
    partialsummen = []
    summe = 0
    
    # Berechne alle Terme und Partialsummen
    for n in range(1, n_max + 1):
        wert = eval(folge_string, {"n": n, "__builtins__": {}})
        terme.append(wert)
        summe += wert
        partialsummen.append(summe)
        print(f"a_{{{n}}} = {wert}, S_{{{n}}} = {summe}")
    
    # Prüfe Konvergenz der Reihe
    n_sym = sp.Symbol('n')
    try:
        reihen_grenzwert = sp.summation(sp.sympify(folge_string), (n_sym, 1, sp.oo))
        
        if reihen_grenzwert == sp.oo or reihen_grenzwert == -sp.oo:
            reihe_konvergiert = False
            konvergenz_info = "Die Reihe divergiert gegen Unendlich"
        else:
            reihe_konvergiert = True
            konvergenz_info = f"Die Reihe konvergiert"
    except:
        reihen_grenzwert = "Unbekannt"
        reihe_konvergiert = False
        konvergenz_info = "Konvergenz konnte nicht bestimmt werden"
    
    return {
        'partialsumme': summe,
        'anzahl_terme': n_max,
        'terme': terme,
        'partialsummen': partialsummen,
        'reihe_konvergiert': reihe_konvergiert,
        'grenzwert': reihen_grenzwert,
        'konvergenz_info': konvergenz_info
    }


# Direktes Ausführen
if __name__ == "__main__":
    f = input("Gib eine Folge ein (verwende 'n' als Variable): ")
    n_max = int(input("Bis zu welchem n soll summiert werden? "))
    
    terme = []
    partialsummen = []
    summe = 0
    
    print("\n=== Berechnung der Partialsumme ===\n")
    
    for n in range(1, n_max + 1):
        wert = eval(f, {"n": n, "__builtins__": {}})
        terme.append(wert)
        summe += wert
        partialsummen.append(summe)
        print(f"a_{{{n}}} = {wert:.8f}, S_{{{n}}} = {summe:.8f}")
    
    print(f"\n✅ Partialsumme S_{{{n_max}}} = {summe}")
    print(f"📊 Anzahl Terme: {n_max}")
    
    # Prüfe Konvergenz
    n_sym = sp.Symbol('n')
    try:
        reihen_grenzwert = sp.summation(sp.sympify(f), (n_sym, 1, sp.oo))
        print(f"\n🎯 Grenzwert der Reihe: {reihen_grenzwert}")
        
        if reihen_grenzwert == sp.oo or reihen_grenzwert == -sp.oo:
            print("❌ Die Reihe divergiert")
        else:
            print("✅ Die Reihe konvergiert")
    except:
        print("\n⚠️ Konvergenz konnte nicht bestimmt werden")