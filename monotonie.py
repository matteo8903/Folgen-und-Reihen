import sympy as sp


def berechne_monotonie(folge_string: str, max_iter: int):
    """
    Untersucht die Monotonie einer Folge
    Für die Streamlit App
    """
    result = []
    intervalle = []
    current = None
    n = 1
    monotonsteigend = False
    monotonfallend = False
    
    while n <= max_iter:
        wert = eval(folge_string, {"n": n, "__builtins__": {}})
        result.append(wert)
        
        if n > 1:
            an = result[-2]
            an1 = result[-1]
            
            if an < an1:  # Steigend
                monotonsteigend = True
                monotonfallend = False
                
                if current == "fallend":
                    intervalle.append({
                        'typ': 'fallend',
                        'von': interwall[0],
                        'bis': interwall[-1]
                    })
                    current = "steigend"
                    interwall = [n-1, n]
                elif current == "steigend":
                    interwall.append(n)
                else:
                    current = "steigend"
                    interwall = [n-1, n]
                    
            else:  # Fallend
                monotonfallend = True
                monotonsteigend = False
                
                if current == "steigend":
                    intervalle.append({
                        'typ': 'steigend',
                        'von': interwall[0],
                        'bis': interwall[-1]
                    })
                    current = "fallend"
                    interwall = [n-1, n]
                elif current == "fallend":
                    interwall.append(n)
                else:
                    current = "fallend"
                    interwall = [n-1, n]
        
        n += 1
    
    # Letztes Intervall hinzufügen
    if interwall:
        if monotonsteigend:
            intervalle.append({
                'typ': 'steigend',
                'von': interwall[0],
                'bis': interwall[-1]
            })
        else:
            intervalle.append({
                'typ': 'fallend',
                'von': interwall[0],
                'bis': interwall[-1]
            })
    
    return {
        'alle_werte': result,
        'intervalle': intervalle
    }


# DEIN ORIGINALER CODE - BLEIBT EXAKT SO!
if __name__ == "__main__":
    f = input("Gib eine Gleichung ein: ")
    max_iter = int(input("Bis zu welchem Glied soll die Monotonie untersucht werden:"))


    def folge(f, max_iter):
        result = []
        interwall = []
        current = None
        n = 1
        monotonsteigend = False
        monotonfallend = False
        while n <= max_iter:
            wert = eval(f, {"n": n, "__builtins__": {}})
            result.append(wert)
            if n > 1:
                an = result[-2]
                an1 = result[-1]
                if an < an1:
                    monotonsteigend = True
                    monotonfallend = False
                    if current == "fallend":
                        current = "steigend"
                        print(f"Die Folge ist Monoton fallend von {interwall[0]} bis {interwall[-1]}")
                        interwall = [n-1, n]  
                    elif current == "steigend":
                        interwall.append(n)
                    else:
                        current = "steigend"
                        interwall = [n-1, n]
                else:
                    monotonfallend = True
                    monotonsteigend = False
                    if current == "steigend":
                        current = "fallend"
                        print(f"Die Folge ist Monoton steigend von {interwall[0]} bis {interwall[-1]}")
                        interwall = [n-1, n]  
                    elif current == "fallend":
                        interwall.append(n)
                    else:
                        current = "fallend"
                        interwall = [n-1, n]
            n += 1
        if interwall:
            if monotonsteigend:
                print(f"Die Folge ist Monoton steigend von {interwall[0]} bis {interwall[-1]}")
            else:
                print(f"Die Folge ist Monoton fallend von {interwall[0]} bis {interwall[-1]}")


    folge(f,max_iter)
