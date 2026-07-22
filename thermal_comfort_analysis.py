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


st.title(" 📊 Analyse der Termische Befinden und Einflussgrößen")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab2,tab3 = st.tabs([
    " 📊 Physikalischen und subjektiven Korrelationsanalyse",
    "🏢 Wichtigste Korrelationen & Gebäude-Beispiele"
    ])



# "Subjektiven Komfortvariablen Korrelation",
#     german_labels = {
#     "thermal_sensation": "Thermische Empfinden",
#     "thermal_acceptability": "Thermische Akzeptanz",
#     "thermal_preference": "Thermische Präferenz",
#     "thermal_comfort": "Thermischer Komfort"
# }

#     # st.markdown("""
#     #     ##### 1. Thermische Empfindung (TS) 
#     #     **Kalt  ◄────── Neutral ──────►  Heiß**  
#     #     `-3    -2    -1    0    +1    +2    +3 `

#     #     ##### 2. Thermische Akzeptanz (TA)
#     #     ○ Nicht akzeptabel  
#     #     ○ Akzeptabel  

#     #     ##### 3. Thermische Präferenz (TP)  
#     #     **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
#     #     `  -1                         0                         +1     `

#     #     ##### 4. Thermischer Komfort (TC, ASHRAE‑Skala 1–6)  
#     #     **Sehr unkomfortabel ◄──────────────────────► Sehr komfortabel**  
#     #            `  1             2            3           4           5            6   `
#     #     """)

   
#     st.subheader("Wie hängen die subjektiven Komfortvariablen miteinander zusammen?")

#     st.markdown("""
#     Die subjektiven Komfortvariablen beschreiben, wie Menschen ihre thermische Umgebung wahrnehmen,
#     bewerten und welche Änderungen sie bevorzugen. Die folgende Analyse zeigt, wie stark diese
#     Parameter miteinander korrelieren und welche Muster im thermischen Erleben sichtbar werden.""")
                
#     st.markdown("<br>", unsafe_allow_html=True)

#     col1, spacer, col2 = st.columns([2, 0.5, 2])
#     col3, spacer, col4 = st.columns([2, 0.5, 2])

#     with col1:
#         st.markdown("""
#             ##### 1. Thermischer Komfort 
#         **Sehr unkomfortabel ◄────────────────► Sehr komfortabel**  
#                 `  1          2          3        4         5        6   `
#         """)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col2:
#         st.markdown("""
#         ##### 2. Thermisches Empfinden
#         **Kalt  ◄────── Neutral ──────►  Heiß**  
#         `-3    -2    -1    0    +1    +2    +3 `
#         """)
#         st.markdown("<br>", unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         ##### 3. Thermische Akzeptanz
#         ○ Nicht akzeptabel  
#         ○ Akzeptabel  
#         """)
#         st.markdown("<br>", unsafe_allow_html=True)

#     with col4:
#         st.markdown("""
#         ##### 4. Thermische Präferenz 
#         **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
#         `  -1                    0                   +1     `
#         """)
#         st.markdown("<br><br>", unsafe_allow_html=True)

#     st.markdown("""
#     ### 🔍 Interpretation der Korrelationen

#     - **Positive Werte:** Beide Variablen steigen gemeinsam (z. B. wärmer empfinden → höherer Komfort).  
#     - **Negative Werte:** Die Variablen entwickeln sich gegensätzlich (z. B. wärmer empfinden → geringere Akzeptanz).  
#     - **Nahe 0:** Kein klarer Zusammenhang.

#     Die farbliche Darstellung der Heatmap und der Analysebox rechts hilft, starke Zusammenhänge sofort zu erkennen.
#     """)

#     # Zwei Spalten erstellen
#     col1, col2 = st.columns([1.8, 1])   # linke Spalte etwas breiter für die Heatmap

#     with col1:
#         # Relevante Spalten
#         cols = [
#             "thermal_sensation",
#             "thermal_acceptability",
#             "thermal_preference",
#             "thermal_comfort"
#         ]

#         df_sub = df[cols].copy()

#         # -----------------------------
#         # 1. Numerische Umwandlung
#         # -----------------------------
#         df_sub["thermal_sensation"] = pd.to_numeric(df_sub["thermal_sensation"], errors="coerce")
#         df_sub["thermal_comfort"] = pd.to_numeric(df_sub["thermal_comfort"], errors="coerce")

#         # -----------------------------
#         # 2. thermal_preference → numerisch
#         # -----------------------------
#         mapping_preference = {
#             "warmer": 1,
#             "no change": 0,
#             "cooler": -1
#         }
#         df_sub["thermal_preference"] = df_sub["thermal_preference"].map(mapping_preference)

