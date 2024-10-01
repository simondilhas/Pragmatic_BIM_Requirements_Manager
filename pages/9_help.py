"""
9_help.py

This module provides a Streamlit page for displaying frequently asked questions and answers.
It loads content from a README file and presents it using Streamlit's markdown functionality.
"""

import streamlit as st
from typing import Dict, Any
from src.ui_elements import custom_sidebar
from src.utils import load_config

def load_help_content() -> str:
    """
    Load the content of the README file.

    Returns:
        str: The content of the README file.
    """
    with open("readme.md", "r", encoding="utf-8") as file:
        return file.read()

def main() -> None:
    """
    Main function to run the Streamlit app for the help page.
    """
    config: Dict[str, Any] = load_config()
    main_language: str = config.get('MAIN_LANGUAGE', '')

    if 'language_suffix' not in st.session_state:
        st.session_state['language_suffix'] = main_language

    language_suffix: str = st.session_state['language_suffix']
    custom_sidebar(language_suffix)

    help_content: str = load_help_content()
    st.markdown(help_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()