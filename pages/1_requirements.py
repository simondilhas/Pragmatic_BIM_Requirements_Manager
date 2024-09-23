import streamlit as st
import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Tuple
import json
from dotenv import load_dotenv

from src.sort import sort_dataframe
from src.load_data import load_file, get_versions, get_project_path
from src.utils import load_config
from src.ui_elements import custom_sidebar  

# Type aliases
DataFrame = pd.DataFrame
PathLike = Path | str

from src.utils import load_config

config = load_config()
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)
FRONTEND_LANGUAGES = config.get('FRONTEND_LANGUAGES', MAIN_LANGUAGE)

# Constants
DATA_FOLDER = 'data' #better logic?
TRANSLATIONS_FILE = 'translations.json'
#EXCEL_FILE_PATTERN = "Elementplan_{version}_raw_data.xlsx"


@st.cache_data
def load_data(version: str) -> pd.DataFrame:
    df = load_file(version, 'data_for_web.csv')
    #Potential for Performance increase?
    #df = df.drop_duplicates(subset='AttributeID')
    return df


@st.cache_data
def load_translations(json_path: Path) -> Dict:
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def x_get_versions(data_folder: Path) -> List[str]:
    return sorted([f.name for f in data_folder.iterdir() 
                   if f.is_dir() and f.name != '__pycache__'], reverse=True)

def filter_columns_by_language(df: pd.DataFrame, language_suffix: str) -> pd.DataFrame:
    common_columns = [
        'AttributeID', 'AttributeName', 'SortAttribute', 'Pset', 'DataTyp', 'Unit',
        'IFC2x3', 'IFC4', 'IFC4.3', 'Applicability', 'ElementID', 'ModelID',
        'WorkflowID', 'SortElement', 'IfcEntityIfc4.0Name', 'SortModels', 'Status'
    ]
    language_specific_columns = [col for col in df.columns if col.endswith(language_suffix)]
    columns_to_keep = common_columns + language_specific_columns
    return df[columns_to_keep]

def filter_by_project_phase(data: pd.DataFrame, language_suffix: str, translations: Dict) -> pd.DataFrame:
    project_phase_column = f'ProjectPhase{language_suffix}'
    if project_phase_column not in data.columns:
        st.warning(f"No Data available for: {language_suffix}")
        return data

    all_phases = set()
    for phases in data[project_phase_column].dropna():
        all_phases.update(phase.strip() for phase in phases.split(','))
    all_phases = sorted(list(all_phases))
      
    selected_phases = st.sidebar.multiselect(
        translations['sidebar_filters']['project_phase'][language_suffix],
        options=all_phases,
        default=[],
        key="project_phase_filter",
        placeholder=translations['sidebar_filters']['project_phase'][language_suffix]
    )
    
    if not selected_phases:
        return data

    mask = data[project_phase_column].fillna('').apply(
        lambda x: any(phase in [p.strip() for p in x.split(',')] for phase in selected_phases)
    )
    filtered_data = data[mask]
    
    if filtered_data.empty:
        st.warning(f"No data found for the selected phase(s): {', '.join(selected_phases)}")
    
    return filtered_data