#         # -----------------------------
#         # 3. thermal_acceptability → numerisch
#         # -----------------------------
#         mapping_acceptability = {
#             "acceptable": 1,
#             "unacceptable": 0,
#             "Unknown": None   # Unknown → NaN
#         }
#         df_sub["thermal_acceptability"] = df_sub["thermal_acceptability"].map(mapping_acceptability)

#         # -----------------------------
#         # 4. Zeilen mit fehlenden Werten entfernen
#         # -----------------------------
#         df_sub = df_sub.dropna()

#         # -----------------------------
#         # 5. Korrelationsmatrix
#         # -----------------------------
#         corr_matrix = df_sub.corr(method="spearman")
#         corr_matrix = corr_matrix.rename(index=german_labels, columns=german_labels)


#             # -----------------------------
#             # 6. Heatmap anzeigen
#             # -----------------------------
#         fig, ax = plt.subplots(figsize=(8, 6))
#         sns.heatmap(
#             corr_matrix,
#             annot=True,
#             cmap="coolwarm",
#             vmin=-1,
#             vmax=1,
#             linewidths=0.5,
#             ax=ax
#         )
#         ax.set_title("Korrelationsmatrix der subjektiven Komfortvariablen")
#         st.pyplot(fig)
#         st.caption(
#         "Diese Korrelationsmatrix zeigt, wie stark die subjektiven Komfortparameter – "
#         "thermische Empfinden, Akzeptanz, Präferenz und Komfortbewertung – miteinander "
#         "verbunden sind.")


# with col2:

#     # --- Werte aus der Matrix ---
#     r_ts_tp = corr_matrix.loc["Thermische Empfinden", "Thermische Präferenz"]
#     r_ts_tc = corr_matrix.loc["Thermische Empfinden", "Thermischer Komfort"]
#     r_tp_tc = corr_matrix.loc["Thermische Präferenz", "Thermischer Komfort"]
#     r_ta_tc = corr_matrix.loc["Thermische Akzeptanz", "Thermischer Komfort"]

#     # --- Farbskala passend zur Heatmap ---
#     def color_for_r(r):
#         if r <= -0.50:
#             return "#005BBB"   # starke negative Korrelation
#         elif r <= -0.15:
#             return "#5F9FE9"   # mittlere negative
#         elif r <= 0.15:
#             return "#E0E0E0"   # neutral
#         elif r < 0.50:
#             return "#F5B97A"   # mittlere positive
#         else:
#             return "#C0392B"   # starke positive

#     c_ts_tp = color_for_r(r_ts_tp)
#     c_ts_tc = color_for_r(r_ts_tc)
#     c_tp_tc = color_for_r(r_tp_tc)
#     c_ta_tc = color_for_r(r_ta_tc)

#     # --- PANEL MIT KURZEN ERKLÄRUNGEN ---
#     st.markdown(f"""
#     <div style="padding-left: 10px; margin-bottom: 18px;">
#         <h5 style="margin:0;">Empfinden ↔ Präferenz  
#         <span style="color:{c_ts_tp}; font-weight:bold;">(r = {r_ts_tp:.2f})</span></h5>
#         <p style="margin:4px 0;">
#         Wärmeres Empfinden führt typischerweise zu einer stärkeren Präferenz für kühlere Bedingungen.
#         </p>
#     </div>

#     <div style="padding-left: 10px; margin-bottom: 18px;">
#         <h5 style="margin:0;">Empfinden ↔ Komfort  
#         <span style="color:{c_ts_tc}; font-weight:bold;">(r = {r_ts_tc:.2f})</span></h5>
#         <p style="margin:4px 0;">
#         Das thermische Empfinden beeinflusst die Komfortbewertung leicht, jedoch nicht stark.
#         </p>
#     </div>

#     <div style="padding-left: 10px; margin-bottom: 18px;">
#         <h5 style="margin:0;">Präferenz ↔ Komfort  
#         <span style="color:{c_tp_tc}; font-weight:bold;">(r = {r_tp_tc:.2f})</span></h5>
#         <p style="margin:4px 0;">
#         Der Wunsch nach Veränderung steht im Zusammenhang mit der empfundenen Komfortqualität.
#         </p>
#     </div>

