import streamlit as st
from limes import berechne_limes
from glied_rechner import berechne_glied
from folgen_rechner import berechne_folge
from partialsummen_rechner import berechne_partialsumme
from monotonie import berechne_monotonie

st.set_page_config(page_title="Folgen Rechner", page_icon="📊", layout="wide")

st.title("📊 Mathematische Folgen Rechner")
st.markdown("---")

# Sidebar für Navigation
st.sidebar.title("Navigation")
modus = st.sidebar.radio(
    "Wähle einen Rechner:",
    ["🎯 Limes bestimmen", "🔢 Glied berechnen", "📉 ε-Umgebung (Konvergenz)", "∑ Partialsumme", "📈 Monotonie untersuchen"]
)

# Limes bestimmen
if modus == "🎯 Limes bestimmen":
    st.header("🎯 Limes bestimmen")
    st.write("Berechnet den Grenzwert (Limes) einer Folge für n → ∞")
    
    folge_input = st.text_input(
        "Gib eine Folge ein (verwende 'n' als Variable):",
        value="(n+1)/n",
        help="Beispiele: 1/n, (n+1)/n, n**2, (-1)**n",
        key="limes_input"
    )
    
    max_iter = st.number_input(
        "Maximale Anzahl Iterationen:",
        min_value=100,
        max_value=100000,
        value=10000,
        step=1000,
        help="Stoppt nach dieser Anzahl falls keine Entscheidung getroffen wurde"
    )
    
    if st.button("🔍 Limes berechnen", key="limes_button"):
        try:
            with st.spinner("Berechne Limes..."):
                resultat = berechne_limes(folge_input, max_iter)
                st.session_state['limes_result'] = resultat
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige Ergebnis
    if 'limes_result' in st.session_state:
        resultat = st.session_state['limes_result']
        
        st.markdown("---")
        st.subheader("📊 Ergebnis")
        
        # Zeige Formel
        import sympy as sp
        n = sp.Symbol('n')
        
        try:
            folge_latex = sp.latex(sp.sympify(folge_input))
        except:
            folge_latex = folge_input
        
        # Zeige LaTeX basierend auf Typ
        if resultat['typ'] == 'oszillierend':
            st.latex(f"\\lim_{{n \\to \\infty}} {folge_latex} = \\text{{existiert nicht}}")
            st.error(f"❌ {resultat['message']}")
            
            if 'test_werte' in resultat:
                st.warning("**Erste 20 Werte zeigen das Oszillieren:**")
                cols = st.columns(5)
                for i, wert in enumerate(resultat['test_werte'][:10], 1):
                    with cols[(i-1) % 5]:
                        st.metric(f"n={i}", f"{wert:.3f}")
        
        elif resultat['typ'] == 'bestimmt_divergent':
            st.latex(f"\\lim_{{n \\to \\infty}} {folge_latex} = \\infty")
            st.error(f"❌ {resultat['message']}")
        
        elif resultat['typ'] == 'konvergent':
            # Formatiere den Limes schön
            if isinstance(resultat['limes'], (int, float)):
                if abs(resultat['limes']) < 0.0001:
                    limes_anzeige = f"{resultat['limes']:.10f}"  # Als Dezimalzahl
                else:
                    limes_anzeige = f"{resultat['limes']}"
            else:
                limes_anzeige = str(resultat['limes'])
            
            try:
                limes_latex = sp.latex(sp.sympify(limes_anzeige))
            except:
                limes_latex = limes_anzeige
            
            st.latex(f"\\lim_{{n \\to \\infty}} {folge_latex} = {limes_latex}")
            st.success(f"✅ {resultat['message']}")
        
        else:
            st.warning(f"⚠️ {resultat['message']}")
        
        # Info Box
        st.info(f"""
        **Grenzwert:** `{resultat['limes']}`
        
        **Status:** {'Divergent ❌' if resultat['divergent'] else 'Konvergent ✅'}
        """)

