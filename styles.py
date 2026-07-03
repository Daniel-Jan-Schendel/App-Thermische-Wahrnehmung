import streamlit as st

def apply_styles():
    st.markdown("""
        <style>

        /* ------------------------------
           GLOBAL FONT & TEXT SIZE
        ------------------------------ */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif !important;
            font-size: 17px !important;
            color: #333333 !important;
        }

        /* ------------------------------
           HEADERS
        ------------------------------ */
        h1 {
            font-size: 38px !important;
            font-weight: 700 !important;
            color: #1A237E !important;
        }

        h2 {
            font-size: 30px !important;
            font-weight: 600 !important;
            color: #283593 !important;
        }

        h3 {
            font-size: 24px !important;
            font-weight: 600 !important;
            color: #303F9F !important;
        }

        /* ------------------------------
           SIDEBAR
        ------------------------------ */
        [data-testid="stSidebar"] {
            background-color: #1E88E5 !important;
        }

        [data-testid="stSidebar"] * {
            color: white !important;
            font-size: 18px !important;
        }

        /* ------------------------------
           MAIN BACKGROUND
        ------------------------------ */
        .stApp {
            background-color: #FAFAFA !important;
        }

        /* ------------------------------
           CARDS (st.info, st.success, etc.)
        ------------------------------ */
        .stAlert {
            border-radius: 10px !important;
            padding: 15px !important;
        }

        /* ------------------------------
           DATAFRAMES
        ------------------------------ */
        .dataframe {
            font-size: 15px !important;
        }

        /* ------------------------------
           TABS
        ------------------------------ */
        .stTabs [role="tab"] {
            font-size: 18px !important;
            padding: 12px 20px !important;
        }

        .stTabs [role="tab"][aria-selected="true"] {
            color: #1A237E !important;
            font-weight: 700 !important;
        }
                
        /* ------------------------------
           REDUCE TOP PADDING (TITLE HIGHER)
        ------------------------------ */
        .block-container {
            padding-top: 1rem !important;
        }
                
        /* ------------------------------
        FIX: TITLE TOO LOW IN WIDE MODE
        ------------------------------ */
        .block-container {
            padding-top: 0rem !important;
        }

        .main {
            padding-top: 0rem !important;
        }

        </style>
    """, unsafe_allow_html=True)
