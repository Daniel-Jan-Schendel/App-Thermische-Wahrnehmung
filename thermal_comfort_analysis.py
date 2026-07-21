import streamlit as st
import pandas as pd
import pydeck as pdk
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from tabulate import tabulate
from PIL import Image



st.set_page_config(page_title="Thermischekomfort Datenanalyse", layout="wide", initial_sidebar_state="expanded")
# Analyse der thermischen Komfortparameter
# ---------------------------------------------------------
# Daten laden
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_bereinigt_final.csv")
df = load_data()


st.title("Analyse der Komfortparameter und Einflussgrößen")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab1, tab2 = st.tabs([
    "Subjektiven Komfortvariablen Korrelation",
    "Physikalischen Korrelationsanalyse"
    ])

with tab1:

    german_labels = {
    "thermal_sensation": "Thermische Empfinden",
    "thermal_acceptability": "Thermische Akzeptanz",
    "thermal_preference": "Thermische Präferenz",
    "thermal_comfort": "Thermischer Komfort"
}

    # st.markdown("""
    #     ##### 1. Thermische Empfindung (TS) 
    #     **Kalt  ◄────── Neutral ──────►  Heiß**  
    #     `-3    -2    -1    0    +1    +2    +3 `

    #     ##### 2. Thermische Akzeptanz (TA)
    #     ○ Nicht akzeptabel  
    #     ○ Akzeptabel  

    #     ##### 3. Thermische Präferenz (TP)  
    #     **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
    #     `  -1                         0                         +1     `

    #     ##### 4. Thermischer Komfort (TC, ASHRAE‑Skala 1–6)  
    #     **Sehr unkomfortabel ◄──────────────────────► Sehr komfortabel**  
    #            `  1             2            3           4           5            6   `
    #     """)

   
    st.subheader("Wie hängen die subjektiven Komfortvariablen miteinander zusammen?")

    st.markdown("""
    Die subjektiven Komfortvariablen beschreiben, wie Menschen ihre thermische Umgebung wahrnehmen,
    bewerten und welche Änderungen sie bevorzugen. Die folgende Analyse zeigt, wie stark diese
    Parameter miteinander korrelieren und welche Muster im thermischen Erleben sichtbar werden.

    ### 🔍 Interpretation der Korrelationen

    - **Positive Werte:** Beide Variablen steigen gemeinsam (z. B. wärmer empfinden → höherer Komfort).  
    - **Negative Werte:** Die Variablen entwickeln sich gegensätzlich (z. B. wärmer empfinden → geringere Akzeptanz).  
    - **Nahe 0:** Kein klarer Zusammenhang.

    Die farbliche Darstellung der Heatmap und der Analysebox rechts hilft, starke Zusammenhänge sofort zu erkennen.
    """)

    # Zwei Spalten erstellen
    col1, col2 = st.columns([1.8, 1])   # linke Spalte etwas breiter für die Heatmap

    with col1:
        # Relevante Spalten
        cols = [
            "thermal_sensation",
            "thermal_acceptability",
            "thermal_preference",
            "thermal_comfort"
        ]

        df_sub = df[cols].copy()

        # -----------------------------
        # 1. Numerische Umwandlung
        # -----------------------------
        df_sub["thermal_sensation"] = pd.to_numeric(df_sub["thermal_sensation"], errors="coerce")
        df_sub["thermal_comfort"] = pd.to_numeric(df_sub["thermal_comfort"], errors="coerce")

        # -----------------------------
        # 2. thermal_preference → numerisch
        # -----------------------------
        mapping_preference = {
            "warmer": 1,
            "no change": 0,
            "cooler": -1
        }
        df_sub["thermal_preference"] = df_sub["thermal_preference"].map(mapping_preference)

        # -----------------------------
        # 3. thermal_acceptability → numerisch
        # -----------------------------
        mapping_acceptability = {
            "acceptable": 1,
            "unacceptable": 0,
            "Unknown": None   # Unknown → NaN
        }
        df_sub["thermal_acceptability"] = df_sub["thermal_acceptability"].map(mapping_acceptability)

        # -----------------------------
        # 4. Zeilen mit fehlenden Werten entfernen
        # -----------------------------
        df_sub = df_sub.dropna()

        # -----------------------------
        # 5. Korrelationsmatrix
        # -----------------------------
        corr_matrix = df_sub.corr(method="spearman")
        corr_matrix = corr_matrix.rename(index=german_labels, columns=german_labels)


            # -----------------------------
            # 6. Heatmap anzeigen
            # -----------------------------
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            linewidths=0.5,
            ax=ax
        )
        ax.set_title("Korrelationsmatrix der subjektiven Komfortvariablen")
        st.pyplot(fig)
        st.caption(
        "Diese Korrelationsmatrix zeigt, wie stark die subjektiven Komfortparameter – "
        "thermische Empfinden, Akzeptanz, Präferenz und Komfortbewertung – miteinander "
        "verbunden sind.")


