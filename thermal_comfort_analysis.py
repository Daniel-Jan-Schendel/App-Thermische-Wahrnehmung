import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from tabulate import tabulate
from PIL import Image



st.set_page_config(page_title="Globale Datenanalyse", layout="wide", initial_sidebar_state="expanded")
  
# ---------------------------------------------------------
# Daten laden
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("db_bereinigt_fertig.csv")
df = load_data()

st.title("Analyse der Komfortparameter")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab0, tab1, tab2, tab3, tab4 = st.tabs([
    "Komfortvariablen Korrelation",
    "MTS vs Indoor Temperature",
    "Einfluss der Kleidung auf die Komforttemperatur",
    "Adaptives Komfortmodell",
    "Korrelationsanalyse"])

with tab0:

    st.subheader("Wie hängen die subjektiven Komfortvariablen miteinander zusammen?")
    st.markdown("""
        Die subjektiven Komfortvariablen beschreiben, wie Menschen ihre thermische Umgebung wahrnehmen,
        bewerten und welche Änderungen sie sich wünschen.
        """, unsafe_allow_html=True)

    # colA, colB, colC, colD = st.columns(4)

    # # ---- ESTILOS ----
    # st.markdown("""
    # <style>
    #     .vcard {
    #         background-color: #ffffff;
    #         padding: 14px;
    #         border-radius: 12px;
    #         margin-bottom: 14px;
    #         box-shadow: 0px 2px 6px rgba(0,0,0,0.12);
    #         transition: transform 0.2s ease, box-shadow 0.2s ease;
    #     }
    #     .vcard:hover {
    #         transform: translateY(-4px);
    #         box-shadow: 0px 4px 12px rgba(0,0,0,0.18);
    #     }
    #     .vtitle {
    #         font-size: 18px;
    #         font-weight: bold;
    #         margin-bottom: 8px;
    #         text-align: center;
    #     }
    #     .vicons {
    #         text-align: center;
    #         font-size: 22px;
    #         margin-bottom: 6px;
    #     }
    #     .vbar {
    #         height: 14px;
    #         border-radius: 6px;
    #         margin: 8px auto;
    #         width: 90%;
    #         background: linear-gradient(to right, #005bbb, #7f8c8d, #c0392b);
    #     }
    #     .vscale-flex {
    #         display: flex;
    #         justify-content: space-between;
    #         font-size: 14px;
    #         font-weight: bold;
    #         margin: 6px 0;
    #         padding: 0 6px;
    #     }
    #     .vtext {
    #         font-size: 14px;
    #         text-align: left;
    #         line-height: 1.3;
    #     }
    # </style>
    # """, unsafe_allow_html=True)

    # # ---- TSV ----
    # with colA:
    #     st.markdown("""
    #     <div class="vcard">
    #         <div class="vtitle">THERMAL SENSATION (TSV)</div>
    #         <div class="vicons">❄️ ◄──── ☁️ ────► ☀️</div>

    #         <div class="vscale-flex">
    #             <span>-3</span><span>-2</span><span>-1</span>
    #             <span>0</span>
    #             <span>+1</span><span>+2</span><span>+3</span>
    #         </div>

    #         <div class="vtext">
    #             <b>-3:</b> Sehr kalt<br>
    #             <b>-2:</b> Kalt<br>
    #             <b>-1:</b> Kühl<br>
    #             <b>0:</b> Neutral<br>
    #             <b>+1:</b> Warm<br>
    #             <b>+2:</b> Heiß<br>
    #             <b>+3:</b> Sehr heiß
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)

    # # ---- TP ----
    # with colB:
    #     st.markdown("""
    #     <div class="vcard">
    #         <div class="vtitle">THERMAL PREFERENCE (TP)</div>
    #         <div class="vicons">⬅️ Kühler &nbsp;&nbsp; ⏺️ Neutral &nbsp;&nbsp; ➡️ Wärmer</div>

    #         <!-- SOLO ESTA BARRA DE COLORES -->
    #         <div class="vbar"></div>

    #         <div class="vscale-flex">
    #             <span>-1</span><span>0</span><span>+1</span>
    #         </div>

    #         <div class="vtext">
    #             <b>-1:</b> Kühler bevorzugt<br>
    #             <b>0:</b> Keine Präferenz / Neutral<br>
    #             <b>+1:</b> Wärmer bevorzugt
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)

    # # ---- TC ----
    # with colC:
    #     st.markdown("""
    #     <div class="vcard">
    #         <div class="vtitle">THERMAL COMFORT (TC)</div>
    #         <div class="vicons">😣 ◄──────────────► 😌</div>

    #         <div class="vscale-flex">
    #             <span>1</span><span>2</span><span>3</span>
    #             <span>4</span><span>5</span><span>6</span>
    #         </div>

    #         <div class="vtext">
    #             <b>1:</b> Ungemütlich<br>
    #             <b>2:</b> Leicht ungemütlich<br>
    #             <b>3:</b> Akzeptabel / Neutral<br>
    #             <b>4:</b> Gemütlich<br>
    #             <b>5:</b> Sehr gemütlich<br>
    #             <b>6:</b> Extrem gemütlich
    #         </div>
    #     </div>""", unsafe_allow_html=True)

    # # ---- TA ----
    # with colD:
    #     st.markdown("""
    #     <div class="vcard">
    #         <div class="vtitle">THERMISCHE AKZEPTANZ (TA)</div>
    #         <div class="vicons">✔️ Akzeptabel &nbsp;&nbsp; ✖️ Nicht akzeptabel</div>

    #         <div class="vtext">
    #             ● Akzeptabel<br>
    #             ○ Nicht akzeptabel
    #         </div>
    #     </div>
    #     """, unsafe_allow_html=True)

    st.markdown("""
        ##### 1. Thermische Empfindung (TS) 
        **Kalt  ◄────── Neutral ──────►  Heiß**  
        `-3    -2    -1    0    +1    +2    +3 `

        ##### 2. Thermische Akzeptanz (TA)
        ○ Nicht akzeptabel  
        ○ Akzeptabel  

        ##### 3. Thermische Präferenz (TP)  
        **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
        `  -1                         0                         +1     `

        ##### 4. Thermischer Komfort (TC, ASHRAE‑Skala 1–6)  
        **Sehr unkomfortabel ◄──────────────────────► Sehr komfortabel**  
               `  1             2            3           4           5            6   `
        """)

   
    # Zwei Spalten erstellen
    col1, col2 = st.columns([1.5, 1])   # linke Spalte etwas breiter für die Heatmap

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
        "thermische Empfindung, Akzeptanz, Präferenz und Komfortbewertung – miteinander "
        "verbunden sind. Positive Werte (+): Die Variablen bewegen sich tendenziell gemeinsam. " 
        "Negative Werte (-): Die Variablen verhalten sich gegensätzlich.")
    

    # ---------------------------------------------------------
    # Rechte Spalte: Automatische Interpretation
    # ---------------------------------------------------------
    with col2:

        # # --- Werte aus deiner Korrelationsmatrix ---
        # r_ts_tp = corr_matrix.loc["thermal_sensation", "thermal_preference"]
        # r_ts_tc = corr_matrix.loc["thermal_sensation", "thermal_comfort"]
        # r_tp_tc = corr_matrix.loc["thermal_preference", "thermal_comfort"]

        # # --- Farblogik basierend auf Heatmap ---
        # def color_for_r(r):
        #     if r <= -0.50:
        #         return "#005BBB"   # starke negative Korrelation (blau)
        #     elif r <= -0.20:
        #         return "#4A90E2"   # mittlere negative Korrelation
        #     elif r < 0.20:
        #         return "#7F8C8D"   # schwach (grau)
        #     elif r < 0.50:
        #         return "#D1A986"   # mittlere positive Korrelation (orange)
        #     else:
        #         return "#C0392B"   # starke positive Korrelation (rot)

        # c_ts_tp = color_for_r(r_ts_tp)
        # c_ts_tc = color_for_r(r_ts_tc)
        # c_tp_tc = color_for_r(r_tp_tc)

        # # --- PANEL AUTOMÁTICO ---
        # st.markdown(f"""
        # <div style="border-left: 6px solid {c_ts_tp}; padding-left: 12px; margin-bottom: 14px;">
        #     <h4 style="margin:0;">TSV ↔ TP  
        #     <span style="color:{c_ts_tp}; font-weight:bold;">(r = {r_ts_tp:.2f})</span></h4>
        #     Kürzerer Zusammenhang:  
        #     • Wärmer → Wunsch nach Kühlung  
        #     • Kälter → Wunsch nach Erwärmung  
        # </div>

        # <div style="border-left: 6px solid {c_ts_tc}; padding-left: 12px; margin-bottom: 14px;">
        #     <h4 style="margin:0;">TSV ↔ TC  
        #     <span style="color:{c_ts_tc}; font-weight:bold;">(r = {r_ts_tc:.2f})</span></h4>
        #     Kurzinterpretation:  
        #     • Wärme senkt Komfort leicht  
        #     • Kühle erhöht Komfort minimal  
        # </div>

        # <div style="border-left: 6px solid {c_tp_tc}; padding-left: 12px; margin-bottom: 14px;">
        #     <h4 style="margin:0;">TP ↔ TC  
        #     <span style="color:{c_tp_tc}; font-weight:bold;">(r = {r_tp_tc:.2f})</span></h4>
        #     Kurzinterpretation:  
        #     • Keine Änderung → etwas mehr Komfort  
        #     • Änderungswunsch → leicht reduzierter Komfort  
        # </div>
        # """, unsafe_allow_html=True)

        # st.markdown("""
        # **Gesamtfazit:**  
        # Subjektive Empfindung beeinflusst die gewünschte Temperaturänderung deutlich,  
        # während Komfort nur schwach auf Empfindung und Präferenz reagiert.
        # """)

        # --- Werte aus deiner Korrelationsmatrix ---
        r_ts_tp = corr_matrix.loc["thermal_sensation", "thermal_preference"]
        r_ts_tc = corr_matrix.loc["thermal_sensation", "thermal_comfort"]
        r_tp_tc = corr_matrix.loc["thermal_preference", "thermal_comfort"]

        # --- Farblogik basierend auf Heatmap ---
        def color_for_r(r):
            if r <= -0.50:
                return "#005BBB"   # starke negative Korrelation (blau)
            elif r <= -0.15:
                return "#5F9FE9"   # mittlere negative Korrelation
            elif r <= 0.17:
                return "#E9CDA0"   # schwach (grau)
            elif r < 0.50:
                return "#D1A986"   # light orange (dein Matrix-Farbton)
            else:
                return "#C0392B"   # starke positive Korrelation (rot)

        c_ts_tp = color_for_r(r_ts_tp)
        c_ts_tc = color_for_r(r_ts_tc)
        c_tp_tc = color_for_r(r_tp_tc)

        # --- PANEL AUTOMÁTISCH MIT KURZEN, KLAREN ERKLÄRUNGEN ---
        st.markdown(f"""
        <div style="border-left: 6px solid {c_ts_tp}; padding-left: 12px; margin-bottom: 14px;">
            <h4 style="margin:0;">TSV ↔ TP  
            <span style="color:{c_ts_tp}; font-weight:bold;">(r = {r_ts_tp:.2f})</span></h4>
            • Wärmeres Empfinden führt klar zu Kühlwunsch<br>
            • Kälteres Empfinden führt klar zu Wärmewunsch<br>
            • Präferenz folgt direkt der Empfindung
        </div>

        <div style="border-left: 6px solid {c_ts_tc}; padding-left: 12px; margin-bottom: 14px;">
            <h4 style="margin:0;">TSV ↔ TC  
            <span style="color:{c_ts_tc}; font-weight:bold;">(r = {r_ts_tc:.2f})</span></h4>
            • Wärme senkt Komfort leicht<br>
            • Kühle erhöht Komfort minimal<br>
            • Einfluss insgesamt gering
        </div>

        <div style="border-left: 6px solid {c_tp_tc}; padding-left: 12px; margin-bottom: 14px;">
            <h4 style="margin:0;">TP ↔ TC  
            <span style="color:{c_tp_tc}; font-weight:bold;">(r = {r_tp_tc:.2f})</span></h4>
            • Keine Änderungswünsche → etwas höherer Komfort<br>
            • Änderungswunsch → leicht reduzierter Komfort<br>
            • Zusammenhang schwach, aber plausibel
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        **Gesamtfazit:**  
        Empfindung beeinflusst die gewünschte Temperaturänderung deutlich,  
        während Komfort nur schwach auf Empfindung und Präferenz reagiert.
        """)