# Glied berechnen
elif modus == "🔢 Glied berechnen":
    st.header("🔢 Einzelnes Glied berechnen")
    st.write("Berechnet ein spezifisches Glied einer Folge.")
    
    folge_input = st.text_input(
        "Gib eine Folge ein (verwende 'n' als Variable):",
        value="1/n",
        help="Beispiele: 1/n, n**2, (n+1)/(2*n)",
        key="glied_input"
    )
    
    glied_nr = st.number_input(
        "Welches Glied willst du berechnen?",
        min_value=1,
        value=10,
        step=1
    )
    
    if st.button("🔍 Glied berechnen", key="glied_button"):
        try:
            with st.spinner("Berechne..."):
                resultat = berechne_glied(folge_input, glied_nr)
                st.session_state['glied_result'] = resultat
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige Ergebnis und Visualisierung (falls vorhanden)
    if 'glied_result' in st.session_state:
        resultat = st.session_state['glied_result']
        
        st.success(f"✅ Das {resultat['anzahl']}. Glied wurde berechnet!")
        st.metric(f"Glied a_{{{resultat['anzahl']}}}", f"{resultat['letzter_wert']:.6f}")
        
        # Visualisierung
        st.markdown("---")
        st.subheader("📊 Visualisierung")
        
        import plotly.graph_objects as go
        
        chart_type = st.radio("Diagramm-Typ:", ["📍 Punkte", "📊 Balken"], horizontal=True, key="chart_glied")
        
        n_values = list(range(1, len(resultat['alle_werte']) + 1))
        values = resultat['alle_werte']
        
        fig = go.Figure()
        
        if chart_type == "📍 Punkte":
            # Normale Punkte
            fig.add_trace(go.Scatter(
                x=n_values[:-1],
                y=values[:-1],
                mode='markers',
                name='Folgenwerte',
                marker=dict(size=8, color='#2ecc71')
            ))
            # Gesuchtes Glied hervorgehoben
            fig.add_trace(go.Scatter(
                x=[n_values[-1]],
                y=[values[-1]],
                mode='markers',
                name=f'Gesuchtes Glied (n={resultat["anzahl"]})',
                marker=dict(size=15, color='red', symbol='star')
            ))
        else:
            # Balken mit letztem rot
            colors = ['#2ecc71'] * (len(values) - 1) + ['red']
            fig.add_trace(go.Bar(
                x=n_values,
                y=values,
                marker=dict(color=colors)
            ))
        
        fig.update_layout(
            xaxis_title='n',
            yaxis_title='a_n',
            hovermode='x unified',
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"🔴 Das gesuchte Glied (n={resultat['anzahl']}) ist rot hervorgehoben")
        
        with st.expander("📈 Alle berechneten Werte anzeigen"):
            for i, wert in enumerate(resultat['alle_werte'], 1):
                st.write(f"a_{{{i}}} = {wert}")

