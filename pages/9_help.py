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
    custom_sidebar(MAIN_LANGUAGE)  
   
    # Load and display the README content
    readme_content = load_readme()
    st.markdown(readme_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()