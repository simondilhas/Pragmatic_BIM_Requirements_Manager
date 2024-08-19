import streamlit as st
import pandas as pd
import os
from plotly import graph_objects as go
import json
from pathlib import Path
import uuid

@st.cache_data
def get_project_path(folder_name: str) -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        # Use a path relative to the root of the repository
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        # For local development, use the current method
        return Path(__file__).parent.parent / folder_name

def load_data(version_path: Path, version: str) -> pd.DataFrame:
    file_path = version_path / f"Elementplan_{version}_raw_data.xlsx"
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_excel(file_path)

def filter_columns_by_language(df, language_suffix):
    common_columns = [
        'AttributID', 'AttributName', 'SortAttribut', 'Pset', 'DataTyp', 'Unit',
        'IFC2x3', 'IFC4', 'IFC4.3', 'Applicability', 'ElementID', 'ModelID',
        'WorkflowID', 'SortElement', 'IfcEntityIfc4.0Name', 'SortModels', 'Status'
    ]
    language_specific_columns = [col for col in df.columns if col.endswith(f'{language_suffix}')]
    columns_to_keep = common_columns + language_specific_columns
    return df[columns_to_keep]

def load_translations(json_path: Path) -> dict:
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_versions(data_folder: Path) -> list:
    return [f.name for f in data_folder.iterdir() 
            if f.is_dir() and f.name != '__pycache__']

def get_column_names(translations, language_suffix):
    return {
        'AttributName': translations['column_names']['AttributName'][language_suffix],
        f'AttributDescription{language_suffix}': translations['column_names'][f'AttributDescription{language_suffix}'][language_suffix],
        'Pset': translations['column_names']['Pset'][language_suffix],
        'DataTyp': translations['column_names']['DataTyp'][language_suffix],
        'Unit': translations['column_names']['Unit'][language_suffix],
        f'AllowedValues{language_suffix}': translations['column_names'][f'AllowedValues{language_suffix}'][language_suffix]
    }

def display_plotly_table(data, translations, language_suffix):
    column_names = get_column_names(translations, language_suffix)
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(column_names.values()),
            align='left',
            fill_color='lightgrey',
            font=dict(size=12)
        ),
        cells=dict(
            values=[data[col] for col in column_names.keys()],
            align='left',
            fill_color='white',
            font=dict(size=11),
            height=30  # Set a fixed height for each cell
        ),
        columnwidth=[150, 300, 100, 100, 80, 200]  # Specify pixel widths for each column
    )])

    # Calculate dynamic height based on the number of rows
    num_rows = len(data)
    header_height = 40
    row_height = 50
    total_height = header_height + (num_rows * row_height)

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=total_height,
        width=930  # Sum of all column widths
    )

    st.plotly_chart(fig, use_container_width=True, config={'responsive': True})

def display_html_table(data, translations, language_suffix):
    column_names = get_column_names(translations, language_suffix)
    
    html = f"""
    <style>
        .styled-table {{
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 400px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }}
        .styled-table thead tr {{
            background-color: #009879;
            color: #ffffff;
            text-align: left;
        }}
        .styled-table th,
        .styled-table td {{
            padding: 12px 15px;
        }}
        .styled-table tbody tr {{
            border-bottom: 1px solid #dddddd;
        }}
        .styled-table tbody tr:nth-of-type(even) {{
            background-color: #f3f3f3;
        }}
        .styled-table tbody tr:last-of-type {{
            border-bottom: 2px solid #009879;
        }}
    </style>
    <table class="styled-table">
        <thead>
            <tr>
                {"".join(f"<th>{col}</th>" for col in column_names.values())}
            </tr>
        </thead>
        <tbody>
    """
    
    for _, row in data.iterrows():
        html += "<tr>"
        for col in column_names.keys():
            html += f"<td>{row[col]}</td>"
        html += "</tr>"
    
    html += """
        </tbody>
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def display_streamlit_columns(data, translations, language_suffix):
    column_names = get_column_names(translations, language_suffix)
    col_width = [1,3,1,1,1,3]
    
    cols = st.columns(col_width)
    for i, (_, name) in enumerate(column_names.items()):
        cols[i].write(f"**{name}**")
    
    for _, row in data.iterrows():
        cols = st.columns(col_width)
        for i, col in enumerate(column_names.keys()):
            value = row[col]
            if not pd.isna(value) and value != '':
                cols[i].write(value)

def main():
    
    st.sidebar.title("Data Display Options")
       
    data_folder = get_project_path('data')
    versions = get_versions(data_folder)
    
    if not versions:
        st.error("No version folders found in the data directory.")
        return

    translations = load_translations(data_folder / 'translations.json')

    selected_version = st.sidebar.selectbox(
        translations['version_select']['EN'],
        versions
    )
    language_suffix = st.sidebar.selectbox("Select Language", ['DE', 'EN', 'FR', 'IT'])
    
    try:
        data = load_data(data_folder / selected_version, selected_version)
    except FileNotFoundError as e:
        st.error(str(e))
        return
    except pd.errors.EmptyDataError:
        st.error(f"The file for version {selected_version} is empty.")
        return
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return

    data_filtered = filter_columns_by_language(data, language_suffix)
    
    st.title(translations['header'][language_suffix])

    unique_model_names = data[f'ModelName{language_suffix}'].unique()

    for model_name in unique_model_names:
        model_data = data[data[f'ModelName{language_suffix}'] == model_name]
        
        with st.expander(f"Model: {model_name}"):
            unique_elements = model_data[f'ElementName{language_suffix}'].unique()
            
            for element_name in unique_elements:
                with st.container():
                    element_data = model_data[model_data[f'ElementName{language_suffix}'] == element_name]
                    
                    st.header(element_name)
                    st.text(element_data['IfcEntityIfc4.0Name'].iloc[0])
                    
                    element_description = element_data[f'ElementDescription{language_suffix}'].iloc[0]
                    if not pd.isna(element_description) and element_description != '':
                        st.write(element_description)
                    st.write("")
                    
                    # Filter out rows where AttributName is NaN or empty
                    valid_attributes = element_data[element_data['AttributName'].notna() & (element_data['AttributName'] != '')]
                    
                    if valid_attributes.empty:
                        st.write("No attributes found for this element.")
                    else:
                        # Prepare a DataFrame for all valid attributes of this element
                        attribute_data = pd.DataFrame({
                            'AttributName': valid_attributes['AttributName'],
                            f'AttributDescription{language_suffix}': valid_attributes[f'AttributDescription{language_suffix}'],
                            'Pset': valid_attributes['Pset'],
                            'DataTyp': valid_attributes['DataTyp'],
                            'Unit': valid_attributes['Unit'],
                            f'AllowedValues{language_suffix}': valid_attributes[f'AllowedValues{language_suffix}']
                        })
                        
                        #display_plotly_table(attribute_data, translations, language_suffix)
                        #display_html_table(attribute_data, translations, language_suffix)
                        display_streamlit_columns(attribute_data, translations, language_suffix)
                        
                        #st.divider()

    st.sidebar.button(translations['sidebar_filters']['download_excel'][language_suffix])


main()