with tab1:
    st.subheader("Welche Gruppen benötigen kühlere oder wärmere Bedingungen für Komfort?")
    st.text("Die Neutraltemperatur zeigt, bei welcher Raumtemperatur Menschen weder Wärme noch Kälte empfinden – sie ist damit der zentrale Vergleichswert für unterschiedliche Komfortpräferenzen.")

    st.markdown(
    """
    **Verständnis der Neutraltemperatur (ASCII‑Grafik):**

           zu kalt              neutral              zu warm
        (MTS < 0)             (MTS = 0)            (MTS > 0)
              \\                 |                 /
               \\                |                /
                \\               |               /
                 \\______________|______________/
                               T_neutral
""")

#    Die Waage zeigt:

#     - Links: Personen empfinden die Temperatur als **zu kalt** (negative MTS‑Werte).
#     - Rechts: Personen empfinden die Temperatur als **zu warm** (positive MTS‑Werte).
#     - In der Mitte: **Neutraltemperatur T_neutral**, bei der die mittlere Empfindung MTS = 0 ist.


    # ============================================================
    # LOAD DATA
    # ============================================================

    @st.cache_data
    def load_data():
        df = pd.read_csv("db_bereinigt_fertig.csv")
        df["operative_temperature"] = pd.to_numeric(df["operative_temperature"], errors="coerce")
        df["thermal_sensation"] = pd.to_numeric(df["thermal_sensation"], errors="coerce")
        return df.dropna(subset=["operative_temperature", "thermal_sensation"])
    df = load_data()

    # ============================================================
    # RESET BUTTON
    # ============================================================

    if st.sidebar.button("Reset filters"):
        st.experimental_set_query_params()
        st.rerun()

    # ============================================================
    # SIDEBAR FILTERS WITH CASCADING LOGIC
    # ============================================================

    st.sidebar.header("Filters")

    # --- REGION ---
    region_list = ["All"] + sorted(df["region"].dropna().unique())
    region = st.sidebar.selectbox("Region", region_list)

    # --- COUNTRY depends on REGION ---
    if region != "All":
        country_list = ["All"] + sorted(df[df["region"] == region]["country"].dropna().unique())
    else:
        country_list = ["All"] + sorted(df["country"].dropna().unique())
    country = st.sidebar.selectbox("Country", country_list)

    # --- CITY depends on COUNTRY ---
    if country != "All":
        city_list = ["All"] + sorted(df[df["country"] == country]["city"].dropna().unique())
    else:
        city_list = ["All"] + sorted(df["city"].dropna().unique())
    city = st.sidebar.selectbox("City", city_list)

    # --- CLIMATE ---
    climate_list = ["All"] + sorted(df["climate"].dropna().unique())
    climate = st.sidebar.selectbox("Climate", climate_list)

    # --- BUILDING TYPE depends on CLIMATE ---
    if climate != "All":
        building_list = ["All"] + sorted(df[df["climate"] == climate]["building_type"].dropna().unique())
    else:
        building_list = ["All"] + sorted(df["building_type"].dropna().unique())
    building_type = st.sidebar.selectbox("Building Type", building_list)

    # --- COOLING TYPE depends on BUILDING TYPE ---
    if building_type != "All":
        cooling_list = ["All"] + sorted(df[df["building_type"] == building_type]["cooling_type"].dropna().unique())
    else:
        cooling_list = ["All"] + sorted(df["cooling_type"].dropna().unique())
    cooling_type = st.sidebar.selectbox("Cooling Type", cooling_list)

    # --- SEASON ---
    season_list = ["All"] + sorted(df["season"].dropna().unique())
    season = st.sidebar.selectbox("Season", season_list)

    # --- CLO depends on SEASON ---
    if season != "All":
        clo_list = ["All"] + sorted(df[df["season"] == season]["clothing_ensemble_insulation"].dropna().unique())
    else:
        clo_list = ["All"] + sorted(df["clothing_ensemble_insulation"].dropna().unique())
    clo = st.sidebar.selectbox("Clothing Insulation (clo)", clo_list)

    # --- METABOLIC RATE depends on CLO ---
    if clo != "All":
        met_list = ["All"] + sorted(df[df["clothing_ensemble_insulation"] == clo]["metabolic_rate"].dropna().unique())
    else:
        met_list = ["All"] + sorted(df["metabolic_rate"].dropna().unique())
    metabolic_rate = st.sidebar.selectbox("Metabolic Rate", met_list)

    # --- GENDER ---
    gender_list = ["All"] + sorted(df["gender"].dropna().unique())
    gender = st.sidebar.selectbox("Gender", gender_list)

    # --- AGE ---
    age_list = ["All"] + sorted(df["age"].dropna().unique())
    age = st.sidebar.selectbox("Age", age_list)

    # ============================================================
    # APPLY FILTERS SAFELY
    # ============================================================

    df_filtered = df.copy()

    if region != "All": df_filtered = df_filtered[df_filtered["region"] == region]
    if country != "All": df_filtered = df_filtered[df_filtered["country"] == country]
    if city != "All": df_filtered = df_filtered[df_filtered["city"] == city]
    if climate != "All": df_filtered = df_filtered[df_filtered["climate"] == climate]
    if building_type != "All": df_filtered = df_filtered[df_filtered["building_type"] == building_type]
    if cooling_type != "All": df_filtered = df_filtered[df_filtered["cooling_type"] == cooling_type]
    if season != "All": df_filtered = df_filtered[df_filtered["season"] == season]
    if clo != "All": df_filtered = df_filtered[df_filtered["clothing_ensemble_insulation"] == clo]
    if metabolic_rate != "All": df_filtered = df_filtered[df_filtered["metabolic_rate"] == metabolic_rate]
    if gender != "All": df_filtered = df_filtered[df_filtered["gender"] == gender]
    if age != "All": df_filtered = df_filtered[df_filtered["age"] == age]

    # ============================================================
    # FILTER TEXT FOR TITLE
    # ============================================================

    active_filters = []

    for name, value in [
        ("Region", region),
        ("Country", country),
        ("City", city),
        ("Climate", climate),
        ("Building Type", building_type),
        ("Cooling Type", cooling_type),
        ("Season", season),
        ("Clo", clo),
        ("Metabolic Rate", metabolic_rate),
        ("Gender", gender),
        ("Age", age)
    ]:
        if value != "All":
            active_filters.append(f"{name}: {value}")

    filter_text = " | ".join(active_filters) if active_filters else "No filters (full dataset)"

    st.caption(f"Current filters: {filter_text}")

    # ============================================================
    # GERMAN EXPLANATION
    # ============================================================

    # st.markdown(
    #     "**Beschreibung (Deutsch):**\n"
    #     "Dieses Diagramm zeigt die mittlere thermische Empfindung (Mean Thermal Sensation, MTS) "
    #     "in Abhängigkeit von der Innenraumtemperatur. Für jede automatisch erkannte Kategorie "
    #     "wird eine lineare Regression berechnet, aus der die neutrale Temperatur (MTS = 0) "
    #     "abgeleitet wird. Die vertikale gestrichelte Linie markiert diese neutrale Temperatur."
    # )

    # ============================================================
    # AUTOMATIC GROUPING
    # ============================================================

    grouping_priority = ["building_type", "season", "gender", "region", "country", "city"]

    column_to_group = None
    for col in grouping_priority:
        if df_filtered[col].nunique() > 1:
            column_to_group = col
            break

    if column_to_group is None:
        column_to_group = "building_type"

    groups = df_filtered[column_to_group].dropna().unique()

    # ============================================================
    # PLOT
    # ============================================================

    if df_filtered.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    fig, axes = plt.subplots(1, len(groups), figsize=(16, 5), sharey=True)

    if len(groups) == 1:
        axes = [axes]

    colors = plt.cm.tab10(np.linspace(0, 1, len(groups)))
    markers = ["o", "s", "^", "D", "P", "X", "*"]
    color_map = dict(zip(groups, colors))
    marker_map = dict(zip(groups, markers))

    results = []

    for ax, g in zip(axes, groups):

        sub = df_filtered[df_filtered[column_to_group] == g]

        if sub.empty:
            ax.set_title(f"{g} (no data)")
            ax.axis("off")
            continue

        mts_df = sub.groupby("operative_temperature")["thermal_sensation"].mean().reset_index()
        mts_df.columns = ["operative_temperature", "MTS"]

        if len(mts_df) < 2:
            ax.set_title(f"{g} (insufficient data)")
            ax.axis("off")
            continue

        X = mts_df["operative_temperature"].values.reshape(-1, 1)
        y = mts_df["MTS"].values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        a = model.coef_[0][0]
        b = model.intercept_[0]
        r2 = model.score(X, y)
        neutral_temp = -b / a

        results.append([g, a, b, r2, neutral_temp])

        x_range = np.linspace(mts_df["operative_temperature"].min(),
                              mts_df["operative_temperature"].max(), 100)
        y_pred = model.predict(x_range.reshape(-1, 1))

        ax.plot(x_range, y_pred, color=color_map[g], linewidth=2)
        ax.scatter(
            mts_df["operative_temperature"],
            mts_df["MTS"],
            color=color_map[g],
            marker=marker_map[g],
            s=60,
            edgecolor="black",
            linewidth=0.6
        )
        ax.axvline(neutral_temp, color=color_map[g], linestyle="--", linewidth=1.5)

        ax.text(
            0.05, 0.95,
            f"{g}\nMTS = {a:.3f}·T + {b:.3f}\nR² = {r2:.3f}\nNeutral = {neutral_temp:.2f} °C",
            transform=ax.transAxes,
            fontsize=9,
            color=color_map[g],
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor=color_map[g])
        )

        ax.set_title(g)
        ax.set_xlabel("Indoor Temperature (°C)")
        ax.grid(True)

    axes[0].set_ylabel("Mean Thermal Sensation (MTS)")
    fig.suptitle(f"MTS vs Indoor Temperature | {filter_text}", fontsize=14)
    plt.tight_layout()
    st.pyplot(fig)
    st.caption("""
    Die Grafik zeigt, wie sich die mittlere thermische Empfindung (MTS) in verschiedenen Kategorien  
    mit der Innenraumtemperatur verändert. Die sortierte Tabelle oben verdeutlicht, welche Gruppen  
    niedrigere oder höhere T_neutral‑Werte aufweisen und damit kühlere bzw. wärmere Bedingungen als  
    komfortabel empfinden.
    """)

    # ============================================================
    # SUMMARY TABLE
    # ============================================================

    if results:
        summary_df = pd.DataFrame(
            results,
            columns=[column_to_group, "Slope a", "Intercept b", "R²", "Neutraltemperatur"]
        )

        # ORDENAR DE MENOR A MAYOR POR TEMPERATURA NEUTRAL
        summary_df = summary_df.sort_values("Neutraltemperatur", ascending=True)

        st.subheader("Neutral Temperature Summary")

        st.dataframe(
            summary_df.style.format({
                "Slope a": "{:.2f}",
                "Intercept b": "{:.2f}",
                "R²": "{:.2f}",
                "Neutraltemperatur": "{:.2f}"
            })
        )
    else:
        st.info("No valid regression results for the selected filters.")