#     <div style="padding-left: 10px; margin-bottom: 18px;">
#         <h5 style="margin:0;">Akzeptanz ↔ Komfort  
#         <span style="color:{c_ta_tc}; font-weight:bold;">(r = {r_ta_tc:.2f})</span></h5>
#         <p style="margin:4px 0;">
#         Akzeptable Bedingungen werden im Durchschnitt als komfortabler bewertet.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)


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
    
    # st.subheader("📊 Analyse der physikalischen und subjektiven Einflussgrößen auf den thermischen KomfortBefinden")

    # st.markdown("""
    # Diese Analyse kombiniert **physikalische Messgrößen** und **subjektive Wahrnehmungen**, um ein vollständiges Bild darüber zu erhalten, wie Menschen thermische Bedingungen erleben und welche Faktoren den Komfort am stärksten beeinflussen.
 
    # """, unsafe_allow_html=True)

    # col1, col2 = st.columns(2)

    # with col1:
    #     st.markdown("""
    #     #### 🔥 Physikalische Einflussgrößen

    #     Die objektiven Parameter bestimmen die tatsächliche Wärmebilanz des Körpers:

    #     - 🔥 **Metabolische Aktivität**
    #     - 👕 **Bekleidungsisolation**
    #     - 🌡️ **Lufttemperatur**
    #     - 💨 **Luftgeschwindigkeit**
    #     - ☀️ **Strahlungstemperatur**
    #     - 💧 **Relative Luftfeuchtigkeit**

    #     Diese Variablen beeinflussen direkt die Wärmeabgabe und ‑aufnahme des Körpers und bilden die Grundlage für die physikalische Bewertung des thermischen Komforts.
    #     """)

    # with col2:
    #     st.markdown("""
    #     #### 🙂 Subjektive Einflussgrößen

    #     Diese Variablen beschreiben die individuelle Wahrnehmung und Bewertung der Umgebung:

    #     - 🙂 **Thermisches Empfinden**
    #     - ✔️ **Thermische Akzeptanz**
    #     - 🔄 **Thermische Präferenz**
    #     - 😌 **Thermischer Komfort**

    #     Sie spiegeln wider, wie Personen die physikalischen Bedingungen erleben und ob sie diese als angenehm, akzeptabel oder veränderungsbedürftig empfinden.
    #     """)

    # st.markdown("""
    # Diese kombinierte Analyse ermöglicht ein tiefes Verständnis darüber, **welche physikalischen Faktoren die subjektive Wahrnehmung dominieren** und wie beide Bereiche zusammenwirken, um den thermischen Komfort zu bestimmen.
    # """)

    st.subheader("📊 Physikalische und subjektive Einflussgrößen des thermischen Befinden")

    st.markdown("""
    Diese Analyse kombiniert **physikalische Messgrößen** und **subjektive Wahrnehmungen**, um ein vollständiges Bild darüber zu erhalten, wie Menschen thermische Bedingungen erleben und welche Faktoren den Komfort am stärksten beeinflussen.
 
    """, unsafe_allow_html=True)

    # Zwei Spalten
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="
            background-color:#e6f2ff;
            padding:15px;
            border-radius:8px;
            font-size:16px;
            line-height:1.55;
        ">
        <h4>🔥 Physikalische Einflussgrößen</h3>

        Diese Variablen beeinflussen direkt die Wärmeabgabe und ‑aufnahme des Körpers 
        und bilden die Grundlage für die physikalische Bewertung des thermischen Komforts.

        <ul>
            <li>🔥 <b>Metabolische Aktivität</b></li> 
            <li>👕 <b>Bekleidungsisolation</b></li>
            <li>🌡️ <b>Lufttemperatur</b></li>
            <li>💨 <b>Luftgeschwindigkeit</b></li>
            <li>☀️ <b>Strahlungstemperatur</b></li>
            <li>💧 <b>Relative Luftfeuchtigkeit</b></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="
            background-color:#e6f2ff;
            padding:15px;
            border-radius:8px;
            font-size:16px;
            line-height:1.55;
        ">
        <h4>🙂 Subjektive Einflussgrößen</h3>

        Diese Variablen beschreiben die individuelle Wahrnehmung und Bewertung der Umgebung 
        und zeigen, wie Menschen die physikalischen Bedingungen tatsächlich erleben.

        <ul>
            <li>🙂 <b>Thermisches Empfinden: </b> Kalt ◄── Neutral ──► Heiß</li>
            <li>✔️ <b>Thermische Akzeptanz: </b> Nicht akzeptabel / Akzeptabel</li>
            <li>🔄 <b>Thermische Präferenz: </b> Kühler ◄── Keine Änderung ──► Wärmer</li>
            <li>😌 <b>Thermischer Komfort: </b> Sehr unkomfortabel ◄──► Sehr komfortabel </li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


    # # ============================================================
    # # 1. Physikalische Variablen auswählen
    # # ============================================================

    # cols_phys = [
    #     "metabolic_rate",
    #     "clothing_ensemble_insulation",
    #     "air_temperature",
    #     "air_speed",
    #     "radiant_temperature",
    #     "relative_humidity"
    # ]

    # # Deutsche Labels für die Darstellung
    # german_phys_labels = {
    #     "metabolic_rate": "Metabolische Aktivität",
    #     "clothing_ensemble_insulation": "Bekleidungsisolation",
    #     "air_temperature": "Lufttemperatur",
    #     "air_speed": "Luftgeschwindigkeit",
    #     "radiant_temperature": "Strahlungstemperatur",
    #     "relative_humidity": "Relative Luftfeuchtigkeit"
    # }

    # # Zwei Spalten erstellen
    # col01, col02 = st.columns([1.8, 1])


    # # ============================================================
    # # 2. Heatmap links
    # # ============================================================
    # with col01:

    #     df_phys = df[cols_phys].copy()

    #     # Numerische Umwandlung (NICHT verändert)
    #     for c in cols_phys:
    #         df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

    #     df_phys = df_phys.dropna()

    #     # Korrelation berechnen (NICHT verändert)
    #     corr_matrix = df_phys.corr(method="spearman")

    #     # Deutsche Labels anwenden
    #     corr_matrix = corr_matrix.rename(index=german_phys_labels, columns=german_phys_labels)

    #     # Heatmap
    #     fig, ax = plt.subplots(figsize=(8, 5))
    #     ax.set_title("Korrelationsmatrix der physikalischen Komfortvariablen")

    #     sns.heatmap(
    #         corr_matrix,
    #         annot=True,
    #         cmap="coolwarm",
    #         vmin=-1,
    #         vmax=1,
    #         linewidths=0.5,
    #         ax=ax
    #     )
    #     st.pyplot(fig)


    # # ============================================================
    # # 3. Interpretationspanel rechts
    # # ============================================================
    # with col02:

    #     st.markdown("#### 🔥 Wichtigste physikalische Zusammenhänge")

    #     # Werte extrahieren (jetzt mit deutschen Labels)
    #     r_ta_tr  = corr_matrix.loc["Lufttemperatur", "Strahlungstemperatur"]
    #     r_clo_tr = corr_matrix.loc["Bekleidungsisolation", "Strahlungstemperatur"]

    #     # Farbskala passend zur Heatmap
    #     def color_for_r(r):
    #         if r >= 0.75:
    #             return "#C0392B"   # starke positive
    #         elif r >= 0.40:
    #             return "#E67E22"   # mittlere positive
    #         elif r >= 0.15:
    #             return "#F1C40F"   # leichte positive
    #         elif r <= -0.75:
    #             return "#005BBB"   # starke negative
    #         elif r <= -0.40:
    #             return "#5F9FE9"   # mittlere negative
    #         elif r <= -0.15:
    #             return "#A9CCE3"   # leichte negative
    #         else:
    #             return "#D5D8DC"   # neutral

    #     c_ta_tr  = color_for_r(r_ta_tr)
    #     c_clo_tr = color_for_r(r_clo_tr)

    #     # Panel
    #     st.markdown(f"""
    #     <div style="font-size:16px; line-height:1.55; padding-left:6px;">

    #     <h5 style="margin-bottom:4px;">🌡️ Lufttemperatur ↔ Strahlungstemperatur  
    #     <span style="color:{c_ta_tr}; font-weight:bold;">(r = {r_ta_tr:.2f})</span></h5>
    #     • Sehr starke positive Korrelation  
    #     • Beide Temperaturen steigen und fallen gemeinsam  
    #     • Deshalb beeinflussen sie die operative Temperatur nahezu identisch  
    #     <br><br>

    #     <h5 style="margin-bottom:4px;">👕 Bekleidungsisolation ↔ Strahlungstemperatur  
    #     <span style="color:{c_clo_tr}; font-weight:bold;">(r = {r_clo_tr:.2f})</span></h5>
    #     • Mittlere negative Korrelation  
    #     • Sinkt die Strahlungstemperatur, wird häufig mehr Kleidung getragen  
    #     • Menschen kompensieren kühlere Oberflächen durch höhere Isolation 
        
         

    #     </div>
    #     """, unsafe_allow_html=True)


    # # ============================================================
    # # 4. Expander – Erklärung
    # # ============================================================
    # with st.expander("📘 Erklärung der wichtigsten Zusammenhänge"):

    #     st.markdown("### 🔥 Wissenschaftliche Interpretation der physikalischen Zusammenhänge")

    #     # Farbskala passend zur Heatmap
    #     def color_for_r(r):
    #         if r >= 0.75:
    #             return "#C0392B"   # starke positive
    #         elif r >= 0.40:
    #             return "#E67E22"   # mittlere positive
    #         elif r >= 0.15:
    #             return "#F1C40F"   # leichte positive
    #         elif r <= -0.75:
    #             return "#005BBB"   # starke negative
    #         elif r <= -0.40:
    #             return "#5F9FE9"   # mittlere negative
    #         elif r <= -0.15:
    #             return "#A9CCE3"   # leichte negative
    #         else:
    #             return "#D5D8DC"   # neutral

    #     # Schwellenwerte für wissenschaftlich relevante Korrelationen
    #     THRESHOLD_POS = 0.15     # leichte positive Korrelation
    #     THRESHOLD_NEG = -0.15    # leichte negative Korrelation

    #     # Wissenschaftliche Erklärungstexte
    #     def explain(var1, var2, r):
    #         color = color_for_r(r)

    #         # Stärke klassifizieren
    #         if r >= 0.75:
    #             strength = "Sehr starke positive Korrelation"
    #             mechanism = (
    #                 "Die beiden Größen zeigen nahezu identische thermische Dynamiken. "
    #                 "Dies weist auf eine direkte physikalische Kopplung oder gemeinsame "
    #                 "Einflussfaktoren hin."
    #             )
    #         elif r >= 0.40:
    #             strength = "Mittlere positive Korrelation"
    #             mechanism = (
    #                 "Die Variablen steigen und fallen gemeinsam, was auf einen "
    #                 "substanziellen thermischen Zusammenhang hindeutet."
    #             )
    #         elif r >= 0.15:
    #             strength = "Leichte positive Korrelation"
    #             mechanism = (
    #                 "Ein moderater Gleichlauf der Variablen deutet auf indirekte "
    #                 "thermische Wechselwirkungen oder gemeinsame Randbedingungen hin."
    #             )
    #         elif r <= -0.75:
    #             strength = "Sehr starke negative Korrelation"
    #             mechanism = (
    #                 "Die Variablen entwickeln sich stark gegensätzlich. Dies spricht "
    #                 "für kompensatorische thermische Mechanismen oder gegenläufige "
    #                 "physikalische Effekte."
    #             )
    #         elif r <= -0.40:
    #             strength = "Mittlere negative Korrelation"
    #             mechanism = (
    #                 "Die Variablen zeigen gegenläufige Trends, was auf thermische "
    #                 "Kompensation oder unterschiedliche physikalische Rollen hinweist."
    #             )
    #         elif r <= -0.15:
    #             strength = "Leichte negative Korrelation"
    #             mechanism = (
    #                 "Ein moderater gegenläufiger Verlauf deutet auf subtile "
    #                 "thermische Ausgleichsmechanismen hin."
    #             )
    #         else:
    #             return None

    #         return f"""
    #         <div style="font-size:16px; line-height:1.55; padding-left:6px;">
    #             <h5 style="margin-bottom:4px;">{var1} ↔ {var2}  
    #             <span style="color:{color}; font-weight:bold;">(r = {r:.2f})</span></h5>
    #             • {strength}<br>
    #             • {mechanism}<br>
    #         </div>
    #         """

    #     # Alle Paare durchgehen
    #     vars_list = corr_matrix.columns.tolist()
    #     explanations = []

    #     for i in range(len(vars_list)):
    #         for j in range(i + 1, len(vars_list)):
    #             var1 = vars_list[i]
    #             var2 = vars_list[j]
    #             r = corr_matrix.loc[var1, var2]

    #             block = explain(var1, var2, r)
    #             if block:
    #                 explanations.append((abs(r), block))

    #     # Sortieren nach Stärke der Korrelation
    #     explanations.sort(reverse=True, key=lambda x: x[0])

    #     # Ausgabe
    #     if explanations:
    #         for _, block in explanations:
    #             st.markdown(block, unsafe_allow_html=True)
    #             st.markdown("<br>", unsafe_allow_html=True)
    #     else:
    #         st.markdown("Keine wissenschaftlich relevanten Zusammenhänge gefunden.")



    col_left, col_right = st.columns([2, 1])

    with col_left:

        #st.subheader("📊 Physikalische und subjektive Einflussgrößen des thermischen Komforts")

        # -----------------------------------------------------------
        # 1. Variablen definieren
        # -----------------------------------------------------------
        cols_phys = [
            "metabolic_rate",
            "clothing_ensemble_insulation",
            "air_temperature",
            "air_speed",
            "radiant_temperature",
            "relative_humidity"
        ]

        cols_subj = [
            "thermal_sensation",
            "thermal_acceptability",
            "thermal_preference",
            "thermal_comfort"
        ]

        cols_all = cols_phys + cols_subj

        # -----------------------------------------------------------
        # 2. Kategorische Variablen in Zahlen umwandeln
        # -----------------------------------------------------------

        mapping_acceptability = {
            "acceptable": 1,
            "unacceptable": 0,
            "Unknown": None
        }

        mapping_preference = {
            "cooler": -1,
            "no change": 0,
            "warmer": 1,
            "Unknown": None
        }

        df["thermal_acceptability_num"] = df["thermal_acceptability"].map(mapping_acceptability)
        df["thermal_preference_num"] = df["thermal_preference"].map(mapping_preference)

        # ersetzen die alten Spalten durch die numerischen
        df["thermal_acceptability"] = df["thermal_acceptability_num"]
        df["thermal_preference"] = df["thermal_preference_num"]

        # -----------------------------------------------------------
        # 3. Heatmap erstellen
        # -----------------------------------------------------------

        df_all = df[cols_all].copy()

        # numerisch machen
        for c in cols_all:
            df_all[c] = pd.to_numeric(df_all[c], errors="coerce")

        # Zeilen entfernen, die komplett leer sind
        df_all = df_all.dropna(how="all")

        if df_all.empty:
            st.error("❌ Keine gültigen Daten für die Korrelationsmatrix.")
        else:
            corr_matrix = df_all.corr(method="spearman")

            # deutsche Labels
            german_all_labels = {
                "metabolic_rate": "Metabolische Aktivität",
                "clothing_ensemble_insulation": "Bekleidungsisolation",
                "air_temperature": "Lufttemperatur",
                "air_speed": "Luftgeschwindigkeit",
                "radiant_temperature": "Strahlungstemperatur",
                "relative_humidity": "Relative Luftfeuchtigkeit",
                "thermal_sensation": "Thermisches Empfinden",
                "thermal_acceptability": "Thermische Akzeptanz",
                "thermal_preference": "Thermische Präferenz",
                "thermal_comfort": "Thermischer Komfort"
            }

            corr_matrix = corr_matrix.rename(index=german_all_labels, columns=german_all_labels)

            fig, ax = plt.subplots(figsize=(10, 7))
            ax.set_title("Korrelationsmatrix: Physikalische & subjektive Komfortvariablen")

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

    with col_right:
        st.markdown("""
        <div style="
            font-size:16px;
            line-height:1.55;
        ">

        <h4 style="margin-top:0;">📌 Wichtigste Ergebnisse</h3>

        <p><b>🌡️ Lufttemperatur → Strahlungstemperatur</b><br>
        <b>r = 0.89</b><br>
        Sehr starke positive Beziehung – beide steigen gemeinsam.</p>

        <hr>

        <p><b>😊 Thermisches Empfinden → ❄️ Thermische Präferenz</b><br>
        <b>r = -0.67</b><br>
        Je wärmer empfunden, desto stärker der Wunsch nach kühleren Bedingungen.</p>

        <hr>

        <p><b>👕 Bekleidungsisolation</b><br>
        <b>r = -0.46</b> zur Lufttemperatur<br>
        <b>r = -0.45</b> zur Strahlungstemperatur<br>
        Höhere Temperaturen → leichtere Kleidung.</p>

        </div>
        """, unsafe_allow_html=True)





    # ============================================================
    # Variablengruppen für Interpretation
    # ============================================================

    phys_vars = [
        "Metabolische Aktivität",
        "Bekleidungsisolation",
        "Lufttemperatur",
        "Luftgeschwindigkeit",
        "Strahlungstemperatur",
        "Relative Luftfeuchtigkeit"
    ]

    subj_vars = [
        "Thermisches Empfinden",
        "Thermische Akzeptanz",
        "Thermische Präferenz",
        "Thermischer Komfort"
    ]

    # ============================================================
    # Interpretationsfunktion
    # ============================================================

    def interpret(corr):
        if corr > 0.6:
            return "sehr starke positive Beziehung 🔥"
        elif corr > 0.3:
            return "moderate positive Beziehung 🙂"
        elif corr > 0.1:
            return "schwache positive Beziehung ➕"
        elif corr < -0.6:
            return "sehr starke negative Beziehung ❄️"
        elif corr < -0.3:
            return "moderate negative Beziehung 😕"
        elif corr < -0.1:
            return "schwache negative Beziehung ➖"
        else:
            return "nahezu kein Zusammenhang ⚪"


    # ============================================================
    # Korrelationen in lange Form bringen + sortieren
    # ============================================================

    corr_long = corr_matrix.stack().reset_index()
    corr_long.columns = ["Variable 1", "Variable 2", "Korrelation"]

    # Selbstkorrelationen entfernen
    corr_long = corr_long[corr_long["Variable 1"] != corr_long["Variable 2"]]

    # Doppelte Paare entfernen (A-B und B-A)
    corr_long["pair"] = corr_long.apply(
        lambda row: tuple(sorted([row["Variable 1"], row["Variable 2"]])),
        axis=1
    )
    corr_long = corr_long.drop_duplicates(subset="pair")

    # Sortieren nach Stärke (absoluter Wert)
    corr_sorted = corr_long.sort_values(
        by="Korrelation",
        key=lambda x: abs(x),
        ascending=False
    )




    # ============================================================
    # EXPANDER 1 — Physikalische Zusammenhänge
    # ============================================================

    with st.expander("🌡️ Physikalische Zusammenhänge"):
        phys_corr = corr_sorted[
            corr_sorted["Variable 1"].isin(phys_vars) &
            corr_sorted["Variable 2"].isin(phys_vars)
        ]

        if phys_corr.empty:
            st.write("Keine physikalischen Zusammenhänge gefunden.")
        else:
            for _, row in phys_corr.iterrows():
                st.markdown(
                    f"- **{row['Variable 1']} ↔ {row['Variable 2']}**: "
                    f"{interpret(row['Korrelation'])} "
                    f"(ρ = {row['Korrelation']:.2f})"
                )

    # ============================================================
    # EXPANDER 2 — Subjektive Zusammenhänge
    # ============================================================

    with st.expander("🙂 Subjektive Zusammenhänge"):
        subj_corr = corr_sorted[
            corr_sorted["Variable 1"].isin(subj_vars) &
            corr_sorted["Variable 2"].isin(subj_vars)
        ]

        if subj_corr.empty:
            st.write("Keine subjektiven Zusammenhänge gefunden.")
        else:
            for _, row in subj_corr.iterrows():
                st.markdown(
                    f"- **{row['Variable 1']} ↔ {row['Variable 2']}**: "
                    f"{interpret(row['Korrelation'])} "
                    f"(ρ = {row['Korrelation']:.2f})"
                )

    # ============================================================
    # EXPANDER 3 — Physikalisch ↔ Subjektiv (Cross-Korrelationen)
    # ============================================================

    with st.expander("🔄 Physikalisch ↔ Subjektiv"):
        cross_corr = corr_sorted[
            (corr_sorted["Variable 1"].isin(phys_vars) & corr_sorted["Variable 2"].isin(subj_vars)) |
            (corr_sorted["Variable 1"].isin(subj_vars) & corr_sorted["Variable 2"].isin(phys_vars))
        ]

        if cross_corr.empty:
            st.write("Keine Beziehungen zwischen physikalischen und subjektiven Variablen gefunden.")
        else:
            for _, row in cross_corr.iterrows():
                st.markdown(
                    f"- **{row['Variable 1']} ↔ {row['Variable 2']}**: "
                    f"{interpret(row['Korrelation'])} "
                    f"(ρ = {row['Korrelation']:.2f})"
                )

    # ============================================================
