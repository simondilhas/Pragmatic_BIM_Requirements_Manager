import streamlit as st
from src.ui_elements import padding, footer

st.set_page_config(
    page_title="BBL Elementplan",
    #page_icon="Pragmatic_fav.png", 
    layout="wide"
)

def main():
    
    #padding()
    st.header("BBL Elementplan & Modellierungsdefinitionen")

    col1, col2,= st.columns(2,gap='large')

    with col1:
        st.markdown("""
    Der Elementplan legt die Modelldatenanforderungen des BBL fest und dient als Grundlage für die Dokumentation an den Betrieb sowie für die projektübergreifende bauherrenseitige Qualitätssicherung.

    Für eine erfolgreiche Projektierung sind möglicherweise zusätzliche Modelle, Elemente und Attribute erforderlich, die über die Vorgaben des BBL hinausgehen. Die Verantwortung für die Erfassung, Pflege und Prüfung dieser zusätzlichen Informationen liegt eigenständig beim Projektverfasser.
""")
        
    with col2:
        st.markdown("""""")

    col1, col2, col3 = st.columns(3,gap='large')

    with col1:
        st.button("Deutsche Version")

    with col2:
        st.button("Englisch Version")

    with col3:
        st.button("Version française")

    

    footer()

if __name__ == "__main__":
    main()