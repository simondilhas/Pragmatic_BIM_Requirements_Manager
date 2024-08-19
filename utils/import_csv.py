import pandas as pd
from pathlib import Path
from typing import Dict, List
import os

from check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

VERSION = 'SampleRequirmentsV.0.1'

def get_data_path(folder_name: str) -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        # Use a path relative to the root of the repository
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        # For local development, use the current method
        return Path(__file__).parent.parent / folder_name

def load_dataframes(data_dir: Path) -> Dict[str, pd.DataFrame]:
    file_names = {
        'attributes': 'Attributes-ExportAll.csv',
        'elements': 'Elements-ExportAll.csv',
        'models': 'Models-ExportAll.csv',
        'workflows': 'Workflows-ExportAll.csv'
    }
    
    return {f"{key}_df": pd.read_csv(data_dir / file_name) 
            for key, file_name in file_names.items()}

def process_attributes_df(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['ElementID', 'ModelID', 'WorkflowID', 'SortAttribut']
    check_required_columns(df, required_columns, 'attributes_df')

    columns_to_explode = ['ElementID', 'ModelID', 'WorkflowID']
    
    df_exploded = df.copy()
    for column in columns_to_explode:
        # Convert column to string type
        df_exploded[column] = df_exploded[column].astype(str)
        if df_exploded[column].str.contains(',', na=False).any():
            df_exploded = df_exploded.assign(**{column: df_exploded[column].str.split(',')}).explode(column)
        df_exploded[column] = df_exploded[column].str.strip()
    
    df_exploded['SortAttribut'] = pd.to_numeric(df_exploded['SortAttribut'], errors='coerce')
    return df_exploded.sort_values('SortAttribut', na_position='last').reset_index(drop=True)

def export_excel(df: pd.DataFrame, data_dir: Path, version: str):
    file = data_dir / f"Elementplan_{version}_raw_data.xlsx"
    df.to_excel(file, index=False)
    print(f"Excel file exported to: {file}")

def main():


    data_dir = get_data_path(VERSION)
    dataframes = load_dataframes(data_dir)
    
    check_required_columns(dataframes['workflows_df'], required_workflows_columns, 'workflows_df')
    check_required_columns(dataframes['elements_df'], required_elements_columns, 'elements_df')
    check_required_columns(dataframes['models_df'], required_models_columns, 'models_df')
    check_required_columns(dataframes['attributes_df'], required_attributes_columns, 'attributes_df')
    
    attributes_df = process_attributes_df(dataframes['attributes_df'])
    
    result_df = attributes_df.merge(dataframes['elements_df'], on='ElementID', how='left')\
                             .merge(dataframes['models_df'], on='ModelID', how='left')\
                             .merge(dataframes['workflows_df'], on='WorkflowID', how='left')
    

    columns_to_check = ['SortModels', 'SortElements', 'SortAttributes']
    available_columns = [col for col in columns_to_check if col in result_df.columns]
    sorted_df = result_df.sort_values(by=available_columns, ascending=[True] * len(available_columns))
    sorted_df = sorted_df.drop_duplicates().reset_index(drop=True)


    print(result_df)


    
    # Export the result to Excel
    export_excel(result_df, data_dir, VERSION)

if __name__ == "__main__":
    main()