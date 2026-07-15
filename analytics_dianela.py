import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches  # 🌟 Importiert für die perfekte Skalierung der Legenden-Quadrate
import streamlit as st
import pandas as pd

# ==============================================================================
# 🛠️ 1. GLOBALE FUNKTIONEN (MÜSSEN AN ERSTER STELLE STEHEN)
# ==============================================================================
def map_tsv(v): 
    if pd.isna(v): return None 
    if v <= -2.5: return -3 
    elif v <= -1.5: return -2 
    elif v <= -0.5: return -1 
    elif v < 0.5: return 0 
    elif v < 1.5: return 1 
    elif v < 2.5: return 2 
    else: return 3 

def map_tc(v): 
    if pd.isna(v): return None 
    if v < 1.5: return 1 
    elif v < 2.5: return 2 
    elif v < 3.5: return 3 
    elif v < 4.5: return 4 
    elif v < 5.5: return 5 
    else: return 6 

def custom_geo_sort(values_list):
    def sort_logic(x):
        item_str = str(x).lower().strip()
        if item_str == "americas":
            return (0, item_str)
        elif "unknown" in item_str or "unbekannt" in item_str or "nan" in item_str:
            return (2, item_str)
        else:
            return (1, item_str)
    return sorted(values_list, key=sort_logic)

# 📊 PLOT-FUNKTION: Jetzt mit perfekt formatierten Legenden ohne Überlappung
def plot_comfort_variable(series, labels, colors, title): 
    series = pd.to_numeric(series, errors="coerce").dropna() 
    counts = series.value_counts().sort_index() 
    total = counts.sum() 
    if total == 0:
        return False
        
    fig, ax = plt.subplots(figsize=(6, 4.2)) 
    x_positions = [str(level) for level in counts.index]
    y_values = counts.values
    bar_colors = [colors[level] for level in counts.index]
    
    bars = ax.bar(x_positions, y_values, color=bar_colors)
    
    # Platzierung der Zahlen INNERHALB der Balken (va="top")
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width()/2., 
                height - (height * 0.05) - 0.2, 
                f"{int(height)}", 
                ha="center", va="top", fontsize=9, fontweight='bold', color="black"
            ) 
    
    # 🌟 KORREKTUR: Verwendung von mpatches.Patch anstelle von dicken Linien,
    # um unschöne Überlappungen in kleinen Diagrammen komplett zu eliminieren.
    legend_patches = []
    for level in sorted(counts.index):
        patch = mpatches.Patch(color=colors[level], label=labels[level])
        legend_patches.append(patch)
    
    ax.set_title(title, fontweight='bold', fontsize=11, pad=10) 
    ax.set_xlabel("Comfort Level Index", fontweight='bold', fontsize=9) 
    ax.set_ylabel("Anzahl (Stimmen)", fontweight='bold', fontsize=9) 
    
    plt.xticks(rotation=0, ha="center")
    
    # 🌟 KORREKTUR: handletextpad sorgt für ausreichend Platz zwischen Quadrat und Text
    ax.legend(
        handles=legend_patches, 
        title="Legende", 
        loc="best", 
        framealpha=0.9, 
        fontsize=8,
        handletextpad=0.8,
        handlelength=1.2
    )
    
    plt.tight_layout()
    st.pyplot(fig, width=550)
    return True

# ==============================================================================
# 🎨 2. DICTIONARIES UND CONFIGURATION
# ==============================================================================
tsv_labels = { -3: "–3 Sehr kalt", -2: "–2 Kalt", -1: "–1 Kühl", 0: "0 Neutral", 1: "+1 Warm", 2: "+2 Heiß", 3: "+3 Sehr heiß" } 
tsv_colors = { -3: "#4575b4", -2: "#74add1", -1: "#abd9e9", 0: "#d9d9d9", 1: "#fdae61", 2: "#f46d43", 3: "#d73027" } 
tp_labels = { -1: "–1 Kühler bevorzugt", 0: "0 Keine Präferenz", 1: "+1 Wärmer bevorzugt" } 
tp_colors = { -1: "#74add1", 0: "#d9d9d9", 1: "#f46d43" } 
tc_labels = { 1: "1 Ungemütlich", 2: "2 Leicht ungemütlich", 3: "3 Akzeptabel / Neutral", 4: "4 Leicht gemütlich", 5: "5 Gemütlich", 6: "6 Sehr gemütlich" } 
tc_colors = { 1: "#fc8d59", 2: "#fee08b", 3: "#d9d9d9", 4: "#a6d96a", 5: "#1a9850", 6: "#006837" } 
ta_labels = { 0: "0 Unakzeptabel", 1: "1 Akzeptabel" }
ta_colors = { 0: "#d73027", 1: "#1a9850" }

