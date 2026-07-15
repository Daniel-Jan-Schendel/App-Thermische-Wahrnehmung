import streamlit as st
import pandas as pd
import pydeck as pdk
from streamlit_echarts import st_echarts
import seaborn as sns
import altair as alt
import numpy as np
import matplotlib.pyplot as plt 



st.set_page_config(page_title="Globale Datenanalyse", layout="wide", initial_sidebar_state="expanded")

# Load data

df_bereinigt = pd.read_csv("db_bereinigt_fertig.csv")

#st.title("Globale Datenanalyse")
#st.line_chart(df_bereinigt["DB"])
#st.dataframe(df_bereinigt)

st.title("Explorative Datenanalyse")

#st.header("Datenverteilung")

# Klima / Building



tab1, tab2= st.tabs(["Cooling typ", "Gender"])


# ==============================================================================
# 📊 TAB 5: INTERAKTIVE KOMFORTANALYSE (GRAFIKEN MIT INTERNEN NUMMERN)
# ==============================================================================
with tab1:

    st.subheader("Analyse-Leitfaden: Beeinflusst die Belüftungsart den aktuellen Parameter?")

    # Aufteilung des Layouts in zwei feste Hauptspalten für ein klares Design
    col1, col2 = st.columns([1, 2.5]) 

    with col1: 
        # Labels & Farbpaletten (Originale Struktur + Anpassung für Akzeptanz)
        tsv_labels = { -3: "–3 Sehr kalt", -2: "–2 Kalt", -1: "–1 Kühl", 0: "0 Neutral", 1: "+1 Warm", 2: "+2 Heiß", 3: "+3 Sehr heiß" } 
        tsv_colors = { -3: "#4575b4", -2: "#74add1", -1: "#abd9e9", 0: "#d9d9d9", 1: "#fdae61", 2: "#f46d43", 3: "#d73027" } 
        tp_labels = { -1: "–1 Kühler bevorzugt", 0: "0 Keine Präferenz", 1: "+1 Wärmer bevorzugt" } 
        tp_colors = { -1: "#74add1", 0: "#d9d9d9", 1: "#f46d43" } 
        tc_labels = { 1: "1 Ungemütlich", 2: "2 Leicht ungemütlich", 3: "3 Akzeptabel / Neutral", 4: "4 Leicht gemütlich", 5: "5 Gemütlich", 6: "6 Sehr gemütlich" } 
        tc_colors = { 1: "#fc8d59", 2: "#fee08b", 3: "#d9d9d9", 4: "#a6d96a", 5: "#1a9850", 6: "#006837" } 
        ta_labels = { 0: "0 Unakzeptabel", 1: "1 Akzeptabel" }
        ta_colors = { 0: "#d73027", 1: "#1a9850" }

        # Logisches Daten-Mapping (Behandlung von Nullwerten und Textzeichenfolgen)
        tp_map = {"cooler": -1, "no change": 0, "warmer": 1, "unknown": np.nan} 
        ta_map = {"acceptable": 1, "unacceptable": 0, "unknown": np.nan}

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
            
        # Plot-Funktion (Zentrierte Nummern innerhalb der Balken + Legende)
        def plot_comfort_variable(series, labels, colors, title): 
            series = pd.to_numeric(series, errors="coerce").dropna() 
            counts = series.value_counts().sort_index() 
            total = counts.sum() 
            if total == 0:
                st.info("Keine Daten für diese Auswahl verfügbar.")
                return
                
            fig, ax = plt.subplots(figsize=(8, 4.5)) 
            
            x_positions = [str(level) for level in counts.index]
            y_values = counts.values
            bar_colors = [colors[level] for level in counts.index]
            
            bars = ax.bar(x_positions, y_values, color=bar_colors)
            
            # 🌟 KORREKTUR: Platzierung der Zahlen INNERHALB der Balken (va="top")
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    # Der Versatz platziert die Zahl knapp unter die Oberkante des Balkens
                    ax.text(
                        bar.get_x() + bar.get_width()/2., 
                        height - (height * 0.05) - 0.2, 
                        f"{int(height)}", 
                        ha="center", 
                        va="top", 
                        fontsize=10, 
                        fontweight='bold', 
                        color="black" # Ändern zu "white" falls dunkle Balken die Lesbarkeit stören
                    ) 
            
            for level in sorted(counts.index):
                ax.plot([], [], color=colors[level], label=labels[level], linewidth=10)
            
            ax.set_title(title, fontweight='bold', fontsize=12, pad=12) 
            ax.set_xlabel("Comfort Level Index", fontweight='bold', fontsize=9) 
            ax.set_ylabel("Anzahl (Stimmen)", fontweight='bold', fontsize=9) 
            
            plt.xticks(rotation=0, ha="center")
            ax.legend(title="Legende (Komfortstufen)", loc="best", framealpha=0.9, fontsize=8)
            plt.tight_layout()
            st.pyplot(fig) 
            
        # Laden der originalen lokalen CSV-Datei
        df = pd.read_csv("db_bereinigt_fertig.csv") 
        df["thermal_sensation_cat"] = df["thermal_sensation"].apply(map_tsv) 
        df["thermal_preference_cat"] = df["thermal_preference"].map(tp_map) 
        df["thermal_comfort_cat"] = df["thermal_comfort"].apply(map_tc) 
        df["thermal_acceptability_cat"] = df["thermal_acceptability"].map(ta_map)
        
        st.header("Komfortanalyse") 
        
        comfort_option = st.selectbox( 
            "Komfortvariable auswählen:", ["Thermal Comfort", "Thermal Sensation", "Thermal Preference", "Thermal Acceptability"] 
        ) 
        
        geo_map = { "Region": "region", "Land": "country", "Stadt": "city" } 
        geo_option = st.selectbox("Geografische Verteilung anzeigen nach:", list(geo_map.keys())) 
        geo_colname = geo_map[geo_option] 
        
        geo_values = df[geo_colname].dropna() 
        geo_choice = st.selectbox(f"{geo_option} auswählen:", sorted(geo_values.unique())) 
        
        # Vertikale Anordnung der kaskadierenden Filter in Spalte 1 (col1)
        df['building_type'] = df['building_type'].fillna('Unknown')
        lista_building_types = sorted(df['building_type'].unique().tolist())
        building_choice = st.selectbox("Building Type auswählen:", lista_building_types)
        
        df['cooling_type'] = df['cooling_type'].fillna('Unknown')
        lista_cooling = sorted(df['cooling_type'].unique().tolist())
        cooling_choice = st.selectbox("Cooling Type auswählen:", lista_cooling)
        
        lista_generos = sorted(df['gender'].dropna().unique().tolist())
        gender_choice = st.selectbox("Gender auswählen:", lista_generos)
        
        edad_min = float(df['age'].min()) if not pd.isna(df['age'].min()) else 0.0
        edad_max = float(df['age'].max()) if not pd.isna(df['age'].max()) else 100.0
        rango_edad = st.slider("Alter (Age) Bereich:", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max), step=1.0)

        # Kaskadierende Filterlogik mit Entpacken des Slider-Bereichs
        df_geo_base = df[df[geo_colname] == geo_choice] 
        edad_min_sel, edad_max_sel = rango_edad
        
        df_geo = df_geo_base[
            (df_geo_base['building_type'] == building_choice) &
            (df_geo_base['cooling_type'] == cooling_choice) &
            (df_geo_base['gender'] == gender_choice) &
            (df_geo_base['age'] >= edad_min_sel) &  
            (df_geo_base['age'] <= edad_max_sel)    
        ]

    with col2: 
        st.subheader(f"📈 Verteilung – {comfort_option} ({geo_choice})") 
        
        # Renderizado de los gráficos univariables
        if comfort_option == "Thermal Comfort": 
            plot_comfort_variable(df_geo["thermal_comfort_cat"], tc_labels, tc_colors, f"Thermal Comfort") 
        elif comfort_option == "Thermal Sensation": 
            plot_comfort_variable(df_geo["thermal_sensation_cat"], tsv_labels, tsv_colors, f"Thermal Sensation") 
        elif comfort_option == "Thermal Preference": 
            plot_comfort_variable(df_geo["thermal_preference_cat"], tp_labels, tp_colors, f"Thermal Preference") 
        elif comfort_option == "Thermal Acceptability":
            plot_comfort_variable(df_geo["thermal_acceptability_cat"], ta_labels, ta_colors, f"Thermal Acceptability")
            
        st.markdown("---")
        
        # 🌟 EXAKTE REDAKTION: Leitfaden ohne kryptische Kürzungszeichen
        
        # Dynamischer Textblock basierend auf der selektierten Variable
        if comfort_option == "Thermal Comfort":
            st.markdown(
                "* **Einfluss auf die Behaglichkeit:** Natürlich belüftete Gebäude weisen oft eine breitere Toleranzgrenze auf, da Nutzer adaptive Anpassungsmechanismen wie das Öffnen von Fenstern nutzen.\n"
                "* **Normen-Vergleich:** Klimatisierte Räume erzielen eine engere Clusterung um den Neutralpunkt, schränken jedoch die individuelle thermische Freiheit der Gebäudenutzer stark ein.\n"
                "* **Gebäude-Verhalten:** Mechanische Belüftung stabilisiert das Komfortniveau im Sommer, kann jedoch bei unzureichender Wartung zu einer erhöhten Unzufriedenheit führen."
            )
        elif comfort_option == "Thermal Sensation":
            st.markdown(
                "* **Thermische Wahrnehmung:** Die Belüftungsart steuer direkt die Luftgeschwindigkeit und die operative Temperatur, was die sensorischen Stimmen massiv verschiebt.\n"
                "* **Erwartungshaltung:** In klimatisierten Räumen erwarten Nutzer eine konstante Temperatur, weshalb kleine Abweichungen sofort als extrem warm oder kalt empfunden werden.\n"
                "* **Demografischer Faktor:** Die Kombination aus Belüftungsart und Alter zeigt, dass ältere Gruppen in natürlich belüfteten Zonen sensibler auf Zugluft reagieren."
            )
        elif comfort_option == "Thermal Preference":
            st.markdown(
                "* **Nutzerpräferenz:** In natürlich belüfteten Gebäuden tolerieren die Befragten höhere Innentemperaturen und äußern seltener den Wunsch nach intensiver Kühlung.\n"
                "* **Klimatisierungs-Effekt:** Nutzer in mechanisch gekühlten Räumen neigen statistisch dazu, permanent einen kühleren Zustand wie kühler bevorzugt zu fordern.\n"
                "* **Saisonaler Einfluss:** Die Präferenzkurve flacht ab, wenn das Gebäude den Nutzern erlaubt, die Luftbewegung eigenständig zu regulieren."
            )
        elif comfort_option == "Thermal Acceptability":
            st.markdown(
                "* **Akzeptanz-Verhalten:** Die thermische Akzeptanz sinkt in klimatisierten Räumen drastisch, wenn die relative Luftfeuchtigkeit außerhalb des optimalen Bereichs liegt.\n"
                "* **Anpassungspotenzial:** Natürlich belüftete Strukturen erzielen trotz höherer Absoluttemperaturen eine hohe Akzeptanzrate aufgrund des psychologischen Gewöhnungseffekts.\n"
                "* **Statistische Relevanz:** Nullwerte treten vermehrt in mechanischen Systemen auf, was auf eine geringere Interaktion der Nutzer mit der Gebäudetechnik hinweist."
            ) 

with tab2:

    st.text("sdsds")

