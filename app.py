import streamlit as st
from folgen_rechner import berechne_folge
from glied_rechner import berechne_glied
from partialsummen_rechner import berechne_partialsumme

st.set_page_config(page_title="Folgen Rechner", page_icon="📊", layout="wide")

# Session State initialisieren
if 'gespeicherte_funktion' not in st.session_state:
    st.session_state.gespeicherte_funktion = None

st.title("📊 Mathematische Folgen Rechner")
st.markdown("---")

# Sidebar für Navigation
st.sidebar.title("Navigation")
modus = st.sidebar.radio(
    "Wähle einen Rechner:",
    ["ε-Umgebung (Konvergenz)", "Glied berechnen", "Partialsumme (Σ)"]
)

st.sidebar.markdown("---")
if st.session_state.gespeicherte_funktion:
    st.sidebar.success(f"💾 Gespeicherte Funktion:\n`{st.session_state.gespeicherte_funktion}`")
    if st.sidebar.button("🗑️ Funktion löschen"):
        st.session_state.gespeicherte_funktion = None
        st.rerun()

# ε-Umgebung Rechner
if modus == "ε-Umgebung (Konvergenz)":
    st.header("🎯 ε-Umgebung und Konvergenz")
    st.write("Berechnet den Grenzwert und prüft die Konvergenz einer Folge.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        folge_input = st.text_input(
            "Gib eine Folge ein (verwende 'n' als Variable):",
            value="1/n",
            help="Beispiele: 1/n, 1/n**2, (n+1)/n"
        )
    
    with col2:
        epsilon = st.number_input(
            "ε-Wert:",
            min_value=0.0,
            value=0.01,
            step=0.01,
            format="%.4f"
        )
    
    if st.button("🔍 Berechnen", key="eps_button"):
        try:
            with st.spinner("Berechne..."):
                resultat = berechne_folge(folge_input, epsilon)
                
                if resultat['divergent']:
                    st.error(f"❌ {resultat['message']}")
                    st.info(f"Grenzwert: {resultat['limes']}")
                else:
                    st.success(f"✅ {resultat['message']}")
                    st.metric("Grenzwert", resultat['limes'])
                    st.metric("Anzahl Berechnungen", resultat['anzahl'])
                    st.metric("Letzter Wert", f"{resultat['letzter_wert']:.6f}")
                    
                    with st.expander("📈 Alle berechneten Werte anzeigen"):
                        for i, wert in enumerate(resultat['alle_werte'], 1):
                            st.write(f"a_{{{i}}} = {wert}")
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")

# Glied Rechner
elif modus == "Glied berechnen":
    st.header("🔢 Einzelnes Glied berechnen")
    st.write("Berechnet ein spezifisches Glied einer Folge und speichert die Funktion.")
    
    folge_input = st.text_input(
        "Gib eine Folge ein (verwende 'n' als Variable):",
        value="1/n",
        help="Beispiele: 1/n, n**2, (n+1)/(2*n)"
    )
    
    glied_nr = st.number_input(
        "Welches Glied willst du berechnen?",
        min_value=1,
        value=10,
        step=1
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Glied berechnen", key="glied_button"):
            try:
                with st.spinner("Berechne..."):
                    resultat = berechne_glied(folge_input, glied_nr)
                    
                    st.success(f"✅ Das {resultat['anzahl']}. Glied wurde berechnet!")
                    st.metric(f"Glied a_{{{resultat['anzahl']}}}", f"{resultat['letzter_wert']:.6f}")
                    
                    with st.expander("📈 Alle berechneten Werte anzeigen"):
                        for i, wert in enumerate(resultat['alle_werte'], 1):
                            st.write(f"a_{{{i}}} = {wert}")
            
            except Exception as e:
                st.error(f"❌ Fehler: {str(e)}")
    
    with col2:
        if st.button("💾 Funktion speichern", key="save_button"):
            st.session_state.gespeicherte_funktion = folge_input
            st.success("✅ Funktion gespeichert!")
            st.rerun()

# Partialsummen Rechner
elif modus == "Partialsumme (Σ)":
    st.header("∑ Partialsummen Rechner")
    st.write("Berechnet die Partialsumme einer Folge von n=1 bis n=N.")
    
    # Option: Gespeicherte Funktion verwenden oder neue eingeben
    use_saved = False
    if st.session_state.gespeicherte_funktion:
        use_saved = st.checkbox(
            f"💾 Gespeicherte Funktion verwenden: `{st.session_state.gespeicherte_funktion}`",
            value=True
        )
    
    if use_saved and st.session_state.gespeicherte_funktion:
        folge_input = st.session_state.gespeicherte_funktion
        st.info(f"Verwende gespeicherte Funktion: `{folge_input}`")
    else:
        folge_input = st.text_input(
            "Gib eine Folge ein (verwende 'n' als Variable):",
            value="1/n**2",
            help="Beispiele: 1/n, 1/n**2, 2**n"
        )
    
    n_max = st.number_input(
        "Bis zu welchem n soll summiert werden?",
        min_value=1,
        value=10,
        step=1
    )
    
    if st.button("🔍 Partialsumme berechnen", key="partial_button"):
        try:
            with st.spinner("Berechne Partialsumme..."):
                resultat = berechne_partialsumme(folge_input, n_max)
                
                st.success("✅ Partialsumme berechnet!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Partialsumme S_n", f"{resultat['partialsumme']:.8f}")
                with col2:
                    st.metric("Anzahl Terme", resultat['anzahl_terme'])
                
                if resultat['reihe_konvergiert']:
                    st.success(f"✅ Die Reihe konvergiert gegen: {resultat['grenzwert']}")
                else:
                    st.warning(f"⚠️ {resultat['konvergenz_info']}")
                
                with st.expander("📊 Einzelne Terme anzeigen"):
                    for i, wert in enumerate(resultat['terme'], 1):
                        st.write(f"a_{{{i}}} = {wert:.8f}")
                
                with st.expander("📈 Partialsummen anzeigen"):
                    for i, summe in enumerate(resultat['partialsummen'], 1):
                        st.write(f"S_{{{i}}} = {summe:.8f}")
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")

st.markdown("---")
st.markdown("*Entwickelt mit Streamlit und SymPy*")