# 3×3 PLOT: Die 9 wichtigsten Zusammenhänge
# ============================================================
    with st.expander("📈 Die 9 wichtigsten Zusammenhänge "):
        
        st.subheader("📈 Die 9 wichtigsten Zusammenhänge ")

        # Mapping Deutsch → Englisch
        german_to_english = {
            "Metabolische Aktivität": "metabolic_rate",
            "Bekleidungsisolation": "clothing_ensemble_insulation",
            "Lufttemperatur": "air_temperature",
            "Luftgeschwindigkeit": "air_speed",
            "Strahlungstemperatur": "radiant_temperature",
            "Relative Luftfeuchtigkeit": "relative_humidity",
            "Thermisches Empfinden": "thermal_sensation",
            "Thermische Akzeptanz": "thermal_acceptability",
            "Thermische Präferenz": "thermal_preference",
            "Thermischer Komfort": "thermal_comfort"
        }

        # Hilfsfunktion für Scatterplot
        def scatter(ax, df, var1_en, var2_en, var1_de, var2_de, corr):
            sns.regplot(
                data=df,
                x=var1_en,
                y=var2_en,
                ax=ax,
                scatter_kws={"alpha": 0.4},
                line_kws={"color": "red", "linewidth": 2}
            )
            ax.set_xlabel(var1_de)
            ax.set_ylabel(var2_de)
            ax.set_title(f"{var1_de} ↔ {var2_de}\nρ = {corr:.2f}")

        # ------------------------------------------------------------
        # 1. Top 3 physikalische Beziehungen
        # ------------------------------------------------------------
        phys_top3 = corr_sorted[
            corr_sorted["Variable 1"].isin(phys_vars) &
            corr_sorted["Variable 2"].isin(phys_vars)
        ].head(3)

        # ------------------------------------------------------------
        # 2. Top 3 subjektive Beziehungen
        # ------------------------------------------------------------
        subj_top3 = corr_sorted[
            corr_sorted["Variable 1"].isin(subj_vars) &
            corr_sorted["Variable 2"].isin(subj_vars)
        ].head(3)

        # ------------------------------------------------------------
        # 3. Top 3 Cross-Beziehungen
        # ------------------------------------------------------------
        cross_top3 = corr_sorted[
            (corr_sorted["Variable 1"].isin(phys_vars) & corr_sorted["Variable 2"].isin(subj_vars)) |
            (corr_sorted["Variable 1"].isin(subj_vars) & corr_sorted["Variable 2"].isin(phys_vars))
        ].head(3)

        # ------------------------------------------------------------
        # 3×3 Figur erstellen
        # ------------------------------------------------------------

        fig, axes = plt.subplots(3, 3, figsize=(18, 15))

        # -------------------------
        # Zeile 1: Physikalisch
        # -------------------------
        for i, (_, row) in enumerate(phys_top3.iterrows()):
            var1_de = row["Variable 1"]
            var2_de = row["Variable 2"]
            var1_en = german_to_english[var1_de]
            var2_en = german_to_english[var2_de]
            scatter(axes[0, i], df_all, var1_en, var2_en, var1_de, var2_de, row["Korrelation"])

        # -------------------------
        # Zeile 2: Subjektiv
        # -------------------------
        for i, (_, row) in enumerate(subj_top3.iterrows()):
            var1_de = row["Variable 1"]
            var2_de = row["Variable 2"]
            var1_en = german_to_english[var1_de]
            var2_en = german_to_english[var2_de]
            scatter(axes[1, i], df_all, var1_en, var2_en, var1_de, var2_de, row["Korrelation"])

        # -------------------------
        # Zeile 3: Cross
        # -------------------------
        for i, (_, row) in enumerate(cross_top3.iterrows()):
            var1_de = row["Variable 1"]
            var2_de = row["Variable 2"]
            var1_en = german_to_english[var1_de]
            var2_en = german_to_english[var2_de]
            scatter(axes[2, i], df_all, var1_en, var2_en, var1_de, var2_de, row["Korrelation"])

        plt.tight_layout()
        st.pyplot(fig)



