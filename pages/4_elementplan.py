import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import json
from pathlib import Path
import uuid

def get_project_path(folder_name: str) -> Path:
    return Path(__file__).parent.parent / folder_name

def load_data(version_path: Path, version: str) -> pd.DataFrame:
    file_path = version_path / f"elementplan_{version}_raw_data.xlsx"
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

def display_plotly_table(data):
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(data.columns),
            align='left',
            fill_color='paleturquoise',
            font=dict(size=12)
        ),
        cells=dict(
            values=[data[col] for col in data.columns],
            align='left',
            fill_color='lavender',
            font=dict(size=11),
            height=30
        )
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=150,
        width=800
    )

    # Set column widths
    column_widths = {
        'Attribute Name': '15%',
        'Attribute Description': '30%',
        'Pset': '15%',
        'Data Type': '10%',
        'Unit': '10%',
        'Allowed Values': '20%'
    }

    for i, col in enumerate(data.columns):
        fig.update_layout({
            f'xaxis{i+1}': dict(
                domain=[sum(float(w[:-1])/100 for w in list(column_widths.values())[:i]),
                        sum(float(w[:-1])/100 for w in list(column_widths.values())[:i+1])]
            )
        })

    st.plotly_chart(fig, use_container_width=True)

def main():
    st.sidebar.title("Data Display Options")
    
    data_folder = get_project_path('data')
    versions = get_versions(data_folder)
    
    if not versions:
        st.error("No version folders found in the data directory.")
        return

    selected_version = st.sidebar.selectbox("Select Version", versions)
    language_suffix = st.sidebar.selectbox("Select Language", ['DE', 'EN', 'FR', 'ES'])
    
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
    
    st.title("Element Data Display")

    unique_model_names = data[f'ModelName{language_suffix}'].unique()

    for model_name in unique_model_names:
        model_data = data[data[f'ModelName{language_suffix}'] == model_name]
        
        with st.expander(f"Model: {model_name}"):
            for _, row in model_data.iterrows():
                element_name_col = f'ElementName{language_suffix}'
                element_description_col = f'ElementDescription{language_suffix}'
                attribute_name_col = 'AttributName'
                attribute_description_col = f'AttributDescription{language_suffix}'
                allowed_values_col = f'AllowedValues{language_suffix}'
                
                st.header(row[element_name_col])
                st.write(row[element_description_col])
                
                table_data = pd.DataFrame({
                    'Attribute Name': [row[attribute_name_col]],
                    'Attribute Description': [row[attribute_description_col]],
                    'Pset': [row['Pset']],
                    'Data Type': [row['DataTyp']],
                    'Unit': [row['Unit']],
                    'Allowed Values': [row[allowed_values_col]]
                })
                
                display_plotly_table(table_data)

if __name__ == "__main__":
    main()