import streamlit as st
from pathlib import Path

from src.ui_elements import padding, footer, custom_sidebar
from src.utils import load_config, load_translations
from src.load_data import get_project_path

config = load_config()

DATA_FOLDER = 'data' #better logic?
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)
FRONTEND_LANGUAGES = config.get('FRONTEND_LANGUAGES')
APP_NAME =config.get('APP_NAME', False)
TRANSLATIONS_FILE = 'translations.json'




st.set_page_config(
    page_title=APP_NAME,
    layout="wide"
)

MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)


def sidebar_select_language(translations, current_language_suffix):
    """
    Displays the language selector in the sidebar and returns the selected language.
    """
    # Create a dropdown to select the language
    selected_language = st.sidebar.selectbox(
        translations['sidebar_filters']['language_select'][current_language_suffix],
        list(FRONTEND_LANGUAGES.keys()),  # Dropdown for language codes (EN, DE, etc.)
        index=list(FRONTEND_LANGUAGES.keys()).index(current_language_suffix)  # Set current language as default
    )
    #st.sidebar.divider()
    return selected_language

def main():
    data_folder = get_project_path(DATA_FOLDER)
    translations = load_translations(data_folder / TRANSLATIONS_FILE)
    
    if 'language_suffix' not in st.session_state:
        st.session_state.language_suffix = MAIN_LANGUAGE

    custom_sidebar(st.session_state.language_suffix)
    
    selected_language = sidebar_select_language(translations, st.session_state.language_suffix)
    if selected_language != st.session_state.language_suffix:
        st.session_state.language_suffix = selected_language
        st.rerun()  
    

    #Replace this text with your companies landing page
    st.header("Pragmatic BIM Requirements Manager")
    

    intro_text = """
    Building Information Modeling (BIM) is crucial in modern design and construction, yet managing BIM requirements 
    and benefiting from BIM Data remains complex. Most BIM requirements are currently scattered across poorly structured files, 
    making them difficult to maintain, inconsistent, and challenging to follow or verify.

    Our lightweight, open-source web application is designed for efficient and pragmatic BIM requirements management, 
    offering a structured, accessible, and purpose-driven approach to defining geometric modeling and attribution guidelines.
    """

    st.subheader("The Challenge & Our Solution")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(intro_text)

    with col2:
        st.markdown("")


    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Key Features")
        st.markdown("""
        - Open Source Flexibility
        - Customization and Extension
        - Multi-view Communication
        - Backend Flexibility
        - Multi-language Publishing
        """)

    with col2:
        st.markdown("### Use Cases")
        st.markdown("""
        - Custom Requirement Definition
        - Streamlined Data Documentation
        - Effective Communication of Data Needs
        """)


    st.divider()

    st.subheader('Licensing Models')
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        #### Community Edition
        - **License:** GNU General Public License (GPL)
        - **Open Source:** Full access to source code
        - **Freedom to Modify:** Adhere to GPL obligations
        - **Community Support:** Forums and documentation
        
        
        """)

    with col2:
        st.markdown("""
        #### Enterprise Edition
        - **Proprietary License:** No GPL obligations
        - **Managed Hosting:** Azure-based, by Abstract Ltd
        - **IDS Export:** Create Information Delivery Specifications
        - **Customized Database Setup:** Tailored Setup and Data Mapping Management to other Systems
        
        
        """)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        [Start Free](https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager/)
        """)

    with col2:
        st.markdown("""
        [Contact Us](mailto:simon.dilhas@abstract.build) | [Call +41 61 563 10 85](tel:+41615631085)
        """)

    st.divider()

    st.subheader("Get Involved")
    st.markdown("""
    We welcome contributions from everyone—whether you're a seasoned developer, new to open-source, or have domain knowledge. 
    Your input is invaluable in making this project better for everyone.
    
    [Learn How to Contribute](https://github.com/simondilhas/Pragmatic_BIM_Requirements_Manager#contributing)
    """)

   

if __name__ == "__main__":
    main()