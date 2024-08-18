import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
import os
import uuid
import json

from src.ui_elements import padding, footer


# Load translations at the start of the script
@st.cache_resource
def load_translations(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Use this to load translations
translations = load_translations('translations.json')

def get_translation(key, language):
    keys = key.split('.')
    value = translations
    for k in keys:
        value = value.get(k, {})
    return value.get(language, key)

@st.cache_data
def load_data(file_path):
    return pd.read_excel(file_path)

@st.cache_data
def get_unique_values(df, column):
    return df[column].unique()

def configure_grid(df, language):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(resizable=True, filterable=True, sortable=True, editable=False)

    column_configs = {
        get_translation("column_names.AttributeDescription", language): {"minWidth": 200, "width": 250},
        get_translation("column_names.AttributeName", language): {"minWidth": 150, "width": 180},
        #get_translation("column_names.PsetQset)", language): {"minWidth": 200, "width": 250},
        #get_translation("column_names.Unit", language): {"minWidth": 100, "width": 120},
        get_translation("column_names.IfcDataTyp", language): {"minWidth": 150, "width": 180},
        get_translation("column_names.Values", language): {"minWidth": 150, "width": 200},
    }

    for col, config in column_configs.items():
        gb.configure_column(col, header_name=col, wrapText=True, autoHeight=True,
                            cellStyle={"white-space": "normal"}, **config)

    for col in ['11', '21', '31', '32', '33', '41', '51', '52', '53', '61']:
        gb.configure_column(col, width=80, wrapText=True, autoHeight=True)

    gb.configure_grid_options(domLayout='normal')
    return gb.build()

def attribute_table(df, table_id, language):
    columns = [
        f'Attribut Beschreibung{language}',
        f'Ifc Attribut_{language}',
        f'Eigenschaften Gruppe (Pset)_{language}',
        f'Einheit_{language}',
        f'Ifc Daten Typ_{language}',
        f'Wertebereich_{language}',
        '11', '21', '31', '32', '33', '41', '51', '52', '53', '61'
    ]
    
    table_data = df[columns].copy()
    
    # Rename columns to their translated versions
    column_translations = {
        f'Attribut Beschreibung_{language}': get_translation("column_names.Attribut Beschreibung", language),
        f'Ifc Attribut_{language}': get_translation("column_names.Ifc Attribut", language),
        f'Eigenschaften Gruppe (Pset)_{language}': get_translation("column_names.Eigenschaften Gruppe (Pset)", language),
        f'Einheit_{language}': get_translation("column_names.Einheit", language),
        f'Ifc Daten Typ_{language}': get_translation("column_names.Ifc Daten Typ", language),
        f'Wertebereich_{language}': get_translation("column_names.Wertebereich", language),
    }
    
    table_data.rename(columns=column_translations, inplace=True)

    grid_options = configure_grid(table_data, language)

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

def sidebar_filters(language):
    st.sidebar.multiselect(get_translation("sidebar_filters.project_phase", language), ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])
    st.sidebar.multiselect(get_translation("sidebar_filters.responsible", language), ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])
    st.sidebar.multiselect(get_translation("sidebar_filters.usecase", language), ["Green", "Yellow", "Red", "Blue"], ["Yellow", "Red"])

    if st.sidebar.button(get_translation("sidebar_filters.download_excel", language)):
        st.sidebar.write("Excel download initiated")
    if st.sidebar.button(get_translation("sidebar_filters.download_ids", language)):
        st.sidebar.write("IDS download initiated")

def display_element_data(element_data, language):
    col1, col2 = st.columns([4,4])

    with col1:
        st.header(element_data['Element'].iloc[0])
        st.write(element_data[f'Element Beschreibung_{language}'].iloc[0])

    with col2:
        st.header("")
        st.write("Bild")

    st.write(f"Ifc Entität: {element_data['IfcEntity'].iloc[0]}")
    st.write(f"Logischer Bezug: {element_data[f'Logischer Bezug_{language}'].iloc[0]}")
    attribute_table(element_data, element_data['Element'].iloc[0], language)

def main():
    languages = ['DE', 'EN', 'FR', 'IT']
    selected_language = st.sidebar.selectbox("Language", languages, index=languages.index('DE'))

    st.header(get_translation("header", selected_language))

    st.markdown(get_translation("version_select", selected_language))

    versions = ['V16.05', 'V16.02']
    
    if 'selected_version' not in st.session_state:
        st.session_state.selected_version = versions[0]

    selected_version = st.sidebar.selectbox("Version", versions, index=versions.index(st.session_state.selected_version))
    st.session_state.selected_version = selected_version

    sidebar_filters(selected_language)

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
                display_element_data(element_data, selected_language)

    footer()

if __name__ == "__main__":
    main()