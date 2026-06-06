import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="Hrishita Sinha | Portfolio",
    page_icon="👩‍💻",
    layout="wide"
)

# Remove all Streamlit default padding/margins so the HTML fills the page
st.markdown("""
    <style>
        /* Hide Streamlit header, footer, and main block padding */
        #MainMenu, header, footer { visibility: hidden; }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        [data-testid="stAppViewContainer"] {
            padding: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load and render the portfolio HTML
html_file = "hrishita_portfolio.html"

if os.path.exists(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=900, scrolling=True)
else:
    st.error(f"❌ '{html_file}' not found. Make sure it's in the same folder as app.py.")