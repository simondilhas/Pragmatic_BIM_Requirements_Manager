import streamlit as st

def load_readme():
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()
    return content

def main():
    st.title("Help Page")
    
    # Load and display the README content
    readme_content = load_readme()
    st.markdown(readme_content, unsafe_allow_html=True)

if __name__ == "__main__":
    main()