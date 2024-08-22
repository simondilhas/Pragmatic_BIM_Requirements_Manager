import streamlit as st
import pandas as pd
import os
from pathlib import Path
from typing import List, Dict, Tuple
import json

from src.sort import sort_dataframe

# Constants
DATA_FOLDER = 'data'
TRANSLATIONS_FILE = 'translations.json'
EXCEL_FILE_PATTERN = "Elementplan_{version}_raw_data.xlsx"
LANGUAGE_OPTIONS = ['DE', 'EN']

# Type aliases
DataFrame = pd.DataFrame
PathLike = Path | str

@st.cache_data
def get_project_path(folder_name: str) -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        return Path(__file__).parent.parent / folder_name

@st.cache_data
def load_data(version_path: PathLike, version: str) -> DataFrame:
    file_path = Path(version_path) / EXCEL_FILE_PATTERN.format(version=version)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_excel(file_path)

@st.cache_data
def load_translations(json_path: PathLike) -> Dict:
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_versions(data_folder: PathLike) -> List[str]:
    return [f.name for f in Path(data_folder).iterdir() 
            if f.is_dir() and f.name != '__pycache__']

def filter_columns_by_language(df: DataFrame, language_suffix: str) -> DataFrame:
    common_columns = [
        'AttributID', 'AttributName', 'SortAttribut', 'Pset', 'DataTyp', 'Unit',
        'IFC2x3', 'IFC4', 'IFC4.3', 'Applicability', 'ElementID', 'ModelID',
        'WorkflowID', 'SortElement', 'IfcEntityIfc4.0Name', 'SortModels', 'Status'
    ]
    language_specific_columns = [col for col in df.columns if col.endswith(f'{language_suffix}')]
    columns_to_keep = common_columns + language_specific_columns
    return df[columns_to_keep]

def filter_by_project_phase(data: DataFrame, language_suffix: str) -> DataFrame:
    all_phases = set()
    for phases in data[f'ProjectPhase{language_suffix}'].dropna():
        all_phases.update(phase.strip() for phase in phases.split(','))
    all_phases = sorted(list(all_phases))
      
    selected_phases = st.sidebar.multiselect(
        "Filter by Project Phase",
        options=all_phases,
        default=[],
        key="project_phase_filter",
        placeholder="Filter by selecting"
    )
    
    if not selected_phases:
        return data

    mask = data[f'ProjectPhase{language_suffix}'].fillna('').apply(
        lambda x: any(phase in [p.strip() for p in x.split(',')] for phase in selected_phases)
    )
    filtered_data = data[mask]
    
    if filtered_data.empty:
        st.warning(f"No data found for the selected phase(s): {', '.join(selected_phases)}")
    
    return filtered_data

def display_download_button(version: str, language: str, data_folder: PathLike):
    file_name = f"Elementplan_{language}_{version}.xlsx" 
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
        st.sidebar.write(f"No file available for {language} in version {version}")

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
                processed_lines.append(f'<p style="{base_style}">{line}</p>')
        
        if in_list:
            processed_lines.append('</ul>' if list_type == 'ul' else '</ol>')
        
        return ''.join(processed_lines)
    else:
        return f'<p style="{base_style}">{text}</p>'

def display_streamlit_columns(data: DataFrame, translations: Dict, language_suffix: str):
    column_names = {
        'AttributName': translations['column_names']['AttributName'][language_suffix],
        f'AttributDescription{language_suffix}': translations['column_names'][f'AttributDescription{language_suffix}'][language_suffix],
        'Pset': translations['column_names']['Pset'][language_suffix],
        'DataTyp': translations['column_names']['DataTyp'][language_suffix],
        'Unit': translations['column_names']['Unit'][language_suffix],
        f'AllowedValues{language_suffix}': translations['column_names'][f'AllowedValues{language_suffix}'][language_suffix]
    }

    col_width = [2, 4, 2, 1, 1, 3]
    
    cols = st.columns(col_width)
    
    for col, (key, value) in zip(cols, column_names.items()):
        col.markdown(custom_text(f"<strong>{value}</strong>"), unsafe_allow_html=True)
    
    for _, row in data.iterrows():
        cols = st.columns(col_width)
        
        for col, key in zip(cols, column_names.keys()):
            if not pd.isna(row[key]) and row[key] != '':
                col.markdown(custom_text(str(row[key])), unsafe_allow_html=True)


def display_element_data(element_data: DataFrame, language_suffix: str, translations: Dict):
    #Alte version BBL
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
        
        display_streamlit_columns(attribute_data, translations, language_suffix)

def get_available_languages(df):
        
        language_columns = [col for col in df.columns if col.startswith('ElementName')]
        return [col.replace('ElementName', '') for col in language_columns]


def get_language_options(data):
    # Language code to full name mapping
    language_names = {
        '': 'English',
        'DE': 'Deutsch',
        'FR': 'Français',
        'IT': 'Italiano',
        # Add more languages as needed
    }

    available_languages = get_available_languages(data)
    language_options = [lang for lang in available_languages if lang in language_names]
    language_display_names = [language_names.get(lang, lang) for lang in language_options]

    return language_options, language_display_names

def select_language(data):
    language_options, language_display_names = get_language_options(data)

    selected_language_name = st.sidebar.selectbox(
        "Select Language",
        language_display_names,
        index=language_options.index('') if '' in language_options else 0
    )

    language_suffix = language_options[language_display_names.index(selected_language_name)]

    return language_suffix

def main():
      
    data_folder = get_project_path(DATA_FOLDER)
    versions = get_versions(data_folder)
    
    if not versions:
        st.error("No version folders found in the data directory.")
        return

    translations = load_translations(data_folder / TRANSLATIONS_FILE)

    
    selected_version = st.sidebar.selectbox(
        translations['version_select']['EN'],
        versions
    )


    #language_suffix = st.sidebar.selectbox("Select Language", LANGUAGE_OPTIONS)
    
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
    
    language_suffix = select_language(data)

    data_filtered = filter_columns_by_language(data, language_suffix)
    data_filtered = filter_by_project_phase(data_filtered, language_suffix)

    display_download_button(selected_version, language_suffix, data_folder)  
    
    if data_filtered.empty:
        st.info("No data to display based on the current filter settings.")
        return

    st.info(translations['choice'][language_suffix])

    model_data_sorted = sort_dataframe(data_filtered)

    # First, convert the SortModels column to proper floats
    #data_filtered['SortModels_float'] = data_filtered['SortModels'].str.replace(',', '.').astype(float)

    #Double sort is not very elegant
    #sorted_file_names = model_data_sorted.sort_values('SortModels')[f'FileName{language_suffix}'].unique()
    #model_tabs = st.tabs([f"{file_name}" for file_name in sorted_file_names])

    tab_labels = model_data_sorted[f'FileName{language_suffix}'].unique().tolist()
    tabs = st.tabs(tab_labels)

    for tab, file_name in zip(tabs, tab_labels):
        with tab:
            model_df = model_data_sorted[model_data_sorted[f'FileName{language_suffix}'] == file_name]

            

            header_content = model_df[f'ModelName{language_suffix}'].unique()
            if len(header_content) == 1:
                st.header(header_content[0])  # Display single value without brackets
            else:
                st.header(', '.join(header_content))

            #TO Contiune sort by modeldata by Model and Element
            
            
            for element_name in model_df[f'ElementName{language_suffix}'].unique():
                with st.container():
                    
                    element_data = model_df[model_df[f'ElementName{language_suffix}'] == element_name]
                    display_element_data(element_data, language_suffix, translations)


main()