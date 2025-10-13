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
    
    max_iterations = st.number_input(
        "Maximale Anzahl Berechnungen:",
        min_value=10,
        max_value=100000,
        value=10000,
        step=100,
        help="Stoppt nach dieser Anzahl, auch wenn ε nicht erreicht wurde"
    )
    
    if st.button("🔍 Berechnen", key="eps_button"):
        try:
            with st.spinner("Berechne..."):
                resultat = berechne_folge(folge_input, epsilon, max_iterations)
                
                if resultat['divergent']:
                    st.error(f"❌ {resultat['message']}")
                    st.info(f"Grenzwert: {resultat['limes']}")
                else:
                    st.success(f"✅ {resultat['message']}")
                    st.metric("Grenzwert", resultat['limes'])
                    st.metric("Anzahl Berechnungen", resultat['anzahl'])
                    st.metric("Letzter Wert", f"{resultat['letzter_wert']:.6f}")
                    
                    # Visualisierung hinzufügen
                    st.markdown("---")
                    st.subheader("📊 Visualisierung")
                    
                    import pandas as pd
                    
                    # DataFrame erstellen
                    df = pd.DataFrame({
                        'n': list(range(1, len(resultat['alle_werte']) + 1)),
                        'a_n': resultat['alle_werte'],
                        'Grenzwert': [float(resultat['limes'])] * len(resultat['alle_werte'])
                    })
                    
                    # Streamlit Line Chart (automatisch interaktiv!)
                    st.line_chart(df.set_index('n'))
                    
                    st.caption(f"🔴 Die rote horizontale Linie würde bei ε = {epsilon} liegen")
                    
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
                    
                    # Visualisierung hinzufügen
                    st.markdown("---")
                    st.subheader("📊 Visualisierung")
                    
                    import plotly.graph_objects as go
                    
                    # Daten vorbereiten
                    n_werte = list(range(1, len(resultat['alle_werte']) + 1))
                    folgen_werte = resultat['alle_werte']
                    
                    # Interaktiven Plot erstellen
                    fig = go.Figure()
                    
                    # Folge hinzufügen
                    fig.add_trace(go.Scatter(
                        x=n_werte,
                        y=folgen_werte,
                        mode='lines+markers',
                        name='Folge a_n',
                        line=dict(color='#1f77b4', width=2),
                        marker=dict(size=6)
                    ))
                    
                    # Markiere das gesuchte Glied
                    fig.add_trace(go.Scatter(
                        x=[resultat['anzahl']],
                        y=[resultat['letzter_wert']],
                        mode='markers',
                        name=f'Glied {resultat["anzahl"]}',
                        marker=dict(size=15, color='red', symbol='star')
                    ))
                    
                    # Layout anpassen
                    fig.update_layout(
                        title='Folgenverlauf (interaktiv - zoom & pan)',
                        xaxis_title='n',
                        yaxis_title='a_n',
                        hovermode='x unified',
                        height=600,
                        template='plotly_dark'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
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
                
                # Visualisierung hinzufügen
                st.markdown("---")
                st.subheader("📊 Visualisierung")
                
                import plotly.graph_objects as go
                from plotly.subplots import make_subplots
                
                # Daten vorbereiten
                n_werte = list(range(1, len(resultat['partialsummen']) + 1))
                
                # Zwei Subplots erstellen
                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=('Einzelne Terme der Folge', 'Partialsummen (Kumulative Summe)'),
                    vertical_spacing=0.12
                )
                
                # Plot 1: Einzelne Terme als Balken
                fig.add_trace(
                    go.Bar(
                        x=n_werte,
                        y=resultat['terme'],
                        name='Terme a_n',
                        marker=dict(color='steelblue'),
                        opacity=0.7
                    ),
                    row=1, col=1
                )
                
                # Plot 2: Partialsummen
                fig.add_trace(
                    go.Scatter(
                        x=n_werte,
                        y=resultat['partialsummen'],
                        mode='lines+markers',
                        name='Partialsummen S_n',
                        line=dict(color='green', width=2),
                        marker=dict(size=5)
                    ),
                    row=2, col=1
                )
                
                # Grenzwert-Linie hinzufügen (falls vorhanden)
                if resultat['reihe_konvergiert'] and resultat['grenzwert'] != "Unbekannt":
                    try:
                        grenzwert_float = float(resultat['grenzwert'])
                        fig.add_trace(
                            go.Scatter(
                                x=[n_werte[0], n_werte[-1]],
                                y=[grenzwert_float, grenzwert_float],
                                mode='lines',
                                name=f'Grenzwert: {resultat["grenzwert"]}',
                                line=dict(color='red', width=2, dash='dash')
                            ),
                            row=2, col=1
                        )
                    except:
                        pass
                
                # Layout anpassen
                fig.update_xaxes(title_text="n", row=1, col=1)
                fig.update_yaxes(title_text="a_n", row=1, col=1)
                fig.update_xaxes(title_text="n", row=2, col=1)
                fig.update_yaxes(title_text="S_n", row=2, col=1)
                
                fig.update_layout(
                    height=900,
                    showlegend=True,
                    hovermode='x unified',
                    template='plotly_dark',
                    title_text="Partialsummen Analyse (interaktiv - zoom & pan)"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
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
