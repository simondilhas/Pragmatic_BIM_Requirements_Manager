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
    st.header("")

    

    footer()

if __name__ == "__main__":
    main()