#########################################################################################################################
#########################################################################################################################

with tab2:

    st.subheader("Wie stark verändert Kleidung die Komforttemperatur?")
    st.text(
        "Kleidung beeinflusst die Wärmeisolierung des Körpers. Höhere Clo‑Werte führen dazu, "
        "dass Personen sich bereits bei niedrigeren Temperaturen thermisch neutral fühlen. "
        "Leichtere Kleidung hingegen verschiebt die Neutraltemperatur nach oben.")


    # CLO-Werte Erklärung
    st.markdown(
        """
        **Was bedeuten die Clo‑Werte?**

        - **0.0–0.2 clo:** sehr leichte Kleidung (Shorts, Tanktop)  
        - **0.3–0.5 clo:** leichte Sommerkleidung (T‑Shirt, dünne Hose)  
        - **0.6–0.8 clo:** normale Alltagskleidung (Hemd + Hose)  
        - **0.9–1.0 clo:** leichte Winterkleidung (Pullover, lange Hose)  
        - **1.1–1.3 clo:** warme Kleidung (Pullover + Jacke)  
        - **1.4–1.7 clo:** sehr warme Kleidung (Winterjacke)  
        - **> 2.0 clo:** extreme Isolation (Ski‑Anzug)
        """
    )

    df_clo = df.copy()
    results_clo = []

    for clo_value in sorted(df_clo["clothing_ensemble_insulation"].dropna().unique()):
        sub = df_clo[df_clo["clothing_ensemble_insulation"] == clo_value]

        if sub.empty:
            continue

        mts_df = sub.groupby("operative_temperature")["thermal_sensation"].mean().reset_index()
        mts_df.columns = ["operative_temperature", "MTS"]

        if len(mts_df) < 2:
            continue

        X = mts_df["operative_temperature"].values.reshape(-1, 1)
        y = mts_df["MTS"].values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        a = model.coef_[0][0]
        b = model.intercept_[0]
        r2 = model.score(X, y)

        # Fehler vermeiden: a = 0 → NeutralTemp = NaN statt -Infinity
        if abs(a) < 1e-6:
            neutral_temp = np.nan
        else:
            neutral_temp = -b / a

        results_clo.append([clo_value, a, b, r2, neutral_temp])

    summary_clo = pd.DataFrame(
        results_clo,
        columns=["Clo-Level", "Slope a", "Intercept b", "R²", "Neutraltemperatur"]).sort_values("Neutraltemperatur", ascending=True)

    st.subheader("Neutraltemperatur pro Clo‑Level")
    st.dataframe(
        summary_clo.style.format({
            "Slope a": "{:.3f}",
            "Intercept b": "{:.3f}",
            "R²": "{:.3f}",
            "Neutraltemperatur": "{:.3f}"
        })
    )

    st.caption(
        "Die Tabelle zeigt, wie Kleidung die Neutraltemperatur beeinflusst. "
        "Höhere Clo‑Werte führen zu niedrigeren Komforttemperaturen."
    )


    # --- ASHRAE-style graphic for clothing vs neutral temperature ---
    st.subheader("Graphical Interpretation – Clothing Influence on Neutral Temperature")

    if not summary_clo.empty:

        fig, ax = plt.subplots(figsize=(8, 5))

        # Sort by clo-level
        summary_clo_sorted = summary_clo.sort_values("Clo-Level")

        # ASHRAE-style neutral line (orange)
        ax.plot(
            summary_clo_sorted["Clo-Level"],
            summary_clo_sorted["Neutraltemperatur"],
            marker="o",
            linestyle="-",
            color="#ff7f0e",   # ASHRAE neutral orange
            linewidth=2,
            markersize=8,
            label="Neutral Temperature Trend"
        )

        # Color-coded points (blue = cold, orange = neutral, red = warm)
        for clo, temp in zip(summary_clo_sorted["Clo-Level"], summary_clo_sorted["Neutraltemperatur"]):
            if temp < 22:
                color = "#1f77b4"   # cold zone (ASHRAE blue)
            elif temp > 25:
                color = "#d62728"   # warm zone (ASHRAE red)
            else:
                color = "#ff7f0e"   # neutral zone (ASHRAE orange)

            ax.scatter(clo, temp, color=color, s=90)

        ax.set_title("Neutral Temperature as a Function of Clothing Insulation (clo)", fontsize=14)
        ax.set_xlabel("Clothing Insulation (clo)", fontsize=12)
        ax.set_ylabel("Neutral Temperature (°C)", fontsize=12)

        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend()

        st.pyplot(fig)

    else:
        st.info("No data available to generate the ASHRAE-style graphic.")


