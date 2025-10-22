import sympy as sp


# Funktionen für die Streamlit App
def check(f):
    """
    Prüft ob die Folge oszilliert
    True = alles OK, kein Oszillieren
    False = Problem, oszilliert!
    """
    checkresult = True
    result = []
    ungeradelistepos = []
    ungeradelisteneg = []
    geradelistepos = []
    geradelisteneg = []
    n = 1
    for i in range(20):
        wert = eval(f, {"n": n, "__builtins__": {}})
        result.append(wert)
        n += 1
    gerade = result[::2]
    ungerade = result[1::2]

    for Glied in ungerade:
        if Glied < 0:
            ungeradelisteneg.append(Glied)
        elif Glied > 0:
            ungeradelistepos.append(Glied)
    for Glied in gerade:
        if Glied < 0: 
            geradelisteneg.append(Glied)
        elif Glied > 0: 
            geradelistepos.append(Glied)

    if len(ungeradelistepos) == 0 and len(geradelisteneg) == 0:
        checkresult = False
    elif len(ungeradelisteneg) == 0 and len(geradelistepos) == 0:
        checkresult = False
    else:
        checkresult = True
    return checkresult


def berechne_limes(folge_string: str):
    """
    Berechnet den Limes einer Folge für n → ∞
    Für die Streamlit App
    """
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(folge_string), n_sym, sp.oo)
    checkresult = check(folge_string)
    
    # Berechne erste 10 Werte zum Anzeigen
    test_werte = []
    for i in range(1, 11):
        try:
            wert = eval(folge_string, {"n": i, "__builtins__": {}})
            test_werte.append(wert)
        except:
            pass
    
    if checkresult == False:
        return {
            'limes': 'existiert nicht',
            'divergent': True,
            'typ': 'oszillierend',
            'message': f"Es gibt hier keinen Limes, da die Folge zwischen positiven und negativen Werten hin und her schwankt.",
            'test_werte': test_werte
        }
    elif limes == sp.oo or limes == sp.zoo:
        return {
            'limes': limes,
            'divergent': True,
            'typ': 'bestimmt_divergent',
            'message': f"Da der Limes gegen ∞ geht ist er Divergent."
        }
    elif limes == -sp.oo:
        return {
            'limes': limes,
            'divergent': True,
            'typ': 'bestimmt_divergent',
            'message': f"Da der Limes gegen -∞ geht ist er Divergent."
        }
    else:
        return {
            'limes': limes,
            'divergent': False,
            'typ': 'konvergent',
            'message': f"Der Limes geht gegen {limes} und ist deshalb konvergent"
        }


# DEIN ORIGINALER CODE - EXAKT SO WIE DU IHN WILLST
if __name__ == "__main__":
    f = input("Gib eine Gleichung ein: ")
    
    n_sym = sp.Symbol('n')
    limes = sp.limit(sp.sympify(f), n_sym, sp.oo)
    
    def check(f):
        checkresult = True
        result = []
        ungeradelistepos = []
        ungeradelisteneg = []
        geradelistepos = []
        geradelisteneg = []
        n = 1
        for i in range(20):
            wert = eval(f, {"n": n, "__builtins__": {}})
            result.append(wert)
            n += 1
        gerade = result[::2]
        ungerade = result[1::2]

        for Glied in ungerade:
            if Glied < 0:
                ungeradelisteneg.append(Glied)
            elif Glied > 0:
                ungeradelistepos.append(Glied)
        for Glied in gerade:
            if Glied < 0: 
                geradelisteneg.append(Glied)
            elif Glied > 0: 
                geradelistepos.append(Glied)

        if len(ungeradelistepos) == 0 and len(geradelisteneg) == 0:
            checkresult = False
        elif len(ungeradelisteneg) == 0 and len(geradelistepos) == 0:
            checkresult = False
        else:
            checkresult = True
        return checkresult
    
    checkresult = check(f)
    
    if checkresult == False:
        print(f"Es gibt hier keinen Limes, da die Folge zwischen positiven und negativen Werten hin und her schwankt.")
    elif limes == sp.oo or limes == sp.zoo:
        print(f"Da der Limes gegen oo geht ist er Divergent.")
    elif limes == -sp.oo:
        print(f"Da der Limes gegen -oo geht ist er Divergent.")
    else:
        print(f"Der Limes geht gegen {limes} und ist deshalb konvergent.")