with col2:

    # --- Werte aus der Matrix ---
    r_ts_tp = corr_matrix.loc["Thermische Empfinden", "Thermische Präferenz"]
    r_ts_tc = corr_matrix.loc["Thermische Empfinden", "Thermischer Komfort"]
    r_tp_tc = corr_matrix.loc["Thermische Präferenz", "Thermischer Komfort"]
    r_ta_tc = corr_matrix.loc["Thermische Akzeptanz", "Thermischer Komfort"]

    # --- Farbskala passend zur Heatmap ---
    def color_for_r(r):
        if r <= -0.50:
            return "#005BBB"   # starke negative Korrelation
        elif r <= -0.15:
            return "#5F9FE9"   # mittlere negative
        elif r <= 0.15:
            return "#E0E0E0"   # neutral
        elif r < 0.50:
            return "#F5B97A"   # mittlere positive
        else:
            return "#C0392B"   # starke positive

    c_ts_tp = color_for_r(r_ts_tp)
    c_ts_tc = color_for_r(r_ts_tc)
    c_tp_tc = color_for_r(r_tp_tc)
    c_ta_tc = color_for_r(r_ta_tc)

    # --- PANEL MIT KURZEN ERKLÄRUNGEN ---
    st.markdown(f"""
    <div style="padding-left: 10px; margin-bottom: 18px;">
        <h5 style="margin:0;">Empfinden ↔ Präferenz  
        <span style="color:{c_ts_tp}; font-weight:bold;">(r = {r_ts_tp:.2f})</span></h5>
        <p style="margin:4px 0;">
        Wärmeres Empfinden führt typischerweise zu einer stärkeren Präferenz für kühlere Bedingungen.
        </p>
    </div>

    <div style="padding-left: 10px; margin-bottom: 18px;">
        <h5 style="margin:0;">Empfinden ↔ Komfort  
        <span style="color:{c_ts_tc}; font-weight:bold;">(r = {r_ts_tc:.2f})</span></h5>
        <p style="margin:4px 0;">
        Das thermische Empfinden beeinflusst die Komfortbewertung leicht, jedoch nicht stark.
        </p>
    </div>

    <div style="padding-left: 10px; margin-bottom: 18px;">
        <h5 style="margin:0;">Präferenz ↔ Komfort  
        <span style="color:{c_tp_tc}; font-weight:bold;">(r = {r_tp_tc:.2f})</span></h5>
        <p style="margin:4px 0;">
        Der Wunsch nach Veränderung steht im Zusammenhang mit der empfundenen Komfortqualität.
        </p>
    </div>

    <div style="padding-left: 10px; margin-bottom: 18px;">
        <h5 style="margin:0;">Akzeptanz ↔ Komfort  
        <span style="color:{c_ta_tc}; font-weight:bold;">(r = {r_ta_tc:.2f})</span></h5>
        <p style="margin:4px 0;">
        Akzeptable Bedingungen werden im Durchschnitt als komfortabler bewertet.
        </p>
    </div>
    """, unsafe_allow_html=True)


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

# with tab2:

#     st.subheader("Welche physikalischen Faktoren beeinflussen den thermischen Komfort am stärksten?")

#     st.markdown("""
#     <div style="font-size:16px; line-height:1.55;">