########################################################################################################################
########################################################################################################################
########################################################################################################################

with tab3:

    # ============================================================
    # EINLEITUNG – kurz, neutral, wissenschaftlich
    # ============================================================

    #st.header("Adaptives Komfortmodell nach ASHRAE 55")

    st.subheader("Welche Kategorie erfüllt die Komfortanforderungen am besten?")
    st.write(
    "Die folgende Analyse untersucht, wie gut verschiedene Kategorien die thermischen "
    "Komfortanforderungen nach dem adaptiven ASHRAE‑55‑Modell erfüllen. "
    "Durch den Vergleich der Komfort‑Compliance wird sichtbar, welche Gruppen sich am "
    "besten an die Außentemperatur anpassen und in welchen Kategorien deutliche Abweichungen "
    "vom Komfortbereich auftreten."
)

    st.markdown(
        """
        **Was zeigt die Grafik?**

        - Die Komfortzonen (80 % und 90 %) geben Bereiche an, in denen die Mehrheit der Personen
          thermischen Komfort empfindet.
        - Punkte oberhalb der Komfortzonen weisen auf mögliche Überhitzung hin.
        - Punkte unterhalb der Komfortzonen deuten auf Unterkühlung oder verstärkte Luftbewegung hin.
        - Die Streuung der Messpunkte zeigt, wie unterschiedlich Gebäude, Nutzungsarten oder Klimata
          auf die Außentemperatur reagieren.
        """
    )

    # ============================================================
    # 1. LOAD DATA
    # ============================================================

    df = pd.read_csv("db_bereinigt_fertig.csv")

    cols_to_numeric = [
        "operative_temperature",
        "outdoor_air_temperature",
        "clothing_ensemble_insulation",
        "metabolic_rate",
        "thermal_sensation",
        "thermal_comfort"
    ]

    for col in cols_to_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=[
        "operative_temperature",
        "outdoor_air_temperature",
        "season",
        "city",
        "country",
        "region"
    ])

    # ============================================================
    # 2. FILTERS – zwei Spalten
    # ============================================================

    colA, colB = st.columns([0.7,2.3])

    with colA:

        st.subheader("Filter")

        region_list = sorted(df["region"].dropna().unique())
        region = st.selectbox("Region", ["Alle"] + region_list)
        if region != "Alle":
            df = df[df["region"] == region]

        country_list = sorted(df["country"].dropna().unique())
        country = st.selectbox("Land", ["Alle"] + country_list)
        if country != "Alle":
            df = df[df["country"] == country]

        city_list = sorted(df["city"].dropna().unique())
        city = st.selectbox("Stadt", ["Alle"] + city_list)
        if city != "Alle":
            df = df[df["city"] == city]

        # Gruppierung NUR für Einzelplots
        column_to_group = st.selectbox(
            "Kategorie für Einzelplots:",
            ["season", "climate", "building_type", "cooling_type", "gender", "age", "country", "region"]
        )


        
    # ============================================================
    # 3. SORT BY OUTDOOR TEMPERATURE
    # ============================================================

    df_sorted = df.sort_values(by="outdoor_air_temperature")

    T_out = df_sorted["outdoor_air_temperature"]
    T_in = df_sorted["operative_temperature"]

    # ============================================================
    # 4. ADAPTIVE COMFORT LIMITS
    # ============================================================

    T_comf = 0.31 * T_out + 17.8
    T_lower_80 = T_comf - 2.5
    T_upper_80 = T_comf + 2.5
    T_lower_90 = T_comf - 3.5
    T_upper_90 = T_comf + 3.5


    with colB:

        # ============================================================
        # 5. MAIN PLOT – Adaptive Comfort Chart
        # ============================================================

        # Titel mit aktiven Filtern
        active_filters = []
        if region != "Alle": active_filters.append(f"Region: {region}")
        if country != "Alle": active_filters.append(f"Land: {country}")
        if city != "Alle": active_filters.append(f"Stadt: {city}")

        filter_text = ", ".join(active_filters) if active_filters else "Keine Filter aktiv"

        st.subheader("Adaptive Comfort Chart")
        st.caption(f"Aktive Filter: {filter_text}")

        fig, ax = plt.subplots(figsize=(12, 7))

        ax.fill_between(T_out, T_lower_90, T_upper_90, color="yellow", alpha=0.15, label="90 % Komfortzone")
        ax.fill_between(T_out, T_lower_80, T_upper_80, color="green", alpha=0.20, label="80 % Komfortzone")

        ax.scatter(
            df_sorted["outdoor_air_temperature"],
            df_sorted["operative_temperature"],
            color="blue",
            alpha=0.7,
            edgecolor="black",
            linewidth=0.5,
            label="Messpunkte"
        )

        ax.set_xlabel("Außentemperatur (°C)")
        ax.set_ylabel("Operative Innentemperatur (°C)")
        ax.set_title("ASHRAE 55 – Adaptives Komfortmodell")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        st.caption(
    "Adaptive Komfortkurve nach ASHRAE 55 für alle gefilterten Daten. "
    "Die farbigen Bereiche markieren die 80 %‑ und 90 %‑Komfortzonen, während die Punkte die "
    "tatsächlichen Messwerte darstellen. So wird sichtbar, wie gut die Daten mit dem Modell "
    "übereinstimmen und ob Tendenzen zu Überhitzung oder Unterkühlung auftreten.")



    # ============================================================
    # 6. EINZELPLOTS – max. 3 pro Reihe
    # ============================================================

    st.subheader("Einzelplots pro Kategorie")
    st.text(
    "Die Einzelplots zeigen jede ausgewählte Kategorie separat. Dadurch wird sichtbar, "
    "wie sich unterschiedliche Gruppen innerhalb der Komfortzonen verhalten und ob "
    "bestimmte Klimata, Gebäudetypen oder Nutzungsarten systematisch von den "
    "Komfortbereichen abweichen.")


    unique_groups = df[column_to_group].dropna().unique()
    palette = sns.color_palette("tab10", len(unique_groups))
    color_map = dict(zip(unique_groups, palette))

    num_groups = len(unique_groups)

    # Fall 1: Nur eine Kategorie → großer Plot
    if num_groups == 1:
        group = unique_groups[0]
        subset = df_sorted[df_sorted[column_to_group] == group]

        fig, ax = plt.subplots(figsize=(10, 6))

        T_out_sub = subset["outdoor_air_temperature"]
        T_comf_sub = 0.31 * T_out_sub + 17.8

        ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                        color="yellow", alpha=0.15)
        ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                        color="green", alpha=0.20)

        ax.scatter(
            subset["outdoor_air_temperature"],
            subset["operative_temperature"],
            color=color_map[group],
            edgecolor="black",
            alpha=0.85,
            linewidth=0.5
        )

        ax.set_title(f"{column_to_group}: {group}")
        ax.set_xlabel("Außentemperatur (°C)")
        ax.set_ylabel("Operative Innentemperatur (°C)")
        ax.grid(True)

        st.pyplot(fig)

    # Fall 2: Zwei Kategorien → zwei große Plots nebeneinander
    elif num_groups == 2:
        col1, col2 = st.columns(2)

        for col, group in zip([col1, col2], unique_groups):
            subset = df_sorted[df_sorted[column_to_group] == group]

            fig, ax = plt.subplots(figsize=(8, 5))

            T_out_sub = subset["outdoor_air_temperature"]
            T_comf_sub = 0.31 * T_out_sub + 17.8

            ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                            color="yellow", alpha=0.15)
            ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                            color="green", alpha=0.20)

            ax.scatter(
                subset["outdoor_air_temperature"],
                subset["operative_temperature"],
                color=color_map[group],
                edgecolor="black",
                alpha=0.85,
                linewidth=0.5
            )

            ax.set_title(f"{column_to_group}: {group}")
            ax.set_xlabel("Außentemperatur (°C)")
            ax.set_ylabel("Operative Innentemperatur (°C)")
            ax.grid(True)

            col.pyplot(fig)

    # Fall 3: Drei oder mehr Kategorien → max. 3 pro Reihe
    else:
        rows = (num_groups + 2) // 3
        idx = 0

        for r in range(rows):
            cols = st.columns(3)
            for c in range(3):
                if idx >= num_groups:
                    break

                group = unique_groups[idx]
                subset = df_sorted[df_sorted[column_to_group] == group]

                fig, ax = plt.subplots(figsize=(6, 4))

                T_out_sub = subset["outdoor_air_temperature"]
                T_comf_sub = 0.31 * T_out_sub + 17.8

                ax.fill_between(T_out_sub, T_comf_sub - 3.5, T_comf_sub + 3.5,
                                color="yellow", alpha=0.15)
                ax.fill_between(T_out_sub, T_comf_sub - 2.5, T_comf_sub + 2.5,
                                color="green", alpha=0.20)

                ax.scatter(
                    subset["outdoor_air_temperature"],
                    subset["operative_temperature"],
                    color=color_map[group],
                    edgecolor="black",
                    alpha=0.85,
                    linewidth=0.5
                )

                ax.set_title(f"{column_to_group}: {group}")
                ax.set_xlabel("Außentemperatur (°C)")
                ax.set_ylabel("Operative Innentemperatur (°C)")
                ax.grid(True)

                cols[c].pyplot(fig)
                idx += 1

        

