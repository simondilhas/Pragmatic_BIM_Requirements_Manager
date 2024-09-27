import streamlit as st

def content_home(selected_language: str, translations: dict):
    """ The template for the content of home"""

    #Read the translations for different sections
    titel = translations['home']['titel'][selected_language]
    intro_text = translations['home']['intro'][selected_language]

    #Replace this text with your companies landing page
    st.header(titel)
    
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