#     🌡️ **Diese Analyse untersucht die Zusammenhänge zwischen den zentralen physikalischen Einflussgrößen des thermischen Komforts.**  
#     Dabei werden folgende Parameter betrachtet:

#     - **Metabolische Aktivität**  
#     - **Bekleidungsisolation**  
#     - **Lufttemperatur**  
#     - **Luftgeschwindigkeit**  
#     - **Mittlere Strahlungstemperatur**  
#     - **Relative Luftfeuchtigkeit**  

#     </div>
#     """, unsafe_allow_html=True)

#     # ============================================================
#     # 1. Select relevant physical variables
#     # ============================================================

#     cols_phys = [
#         "metabolic_rate",
#         "clothing_ensemble_insulation",
#         "air_temperature",
#         "air_speed",
#         "radiant_temperature",
#         "relative_humidity"
#     ]

#         # Zwei Spalten erstellen
#     col01, col02 = st.columns([1.8, 1])   # linke Spalte etwas breiter für die Heatmap
    
#     with col01:
            
#         df_phys = df[cols_phys].copy()

#         # Convert to numeric
#         for c in cols_phys:
#             df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

#         df_phys = df_phys.dropna()

#         # ============================================================
#         # 2. Compute correlation matrix (Spearman recommended)
#         # ============================================================

#         corr_matrix = df_phys.corr(method="spearman")

#         # ============================================================
#         # 3. Heatmap visualization
#         # ============================================================

#         fig, ax = plt.subplots(figsize=(8, 5))
#         ax.set_title("Korrelationsmatrix der physikalischen Komfortvariablen")

#         sns.heatmap(
#             corr_matrix,
#             annot=True,
#             cmap="coolwarm",
#             vmin=-1,
#             vmax=1,
#             linewidths=0.5,
#             ax=ax
#         )
#         st.pyplot(fig)
    
#     with col02:

#         st.markdown("""
                    
#     ##### 🔥 Wichtigste Korrelationen
#     <div style="font-size:16px; line-height:1.55;">

#     🌡️ **Strahlungstemperatur ↔ Lufttemperatur (r = 0.96)**  
#     - Starke positive Korrelation 
#     - Lufttemperatur und Strahlungstemperatur sind stark thermisch miteinander verknüpft.<br>
#         T_o = (T_a + T_r)/2<br>
#      👕 **Bekleidungsisolation ↔ Strahlungstemperatur (-0.42)**  
#     - Negative Korrelation 
#     - Bekleidungsisolation steigt bei geringerer Strahlungstemperatur.
#     </div>
#     """, unsafe_allow_html=True)


#         #col02.subheader("Automatische Interpretation der physikalischen Einflussgrößen")

#         interpret = []

#         # ---- Filtro de correlaciones
#         def passes_filter(r):
#             return (r >= -0.40) or (r <= -0.42) or (r >= 0.96)

#         # ---- Clasificación visual
#         def describe_corr(r):
#             if r > 0.6:
#                 return ("Starke positive Korrelation", "green")
#             elif r > 0.3:
#                 return ("Positive Korrelation", "darkgreen")
#             elif r > 0.1:
#                 return ("Sehr schwache positive Korrelation", "gray")
#             elif r < -0.6:
#                 return ("Starke negative Korrelation", "red")
#             elif r < -0.3:
#                 return ("Negative Korrelation", "darkred")
#             elif r < -0.1:
#                 return ("Sehr schwache negative Korrelation", "gray")
#             else:
#                 return ("Keine relevante Korrelation", "black")

#         # ---- Generador de bullet‑points
#         def add_corr(r, text):
#             if passes_filter(r):
#                 direction, color = describe_corr(r)
#                 interpret.append(
#                     f"- <span style='color:{color}; font-weight:bold;'>{direction} (r = {r:.2f})</span><br>"
#                     f"  {text}"
#                 )

#         # ---- Variables de la matriz
#         mr  = corr_matrix["metabolic_rate"]
#         clo = corr_matrix["clothing_ensemble_insulation"]
#         ta  = corr_matrix["air_temperature"]
#         vel = corr_matrix["air_speed"]
#         tr  = corr_matrix["radiant_temperature"]
#         rh  = corr_matrix["relative_humidity"]

#         # ---- Reglas con filtro aplicado

