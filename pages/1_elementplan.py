import streamlit as st
import pandas as pd
import os
from plotly import graph_objects as go
import json
from pathlib import Path


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

#Not used experiment
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

#Not used experiment
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

def custom_text(text, font_size="0.7rem"):
    #ugly code! Is there a better solution
    def to_rem(size):
        if isinstance(size, (int, float)):
            return f"{size}rem"
        elif isinstance(size, str):
            if size.endswith('rem'):
                return size
            elif size.endswith('em'):
                return f"{size[:-2]}rem"
            elif size.endswith('px'):
                return f"{float(size[:-2]) / 16}rem"
            else:
                try:
                    return f"{float(size.rstrip('r'))}rem"
                except ValueError:
                    return "1rem"
        else:
            return "1rem"
    
    font_size_rem = to_rem(font_size)
    
    # Base style for all text
    base_style = f"font-size: {font_size_rem}; line-height: 1.5;"
    
    # Additional styles for lists
    ul_style = f"list-style-type: disc; padding-left: 1.5em; margin: 0.5em 0;"
    ol_style = f"padding-left: 1.5em; margin: 0.5em 0;"
    li_style = f"{base_style} margin: 0.25em 0;"
    
    if '\n- ' in text or '\n1. ' in text:
        lines = text.split('\n')
        processed_lines = []
        in_list = False
        list_type = None
        
        for line in lines:
            if line.strip().startswith('- '):
                if not in_list or list_type != 'ul':
                    if in_list:
                        processed_lines.append('</ol>' if list_type == 'ol' else '</ul>')
                    processed_lines.append(f'<ul style="{ul_style}">')
                    in_list = True
                    list_type = 'ul'
                processed_lines.append(f'<li style="{li_style}">{line.strip()[2:]}</li>')
            elif line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
                if not in_list or list_type != 'ol':
                    if in_list:
                        processed_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                    processed_lines.append(f'<ol style="{ol_style}">')
                    in_list = True
                    list_type = 'ol'
                processed_lines.append(f'<li style="{li_style}">{line.strip()[2:].strip()}</li>')
            else:
                if in_list:
                    processed_lines.append('</ul>' if list_type == 'ul' else '</ol>')
                    in_list = False
                    list_type = None
                processed_lines.append(f'<p style="{base_style}">{line}</p>')
        
        if in_list:
            processed_lines.append('</ul>' if list_type == 'ul' else '</ol>')
        
        return ''.join(processed_lines)
    else:
        return f'<p style="{base_style}">{text}</p>'

def display_streamlit_columns(data, translations, language_suffix):
    #ugly code! Is there a better solution
    column_names = get_column_names(translations, language_suffix)

    col_width = [2, 4, 2, 1, 1, 3]
    
    # Create columns
    col1, col2, col3, col4, col5, col6 = st.columns(col_width)
    
    # Display column headers
    col1.markdown(custom_text(f"<strong>{column_names['AttributName']}</strong>"), unsafe_allow_html=True)
    col2.markdown(custom_text(f"<strong>{column_names[f'AttributDescription{language_suffix}']}</strong>"), unsafe_allow_html=True)
    col3.markdown(custom_text(f"<strong>{column_names['Pset']}</strong>"), unsafe_allow_html=True)
    col4.markdown(custom_text(f"<strong>{column_names['DataTyp']}</strong>"), unsafe_allow_html=True)
    col5.markdown(custom_text(f"<strong>{column_names['Unit']}</strong>"), unsafe_allow_html=True)
    col6.markdown(custom_text(f"<strong>{column_names[f'AllowedValues{language_suffix}']}</strong>"), unsafe_allow_html=True)
    
    # Display data rows
    for _, row in data.iterrows():
        # Create new columns for each row
        col1, col2, col3, col4, col5, col6 = st.columns(col_width)
        
        # AttributName
        if not pd.isna(row['AttributName']) and row['AttributName'] != '':
            col1.markdown(custom_text(str(row['AttributName'])), unsafe_allow_html=True)
        
        # AttributDescription
        if not pd.isna(row[f'AttributDescription{language_suffix}']) and row[f'AttributDescription{language_suffix}'] != '':
            col2.markdown(custom_text(str(row[f'AttributDescription{language_suffix}'])), unsafe_allow_html=True)
        
        # Pset
        if not pd.isna(row['Pset']) and row['Pset'] != '':
            col3.markdown(custom_text(str(row['Pset'])), unsafe_allow_html=True)
        
        # DataTyp
        if not pd.isna(row['DataTyp']) and row['DataTyp'] != '':
            col4.markdown(custom_text(str(row['DataTyp'])), unsafe_allow_html=True)
        
        # Unit
        if not pd.isna(row['Unit']) and row['Unit'] != '':
            col5.markdown(custom_text(str(row['Unit'])), unsafe_allow_html=True)
        
        # AllowedValues
        if not pd.isna(row[f'AllowedValues{language_suffix}']) and row[f'AllowedValues{language_suffix}'] != '':
            col6.markdown(custom_text(str(row[f'AllowedValues{language_suffix}'])), unsafe_allow_html=True)

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
                    
                    st.header(f"{element_name} ({element_data['IfcEntityIfc4.0Name'].iloc[0]})")
                    #st.write(f"IfcEntity: {element_data['IfcEntityIfc4.0Name'].iloc[0]}")
                    st.write(f"IfcRel: {element_data[f'ContainedIn{language_suffix}'].iloc[0]}")
                    
                    element_description = element_data[f'ElementDescription{language_suffix}'].iloc[0]
                    if not pd.isna(element_description) and element_description != '':
                        st.write(element_description)
                    st.write("")
                    

                    valid_attributes = element_data[element_data['AttributName'].notna() & (element_data['AttributName'] != '')]
                    
                    if valid_attributes.empty:
                        st.write("No attributes found for this element.")
                    else:
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
                        

    st.sidebar.button(translations['sidebar_filters']['download_excel'][language_suffix])


main()