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


st.title(" 📊 Analyse der thermischen Wahrnehmung und Einflussgrößen")

# ---------------------------------------------------------
# Tabs definieren
# ---------------------------------------------------------
tab1,tab2 = st.tabs([
    " 📊 Physikalische und subjektive Korrelationsanalyse",
    "🏢 Wichtigste Korrelationen & Gebäudebeispiele"
    ])


with tab1:
    
    st.subheader("📊 Physikalische und subjektive Einflussgrößen der thermischen Wahrnehmung")

    st.markdown("""
    Diese Analyse kombiniert **physikalische Messgrößen** und **subjektive Wahrnehmungen**, um ein vollständiges Bild darüber zu erhalten, wie Menschen thermische Bedingungen empfinden und welche Faktoren den Komfort am stärksten beeinflussen.
 
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
        <h4>🔥 Physikalische Einflussgrößen (Innenräume) </h3>

        Diese Variablen beeinflussen direkt die Wärmeabgabe und ‑aufnahme des Körpers 
        und bilden die Grundlage für die physikalische Bewertung des thermischen Komforts.

        <ul>
            <li><b>Metabolische Aktivität</b> (wie aktiv ist eine Person) </li> 
             </br>       
            <li><b>Bekleidungsisolation</b> (Art und Dicke der Kleidung)</li>
            </br>
            <li><b>Lufttemperatur</b> (Wärme der Raumluft)</li>
            </br>
            <li><b>Luftgeschwindigkeit</b> (spürbare Luftbewegung oder Luftzug) </li>
            </br>
            <li> <b>Strahlungstemperatur</b> (Wärmeabstrahlung von Wänden, Fenstern und Oberflächen) </li>
            </br>
            <li><b>Relative Luftfeuchtigkeit</b> (Feuchtegehalt der Luft)</li>
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
        und zeigen, wie Menschen die physikalischen Bedingungen tatsächlich empfinden.
         ##### 1. Thermische Empfindung (TS) 
        **Kalt  ◄────── Neutral ──────►  Heiß**  
        `-3    -2    -1    0    +1    +2    +3 `

        ##### 2. Thermische Akzeptanz (TA)
        ○ nicht akzeptabel  
        ○ akzeptabel  

        ##### 3. Thermische Präferenz (TP)  
        **Kühler ◄──────── Keine Änderung ────────► Wärmer**  
        `  -1                         0                         +1     `

        ##### 4. Thermischer Komfort (TC, ASHRAE‑Skala 1–6)  
        **Sehr unkomfortabel ◄──────────────────────► Sehr komfortabel**  
               `  1             2            3           4           5            6   `

        </ul>
        </div>
        """, unsafe_allow_html=True)


    st.subheader("🌡️ Wie stark hängen die physikalischen Umweltvariablen tatsächlich mit den vier subjektiven Wahrnehmungsparametern zusammen?")


    st.markdown("""
    <div style="display: flex; flex-direction: column; gap: 14px;">

    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 18px; height: 18px; background-color: #e63946; border-radius: 50%;"></div>
        <b>Positive Korrelation</b> – Beide Variablen bewegen sich in die gleiche Richtung.
    </div>

    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 18px; height: 18px; background-color: #457b9d; border-radius: 50%;"></div>
        <b>Negative Korrelation</b> – Die Variablen entwickeln sich gegensätzlich.
    </div>

    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 18px; height: 18px; background-color: #adb5bd; border-radius: 50%;"></div>
        <b>Nahe 0</b> – Kein relevanter Zusammenhang erkennbar.
    </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border: 1px solid #ccc;'>", unsafe_allow_html=True)



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
            plt.xticks(rotation=45, ha='right')   # 🔥 X‑Labels 45° gedreht
            plt.yticks(rotation=0)   
            st.pyplot(fig)

    with col_right:
        st.markdown("""
        <div style="
            font-size:16px;
            line-height:1.55;
        ">

        <h4 style="margin-top:0;">📌 Wichtigste Ergebnisse</h4>

        <p><b>🌡️ Lufttemperatur → Strahlungstemperatur</b><br>
        <b>r = 0.89</b><br>
        Sehr starke positive Beziehung – Beide steigen gemeinsam.</p>

        <hr>

        <p><b>😊 Thermisches Empfinden → ❄️ Thermische Präferenz</b><br>
        <b>r = -0.67</b><br>
        Je wärmer empfunden, desto stärker der Wunsch nach kühleren Bedingungen.</p>

        <hr>

        <p><b>👕 Bekleidungsisolation</b><br>
        <b>r = -0.46</b> zur Lufttemperatur<br>
        <b>r = -0.45</b> zur Strahlungstemperatur<br>
        Höhere Temperaturen → Leichtere Kleidung.</p>

        <hr>

        <p><b>❄️ Lufttemperatur → Thermische Präferenz</b><br>
        <b>r = -0.44</b><br>
        Höhere Lufttemperatur führt zu einer stärkeren Präferenz für kühlere Bedingungen.</p>

        <hr>

        <p><b>☀️ Strahlungstemperatur → Thermische Präferenz</b><br>
        <b>r = -0.41</b><br>
        Warme Oberflächen erzeugen ebenfalls den Wunsch nach einer kühleren Umgebung.</p>

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



with tab2:
    
    st.subheader("🏠 Wichtigste Korrelationen mit Gebäudebeispielen")

    st.markdown("""
    Diese Übersicht zeigt, wie physikalische Komfortparameter (z.B. Lufttemperatur,
    Strahlungstemperatur und Bekleidungsisolation) mit dem Verhalten und Empfinden
    von Personen in verschiedenen Gebäudetypen zusammenhängen.
    """)



    st.markdown("""
    <style>
    .box {
        background-color: #f7f9fc;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 18px;
        border: 1px solid #e3e6eb;
    }
    .title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .text {
        font-size: 18px;
        line-height: 1.55;
    }
    </style>

    <div class="box">
        <div class="title">🏢 Bürogebäude</div>
        <div class="text">
            • Große Glasflächen können die Luft- und Strahlungstemperatur erhöhen.<br>
            • Deshalb werden häufig kühlere Raumtemperaturen bevorzugt.
        </div>
    </div>

    <div class="box">
        <div class="title">🏠 Mehrfamilienhäuser</div>
        <div class="text">
            • Die Bekleidungsisolation passt sich oft an die Innentemperatur an.<br>
            • Sonneneinstrahlung kann die thermische Wahrnehmung beeinflussen.
        </div>
    </div>

    <div class="box">
        <div class="title">👩‍🏫 Klassenräume</div>
        <div class="text">
            • Eine hohe Personenanzahl erhöht die Wärmebelastung.<br>
            • Deshalb werden häufig Fenster geöffnet oder Ventilatoren genutzt.
        </div>
    </div>

    <div class="box">
        <div class="title">👴 Seniorenzentren</div>
        <div class="text">
            • Das thermische Empfinden spielt eine wichtige Rolle für die thermische Präferenz.<br>
            • Deshalb sind stabile und angenehme Raumtemperaturen besonders wichtig.
        </div>
    </div>
    """, unsafe_allow_html=True)

    
    st.markdown("""
    <div style="font-size:22px; line-height:1.6;">
    <b>Die Temperatur, sowohl Luft- als auch Strahlungstemperatur, ist in allen Gebäudetypen
        der wichtigste Einflussfaktor auf die thermische Wahrnehmung.<b>
    </div>
    """, unsafe_allow_html=True)