#         # Metabolic Rate
#         add_corr(mr["air_temperature"],
#                 "Höhere metabolische Aktivität tritt häufig bei höheren Lufttemperaturen auf.")
#         add_corr(mr["air_speed"],
#                 "Personen mit höherem Metabolismus bevorzugen oft höhere Luftgeschwindigkeiten.")

#         # Clothing
#         add_corr(clo["air_temperature"],
#                 "Mehr Kleidung wird typischerweise bei niedrigeren Lufttemperaturen getragen.")
#         add_corr(clo["radiant_temperature"],
#                 "Bekleidungsisolation steigt bei geringerer Strahlungstemperatur.")

#         # Air Temperature
#         add_corr(ta["radiant_temperature"],
#                 "Lufttemperatur und Strahlungstemperatur sind thermisch stark gekoppelt.")
#         add_corr(ta["relative_humidity"],
#                 "Höhere Lufttemperaturen gehen oft mit höherer Luftfeuchtigkeit einher.")

#         # Air Velocity
#         add_corr(vel["air_temperature"],
#                 "Höhere Luftgeschwindigkeiten treten häufig bei höheren Temperaturen auf (Kühlbedarf).")

#         # Humidity
#         add_corr(rh["air_temperature"],
#                 "Warme Bedingungen sind häufig feuchter, was die Verdunstungskühlung reduziert.")

#         # ---- Output
#         #col02.markdown("<br>".join(interpret), unsafe_allow_html=True)

   
#     with st.expander("📘 Erklärung:  Beziehung zu Lufttemperatur & Strahlungstemperatur"):
#         st.markdown("""
  
#             #### 📈 Zusammenhang 

#             - **Strahlungstemperatur ↔ Lufttemperatur (r = 0.96)**  
#             → Sehr starke positive Korrelation  
#             → Beide Temperaturen steigen und fallen gemeinsam  
#             → Deshalb beeinflussen sie die operative Temperatur fast identisch

#             - **Bekleidungsisolation ↔ Strahlungstemperatur (r = -0.42)**  
#             → Negative Korrelation  
#             → Sinkt die Strahlungstemperatur, steigt oft die Bekleidungsisolation  
#             → Menschen kompensieren kühlere Oberflächen durch mehr Kleidung

#             </div>
#         """, unsafe_allow_html=True)


################################################################################################################################
# ============================================================
# TAB 2 – Physikalische Korrelationsanalyse
# ============================================================

