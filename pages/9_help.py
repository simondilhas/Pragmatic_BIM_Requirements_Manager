import streamlit as st
from src.ui_elements import custom_sidebar
from src.utils import load_config

config = load_config()
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)

def load_readme():
    with open("readme.md", "r", encoding="utf-8") as file:
        content = file.read()
    return content

def main():
    if 'language_suffix' not in st.session_state:
        st.session_state['language_suffix'] = MAIN_LANGUAGE
    
    language_suffix = st.session_state['language_suffix']

    custom_sidebar(language_suffix) 
   
    # Load and display the README content
    readme_content = load_readme()
    st.markdown(readme_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()