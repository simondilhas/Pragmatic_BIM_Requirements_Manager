"""
import_csv.py

This script processes and prepares CSV data from Workflows, Models, Elements, 
and Attributes for further use.

The processed data is combined and exported as a 
comprehensive Excel file containing all the Element Plan data.

Key Features:
-------------
- Reads CSV files related to workflows, models, elements, and attributes.
- Merges the data into a single dataset.
- Exports the final dataset to a structured Excel file for further analysis or reporting.

Output:
-------
- A consolidated Excel file containing all relevant Element Plan data, 
ready for further use in analysis or reporting.

"""

import pandas as pd
from pathlib import Path
import shutil
from typing import Dict, List
import os
import sys
from dotenv import load_dotenv
import io
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.load_data import load_file, store_file  # Import from load_file.py
from src.check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

def _process_attributes_df(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['ElementID', 'ModelID', 'WorkflowID', 'SortAttribute']
    check_required_columns(df, required_columns)

    columns_to_explode = ['ElementID', 'ModelID']
    #columns_to_explode = ['ElementID', 'ModelID', 'WorkflowID']
    
    df_exploded = df.copy()
    for column in columns_to_explode:
        # Convert column to string type
        df_exploded[column] = df_exploded[column].astype(str)
        if df_exploded[column].str.contains(',', na=False).any():
            df_exploded = df_exploded.assign(**{column: df_exploded[column].str.split(',')}).explode(column)
        df_exploded[column] = df_exploded[column].str.strip()
    
    df_exploded['SortAttribute'] = pd.to_numeric(df_exploded['SortAttribute'], errors='coerce')
    return df_exploded.sort_values('SortAttribute', na_position='last').reset_index(drop=True)

def import_csv():

    VERSION = os.environ.get('VERSION')
    if not VERSION:
        raise ValueError("VERSION environment variable is not set")
    
       
    workflows_df = load_file(VERSION, 'Workflows-ExportAll.csv')
    models_df = load_file(VERSION, 'Models-ExportAll.csv')
    elements_df = load_file(VERSION, 'Elements-ExportAll.csv')
    attributes_df = load_file(VERSION, 'Attributes-ExportAll.csv')

    attributes_df = _process_attributes_df(attributes_df)

    result_df = attributes_df.merge(elements_df, on='ElementID', how='left') \
                                 .merge(models_df, on='ModelID', how='left') \
                                 .merge(workflows_df, on='WorkflowID', how='left')

    columns_to_check = ['SortModels', 'SortElements', 'SortAttributes']
    available_columns = [col for col in columns_to_check if col in result_df.columns]

    if available_columns:
        result_df = result_df.sort_values(by=available_columns, ascending=True)

    sorted_df = result_df.drop_duplicates().reset_index(drop=True)

    try:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            sorted_df.to_excel(writer, index=False)
        excel_buffer.seek(0)

        store_file(excel_buffer.getvalue(), VERSION, f"Elementplan_{VERSION}_raw_data.xlsx")

    except Exception as e:
        raise ValueError(f"Error exporting DataFrame to Excel: {e}")