# ============================================================
# 6. Komfort‑Compliance pro Kategorie
# ============================================================

    st.subheader("Komfort‑Compliance pro Kategorie")

    compliance_rows = []

    for group in unique_groups:
        subset = df_sorted[df_sorted[column_to_group] == group]

        if subset.empty:
            continue

        T_out_sub = subset["outdoor_air_temperature"]
        T_comf_sub = 0.31 * T_out_sub + 17.8

        T_lower_80_sub = T_comf_sub - 2.5
        T_upper_80_sub = T_comf_sub + 2.5

        T_lower_90_sub = T_comf_sub - 3.5
        T_upper_90_sub = T_comf_sub + 3.5

        inside_80 = ((subset["operative_temperature"] >= T_lower_80_sub) &
                    (subset["operative_temperature"] <= T_upper_80_sub)).mean()

        inside_90 = ((subset["operative_temperature"] >= T_lower_90_sub) &
                    (subset["operative_temperature"] <= T_upper_90_sub)).mean()

        compliance_rows.append([
            group,
            round(inside_80 * 100, 1),
            round(inside_90 * 100, 1)
        ])

    df_compliance = pd.DataFrame(
        compliance_rows,
        columns=["Kategorie", "80%-Komfortzone (%)", "90%-Komfortzone (%)"]
    )

    st.dataframe(df_compliance)