tp_map = {"cooler": -1, "no change": 0, "warmer": 1, "unknown": np.nan} 
ta_map = {"acceptable": 1, "unacceptable": 0, "unknown": np.nan}

# REITER INITIALISIERUNG
tab1, tab2 = st.tabs(["Cooling typ", "Gender"])

# ==============================================================================
# 💾 3. DATENLADUNG & VARIABLEN-MAPPING
# ==============================================================================
df = pd.read_csv("db_bereinigt_final.csv")
df["thermal_sensation_cat"] = df["thermal_sensation"].apply(map_tsv) 
df["thermal_preference_cat"] = df["thermal_preference"].map(tp_map) 
df["thermal_comfort_cat"] = df["thermal_comfort"].apply(map_tc) 
df["thermal_acceptability_cat"] = df["thermal_acceptability"].map(ta_map)

# ==============================================================================
# 📊 TAB 1: GEOGRAFISCHE KOMFORTANALYSE (DINAMISCHES 2x2 NEBENEINANDER LAYOUT)
# ==============================================================================
with tab1:
    st.subheader("Analyse-Leitfaden: Beeinflusst die Belüftungsart den aktuellen Parameter?")
    
    geo_map = { "Region": "region", "Land": "country", "Stadt": "city" } 
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        geo_option = st.selectbox("Geografische Verteilung anzeigen nach:", list(geo_map.keys()), key="geo_opt_t1") 
        geo_colname = geo_map[geo_option] 
    with col_f2:
        raw_geo_values_t1 = df[geo_colname].dropna().unique().tolist()
        sorted_geo_values_t1 = custom_geo_sort(raw_geo_values_t1)
        geo_choice = st.selectbox(f"{geo_option} auswählen:", sorted_geo_values_t1, key="geo_cho_t1") 
    with col_f3:
        df['building_type'] = df['building_type'].fillna('Unknown')
        lista_building_types = sorted(df['building_type'].unique().tolist())
        building_choice = st.selectbox("Building Type auswählen:", lista_building_types, key="bld_t1")

    df_t1_filtered = df[
        (df[geo_colname] == geo_choice) & 
        (df['building_type'] == building_choice)
    ]
    
    st.markdown("---")
    st.markdown(f"### 📈 Thermische Verteilung in {geo_choice} ({building_choice})")
    
    row1_has_data1 = not pd.to_numeric(df_t1_filtered["thermal_comfort_cat"], errors="coerce").dropna().empty
    row1_has_data2 = not pd.to_numeric(df_t1_filtered["thermal_sensation_cat"], errors="coerce").dropna().empty
    
    if row1_has_data1 and row1_has_data2:
        r1_col1, r1_col2 = st.columns(2)
        with r1_col1:
            plot_comfort_variable(df_t1_filtered["thermal_comfort_cat"], tc_labels, tc_colors, "1. Thermal Comfort Verteilung")
            st.markdown("**Analyse-Leitfaden (Comfort):** Natürlich belüftete Gebäude weisen oft breitere Toleranzgrenzen auf, da Nutzer adaptive Anpassungsmechanismen wie das Öffnen von Fenstern nutzen.")
        with r1_col2:
            plot_comfort_variable(df_t1_filtered["thermal_sensation_cat"], tsv_labels, tsv_colors, "2. Thermal Sensation Verteilung")
            st.markdown("**Analyse-Leitfaden (Sensation):** Die Belüftungsart steuer direkt die Luftgeschwindigkeit und die operative Temperatur, was die sensorischen Stimmen massiv verschiebt.")
    elif row1_has_data1:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t1_filtered["thermal_comfort_cat"], tc_labels, tc_colors, "1. Thermal Comfort Verteilung")
            st.markdown("**Analyse-Leitfaden (Comfort):** Natürlich belüftete Gebäude weisen oft breitere Toleranzgrenzen auf, da Nutzer adaptive Anpassungsmechanismen wie das Öffnen von Fenstern nutzen.")
    elif row1_has_data2:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t1_filtered["thermal_sensation_cat"], tsv_labels, tsv_colors, "2. Thermal Sensation Verteilung")
            st.markdown("**Analyse-Leitfaden (Sensation):** Die Belüftungsart steuer direkt die Luftgeschwindigkeit und die operative Temperatur, was die sensorischen Stimmen massiv verschiebt.")

    st.markdown("---")

    row2_has_data3 = not pd.to_numeric(df_t1_filtered["thermal_preference_cat"], errors="coerce").dropna().empty
    row2_has_data4 = not pd.to_numeric(df_t1_filtered["thermal_acceptability_cat"], errors="coerce").dropna().empty
    
    if row2_has_data3 and row2_has_data4:
        r2_col1, r2_col2 = st.columns(2)
        with r2_col1:
            plot_comfort_variable(df_t1_filtered["thermal_preference_cat"], tp_labels, tp_colors, "3. Thermal Preference Verteilung")
            st.markdown("**Analyse-Leitfaden (Preference):** In natürlich belüfteten Gebäuden tolerieren die Befragten höhere Innentemperaturen. Nutzer in mechanisch gekühlten Räumen fordern permanent kühlere Zustände.")
        with r2_col2:
            plot_comfort_variable(df_t1_filtered["thermal_acceptability_cat"], ta_labels, ta_colors, "4. Thermal Acceptability Verteilung")
            st.markdown("**Analyse-Leitfaden (Acceptability):** Die thermische Akzeptanz sinkt in klimatisierten Räumen drastisch, wenn die relative Luftfeuchtigkeit außerhalb des optimalen Bereichs liegt.")
    elif row2_has_data3:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t1_filtered["thermal_preference_cat"], tp_labels, tp_colors, "3. Thermal Preference Verteilung")
            st.markdown("**Analyse-Leitfaden (Preference):** In natürlich belüfteten Gebäuden tolerieren die Befragten höhere Innentemperaturen. Nutzer in mechanisch gekühlten Räumen fordern permanent kühlere Zustände.")
    elif row2_has_data4:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t1_filtered["thermal_acceptability_cat"], ta_labels, ta_colors, "4. Thermal Acceptability Verteilung")
                
