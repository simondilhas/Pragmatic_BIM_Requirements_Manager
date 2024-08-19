# [Original license and setup instructions remain unchanged]

import streamlit as st
from src.ui_elements import padding, footer

st.set_page_config(
    page_title="Elementplan",
    layout="wide"
)

def main():
    st.header("Pragmatic Elementplan and Modeling Guidelines")

    intro_text = """
    Most BIM requirements are currently scattered across poorly structured files, making them difficult to maintain, 
    inconsistent, and challenging to follow or verify. These fragmented requirements often lose alignment with a 
    company's value creation processes, leading to inefficiencies and misaligned objectives.

    This open-source project offers a structured, accessible, and purpose-driven approach to defining geometric 
    modeling and attribution guidelines.
    """

    st.subheader("Main Components")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(intro_text)
        

    with col2:
        st.markdown("""
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
        
        [Start Free](https://github.com/simondilhas/pragmatic_element_plan)
        """)

    with col2:
        st.markdown("""
        #### Enterprise Edition
        - **Proprietary License:** No GPL obligations
        - **Managed Hosting:** Azure-based, by Abstract Ltd
        - **IDS Export:** Create Information Delivery Specifications
        - **Customized Database Setup:** Tailored setup and Data Mapping Management to other Systems
        
        [Contact Us](mailto:simon.dilhas@abstract.build) | [Call +41 61 563 10 85](tel:+41615631085)
        """)

    footer()

if __name__ == "__main__":
    main()