# # ============================================================
# # 7. Dynamische Interpretation der Grafik
# # ============================================================

#     st.subheader("Dynamische Interpretation der Ergebnisse")

#     # Anteil der Punkte innerhalb der Komfortzonen
#     inside_80 = ((df_sorted["operative_temperature"] >= T_lower_80) &
#                 (df_sorted["operative_temperature"] <= T_upper_80)).mean()

#     inside_90 = ((df_sorted["operative_temperature"] >= T_lower_90) &
#                 (df_sorted["operative_temperature"] <= T_upper_90)).mean()

#     # Durchschnittliche operative Temperatur
#     avg_T_in = df_sorted["operative_temperature"].mean()

#     # Durchschnittliche Außentemperatur
#     avg_T_out = df_sorted["outdoor_air_temperature"].mean()

#     # Dynamische Textanalyse
#     interpretation = f"""
#     **Kurze Auswertung basierend auf deinen Daten:**

#     - Die durchschnittliche Außentemperatur beträgt **{avg_T_out:.1f} °C**.
#     - Die durchschnittliche operative Innentemperatur liegt bei **{avg_T_in:.1f} °C**.

#     **Komfortbewertung nach ASHRAE 55:**

#     - **{inside_80*100:.1f}%** aller Messpunkte liegen innerhalb der **80%-Komfortzone**.
#     - **{inside_90*100:.1f}%** aller Messpunkte liegen innerhalb der **90%-Komfortzone**.

#     **Was bedeutet das?**

#     - Wenn viele Punkte in den grünen Bereich fallen, zeigt das eine **hohe Übereinstimmung mit dem adaptiven Komfortmodell**.
#     - Punkte oberhalb der Komfortzonen deuten auf **Überhitzung** hin (z. B. unzureichende Kühlung oder hohe interne Lasten).
#     - Punkte unterhalb der Komfortzonen weisen auf **Unterkühlung** hin (z. B. starke Lüftung, kalte Außenbedingungen oder hohe Luftbewegung).
#     - Die Streuung der Punkte zeigt, wie **unterschiedlich Nutzer oder Gebäude auf Außenbedingungen reagieren**.

#     **Interpretation für die Gruppierung „{column_to_group}“:**

#     - Gruppen, die überwiegend im Komfortbereich liegen, weisen auf **gute adaptive Anpassung** hin.
#     - Gruppen außerhalb der Komfortzonen könnten **saisonale Effekte**, **Gebäudetypen**, **Nutzungsverhalten** oder **klimatische Besonderheiten** widerspiegeln.
#     """

#     st.markdown(interpretation)



# # ============================================================
# # 7. Automatische Interpretation pro Kategorie
# # ============================================================

#     st.subheader("Automatische Interpretation pro Kategorie")

#     interpretation_text = ""

#     for group, inside80, inside90 in zip(
#         df_compliance["Kategorie"],
#         df_compliance["80%-Komfortzone (%)"],
#         df_compliance["90%-Komfortzone (%)"]
#     ):

#         # Interpretation basierend auf Komfortanteilen
#         if inside80 >= 70:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** weist eine hohe Übereinstimmung mit dem adaptiven "
#                 f"Komfortmodell auf. Mit **{inside80}%** der Messpunkte innerhalb der 80%-Komfortzone "
#                 f"befindet sich der Großteil der Werte im thermisch akzeptablen Bereich."
#             )
#         elif inside80 >= 40:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** zeigt eine gemischte Komfortsituation. "
#                 f"Etwa **{inside80}%** der Messpunkte liegen innerhalb der 80%-Komfortzone, "
#                 f"was auf teilweise gute, aber nicht durchgehend stabile Komfortbedingungen hinweist."
#             )
#         else:
#             comfort_statement = (
#                 f"Die Kategorie **{group}** weist eine geringe Übereinstimmung mit dem adaptiven "
#                 f"Komfortmodell auf. Nur **{inside80}%** der Messpunkte liegen innerhalb der "
#                 f"80%-Komfortzone, was auf mögliche Überhitzung oder Unterkühlung hindeutet."
#             )

#         # Ergänzung basierend auf 90%-Zone
#         if inside90 >= 80:
#             detail_statement = (
#                 f"Zusätzlich liegen **{inside90}%** der Messpunkte innerhalb der 90%-Komfortzone, "
#                 f"was eine insgesamt stabile thermische Situation bestätigt."
#             )
#         elif inside90 >= 50:
#             detail_statement = (
#                 f"Mit **{inside90}%** innerhalb der 90%-Komfortzone zeigt sich eine moderate "
#                 f"Komfortlage mit deutlicher Streuung."
#             )
#         else:
#             detail_statement = (
#                 f"Nur **{inside90}%** der Messpunkte liegen innerhalb der 90%-Komfortzone, "
#                 f"was auf stark variierende Bedingungen oder deutliche Abweichungen vom Modell hinweist."
#             )

#         interpretation_text += f"- {comfort_statement} {detail_statement}\n\n"

#     st.markdown(interpretation_text)



# ============================================================
# 8. Natürliche Zusammenfassung: Welche Kategorie ist am besten?
# ============================================================

    st.subheader("Zusammenfassung")

    # Beste und schlechteste Kategorie anhand der 80%-Komfortzone
    best_row = df_compliance.loc[df_compliance["80%-Komfortzone (%)"].idxmax()]
    worst_row = df_compliance.loc[df_compliance["80%-Komfortzone (%)"].idxmin()]

    best_cat = best_row["Kategorie"]
    best_80 = best_row["80%-Komfortzone (%)"]
    best_90 = best_row["90%-Komfortzone (%)"]

    worst_cat = worst_row["Kategorie"]
    worst_80 = worst_row["80%-Komfortzone (%)"]
    worst_90 = worst_row["90%-Komfortzone (%)"]

    summary_text = f"""
    **Welche Kategorie zeigt die beste Komfortleistung?**

    Die Kategorie **{best_cat}** weist die höchste Übereinstimmung mit dem adaptiven Komfortmodell auf.
    Mit **{best_80}%** innerhalb der 80%-Komfortzone und **{best_90}%** innerhalb der 90%-Komfortzone
    zeigt diese Gruppe die stabilsten thermischen Bedingungen.

    **Welche Kategorie schneidet am schlechtesten ab?**

    Die Kategorie **{worst_cat}** liegt mit nur **{worst_80}%** in der 80%-Komfortzone deutlich unter den
    anderen Gruppen. Auch die 90%-Komfortzone (**{worst_90}%**) zeigt eine geringere Übereinstimmung,
    was auf stärkere Abweichungen vom Komfortmodell hindeutet.

    **Was bedeutet das insgesamt?**

    Die Analyse zeigt, dass sich die Kategorien klar unterscheiden: Einige Gruppen passen sich gut an
    die Außentemperatur an und bleiben überwiegend innerhalb der Komfortbereiche, während andere
    deutliche Tendenzen zu Überhitzung oder Unterkühlung aufweisen. Diese Unterschiede können durch
    Gebäudetypen, Klimazonen, Nutzungsverhalten oder saisonale Effekte beeinflusst sein.
    """

    st.markdown(summary_text)


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

