import streamlit as st
from pathlib import Path

from src.ui_elements import padding, footer, custom_sidebar
from src.utils import load_config, load_translations
from src.load_data import get_project_path

from organisation_data.content_home import content_home

config = load_config()
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)
FRONTEND_LANGUAGES = config.get('FRONTEND_LANGUAGES')
ORGANISATION_NAME = config.get('ORGANISATION_NAME')

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
    data_folder = get_project_path('organisation_data')
    translations = load_translations(data_folder / TRANSLATIONS_FILE)
    
    if 'language_suffix' not in st.session_state:
        st.session_state.language_suffix = MAIN_LANGUAGE

    custom_sidebar(st.session_state.language_suffix)
    
    selected_language = sidebar_select_language(translations, st.session_state.language_suffix)
    if selected_language != st.session_state.language_suffix:
        st.session_state.language_suffix = selected_language
        st.rerun() 

    #Replace this text with your companies landing page
    content_home(selected_language, translations)
   

if __name__ == "__main__":
    main()