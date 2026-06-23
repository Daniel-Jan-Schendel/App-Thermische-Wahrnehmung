import streamlit as st

st.set_page_config(page_title="Introduction - ASHRAE", layout="wide",initial_sidebar_state="expanded")




st.title("Introduction to the Global Thermal Comfort Database")

st.write("""
The Global Thermal Comfort Database is an international collection of field studies 
that document how people experience thermal conditions in real buildings across 
different climates, seasons, and building types. The database integrates thousands 
of observations that include environmental measurements, occupant surveys, and 
contextual metadata. 

Its purpose is to support research on human thermal comfort, adaptive behavior, 
and indoor environmental quality by providing a unified and standardized dataset 
that researchers can analyze and compare across regions.
""")

st.subheader("Why the Data Collection Method Matters")

st.write("""
Understanding how the data was collected is essential for interpreting the results 
correctly. Each study in the database may differ in terms of measurement equipment, 
survey methods, building characteristics, and climatic context. These differences 
influence how occupants perceive their environment and how comfort models should 
be applied.

Documenting the data collection process ensures:

- **Transparency**: Researchers can evaluate the reliability and limitations of each dataset.
- **Reproducibility**: Other analysts can replicate or extend the study using the same methods.
- **Comparability**: Differences between studies can be understood rather than mistaken for 
    behavioral or climatic effects.
- **Correct interpretation**: Comfort responses depend on context—building type, season, 
    climate, and occupant expectations all matter.

For these reasons, the metadata describing how each study was conducted is just as 
important as the measurements themselves.
""")

st.subheader("Structure of the Database")

st.write("""
The database is organized into two main components:

- **Metadata**: Information about the study, building, climate, and measurement methods.
- **Measurements**: Individual observations including temperatures, humidity, air speed, 
    clothing levels, metabolic rates, and subjective comfort votes.

This structure allows users to link each measurement to its environmental and contextual 
background, enabling multi‑scale analysis and robust interpretation.
""")




st.subheader("Why is it important to study this topic today?")

st.write("""
🌍 **1. Climate change and more frequent heatwaves**  
Due to climate change, extreme temperatures are becoming more common. Buildings must 
protect people under these conditions and maintain comfort. Understanding thermal 
comfort helps us design better and more resilient buildings.
""")

st.write("""
⚡ **2. Energy crisis and the need for efficiency**  
Heating, cooling, and ventilation account for **30–50%** of a building’s total energy use.  
If we can better predict how people perceive thermal conditions, we can:
- Save energy  
- Reduce operational costs  
- Avoid overheating or overcooling  

Thermal comfort models (e.g., based on ASHRAE data) are essential for this.
""")

st.write("""
🧠 **3. Artificial intelligence in buildings**  
Modern buildings are becoming *smart*. Data such as those from the ASHRAE Global Thermal 
Comfort Database enable:
- AI models that predict comfort  
- Automatic adjustment of HVAC systems  
- Personalized indoor climate control  

This makes the topic highly relevant today.
""")

st.write("""
🏢 **4. Health, wellbeing, and productivity**  
Thermal comfort influences:
- Concentration  
- Performance  
- Health  
- User satisfaction  

Companies and public institutions increasingly focus on indoor wellbeing.
""")

st.write("""
🌐 **5. Sustainable building and international standards**  
ASHRAE standards such as **55**, **62.1**, and **90.1** are globally important.  
Anyone working in architecture, building engineering, or research will encounter them.

This topic matters today because it connects people, energy, climate, technology, 
and health. It is a research field with direct impact on the future of our buildings 
and cities.
""")
