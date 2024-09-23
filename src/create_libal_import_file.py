"""
create_libal_import_file.py

This module prepares the Element Plan data for seamless project setup in Libal, 
a CDE (Common Data Environment) specialist for data handover to clients (www.libal-tech.de).

Input:
------
- `Elementplan_{version}_raw_data.xlsx`: The raw Element Plan data generated from the import process.

Output:
-------
- A formatted Excel configuration file tailored for easy import into Libal's platform.

Key Features:
-------------
- Processes and formats the raw Element Plan data into a structure required by Libal for project initialization.
- Ensures compatibility with Libal's system for smooth data handover.
- Generates a ready-to-use Excel configuration file that meets Libal's project setup requirements.

Example usage:
--------------
```bash
python create_libal_import_file.py


"""

import pandas as pd
from pathlib import Path
import os
import io
from dotenv import load_dotenv
from src.sort import sort_dataframe

from src.load_data import load_file, store_file


#VERSION = 'V16.6'
#VERSION = 'SampleV.01'
#languages = ['DE','EN','FR','IT'] 

column_order = [
    'ElementName*',
    'IfcEntityIfc4.0Name',
    'Pset',
    'AttributeName',
    'AttributeName',
    'AttributeDescription*',
    'DataTyp',
    'ModelName*',
    'Unit',
    '11', #Change if the Phases are named differently 
    '21', #TODO #8 find better logic that works for all cases
    '22',
    '31',
    '32',
    '33',
    '41',
    '51',
    '52',
    '53',
    '61',
    '62'
]

def get_available_languages(df):
        language_columns = [col for col in df.columns if col.startswith('ElementName')]
        return [col.replace('ElementName', '') for col in language_columns]

def rename_phase_columns(df):
    phase_dict = {}
    
    for col in df.columns:
        if col.startswith('Phase_'):
            # Extract the number part (everything before the first space after 'Phase_')
            phase_number = col.split()[0].replace('Phase_', '')
            # Update the dictionary with the new column name
            if phase_number.isdigit():
                phase_dict[col] = phase_number
            else:
                phase_dict[col] = phase_number
    
    # Rename the columns in the DataFrame
    df.rename(columns=phase_dict, inplace=True)
    return df



def get_data_path(folder_name: str) -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        # Use a path relative to the root of the repository
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        # For local development, use the current method
        return Path(__file__).parent.parent / 'data' / folder_name


def extract_phase_definitions(df, column):
    all_phases = set()
    for phases in df[column].str.split(','):
        all_phases.update([phase.strip() for phase in phases if isinstance(phases, list)])
    
    all_phases = sorted(all_phases)
    return all_phases

def extract_phase_definitions(df, column):
    all_phases = set()
    for phases in df[column].str.split(','):
        all_phases.update([phase.strip() for phase in phases if isinstance(phases, list)])
    
    all_phases = sorted(all_phases)
    return all_phases

def explode_phases_to_matrix(df, column, lang):
    
    all_phases = extract_phase_definitions(df, column)
    
    for phase in all_phases:
        df[f'Phase_{phase}'] = ''

    # Fill the new columns with 'X' where appropriate
    for index, row in df.iterrows():
        phases = row[column].split(',') if isinstance(row[column], str) else []
        for phase in phases:
            phase = phase.strip()
            if phase in all_phases:
                df.at[index, f'Phase_{phase}'] = 'X'
    return df



def libal_config_export(df, column_widths, language, export_file_type_name, VERSION):
    excel_buffer = io.BytesIO()

    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        workbook = writer.book

        default_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
        })
        default_column_width = 8

        grey_text_format = workbook.add_format({'font_color': '#d3d3d3'})

        black_text_format = workbook.add_format({
            'top': 1,
            'text_wrap': True,
            'valign': 'top',
            'font_color': 'black'
        })

        centered_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'top',
            'align': 'center',
        })

        sheet_name = 'Config'
        df['Sort'] = range(1, len(df) + 1)

        df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)

        worksheet = writer.sheets[sheet_name]

        for col_num, col_name in enumerate(df.columns):
            width = column_widths[col_num] if col_num < len(column_widths) else default_column_width
            
            if 11 <= col_num <= 22 or col_name == 'Sort':
                worksheet.set_column(col_num, col_num, width, centered_format)
            else:
                worksheet.set_column(col_num, col_num, width, default_format)

        worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)

        # Freeze panes at C2
        worksheet.freeze_panes(1, 3)

        # Apply a thin top border and black text starting from column C if column C is different from above
        worksheet.conditional_format(1, 2, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': '=$C2<>$C1',
            'format': black_text_format
        })

        # Apply a line across all cells if column A is different from above
        worksheet.conditional_format(1, 0, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': '=$A2<>$A1',
            'format': black_text_format
        })

        # Apply a line from column F onward, even if the cells are empty
        worksheet.conditional_format(1, 5, len(df), len(df.columns) - 1, {
            'type': 'formula',
            'criteria': '=$F2<>$F1',
            'format': black_text_format
        })

        # Always apply a thin line starting from column G onward, including empty cells
        worksheet.conditional_format(1, 6, len(df), len(df.columns) - 1, {
            'type': 'no_errors',
            'format': black_text_format
        })

        # Apply grey text formatting to columns A to F where the value is the same as the row above
        for col in range(6):
            col_letter = chr(65 + col)
            worksheet.conditional_format(1, col, len(df), col, {
                'type': 'formula',
                'criteria': f'=${col_letter}2=${col_letter}1',
                'format': grey_text_format
            })

    excel_buffer.seek(0)  # Reset the buffer pointer to the beginning

    # Use store_file to save the file either in Azure Blob or locally
    file_name = f'{export_file_type_name}_{language}_{VERSION}.xlsx'
    store_file(excel_buffer.getvalue(), VERSION, file_name)  # Save to Azure or locally
    print(f"Excel file exported to: {file_name}")

def create_filtered_df(df, language):
    filtered_columns = [
        col.replace('*', language) if '*' in col else col for col in column_order
    ]
    return df[filtered_columns]

def create_libal_import_file(version, master_or_project):
    df = load_file(version, f'RawData_{version}.xlsx')

    languages = get_available_languages(df)
    first_lang = languages[0]

    column_lang = f'ProjectPhase{first_lang}'
    df = explode_phases_to_matrix(df, column_lang, first_lang)
    df_sorted = sort_dataframe(df)
    df = rename_phase_columns(df_sorted)
    column_widths = [20, 20, 20, 20, 35, 45, 20, 20, 20, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]

    export_file_type_name = 'Libal_Config'

    for language in languages:
        filtered_df = create_filtered_df(df, language)
        output_file_path = libal_config_export(filtered_df, column_widths, language, export_file_type_name, version)
        print(output_file_path)