with tab4:

    st.subheader("Welche physikalischen Faktoren beeinflussen den thermischen Komfort am stärksten?")

    # st.write(
    # """
    # • Metabolische Aktivität (met) bestimmt die körpereigene Wärmeproduktion und beeinflusst,
    #   wie schnell Personen Wärme abgeben oder speichern.

    # • Bekleidungsisolation (Clo-Wert) verändert die Wärmeabgabe des Körpers und verschiebt
    #   die individuelle Neutraltemperatur.

    # • Lufttemperatur ist der stärkste direkte Einflussfaktor auf das thermische Empfinden
    #   und bestimmt die Wärmebilanz des Körpers.

    # • Luftgeschwindigkeit (Air Velocity) erhöht die konvektive Kühlung und kann warme
    #   Bedingungen deutlich erträglicher machen.

    # • Mittlere Strahlungstemperatur beeinflusst die Wärmeabgabe durch Strahlung und wirkt
    #   besonders in Räumen mit großen Fensterflächen oder warmen Oberflächen.

    # • Relative Luftfeuchtigkeit beeinflusst die Verdunstungskühlung und verstärkt
    #   Wärmebelastung bei hohen Temperaturen.
    # """
    # )

    st.write(
    "Diese Analyse untersucht die Zusammenhänge zwischen den wichtigsten physikalischen "
    "Einflussgrößen des thermischen Komforts. Dazu gehören metabolische Aktivität, "
    "Bekleidungsisolation, Lufttemperatur, Luftgeschwindigkeit, mittlere Strahlungstemperatur "
    "und relative Luftfeuchtigkeit. Die Korrelationsmatrix zeigt, welche dieser Variablen "
    "gemeinsam variieren und welche Faktoren besonders stark zur thermischen Belastung oder "
    "Entlastung beitragen. Dadurch lassen sich Muster erkennen, die für die Bewertung von "
    "Innenraumklima und Komfortbedingungen entscheidend sind."
    )


    # ============================================================
    # 1. Select relevant physical variables
    # ============================================================

    cols_phys = [
        "metabolic_rate",
        "clothing_ensemble_insulation",
        "air_temperature",
        "air_speed",
        "radiant_temperature",
        "relative_humidity"
    ]

    df_phys = df[cols_phys].copy()

    # Convert to numeric
    for c in cols_phys:
        df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

    df_phys = df_phys.dropna()

    # ============================================================
    # 2. Compute correlation matrix (Spearman recommended)
    # ============================================================

    corr_matrix = df_phys.corr(method="spearman")

    # ============================================================
    # 3. Heatmap visualization
    # ============================================================

    st.subheader("Heatmap der physikalischen Komfortkorrelationen")

    fig, ax = plt.subplots(figsize=(10, 7))
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
    # 4. Scatter matrix (pairwise relationships)
    # ============================================================

    st.subheader("Pairwise Relationships (Scatter Matrix)")

    pairplot_fig = sns.pairplot(df_phys, diag_kind="kde")
    pairplot_fig.fig.set_size_inches(12, 10)  # optional resize

    st.pyplot(pairplot_fig.fig)
    st.caption(
        "Diese Analyse zeigt, wie die wichtigsten physikalischen Einflussgrößen des "
        "thermischen Komforts miteinander zusammenhängen. Die Korrelationen verdeutlichen, "
        "welche Faktoren gemeinsam auftreten und wie sie die thermische Wahrnehmung beeinflussen."
    )

    # ============================================================
    # 5. Automatic Interpretation
    # ============================================================

    st.subheader("Automatic Interpretation of Physical Comfort Correlations")

    interpret = []

    def add_if(condition, text):
        if condition:
            interpret.append(text)

    mr = corr_matrix["metabolic_rate"]
    clo = corr_matrix["clothing_ensemble_insulation"]
    ta = corr_matrix["air_temperature"]
    vel = corr_matrix["air_speed"]
    tr = corr_matrix["radiant_temperature"]
    rh = corr_matrix["relative_humidity"]

    # Metabolic Rate
    add_if(mr["air_temperature"] > 0.4,
        "- Höhere metabolische Aktivität korreliert mit höheren Lufttemperaturen.")
    add_if(mr["air_speed"] > 0.4,
        "- Personen mit höherem Metabolismus bevorzugen höhere Luftgeschwindigkeiten.")

    # Clothing
    add_if(clo["air_temperature"] < -0.4,
        "- Höhere Bekleidungsisolation tritt häufig bei niedrigeren Lufttemperaturen auf.")
    add_if(clo["radiant_temperature"] < -0.4,
        "- Mehr Kleidung wird bei geringerer Strahlungstemperatur getragen.")

    # Air Temperature
    add_if(ta["radiant_temperature"] > 0.6,
        "- Lufttemperatur und Strahlungstemperatur sind stark gekoppelt (hohe Wärmebelastung).")
    add_if(ta["relative_humidity"] > 0.4,
        "- Höhere Lufttemperaturen gehen oft mit höherer Luftfeuchtigkeit einher.")

    # Air Velocity
    add_if(vel["air_temperature"] < -0.4,
        "- Höhere Luftgeschwindigkeiten treten häufiger bei höheren Temperaturen auf (Kühlbedarf).")

    # Humidity
    add_if(rh["air_temperature"] > 0.4,
        "- Warme Bedingungen sind häufig feuchter, was die Verdunstungskühlung reduziert.")

    st.markdown("\n".join(interpret))



