# This script is part of an open-source project licensed under the GNU Lesser General Public License v2.1.
# It uses several third-party libraries with their own licenses:
#
# 1. Streamlit - Apache License 2.0
#    https://github.com/streamlit/streamlit/blob/develop/LICENSE
#
# 2. Plotly - MIT License
#    https://github.com/plotly/plotly.py/blob/master/LICENSE.txt
#
# 3. Pandas - BSD 3-Clause License
#    https://github.com/pandas-dev/pandas/blob/master/LICENSE
#
# To comply with these licenses, please follow these steps:
#
# 1. Keep this header in all source files.
# 2. Include the full text of the GNU LGPL v2.1 in a file named 'LICENSE' in your project root.
# 3. In a file named 'THIRD_PARTY_LICENSES' in your project root, include the full license texts for 
#    Streamlit, Plotly, and Pandas. You can copy these from the URLs provided above.
# 4. If distributing the software, ensure all license texts are included with the distribution.
#
# Streamlit - Copyright (c) 2019 Streamlit Inc.
# Plotly - Copyright (c) 2016-2018 Plotly, Inc
# Pandas - Copyright (c) 2008-2011, AQR Capital Management, LLC, Lambda Foundry, Inc. and PyData Development Team
#
# Setup Instructions:
# 1. Ensure you have Python 3.7 or later installed on your system.
#
# 2. It's recommended to use a virtual environment. Create and activate one:
#    python -m venv venv
#    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
#
# 3. Install the required packages using the provided requirements.txt file:
#    pip install -r requirements.txt
#
# 4. If you need to update requirements.txt (for developers):
#    pip freeze > requirements.txt
#
# 5. To run the application:
#    streamlit run home.py

import streamlit as st
from src.ui_elements import padding, footer

st.set_page_config(
    page_title="Elementplan",
    layout="wide"
)

def main():
    
    #padding()
    st.header("Pragmatic Elementplan and Modeling Guidlines ")
    col1, col2  = st.columns([5,5])

    with col1:

        st.markdown("""
            Most BIM requirements are currently scattered across poorly structured Excel or Word files, 
            making them difficult to maintain, inconsistent, and challenging to follow or verify.
            These fragmented requirements often loose alignment with a company's value creation processes, 
            leading to inefficiencies and misaligned business objectives.

            This open-source project takes a different approach by offering an interface to
            define a more structured, accessible, and purpose-driven set of guidelines for geometric modeling and attribution.

            This project consists these main components:

            """
        )

    with col2:
        st.write("")

    col1, col2 = st.columns([5,5])

    with col1:
        st.markdown("""
            **1. Viewer for Modeling Guidelines**

            A user-friendly viewer that allows stakeholders to easily communicate, access and understand the BIM modeling guidelines. This viewer presents the guidelines in a clear and structured manner, ensuring that they are easy to follow and apply consistently across organizations and projects. 

            To create your own instance clone the Github project and adapt to your specific needs.

    """
    )

    with col2:
        st.markdown("""
            **2. Structured Approach for Defining Requirements**

            It beginns with:
            - Defining the Purpose and Workflow: Start by identifying the purpose and workflow that the requirement supports.
            - Assigning Responsibility: Specify who should deliver the information and in which model or file.
            - Detailing Requirements: Outline what needs to be modeled and at what quality to achieve the desired outcome.
            - Specifying Attributes: Identify the necessary attributes to achieve the business value.

        """
        )
        
    st.divider()
    
    st.subheader('Licencing models')



    col1, col2 = st.columns([5,5])

    with col1:
        st.markdown("""
        #### **Community Edition**
        - **License:** GNU General Public License (GPL)
        - **Open Source:** Full access to the source code, fostering community contributions and transparency.
        - **Freedom to Modify:** Users can freely modify, distribute, and use the software as long as they adhere to GPL obligations (e.g., sharing source code of any modifications).
        - **Community Support:** Access to community-driven support through forums, documentation, and community discussions.

        """
        )
        
    with col2:
        st.markdown("""
            #### **Enterprise Edition**
            - **No GPL Obligation, Proprietary License:** The enterprise version is available under a proprietary license, allowing your customers to keep their code and modifications private without any GPL obligations.
            - **Peace of Mind:** Ideal for businesses that need to maintain proprietary aspects of their software while leveraging your platform.
            - **Managed Hosting:** Enterprise customers enjoy a fully managed hosting service managed by Abstract ltd on Azur , ensuring optimal performance, scalability, and security.
            - **IDS Export:** Easily create Information Delivery Specification (IDS) for streamlined data quality checks.
            - **Customized Database Configuration:** Tailored database setup to manage requirements user-friendly, including mapping tables and logics to other systems.
            - **Seamless Integration:** Supports exporting data in formats compatible with your existing systems and workflows.
        """
        )

    col1, col2 = st.columns([5,5])
    with col1:
        # Create a markdown link for "Start Free"
        st.markdown("[Start Free](https://github.com/simondilhas/pragmatic_element_plan)", unsafe_allow_html=True)

    with col2:
        # Create a markdown link for "Contact Simon"
        st.markdown("[Email simon.dilhas@abstract.build](mailto:simon.dilhas@abstract.build) or [Call +41 61 563 10 85](tel:+41615631085)", unsafe_allow_html=True)

        #st.markdown("[Call Simon](tel:+41615631085)", unsafe_allow_html=True)


    footer()

if __name__ == "__main__":
    main()