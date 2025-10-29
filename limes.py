import sympy as sp


# Funktionen für die Streamlit App
def check_oszillation(f):
    """
    Prüft ob Folge oszilliert
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


def berechne_limes(folge_string: str, max_iter: int = 10000):
    """
    Berechnet den Limes für die Streamlit App
    """
    result = []
    differenzen = [] 
    n = 1
    limesentscheid = None
    
    while n <= max_iter and limesentscheid == None:
        wert = eval(folge_string, {"n": n, "__builtins__": {}})
        result.append(wert)
        
        if n > 1:
            an = result[-2]
            an1 = result[-1]
            differenz = abs(an1 - an)
            differenzen.append(differenz)
            
            if n > 2: 
                diff = differenzen[-2]
                diff_plus_1 = differenzen[-1]
                
                if diff == 0 and diff_plus_1 == 0:
                    return {
                        'limes': an,
                        'divergent': False,
                        'typ': 'konvergent',
                        'message': f"Der Limes geht gegen {an}",
                        'alle_werte': result[:min(100, len(result))]
                    }
                
                elif diff < diff_plus_1:
                    checkresult = check_oszillation(folge_string)
                    
                    if checkresult == False: 
                        return {
                            'limes': 'existiert nicht',
                            'divergent': True,
                            'typ': 'oszillierend',
                            'message': f"Es gibt hier keinen Limes, da die Folge zwischen positiven und negativen Werten hin und her schwankt.",
                            'test_werte': result[:20]
                        }
                    else:
                        return {
                            'limes': sp.oo,
                            'divergent': True,
                            'typ': 'bestimmt_divergent',
                            'message': f"Der Limes geht gegen unendlich"
                        }
                
                elif diff_plus_1 < 0.00000001:
                    return {
                        'limes': an1,
                        'divergent': False,
                        'typ': 'konvergent',
                        'message': f"Die Folge konvergiert gegen {an1}",
                        'alle_werte': result[:min(100, len(result))]
                    }
                
                elif diff == diff_plus_1:
                    return {
                        'limes': sp.oo,
                        'divergent': True,
                        'typ': 'bestimmt_divergent',
                        'message': f"Die Folge Divergiert gegen unendlich"
                    }
        
        n += 1
    
    # Falls keine Entscheidung
    return {
        'limes': 'unbekannt',
        'divergent': True,
        'typ': 'unbekannt',
        'message': f"Nach {max_iter} Iterationen keine Entscheidung möglich"
    }


# DEIN ORIGINALER CODE - EXAKT SO WIE DU IHN WILLST
if __name__ == "__main__":
    f = input("Gib eine Gleichung ein: ")
    max_iter = 10000000


    def folge(f, max_iter):
        result = []
        differenzen = [] 
        n = 1
        limesentscheid = None
        while n <= max_iter and limesentscheid == None:
            wert = eval(f, {"n": n, "__builtins__": {}})
            result.append(wert)
            if n > 1:
                an = result[-2]
                an1 = result[-1]
                differenz = abs(an1 - an)
                differenzen.append(differenz)
                if n > 2: 
                    diff = differenzen[-2]
                    diff_plus_1 = differenzen[-1]
                    if diff == 0 and diff_plus_1 == 0:
                        print(f"Der limes geht gegen {an}")
                        limesentscheid = True

                    elif diff < diff_plus_1:
                        checkresult = check_oszillation(f)

                        if checkresult == False: 
                            print(f"Es gibt hier keinen Limes, da die Folge zwischen positiven und negativen Werten hin und her schwankt.")
                        else:
                            print(f"Der Limes geht gegen unendlich")
                        limesentscheid = True

                    elif diff_plus_1 < 0.00000001:
                        limesentscheid = True
                        print(f"Die Folge konvergiert gegen {an1}")
                    
                    elif diff == diff_plus_1:
                        print(f"Die Folge Divergiert gegen unendlich")
                        limesentscheid = True
                    else:
                        pass

            n += 1

    def check_oszillation(f):
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


    folge(f,max_iter)