# ==============================================================================
# 👥 TAB 2: DEMOGRAFISCHE KOMFORTANALYSE (STRIKT GENDER & ALTER IN 2x2 GRID)
# ==============================================================================
with tab2:
    # Synchronisation der Datenquelle mit dem Hauptdatensatz
    #df = df_bereinigt
    
    st.subheader("Analyse-Leitfaden: Beeinflusst die Belüftungsart den aktuellen Parameter?")
    
    # Aufteilung der Benutzeroberfläche in Filter und interaktiven Grafikbereich
    col_t2_f1, col_t2_f2, col_t2_f3, col_t2_f4 = st.columns(4)
    
    with col_t2_f1:
        geo_option_t2 = st.selectbox("Geografische Verteilung anzeigen nach:", list(geo_map.keys()), key="geo_opt_t2") 
        geo_colname_t2 = geo_map[geo_option_t2] 
    with col_t2_f2:
        # 🌟 Sortierung: Americas immer zuerst, Unknown am Ende (Tab 2)
        raw_geo_values_t2 = df[geo_colname_t2].dropna().unique().tolist()
        sorted_geo_values_t2 = custom_geo_sort(raw_geo_values_t2)
        geo_choice_t2 = st.selectbox(f"{geo_option_t2} auswählen:", sorted_geo_values_t2, key="geo_cho_t2") 
    with col_t2_f3:
        building_choice_t2 = st.selectbox("Building Type auswählen:", lista_building_types, key="bld_t2")
    with col_t2_f4:
        # Genderspezifische Zuordnung inklusive automatischer Bereinigung von Nullwerten
        #df['gender'] = df['gender'].fillna('indefizierte / unbekannt')
        #lista_genders = sorted(df['gender'].unique().tolist())
        #gender_choice = st.selectbox("Gender auswählen:", lista_genders, key="gen_t2")
        df['gender'] = df['gender'].fillna('unknown')
        
        # Erstellt die exakte Wunsch-Reihenfolge basierend auf den vorhandenen Werten
        raw_genders = df['gender'].unique().tolist()
        
        def gender_sort_logic(x):
            g_str = str(x).lower().strip()
            if "female" in g_str:
                return (0, g_str)
            elif "male" in g_str:
                return (1, g_str)
            elif "undefined" in g_str or "indefizierte" in g_str:
                return (2, g_str)
            else:
                return (3, g_str) # unknown und andere nulos landen ganz unten
                
        lista_genders = sorted(raw_genders, key=gender_sort_logic)
        gender_choice = st.selectbox("Gender auswählen:", lista_genders, key="gen_t2")        
        
    # Kontinuierlicher numerischer Altersschieberegler für präzise Kohorten-Analysen
    edad_min = float(df['age'].min()) if not pd.isna(df['age'].min()) else 0.0
    edad_max = float(df['age'].max()) if not pd.isna(df['age'].max()) else 100.0
    rango_edad = st.slider("Alter (Age) Bereich:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max), step=1.0, key="sld_t2")
    
    # Ausführung der kaskadierenden Datenfilterung im Hintergrund
    edad_min_sel, edad_max_sel = rango_edad
    df_t2_filtered = df[
        (df[geo_colname_t2] == geo_choice_t2) & 
        (df['building_type'] == building_choice_t2) &
        (df['gender'] == gender_choice) &
        (df['age'] >= edad_min_sel) &
        (df['age'] <= edad_max_sel)
    ]
    
    st.markdown("---")
    st.header(f"👥 Demografisches Profil ({gender_choice}, Age: {int(edad_min_sel)}-{int(edad_max_sel)})")
    
    # 🌟 FILA 1 DEMOGRAFÍA: Steuerung und automatische Zentrierung bei fehlenden Daten
    t2_has_data1 = not pd.to_numeric(df_t2_filtered["thermal_comfort_cat"], errors="coerce").dropna().empty
    t2_has_data2 = not pd.to_numeric(df_t2_filtered["thermal_sensation_cat"], errors="coerce").dropna().empty
    
    if t2_has_data1 and t2_has_data2:
        t2_r1c1, t2_r1c2 = st.columns(2)
        with t2_r1c1:
            plot_comfort_variable(df_t2_filtered["thermal_comfort_cat"], tc_labels, tc_colors, "1. Thermal Comfort (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die demografische Verteilung zeigt, wie das Zusammenspiel aus Lüftungssystem und Genderspezifikation das Wohlbefinden prägt. Bestimmte Gruppen zeigen eine höhere Toleranz in adaptiven Umgebungen.*")
        with t2_r1c2:
            plot_comfort_variable(df_t2_filtered["thermal_sensation_cat"], tsv_labels, tsv_colors, "2. Thermal Sensation (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Altersabhängige Stoffwechselraten verändern die sensorische Wahrnehmung der operativen Raumtemperatur drastisch. Ältere Kohorten reagieren in frei belüfteten Räumen empfindlicher auf Luftbewegungen.*")
    elif t2_has_data1:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t2_filtered["thermal_comfort_cat"], tc_labels, tc_colors, "1. Thermal Comfort (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die demografische Verteilung zeigt, wie das Zusammenspiel aus高度 lüftungssystem und Genderspezifikation das Wohlbefinden prägt. Bestimmte Gruppen zeigen eine höhere Toleranz in adaptiven Umgebungen.*")
    elif t2_has_data2:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t2_filtered["thermal_sensation_cat"], tsv_labels, tsv_colors, "2. Thermal Sensation (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Altersabhängige Stoffwechselraten verändern die sensorische Wahrnehmung der operativen Raumtemperatur drastisch. Ältere Kohorten reagieren in frei belüfteten Räumen empfindlicher auf Luftbewegungen.*")

    st.markdown("---")

    # 🌟 FILA 2 DEMOGRAFÍA: Steuerung und automatische Zentrierung bei fehlenden Daten
    t2_has_data3 = not pd.to_numeric(df_t2_filtered["thermal_preference_cat"], errors="coerce").dropna().empty
    t2_has_data4 = not pd.to_numeric(df_t2_filtered["thermal_acceptability_cat"], errors="coerce").dropna().empty
    
    if t2_has_data3 and t2_has_data4:
        t2_r2c1, t2_r2c2 = st.columns(2)
        with t2_r2c1:
            plot_comfort_variable(df_t2_filtered["thermal_preference_cat"], tp_labels, tp_colors, "3. Thermal Preference (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die Neigung zur Anforderung kühlerer Luftströme variiert signifikant zwischen den biologischen Geschlechtern, wobei mechanische Kühlsysteme oft zu ungleichmäßigen Präferenz-Clustern führen.*")
        with t2_r2c2:
            plot_comfort_variable(df_t2_filtered["thermal_acceptability_cat"], ta_labels, ta_colors, "4. Thermal Acceptability (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die Raumklima-Akzeptanz stabilisiert sich bei Gruppen, denen das Gebäude eine hohe adaptive Freiheit gewährt. Unbekannte demografische Variablen korrelieren oft mit standardisierter mechanischer Belüftung.*")
    elif t2_has_data3:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t2_filtered["thermal_preference_cat"], tp_labels, tp_colors, "3. Thermal Preference (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die Neigung zur Anforderung kühlerer Luftströme variiert signifikant zwischen den biologischen Geschlechtern, wobei mechanische Kühlsysteme oft zu ungleichmäßigen Präferenz-Clustern führen.*")
    elif t2_has_data4:
        _, center_col, _ = st.columns([0.25, 1.5, 0.25])
        with center_col:
            plot_comfort_variable(df_t2_filtered["thermal_acceptability_cat"], ta_labels, ta_colors, "4. Thermal Acceptability (Demografie)")
            st.markdown("**Analyse-Leitfaden:** *Die Raumklima-Akzeptanz stabilisiert sich bei Gruppen, denen das Gebäude eine hohe adaptive Freiheit gewährt. Unbekannte demografische Variablen korrelieren oft mit standardisierter mechanischer Belüftung.*")


