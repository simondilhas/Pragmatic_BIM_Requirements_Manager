import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
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
    # Columns to always keep (not language-specific)
    common_columns = [
        'AttributID',
        'AttributName',
        'SortAttribut',
        'Pset',
        'DataTyp',
        'Unit',
        'IFC2x3',
        'IFC4',
        'IFC4.3',
        'Applicability',
        'ElementID',
        'ModelID',
        'WorkflowID',
        'SortElement',
        'IfcEntityIfc4.0Name',
        'SortModels',
        'Status'
    ]

    # Filter columns that match the language suffix
    language_specific_columns = [col for col in df.columns if col.endswith(f'{language_suffix}')]

    # Combine common columns with the language-specific ones
    columns_to_keep = common_columns + language_specific_columns

    # Return the filtered DataFrame
    return df[columns_to_keep]

def load_translations(json_path: Path) -> dict:
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def rename_columns(df: pd.DataFrame, language: str, translations: dict) -> pd.DataFrame:
    column_rename_map = {}
    for column in df.columns:
        # Check if the column has a translation
        if column in translations['column_names']:
            column_rename_map[column] = translations['column_names'][column].get(language, column)
    
    # Rename the columns in the DataFrame
    return df.rename(columns=column_rename_map)

def get_versions(data_folder: Path) -> list:
    return [f.name for f in data_folder.iterdir() 
            if f.is_dir() and f.name != '__pycache__']

def truncate_text(text, max_length=800):
    """Truncate text to a specified length and add ellipsis if necessary."""
    return (text[:max_length] + '...') if len(text) > max_length else text


def x_display_ag_grid(data, key):
    unique_id = str(uuid.uuid4())
    
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(
        resizable=False,  # Disable resizing
        filterable=True, 
        sortable=True, 
        editable=False,
        wrapText=True,
        autoHeight=True
    )
    
    # Set fixed pixel widths for all columns
    column_widths = {
        'Attribute Name': 130,
        'Attribute Description': 350,
        'Pset': 150,
        'Data Type': 100,
        'Unit': 80,
        'Allowed Values': 200
    }
    
    for col, width in column_widths.items():
        gb.configure_column(col, 
                            width=width, 
                            minWidth=width, 
                            maxWidth=width,
                            suppressSizeToFit=True)
    
    gb.configure_grid_options(
        domLayout='autoHeight',
        suppressColumnVirtualisation=True,
        suppressRowVirtualisation=True,
        enableCellTextSelection=True,
        suppressAutoSize=True
    )
    
    grid_options = gb.build()
    
    return AgGrid(
        data, 
        gridOptions=grid_options, 
        key=key+unique_id,
        fit_columns_on_grid_load=False,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False
    )

def x_display_ag_grid(data, key, height=400):
    unique_id = str(uuid.uuid4())
    
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(
        resizable=False,  # Disable resizing
        filterable=True, 
        sortable=True, 
        editable=False,
        wrapText=True,
        autoHeight=False  # Disable auto-height to allow scrolling
    )
    
    # Set fixed pixel widths for all columns
    column_widths = {
        'Attribute Name': 200,
        'Attribute Description': 300,
        'Pset': 150,
        'Data Type': 100,
        'Unit': 80,
        'Allowed Values': 200
    }
    
    for col, width in column_widths.items():
        gb.configure_column(col, 
                            width=width, 
                            minWidth=width, 
                            maxWidth=width,
                            suppressSizeToFit=True)
    
    gb.configure_grid_options(
        domLayout='normal',  # Changed from 'autoHeight' to enable scrolling
        suppressColumnVirtualisation=True,
        enableCellTextSelection=True,
        suppressAutoSize=True,
        rowHeight=50  # Set a fixed row height
    )
    
    grid_options = gb.build()
    
    return AgGrid(
        data, 
        gridOptions=grid_options, 
        key=key+unique_id,
        fit_columns_on_grid_load=False,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False,
        height=height  # Set the height of the grid
    )

def display_ag_grid(data, key):
    unique_id = str(uuid.uuid4())
    
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_default_column(
        resizable=False,  # Disable resizing
        filterable=True, 
        sortable=True, 
        editable=False,
        wrapText=True,
        autoHeight=True  # Enable auto-height for rows
    )
    
    # Set fixed pixel widths for all columns
    column_widths = {
        'Attribute Name': 130,
        'Attribute Description': 350,
        'Pset': 150,
        'Data Type': 100,
        'Unit': 80,
        'Allowed Values': 200
    }

    # # Set fixed pixel widths for all columns
    #column_widths = {
    #    'Attribute Name': '10%' , 
    #    'Attribute Description': '30%',
    #    'Pset': '10%',
    #    'Data Type': '10%',
    #    'Unit': '10%',
    #    'Allowed Values': '30%'
    #}
    
    for col, width in column_widths.items():
        gb.configure_column(col, 
                            width=width, 
                            minWidth=width, 
                            maxWidth=width,
                            suppressSizeToFit=True)
    
    gb.configure_grid_options(
        domLayout='autoHeight',
        suppressColumnVirtualisation=True,
        suppressRowVirtualisation=True,
        enableCellTextSelection=True,
        suppressAutoSize=True
    )
    
    grid_options = gb.build()
    
    return AgGrid(
        data, 
        gridOptions=grid_options, 
        key=key+unique_id,
        fit_columns_on_grid_load=False,
        update_mode=GridUpdateMode.VALUE_CHANGED,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=False
    )

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

    # Load translations from the JSON file
    translations = load_translations(get_project_path('conf') / 'translations.json')
    
    # Filter columns based on language suffix
    data_filtered = filter_columns_by_language(data, language_suffix)
    
    # Rename columns based on the selected language
    #data_renamed = rename_columns(data_filtered, language_suffix, translations)

    #st.write(data_renamed)
    
    st.title("Element Data Display")

    unique_model_names = data[f'ModelName{language_suffix}'].unique()

    for model_name in unique_model_names:
    # Filter the DataFrame for rows corresponding to the current model name
        model_data = data[data[f'ModelName{language_suffix}'] == model_name]
        
        with st.expander(f"Model: {model_name}"):
            # Iterate through each row within the filtered model data
            for _, row in model_data.iterrows():
                element_name_col = f'ElementName{language_suffix}'
                element_description_col = f'ElementDescription{language_suffix}'
                attribute_name_col = 'AttributName'
                attribute_description_col = f'AttributDescription{language_suffix}'
                allowed_values_col = f'AllowedValues{language_suffix}'
                
                st.header(row[element_name_col])
                st.write(row[element_description_col])
                
                # Prepare the data for the ag-Grid table
                table_data = pd.DataFrame({
                    'Attribute Name': [row[attribute_name_col]],
                    'Attribute Description': [row[attribute_description_col]], #truncate?
                    'Pset': [row['Pset']],
                    'Data Type': [row['DataTyp']],
                    'Unit': [row['Unit']],
                    'Allowed Values': [row[allowed_values_col]]
                })
                
                # Display the table using ag-Grid
                display_ag_grid(table_data, key=model_name)



if __name__ == "__main__":
    main()