with tab2:
    
    st.subheader("📊 Physikalische Einflussgrößen des thermischen Komforts")

    st.markdown("""
    <div style="font-size:16px; line-height:1.55;">

    Diese Analyse zeigt, wie stark zentrale **physikalische Parameter** miteinander korrelieren und 
    welche davon den thermischen Komfort am stärksten beeinflussen.  
    Untersuchte Einflussgrößen:

    - 🔥 **Metabolische Aktivität**  
    - 👕 **Bekleidungsisolation**  
    - 🌡️ **Lufttemperatur**  
    - 💨 **Luftgeschwindigkeit**  
    - ☀️ **Strahlungstemperatur**  
    - 💧 **Relative Luftfeuchtigkeit**  

    Die Heatmap links zeigt die Stärke der Zusammenhänge (Spearman‑Korrelation), während rechts die 
    wichtigsten Beziehungen automatisch interpretiert werden.

    </div>
    """, unsafe_allow_html=True)


    # ============================================================
    # 1. Physikalische Variablen auswählen
    # ============================================================

    cols_phys = [
        "metabolic_rate",
        "clothing_ensemble_insulation",
        "air_temperature",
        "air_speed",
        "radiant_temperature",
        "relative_humidity"
    ]

    # Deutsche Labels für die Darstellung
    german_phys_labels = {
        "metabolic_rate": "Metabolische Aktivität",
        "clothing_ensemble_insulation": "Bekleidungsisolation",
        "air_temperature": "Lufttemperatur",
        "air_speed": "Luftgeschwindigkeit",
        "radiant_temperature": "Strahlungstemperatur",
        "relative_humidity": "Relative Luftfeuchtigkeit"
    }

    # Zwei Spalten erstellen
    col01, col02 = st.columns([1.8, 1])


    # ============================================================
    # 2. Heatmap links
    # ============================================================
    with col01:

        df_phys = df[cols_phys].copy()

        # Numerische Umwandlung (NICHT verändert)
        for c in cols_phys:
            df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

        df_phys = df_phys.dropna()

        # Korrelation berechnen (NICHT verändert)
        corr_matrix = df_phys.corr(method="spearman")

        # Deutsche Labels anwenden
        corr_matrix = corr_matrix.rename(index=german_phys_labels, columns=german_phys_labels)

        # Heatmap
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_title("Korrelationsmatrix der physikalischen Komfortvariablen")

        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            vmin=-1,
            vmax=1,
            linewidths=0.5,
            ax=ax
        )
        st.pyplot(fig)


    # ============================================================
    # 3. Interpretationspanel rechts
    # ============================================================
    with col02:

        st.markdown("#### 🔥 Wichtigste physikalische Zusammenhänge")

        # Werte extrahieren (jetzt mit deutschen Labels)
        r_ta_tr  = corr_matrix.loc["Lufttemperatur", "Strahlungstemperatur"]
        r_clo_tr = corr_matrix.loc["Bekleidungsisolation", "Strahlungstemperatur"]

        # Farbskala passend zur Heatmap
        def color_for_r(r):
            if r >= 0.75:
                return "#C0392B"   # starke positive
            elif r >= 0.40:
                return "#E67E22"   # mittlere positive
            elif r >= 0.15:
                return "#F1C40F"   # leichte positive
            elif r <= -0.75:
                return "#005BBB"   # starke negative
            elif r <= -0.40:
                return "#5F9FE9"   # mittlere negative
            elif r <= -0.15:
                return "#A9CCE3"   # leichte negative
            else:
                return "#D5D8DC"   # neutral

        c_ta_tr  = color_for_r(r_ta_tr)
        c_clo_tr = color_for_r(r_clo_tr)

        # Panel
        st.markdown(f"""
        <div style="font-size:16px; line-height:1.55; padding-left:6px;">

        <h5 style="margin-bottom:4px;">🌡️ Lufttemperatur ↔ Strahlungstemperatur  
        <span style="color:{c_ta_tr}; font-weight:bold;">(r = {r_ta_tr:.2f})</span></h5>
        • Sehr starke positive Korrelation  
        • Beide Temperaturen steigen und fallen gemeinsam  
        • Deshalb beeinflussen sie die operative Temperatur nahezu identisch  
        <br><br>

        <h5 style="margin-bottom:4px;">👕 Bekleidungsisolation ↔ Strahlungstemperatur  
        <span style="color:{c_clo_tr}; font-weight:bold;">(r = {r_clo_tr:.2f})</span></h5>
        • Mittlere negative Korrelation  
        • Sinkt die Strahlungstemperatur, wird häufig mehr Kleidung getragen  
        • Menschen kompensieren kühlere Oberflächen durch höhere Isolation 
        
         

        </div>
        """, unsafe_allow_html=True)


    # ============================================================
    # 4. Expander – Erklärung
    # ============================================================
    with st.expander("📘 Erklärung der wichtigsten Zusammenhänge"):

        st.markdown("### 🔥 Wissenschaftliche Interpretation der physikalischen Zusammenhänge")

        # Farbskala passend zur Heatmap
        def color_for_r(r):
            if r >= 0.75:
                return "#C0392B"   # starke positive
            elif r >= 0.40:
                return "#E67E22"   # mittlere positive
            elif r >= 0.15:
                return "#F1C40F"   # leichte positive
            elif r <= -0.75:
                return "#005BBB"   # starke negative
            elif r <= -0.40:
                return "#5F9FE9"   # mittlere negative
            elif r <= -0.15:
                return "#A9CCE3"   # leichte negative
            else:
                return "#D5D8DC"   # neutral

        # Schwellenwerte für wissenschaftlich relevante Korrelationen
        THRESHOLD_POS = 0.15     # leichte positive Korrelation
        THRESHOLD_NEG = -0.15    # leichte negative Korrelation

        # Wissenschaftliche Erklärungstexte
        def explain(var1, var2, r):
            color = color_for_r(r)

            # Stärke klassifizieren
            if r >= 0.75:
                strength = "Sehr starke positive Korrelation"
                mechanism = (
                    "Die beiden Größen zeigen nahezu identische thermische Dynamiken. "
                    "Dies weist auf eine direkte physikalische Kopplung oder gemeinsame "
                    "Einflussfaktoren hin."
                )
            elif r >= 0.40:
                strength = "Mittlere positive Korrelation"
                mechanism = (
                    "Die Variablen steigen und fallen gemeinsam, was auf einen "
                    "substanziellen thermischen Zusammenhang hindeutet."
                )
            elif r >= 0.15:
                strength = "Leichte positive Korrelation"
                mechanism = (
                    "Ein moderater Gleichlauf der Variablen deutet auf indirekte "
                    "thermische Wechselwirkungen oder gemeinsame Randbedingungen hin."
                )
            elif r <= -0.75:
                strength = "Sehr starke negative Korrelation"
                mechanism = (
                    "Die Variablen entwickeln sich stark gegensätzlich. Dies spricht "
                    "für kompensatorische thermische Mechanismen oder gegenläufige "
                    "physikalische Effekte."
                )
            elif r <= -0.40:
                strength = "Mittlere negative Korrelation"
                mechanism = (
                    "Die Variablen zeigen gegenläufige Trends, was auf thermische "
                    "Kompensation oder unterschiedliche physikalische Rollen hinweist."
                )
            elif r <= -0.15:
                strength = "Leichte negative Korrelation"
                mechanism = (
                    "Ein moderater gegenläufiger Verlauf deutet auf subtile "
                    "thermische Ausgleichsmechanismen hin."
                )
            else:
                return None

            return f"""
            <div style="font-size:16px; line-height:1.55; padding-left:6px;">
                <h5 style="margin-bottom:4px;">{var1} ↔ {var2}  
                <span style="color:{color}; font-weight:bold;">(r = {r:.2f})</span></h5>
                • {strength}<br>
                • {mechanism}<br>
            </div>
            """

        # Alle Paare durchgehen
        vars_list = corr_matrix.columns.tolist()
        explanations = []

        for i in range(len(vars_list)):
            for j in range(i + 1, len(vars_list)):
                var1 = vars_list[i]
                var2 = vars_list[j]
                r = corr_matrix.loc[var1, var2]

                block = explain(var1, var2, r)
                if block:
                    explanations.append((abs(r), block))

        # Sortieren nach Stärke der Korrelation
        explanations.sort(reverse=True, key=lambda x: x[0])

        # Ausgabe
        if explanations:
            for _, block in explanations:
                st.markdown(block, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.markdown("Keine wissenschaftlich relevanten Zusammenhänge gefunden.")





#     st.subheader("Optimale Raumtemperatur nach Aktivität und Bekleidung")

#     # Sicherstellen, dass die Felder numerisch sind
#     df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
#     df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

#     # Nur gültige Zeilen
#     df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

#     # Funktion zur Berechnung der optimalen Temperatur nach ISO 7730 (vereinfachte Näherung)
#     def optimal_temp(met, clo):
#         """
#         Vereinfachte Näherung basierend auf ISO 7730:
#         - höhere Aktivität → niedrigere optimale Temperatur
#         - höhere Bekleidung → niedrigere optimale Temperatur
#         """
#         return 22 - (met - 1.2)*2 - (clo - 0.5)*4

#     # Temperatur berechnen
#     df8["optimal_temp"] = df8.apply(lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]), axis=1)

#     # Plot vorbereiten
#     fig, ax = plt.subplots(figsize=(6, 5))

#     scatter = ax.scatter(
#         df8["metabolic_rate"],
#         df8["clothing_ensemble_insulation"],
#         c=df8["optimal_temp"],
#         cmap="coolwarm",
#         s=70,
#         edgecolor="black"
#     )

#     cbar = plt.colorbar(scatter, ax=ax)
#     cbar.set_label("Optimale Raumtemperatur (°C)")

#     ax.set_xlabel("Aktivität (met)")
#     ax.set_ylabel("Bekleidung (clo)")
#     ax.set_title("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung)")

#     ax.grid(True)

#     st.pyplot(fig)

# ######################################################################################################################################
# ######################################################################################################################################


#     st.subheader("Optimale Raumtemperatur nach Aktivität und Bekleidung")
#     # st.text("Diese Abbildung zeigt, wie sich die optimale Raumtemperatur in Abhängigkeit von Aktivitätsniveau (met) und Bekleidungsisolation (clo) verändert. Die Farbskala verdeutlicht die geschätzte Komforttemperatur. Typische Kleidungsetiketten – von kurzärmligen Sommeroutfits bis hin zu Jacken und Wintermänteln – machen sichtbar, dass schwerere Kleidung den Komfortbereich zu niedrigeren Temperaturen verschiebt, während leichtere Kleidung höhere Temperaturen erfordert.")

#     # Asegurar que los campos sean numéricos
#     df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
#     df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

#     df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

#     # Fórmula aproximada ISO 7730 para temperatura óptima
#     def optimal_temp(met, clo):
#         return 22 - (met - 1.2)*2 - (clo - 0.5)*4

#     df8["optimal_temp"] = df8.apply(
#         lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]),axis=1)

#     fig, ax = plt.subplots(figsize=(8, 6))

#     scatter = ax.scatter(
#         df8["metabolic_rate"],
#         df8["clothing_ensemble_insulation"],
#         c=df8["optimal_temp"],
#         cmap="coolwarm",
#         s=80,
#         edgecolor="black"
#     )

#     cbar = plt.colorbar(scatter, ax=ax)
#     cbar.set_label("Optimale operative Temperatur (°C)")

#     ax.set_xlabel("Aktivität (met)")
#     ax.set_ylabel("Bekleidung (clo)")
#     #ax.set_title("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung")
#     ax.grid(True)


#     with st.expander("Optimale Raumtemperatur in Abhängigkeit von Aktivität und Bekleidung - mit Labels"):

#         # Ensure numeric fields
#         df["metabolic_rate"] = pd.to_numeric(df["metabolic_rate"], errors="coerce")
#         df["clothing_ensemble_insulation"] = pd.to_numeric(df["clothing_ensemble_insulation"], errors="coerce")

#         df8 = df.dropna(subset=["metabolic_rate", "clothing_ensemble_insulation"])

#         # Simplified ISO 7730 formula for optimal temperature
#         def optimal_temp(met, clo):
#             return 22 - (met - 1.2)*2 - (clo - 0.5)*4

#         df8["optimal_temp"] = df8.apply(
#             lambda r: optimal_temp(r["metabolic_rate"], r["clothing_ensemble_insulation"]),
#             axis=1)

#         fig, ax = plt.subplots(figsize=(8, 6))

#         scatter = ax.scatter(
#             df8["metabolic_rate"],
#             df8["clothing_ensemble_insulation"],
#             c=df8["optimal_temp"],
#             cmap="coolwarm",
#             s=80,
#             edgecolor="black"
#         )

#         cbar = plt.colorbar(scatter, ax=ax)
#         cbar.set_label("Optimal operative temperature (°C)")
#         ax.set_xlabel("Aktivität (met)")
#         ax.set_ylabel("Bekleidung (clo)")
#         ax.set_title("Optimale Raumtemperatur nach Aktivität und Bekleidung")

#         ax.grid(True)

#         # Clothing labels (example CLO values)
#         clothing_labels = [
#             (1.2, 0.30, "Short sleeves + shorts"),
#             (1.2, 0.50, "T‑shirt + pants"),
#             (1.2, 0.80, "Light jacket"),
#             (1.2, 1.20, "Winter coat"),
#         ]

#         for met, clo, label in clothing_labels:
#             t_opt = optimal_temp(met, clo)
#             ax.scatter(met, clo, c="black", s=40)
#             ax.text(
#                 met + 0.02,
#                 clo + 0.02,
#                 f"{label}\n≈ {t_opt:.1f} °C",
#                 fontsize=9,
#                 color="black",
#                 bbox=dict(facecolor="white", alpha=0.7, edgecolor="gray")
#             )

#         st.pyplot(fig)
#         st.caption("Diese Grafik zeigt, wie sich die optimale Raumtemperatur in Abhängigkeit vom Aktivitätsniveau (met) und der Bekleidungsisolation (clo) verändert." \
#         " Leichte Kleidung wie kurzärmlige Shirts oder Sommeroutfits erfordert eine wärmere Innenraumtemperatur, um thermischen Komfort zu gewährleisten.  " \
#         "Schwerere Kleidung wie leichte Jacken oder Wintermäntel verschiebt den Komfortbereich zu niedrigeren Temperaturen. Die Farbskala zeigt die geschätzte optimale operative Temperatur basierend auf den Prinzipien der ISO 7730.")

    
#     # ============================================================
#     # STATISTICAL MAP: Most Influential CLO Variable per Country
#     # ============================================================

#     st.subheader("Weltkarte – Wichtigste statistische Einflussvariable auf CLO nach Land")

#     import pandas as pd
#     import numpy as np
#     import plotly.express as px
#     from scipy.stats import pearsonr, f_oneway

#     numeric_vars = [
#         "metabolic_rate", "operative_temperature",
#         "air_temperature", "radiant_temperature",
#         "age"
#     ]

#     categorical_vars = [
#         "season", "climate", "gender",
#         "building_type", "cooling_type"
#     ]

#     results = []

#     for country in sorted(df["country"].dropna().unique()):

#         country_df = df[df["country"] == country].dropna(subset=["clothing_ensemble_insulation"])

#         if len(country_df) < 10:
#             results.append({
#                 "country": country,
#                 "top_variable": "Keine Daten",
#                 "effect_strength": 0
#             })
#             continue

#         effects = {}

#         # NUMERIC VARIABLES
#         for var in numeric_vars:
#             if var not in country_df.columns:
#                 effects[var] = 0
#                 continue

#             col_data = pd.to_numeric(country_df[var], errors="coerce").dropna()
#             clo_data = country_df["clothing_ensemble_insulation"].loc[col_data.index]

#             if len(col_data) < 5:
#                 effects[var] = 0
#                 continue

#             try:
#                 corr, _ = pearsonr(col_data, clo_data)
#                 effects[var] = abs(corr)
#             except:
#                 effects[var] = 0

#         # CATEGORICAL VARIABLES
#         for var in categorical_vars:
#             if var not in country_df.columns:
#                 effects[var] = 0
#                 continue

#             try:
#                 groups = [
#                     group["clothing_ensemble_insulation"].values
#                     for _, group in country_df.groupby(var)
#                     if len(group) >= 3
#                 ]
#                 if len(groups) > 1:
#                     f_stat, _ = f_oneway(*groups)
#                     effects[var] = f_stat
#                 else:
#                     effects[var] = 0
#             except:
#                 effects[var] = 0

#         top_var = max(effects, key=effects.get)
#         effect_strength = effects[top_var]

#         results.append({
#             "country": country,
#             "top_variable": top_var,
#             "effect_strength": effect_strength
#         })

#     stat_df = pd.DataFrame(results)

#     unique_vars = stat_df["top_variable"].unique()
#     var_to_code = {v: i for i, v in enumerate(unique_vars)}
#     stat_df["var_code"] = stat_df["top_variable"].map(var_to_code)

#     fig = px.choropleth(
#         stat_df,
#         locations="country",
#         locationmode="country names",
#         color="var_code",
#         hover_name="country",
#         hover_data={
#             "top_variable": True,
#             "effect_strength": True,
#             "var_code": False
#         },
#         color_continuous_scale="Turbo",
#         title="Wichtigste statistische Einflussvariable auf CLO nach Land"
#     )

#     fig.update_layout(
#         title_font_size=22,
#         geo=dict(showframe=False, showcoastlines=True)
#     )

#     st.plotly_chart(fig, use_container_width=True)
#     st.markdown("""
#         Diese Unterschiede sind **normal**:  
#         Jedes Land hat **eigenes Klima**, **eigene Gebäude**, **eigene Kultur** und **eigene Datenverteilung**.  
#         Darum zeigt die Statistik **verschiedene dominante Variablen**.
#         """)

    