######################################################################################################################################
######################################################################################################################################

    # st.header("PCA (Principal Component Analysis) of Physical Comfort Variables")

    # # ============================================================
    # # 1. Select relevant physical variables
    # # ============================================================

    # cols_phys = [
    #     "metabolic_rate",
    #     "clothing_ensemble_insulation",
    #     "air_temperature",
    #     "air_speed",
    #     "radiant_temperature",
    #     "relative_humidity"
    # ]

    # df_phys = df[cols_phys].copy()

    # # Convert to numeric
    # for c in cols_phys:
    #     df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

    # df_phys = df_phys.dropna()

    # # ============================================================
    # # 2. Standardize data (PCA requires scaling)
    # # ============================================================

    # from sklearn.preprocessing import StandardScaler
    # from sklearn.decomposition import PCA

    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(df_phys)

    # # ============================================================
    # # 3. PCA computation (2 components)
    # # ============================================================

    # pca = PCA(n_components=2)
    # pca_result = pca.fit_transform(X_scaled)

    # df_pca = pd.DataFrame({
    #     "PC1": pca_result[:, 0],
    #     "PC2": pca_result[:, 1]
    # })

    # # Loadings (variable contributions)
    # loadings = pd.DataFrame(
    #     pca.components_.T,
    #     columns=["PC1", "PC2"],
    #     index=cols_phys
    # )

    # # ============================================================
    # # 4. PCA Scatter Plot
    # # ============================================================

    # st.subheader("PCA Scatter Plot (PC1 vs PC2)")

    # fig, ax = plt.subplots(figsize=(10, 7))
    # ax.scatter(df_pca["PC1"], df_pca["PC2"], alpha=0.6)

    # ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    # ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    # ax.set_title("PCA of Physical Comfort Variables")

    # ax.grid(True)
    # st.pyplot(fig)

    # # ============================================================
    # # 5. PCA Loadings Plot (Variable Influence)
    # # ============================================================

    # st.subheader("Variable Contributions to PCA Components")

    # fig2, ax2 = plt.subplots(figsize=(10, 6))
    # loadings.plot(kind="bar", ax=ax2)
    # ax2.set_title("PCA Loadings (Influence of Each Variable)")
    # ax2.set_ylabel("Loading Value")
    # ax2.grid(True)

    # st.pyplot(fig2)

    # # ============================================================
    # # 6. Automatic Interpretation
    # # ============================================================

    # st.subheader("Automatic Interpretation of PCA Results")

    # interpret = []

    # # PC1 interpretation
    # pc1_top = loadings["PC1"].abs().sort_values(ascending=False).index[:2]
    # interpret.append(
    #     f"- **PC1** wird hauptsächlich durch **{pc1_top[0]}** und **{pc1_top[1]}** bestimmt."
    # )

    # # PC2 interpretation
    # pc2_top = loadings["PC2"].abs().sort_values(ascending=False).index[:2]
    # interpret.append(
    #     f"- **PC2** wird hauptsächlich durch **{pc2_top[0]}** und **{pc2_top[1]}** beeinflusst."
    # )

    # # Variance explanation
    # interpret.append(
    #     f"- PC1 erklärt **{pca.explained_variance_ratio_[0]*100:.1f}%** der Gesamtvarianz, "
    #     f"PC2 erklärt **{pca.explained_variance_ratio_[1]*100:.1f}%**."
    # )

    # # Comfort insight
    # interpret.append(
    #     "- Die PCA zeigt, welche physikalischen Faktoren gemeinsam variieren und "
    #     "welche Variablen die dominanten thermischen Einflussachsen bilden."
    # )

    # st.markdown("\n".join(interpret))

    # # ============================================================
    # # 7. Caption
    # # ============================================================

    # st.caption(
    #     "Die PCA zeigt die Hauptvariationsachsen der physikalischen Komfortparameter. "
    #     "Dadurch wird sichtbar, welche Faktoren gemeinsam auftreten und welche Variablen "
    #     "die thermische Umgebung am stärksten prägen."
    # )




    # st.header("Grouped PCA of Physical Comfort Variables")

    # # ============================================================
    # # 1. Select grouping variable
    # # ============================================================

    # group_option = st.selectbox(
    #     "Group PCA by:",
    #     ["season", "climate", "building_type"]
    # )

    # # Clean grouping column
    # df_grouped = df.copy()
    # df_grouped[group_option] = df_grouped[group_option].replace({"Unknown": None})
    # df_grouped = df_grouped.dropna(subset=[group_option])

    # # ============================================================
    # # 2. Select physical comfort variables
    # # ============================================================

    # cols_phys = [
    #     "metabolic_rate",
    #     "clothing_ensemble_insulation",
    #     "air_temperature",
    #     "air_speed",
    #     "radiant_temperature",
    #     "relative_humidity"
    # ]

    # df_phys = df_grouped[cols_phys + [group_option]].copy()

    # # Convert to numeric
    # for c in cols_phys:
    #     df_phys[c] = pd.to_numeric(df_phys[c], errors="coerce")

    # df_phys = df_phys.dropna()

    # # ============================================================
    # # 3. Standardize data
    # # ============================================================

    # from sklearn.preprocessing import StandardScaler
    # from sklearn.decomposition import PCA

    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(df_phys[cols_phys])

    # # ============================================================
    # # 4. PCA computation
    # # ============================================================

    # pca = PCA(n_components=2)
    # pca_result = pca.fit_transform(X_scaled)

    # df_pca = pd.DataFrame({
    #     "PC1": pca_result[:, 0],
    #     "PC2": pca_result[:, 1],
    #     group_option: df_phys[group_option].values
    # })

    # # Loadings (variable contributions)
    # loadings = pd.DataFrame(
    #     pca.components_.T,
    #     columns=["PC1", "PC2"],
    #     index=cols_phys
    # )

    # # ============================================================
    # # 5. PCA Scatter Plot (Grouped)
    # # ============================================================

    # st.subheader(f"PCA grouped by {group_option}")

    # fig, ax = plt.subplots(figsize=(10, 7))

    # groups = df_pca[group_option].unique()
    # palette = sns.color_palette("tab10", len(groups))

    # for g, color in zip(groups, palette):
    #     subset = df_pca[df_pca[group_option] == g]
    #     ax.scatter(
    #         subset["PC1"],
    #         subset["PC2"],
    #         label=g,
    #         alpha=0.7,
    #         color=color
    #     )

    # ax.set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)")
    # ax.set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)")
    # ax.set_title(f"PCA of Physical Comfort Variables grouped by {group_option}")
    # ax.grid(True)
    # ax.legend(title=group_option)

    # st.pyplot(fig)

    # # ============================================================
    # # 6. PCA Loadings Plot
    # # ============================================================

    # st.subheader("Variable Contributions to PCA Components")

    # fig2, ax2 = plt.subplots(figsize=(10, 6))
    # loadings.plot(kind="bar", ax=ax2)
    # ax2.set_title("PCA Loadings (Influence of Each Variable)")
    # ax2.set_ylabel("Loading Value")
    # ax2.grid(True)

    # st.pyplot(fig2)

    # # ============================================================
    # # 7. Automatic Interpretation
    # # ============================================================

    # st.subheader("Automatic Interpretation of Grouped PCA")

    # interpret = []

    # pc1_top = loadings["PC1"].abs().sort_values(ascending=False).index[:2]
    # pc2_top = loadings["PC2"].abs().sort_values(ascending=False).index[:2]

    # interpret.append(
    #     f"- **PC1** is mainly driven by **{pc1_top[0]}** and **{pc1_top[1]}**."
    # )
    # interpret.append(
    #     f"- **PC2** is mainly influenced by **{pc2_top[0]}** and **{pc2_top[1]}**."
    # )
    # interpret.append(
    #     f"- PC1 explains **{pca.explained_variance_ratio_[0]*100:.1f}%** of total variance, "
    #     f"PC2 explains **{pca.explained_variance_ratio_[1]*100:.1f}%**."
    # )
    # interpret.append(
    #     f"- Grouping by **{group_option}** reveals how physical comfort conditions differ "
    #     "across seasons, climates, or building types."
    # )

    # st.markdown("\n".join(interpret))

    # # ============================================================
    # # 8. Caption
    # # ============================================================

    # st.caption(
    #     "This grouped PCA shows how physical comfort variables cluster differently across "
    #     "seasons, climate zones, or building types. It highlights dominant comfort drivers "
    #     "and reveals structural differences between environmental conditions."
    # )










    # st.text("tests")

    # df_year = df.groupby("year").agg({
    # "operative_temperature": "mean",
    # "outdoor_air_temperature": "mean"
    # }).reset_index()

    # fig, ax = plt.subplots(figsize=(12, 6))

    # ax.plot(df_year["year"], df_year["operative_temperature"], marker="o", label="Indoor (Ø)")
    # ax.plot(df_year["year"], df_year["outdoor_air_temperature"], marker="o", label="Outdoor (Ø)")

    # ax.set_xlabel("Jahr")
    # ax.set_ylabel("Temperatur (°C)")
    # ax.set_title("Durchschnittliche Innen- und Außentemperatur pro Jahr")
    # ax.grid(True)
    # ax.legend()

    # st.pyplot(fig)


    # st.subheader("Occupants’ Preferred Thermal Comfort Vote")

    # # Clean preference column
    # df_pref = df.copy()
    # df_pref["thermal_preference"] = df_pref["thermal_preference"].replace({
    #     "Unknown": None
    # })

    # # Count votes
    # pref_counts = df_pref["thermal_preference"].value_counts().reset_index()
    # pref_counts.columns = ["thermal_preference", "count"]

    # # Plot
    # fig, ax = plt.subplots(figsize=(10, 6))

    # sns.barplot(
    #     data=pref_counts,
    #     x="thermal_preference",
    #     y="count",
    #     palette="viridis",
    #     ax=ax
    # )

    # ax.set_xlabel("Thermal Preference")
    # ax.set_ylabel("Number of Votes")
    # ax.set_title("Occupants’ Preferred Thermal Comfort Vote")

    # st.pyplot(fig)


    # st.subheader("Thermal Preference vs Other Comfort Indicators")

    # fig, ax = plt.subplots(figsize=(12, 6))

    # sns.countplot(
    #     data=df,
    #     x="thermal_preference",
    #     hue="thermal_acceptability",
    #     palette="coolwarm",
    #     ax=ax
    # )

    # ax.set_xlabel("Thermal Preference")
    # ax.set_ylabel("Count")
    # ax.set_title("Thermal Preference by Acceptability")

    # st.pyplot(fig)