# ε-Umgebung Rechner
elif modus == "📉 ε-Umgebung (Konvergenz)":
    st.header("🎯 ε-Umgebung und Konvergenz")
    st.write("Berechnet den Grenzwert und prüft die Konvergenz einer Folge.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        folge_input = st.text_input(
            "Gib eine Folge ein (verwende 'n' als Variable):",
            value="1/n",
            help="Beispiele: 1/n, 1/n**2, (n+1)/n",
            key="eps_input"
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
                st.session_state['eps_result'] = resultat
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige Ergebnis und Visualisierung (falls vorhanden)
    if 'eps_result' in st.session_state:
        resultat = st.session_state['eps_result']
        
        if resultat['divergent']:
            st.error(f"❌ {resultat['message']}")
            st.info(f"Grenzwert: {resultat['limes']}")
        else:
            st.success(f"✅ {resultat['message']}")
            st.metric("Grenzwert", resultat['limes'])
            st.metric("Anzahl Berechnungen", resultat['anzahl'])
            st.metric("Letzter Wert", f"{resultat['letzter_wert']:.6f}")
            
            # Visualisierung
            st.markdown("---")
            st.subheader("📊 Visualisierung")
            
            import plotly.graph_objects as go
            
            chart_type = st.radio("Diagramm-Typ:", ["📍 Punkte", "📊 Balken"], horizontal=True, key="chart_eps")
            
            n_values = list(range(1, len(resultat['alle_werte']) + 1))
            values = resultat['alle_werte']
            
            fig = go.Figure()
            
            if chart_type == "📍 Punkte":
                # Normale Punkte
                fig.add_trace(go.Scatter(
                    x=n_values[:-1],
                    y=values[:-1],
                    mode='markers',
                    name='Folgenwerte',
                    marker=dict(size=8, color='#1f77b4')
                ))
                # Letzter Punkt hervorgehoben
                fig.add_trace(go.Scatter(
                    x=[n_values[-1]],
                    y=[values[-1]],
                    mode='markers',
                    name=f'Letztes Glied (n={resultat["anzahl"]})',
                    marker=dict(size=15, color='red', symbol='star')
                ))
            else:
                # Balken mit letztem rot
                colors = ['#1f77b4'] * (len(values) - 1) + ['red']
                fig.add_trace(go.Bar(
                    x=n_values,
                    y=values,
                    marker=dict(color=colors)
                ))
            
            fig.update_layout(
                xaxis_title='n',
                yaxis_title='a_n',
                hovermode='x unified',
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"🔴 Der letzte Punkt/Balken (n={resultat['anzahl']}) ist rot hervorgehoben")
            
            with st.expander("📈 Alle berechneten Werte anzeigen"):
                for i, wert in enumerate(resultat['alle_werte'], 1):
                    st.write(f"a_{{{i}}} = {wert}")

# Partialsummen Rechner
elif modus == "∑ Partialsumme":
    st.header("∑ Partialsummen Rechner")
    st.write("Berechnet die Partialsumme einer Folge von n=1 bis n=N.")
    
    folge_input = st.text_input(
        "Gib eine Folge ein (verwende 'n' als Variable):",
        value="1/n**2",
        help="Beispiele: 1/n, 1/n**2, 2**n",
        key="partial_input"
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
                st.session_state['partial_result'] = resultat
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige Ergebnis und Visualisierung (falls vorhanden)
    if 'partial_result' in st.session_state:
        resultat = st.session_state['partial_result']
        
        st.success("✅ Partialsumme berechnet!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Partialsumme S_n", f"{resultat['partialsumme']:.8f}")
        with col2:
            st.metric("Anzahl Terme", resultat['anzahl_terme'])
        
        # Rechnung als Summe
        st.markdown("---")
        st.subheader("🧮 Summenrechnung")
        
        show_fractions = st.checkbox("Als Brüche anzeigen", value=True, key="show_frac")
        
        max_show = min(15, len(resultat['terme']))
        
        if show_fractions:
            from fractions import Fraction
            terme_str_list = []
            for t in resultat['terme'][:max_show]:
                try:
                    frac = Fraction(t).limit_denominator(1000)
                    if frac.denominator == 1:
                        terme_str_list.append(str(frac.numerator))
                    else:
                        terme_str_list.append(f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}")
                except:
                    terme_str_list.append(f"{t:.6f}")
            
            terme_latex = " + ".join(terme_str_list)
            if len(resultat['terme']) > max_show:
                terme_latex += f" + \\cdots"
            
            st.latex(f"{terme_latex} = {resultat['partialsumme']:.8f}")
        else:
            terme_str = " + ".join([f"{t:.6f}" for t in resultat['terme'][:max_show]])
            if len(resultat['terme']) > max_show:
                terme_str += f" + ..."
            
            st.latex(f"{terme_str} = {resultat['partialsumme']:.8f}")
        
        # Visualisierung
        st.markdown("---")
        st.subheader("📊 Visualisierung")
        
        import plotly.graph_objects as go
        
        tab1, tab2 = st.tabs(["📊 Einzelne Terme a_n", "📈 Partialsummen S_n"])
        
        with tab1:
            st.write("**Einzelne Terme der Folge**")
            chart_type1 = st.radio("Diagramm-Typ:", ["📍 Punkte", "📊 Balken"], horizontal=True, key="chart_terme")
            
            n_values = list(range(1, len(resultat['terme']) + 1))
            
            fig1 = go.Figure()
            
            if chart_type1 == "📍 Punkte":
                fig1.add_trace(go.Scatter(
                    x=n_values,
                    y=resultat['terme'],
                    mode='markers',
                    marker=dict(size=8, color='#3498db')
                ))
            else:
                fig1.add_trace(go.Bar(
                    x=n_values,
                    y=resultat['terme'],
                    marker=dict(color='#3498db')
                ))
            
            fig1.update_layout(
                xaxis_title='n',
                yaxis_title='a_n',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig1, use_container_width=True)
            st.caption("📊 Größe der einzelnen Terme")
        
        with tab2:
            st.write("**Kumulative Partialsummen**")
            chart_type2 = st.radio("Diagramm-Typ:", ["📍 Punkte", "📊 Balken"], horizontal=True, key="chart_summen")
            
            fig2 = go.Figure()
            
            if chart_type2 == "📍 Punkte":
                fig2.add_trace(go.Scatter(
                    x=n_values,
                    y=resultat['partialsummen'],
                    mode='markers',
                    marker=dict(size=8, color='#e74c3c')
                ))
            else:
                fig2.add_trace(go.Bar(
                    x=n_values,
                    y=resultat['partialsummen'],
                    marker=dict(color='#e74c3c')
                ))
            
            fig2.update_layout(
                xaxis_title='n',
                yaxis_title='S_n',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig2, use_container_width=True)
            st.caption("📈 Kumulative Summe bis n")
        
        with st.expander("📋 Alle Terme einzeln anzeigen"):
            for i, (term, partial) in enumerate(zip(resultat['terme'], resultat['partialsummen']), 1):
                if show_fractions:
                    try:
                        from fractions import Fraction
                        frac = Fraction(term).limit_denominator(1000)
                        st.write(f"a_{{{i}}} = {frac} = {term:.8f} → S_{{{i}}} = {partial:.8f}")
                    except:
                        st.write(f"a_{{{i}}} = {term:.8f} → S_{{{i}}} = {partial:.8f}")
                else:
                    st.write(f"a_{{{i}}} = {term:.8f} → S_{{{i}}} = {partial:.8f}")

# Monotonie untersuchen
elif modus == "📈 Monotonie untersuchen":
    st.header("📈 Monotonie untersuchen")
    st.write("Untersucht ob eine Folge monoton steigend oder fallend ist.")
    
    folge_input = st.text_input(
        "Gib eine Folge ein (verwende 'n' als Variable):",
        value="(-1)**n",
        help="Beispiele: n, -n, (-1)**n, n**2",
        key="mono_input"
    )
    
    max_iter = st.number_input(
        "Bis zu welchem Glied soll die Monotonie untersucht werden?",
        min_value=2,
        value=20,
        step=1
    )
    
    if st.button("🔍 Monotonie untersuchen", key="mono_button"):
        try:
            with st.spinner("Untersuche Monotonie..."):
                resultat = berechne_monotonie(folge_input, max_iter)
                st.session_state['mono_result'] = resultat
        
        except Exception as e:
            st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige Ergebnis und Visualisierung (falls vorhanden)
    if 'mono_result' in st.session_state:
        resultat = st.session_state['mono_result']
        
        st.success("✅ Monotonie untersucht!")
        
        # Zeige Intervalle
        st.markdown("---")
        st.subheader("📋 Monotonie-Intervalle")
        
        # Zusammenfassung
        anzahl_steigend = sum(1 for i in resultat['intervalle'] if i['typ'] == 'steigend')
        anzahl_fallend = sum(1 for i in resultat['intervalle'] if i['typ'] == 'fallend')
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📈 Steigende Intervalle", anzahl_steigend)
        with col2:
            st.metric("📉 Fallende Intervalle", anzahl_fallend)
        
        # Alle Intervalle in Expander (aufklappbar)
        with st.expander(f"📋 Alle {len(resultat['intervalle'])} Intervalle anzeigen", expanded=False):
            for intervall in resultat['intervalle']:
                if intervall['typ'] == 'steigend':
                    st.info(f"📈 **Monoton steigend** von n={intervall['von']} bis n={intervall['bis']}")
                else:
                    st.warning(f"📉 **Monoton fallend** von n={intervall['von']} bis n={intervall['bis']}")
        
        # Visualisierung
        st.markdown("---")
        st.subheader("📊 Visualisierung")
        
        import plotly.graph_objects as go
        
        n_values = list(range(1, len(resultat['alle_werte']) + 1))
        values = resultat['alle_werte']
        
        fig = go.Figure()
        
        # Zeichne farbige Liniensegmente für jedes Intervall
        for intervall in resultat['intervalle']:
            # Finde die Indizes für dieses Intervall
            start_idx = intervall['von'] - 1  # -1 weil Liste bei 0 beginnt
            end_idx = intervall['bis'] - 1
            
            # Extrahiere die Werte für dieses Intervall
            x_segment = n_values[start_idx:end_idx+1]
            y_segment = values[start_idx:end_idx+1]
            
            # Farbe basierend auf Typ
            if intervall['typ'] == 'steigend':
                color = '#2ecc71'  # Grün/Blau für steigend
                name = f'Steigend ({intervall["von"]}-{intervall["bis"]})'
            else:
                color = '#e74c3c'  # Rot für fallend
                name = f'Fallend ({intervall["von"]}-{intervall["bis"]})'
            
            # Zeichne Linie für dieses Segment
            fig.add_trace(go.Scatter(
                x=x_segment,
                y=y_segment,
                mode='lines+markers',
                line=dict(color=color, width=3),
                marker=dict(size=8, color=color),
                name=name,
                showlegend=True
            ))
        
        fig.update_layout(
            xaxis_title='n',
            yaxis_title='a_n',
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("🔵 Blau/Grün = Monoton steigend | 🔴 Rot = Monoton fallend")
        
        with st.expander("📋 Alle Werte anzeigen"):
            for i, wert in enumerate(resultat['alle_werte'], 1):
                st.write(f"a_{{{i}}} = {wert:.6f}")

st.markdown("---")
st.markdown("*Entwickelt mit Streamlit und SymPy*")