with tab3:
    
    st.subheader("🏠 Wichtigste Korrelationen mit Gebäude-Beispielen")


    st.markdown("""
    Diese Übersicht zeigt, wie physikalische Komfortparameter – wie Lufttemperatur,
    Strahlungstemperatur und Bekleidungsisolation – mit dem Verhalten und Empfinden
    von Personen in verschiedenen Gebäudetypen zusammenhängen.

    """)


    st.image("komfort_erklarung2.png", width=1200)

    # with st.expander("📌 Wichtigste Korrelationen mit Gebäude-Beispielen"):

    #     data = {
    #         "Korrelation": [
    #             "🌡️ Lufttemperatur ↔ Strahlungstemperatur (r = 0,89)",
    #             "😊 Thermisches Empfinden ↔ Thermische Präferenz (r = -0,67)",
    #             "👕 Bekleidungsisolation ↔ Lufttemperatur (r = -0,46)",
    #             "👕 Bekleidungsisolation ↔ Strahlungstemperatur (r = -0,45)",
    #             "❄️ Lufttemperatur ↔ Thermische Präferenz (r = -0,44)",
    #             "☀️ Strahlungstemperatur ↔ Thermische Präferenz (r = -0,41)"
    #         ],
    #         "Erklärung": [
    #             "Beide Temperaturen steigen gemeinsam an.",
    #             "Je wärmer sich Personen fühlen, desto stärker bevorzugen sie kühlere Bedingungen.",
    #             "Mit steigender Lufttemperatur wird leichtere Kleidung getragen.",
    #             "Höhere Strahlungswärme führt zu geringerer Bekleidungsisolation.",
    #             "Mit steigender Temperatur wünschen sich die Nutzer kühlere Bedingungen.",
    #             "Warme Oberflächen erhöhen den Wunsch nach einer kühleren Umgebung."
    #         ],
    #         "Gebäudetyp": [
    #             "🏢 Bürogebäude mit großen Glasfassaden oder Klassenräume mit hoher Sonneneinstrahlung.",
    #             "👴 Seniorenzentrum oder 👩‍🏫 Klassenraum, in denen viele Personen gleichzeitig den Raum nutzen.",
    #             "🏠 Mehrfamilienhaus im Sommer oder 🏢 Bürogebäude mit natürlicher Lüftung.",
    #             "🏢 Bürogebäude mit Glasfassade oder ☀️ Klassenraum auf der Südseite.",
    #             "👩‍🏫 Klassenräume ohne Klimaanlage oder 👴 Seniorenzentren während warmer Sommertage.",
    #             "🏠 Mehrfamilienhäuser mit großen Fenstern oder 🏢 Büros mit direkter Sonneneinstrahlung."
    #         ]
    #     }

    #     df_data = pd.DataFrame(data)

    #     with st.expander("📌 Wichtigste Korrelationen mit Gebäude-Beispielen"):
    #         st.table(df_data)