def display_download_button(version: str, language: str, data_folder: PathLike, file_type_name: str):
   
    file_name = f"{file_type_name}_{language}_{version}.xlsx" 
    file_path = Path(data_folder) / version / file_name

    if file_path.exists():
        with open(file_path, "rb") as file:
            st.sidebar.download_button(
                label=f"Download {file_name}",
                data=file,
                file_name=file_name,
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    else:
        return
        #st.sidebar.write(f"No file available for {language} in version {version}")

def custom_text(text: str, font_size: str = "0.7rem") -> str:
    def to_rem(size: str) -> str:
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
    base_style = f"font-size: {font_size_rem}; line-height: 1.5;"
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
                processed_lines.append(f'<span style="{base_style}">{line}</span><br>')
        
        if in_list:
            processed_lines.append('</ul>' if list_type == 'ul' else '</ol>')
        
        return ''.join(processed_lines)
    else:
        return f'<span style="{base_style}">{text.replace(chr(10), "<br>")}</span>'

def display_streamlit_columns(data: pd.DataFrame, translations: Dict, language_suffix: str):
    column_names = {
        'AttributeName': translations['column_names']['AttributeName'][language_suffix],
        f'AttributeDescription{language_suffix}': translations['column_names']['AttributeDescription'][language_suffix],
        'Pset': translations['column_names']['Pset'][language_suffix],
        'DataTyp': translations['column_names']['DataTyp'][language_suffix],
        'Unit': translations['column_names']['Unit'][language_suffix],
        f'AllowedValues{language_suffix}': translations['column_names']['AllowedValues'][language_suffix]
    }

    col_width = [2, 4, 2, 1, 1, 3]
    
    cols = st.columns(col_width)
    
    for col, value in zip(cols, column_names.values()):
        col.markdown(custom_text(f"<strong>{value}</strong>"), unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        cols = st.columns(col_width)
        
        for col, (df_key, _) in zip(cols, column_names.items()):
            if df_key in data.columns:
                if not pd.isna(row[df_key]) and row[df_key] != '':
                    col.markdown(custom_text(str(row[df_key])), unsafe_allow_html=True)
            else:
                st.write(f"Column {df_key} not found in DataFrame")

def display_element_data(element_data: pd.DataFrame, language_suffix: str, translations: Dict):
    if element_data.empty:
        st.warning("No data available for this element.")
        return

    element_name = element_data[f'ElementName{language_suffix}'].iloc[0] if not element_data[f'ElementName{language_suffix}'].empty else "Unknown Element"
    ifc_entity = element_data['IfcEntityIfc4.0Name'].iloc[0] if not element_data['IfcEntityIfc4.0Name'].empty else ""

    header_text = element_name
    if ifc_entity:
        header_text += f" ({ifc_entity})"
    st.header(header_text)

    contained_in = element_data[f'ContainedIn{language_suffix}'].iloc[0] if not element_data[f'ContainedIn{language_suffix}'].empty else "N/A"
    st.write(f"IfcRel: {contained_in}")

    element_description = element_data[f'ElementDescription{language_suffix}'].iloc[0]
    if not pd.isna(element_description) and element_description != '':
        st.write(element_description)
    st.write("")
    
    valid_attributes = element_data[element_data['AttributeName'].notna() & (element_data['AttributeName'] != '')]
    
    if valid_attributes.empty:
        st.write("No attributes found for this element.")
    else:
        attribute_data = pd.DataFrame({
            'AttributeName': valid_attributes['AttributeName'],
            f'AttributeDescription{language_suffix}': valid_attributes[f'AttributeDescription{language_suffix}'],
            'Pset': valid_attributes['Pset'],
            'DataTyp': valid_attributes['DataTyp'],
            'Unit': valid_attributes['Unit'],
            f'AllowedValues{language_suffix}': valid_attributes[f'AllowedValues{language_suffix}']
        })
        
        display_streamlit_columns(attribute_data, translations, language_suffix)



#def sidebar_select_language(available_version, language_suffix, language_options, language_display_names, translations):
#    #This only shows theavailable languages
#    selected_language_name = st.sidebar.selectbox(
#        translations['sidebar_filters']['language'][language_suffix],
#        language_display_names,
#        index=language_options.index('') if '' in language_options else 0
#    )
#
#    language_suffix = language_options[language_display_names.index(selected_language_name)]
#    return language_suffix

def sidebar_select_version(available_version, language_suffix, translations):
    selected_version = st.sidebar.selectbox(
        translations['version_select'][language_suffix], 
        available_version
    )

    return selected_version

def sidebar_select_language(translations, current_language_suffix):
    """
    Displays the language selector in the sidebar and returns the selected language.
    """
    # Create a dropdown to select the language
    selected_language = st.sidebar.selectbox(
        #translations['sidebar_filters']['language_select'][current_language_suffix],
        "",
        list(FRONTEND_LANGUAGES.keys()),  # Dropdown for language codes (EN, DE, etc.)
        index=list(FRONTEND_LANGUAGES.keys()).index(current_language_suffix)  # Set current language as default
    )
    st.sidebar.divider()
    
    return selected_language

def main():
    custom_sidebar(MAIN_LANGUAGE)
    data_folder = get_project_path(DATA_FOLDER) #Better logic?
    available_version = get_versions(data_folder)
    translations = load_translations(data_folder / TRANSLATIONS_FILE)

    if 'language_suffix' not in st.session_state:
        st.session_state['language_suffix'] = MAIN_LANGUAGE
    
    st.session_state['language_suffix'] = sidebar_select_language(translations, st.session_state['language_suffix'])
    language_suffix = st.session_state['language_suffix']

    try:
        selected_version = sidebar_select_version(available_version, language_suffix, translations)
    except:
        if not available_version:
            st.error(translations['error'][language_suffix])
            return

    # Load data for the selected version
    try:
        data = load_data(selected_version)
    except FileNotFoundError as e:
        st.error(f"The data for version {selected_version} is missing.")
        return
    except pd.errors.EmptyDataError:
        st.error(f"The file for version {selected_version} is empty.")
        return
    except Exception as e:
        st.error(f"Error loading data for for version {selected_version}")
        return

    # Filter data by the selected language and handle missing data early
    try:
        data_filtered_by_language = filter_columns_by_language(data, language_suffix)
    except KeyError:
        st.warning(f"No data available for the selected language: {language_suffix}")
        return

    # If no data for the language, show warning and stop further execution
    if data_filtered_by_language.empty:
        st.warning(f"No data for the selected language: {language_suffix}")
        return

    # Proceed only if data is available
    try:
        data_filtered_by_phase = filter_by_project_phase(data_filtered_by_language, language_suffix, translations)
        display_download_button(selected_version, language_suffix, data_folder, 'Elementplan')  
        display_download_button(selected_version, language_suffix, data_folder, 'Libal_Config')   
        
        model_data_sorted = sort_dataframe(data_filtered_by_phase)
        tab_labels = model_data_sorted[f'FileName{language_suffix}'].unique().tolist()
        tabs = st.tabs(tab_labels)
        for tab, file_name in zip(tabs, tab_labels):
            with tab:
                model_df = model_data_sorted[model_data_sorted[f'FileName{language_suffix}'] == file_name]
                header_content = model_df[f'ModelName{language_suffix}'].unique()
                if len(header_content) == 1:
                    st.header(header_content[0])
                else:
                    st.header(', '.join(header_content))
                
                for element_name in model_df[f'ElementName{language_suffix}'].unique():
                    with st.container():
                        element_data = model_df[model_df[f'ElementName{language_suffix}'] == element_name]
                        display_element_data(element_data, language_suffix, translations)

    except Exception as e:
        #st.error(f"No data available for the selected project phase: {str(e)}")
        return

main()