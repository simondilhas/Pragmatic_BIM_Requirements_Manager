import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import os
import uuid

from src.ui_elements import padding, footer

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

@st.cache_data
def get_unique_values(df, column):
    return df[column].unique()

def configure_grid(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True, editable=False)

    column_configs = {
        "Attribut Beschreibung": {"minWidth": 200, "width": 250},
        "Ifc Attribut": {"minWidth": 150, "width": 180},
        "Eigenschaften Gruppe (Pset)": {"minWidth": 200, "width": 250},
        "Einheit": {"minWidth": 100, "width": 120},
        "Ifc Daten Typ": {"minWidth": 150, "width": 180},
        "Wertebereich": {"minWidth": 150, "width": 200},
    }

    for col, config in column_configs.items():
        gb.configure_column(col, header_name=col, wrapText=True, autoHeight=True,
                            cellStyle={"white-space": "normal"}, **config)

    for col in ['11', '21', '31', '32', '33', '41', '51', '52', '53', '61']:
        gb.configure_column(col, width=80, wrapText=True, autoHeight=True)

    gb.configure_grid_options(domLayout='normal')
    return gb.build()

def attribute_table(df, table_id):
    table_data = df[['Attribut Beschreibung', 'Ifc Attribut', 'Eigenschaften Gruppe (Pset)', 'Einheit', 
                     'Ifc Daten Typ', 'Wertebereich','11', '21', '31', '32', '33', '41', '51', '52', '53', '61']]

    grid_options = configure_grid(table_data)

    row_height, header_height = 35, 40
    num_rows = len(table_data)
    grid_height = max(300, min((num_rows * row_height) + header_height, 1200))

    return AgGrid(
        table_data, 
        gridOptions=grid_options,
        height=grid_height,
        theme='streamlit',
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        key=f"grid_Projekt_{uuid.uuid4()}"
    )

def sidebar_filters():
    st.sidebar.multiselect("Filter nach Projektphase", ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])
    st.sidebar.multiselect("Filter nach Verantwortlicher", ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])
    st.sidebar.multiselect("Filter nach Usecase/Workflow", ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])

    if st.sidebar.button("Download Excel"):
        st.sidebar.write("Excel download initiated")
    if st.sidebar.button("Download IDS"):
        st.sidebar.write("IDS download initiated")

def display_element_data(element_data):
    col1, col2 = st.columns([4,4])

    with col1:
        st.header(element_data['Element'].iloc[0])
        st.write(element_data['Element Beschreibung'].iloc[0])

    with col2:
        st.header("")
        st.write("Bild")


    st.write(f"Ifc Entität: {element_data['Ifc Entität'].iloc[0]}")
    st.write(f"Logischer Bezug: {element_data['Logischer Bezug'].iloc[0]}")
    attribute_table(element_data, element_data['Element'].iloc[0])

def main():
    st.header("BBL Elementplan & Modellierungsdefinitionen")

    

    st.markdown("Wählen sie die in Ihrem Vertrag definierte Version:")

    versions = ['V16.05', 'V16.02']
    
    if 'selected_version' not in st.session_state:
        st.session_state.selected_version = versions[0]

    selected_version = st.sidebar.selectbox("Version", versions, index=versions.index(st.session_state.selected_version))
    st.session_state.selected_version = selected_version

    sidebar_filters()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    data_dir = os.path.join(project_root, 'data', selected_version)
    file_path = os.path.join(data_dir, f'Elementplan_BBL_{selected_version.replace(".", "_")}_raw_data.xlsx')

    data_filtered = load_data(file_path)

    models = get_unique_values(data_filtered, 'Modell')

    for model in models:
        with st.expander(f"Modell: {model}"):
            elements = get_unique_values(data_filtered[data_filtered['Modell'] == model], 'Element')
            for element in elements:
                element_data = data_filtered[(data_filtered['Modell'] == model) & (data_filtered['Element'] == element)]
                display_element_data(element_data)

    footer()


main()