import pandas as pd
from pathlib import Path
import os
import sys
from src.sort import sort_dataframe
import json
import re

column_order = [
    'FileName*',
    'ModelName*',
    'ElementName*',
    'ElementDescription*',
    'IfcEntityIfc4.0Name',
    'Pset',
    'AttributeDescription*',
    'AttributeName',
    'Unit',
    'DataTyp',
    'AllowedValues*',
    'ContainedIn*',
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

def translate_column_names(df, language):
    print("Start Translating")
    # Load the translations
    data_path = get_data_path('translations.json')
    with open(data_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    # Get the column translations for the specified language
    column_translations = translations['column_names']
    
    # Function to remove language postfix
    def remove_language_postfix(column_name):
        return re.sub(r'(DE|EN|FR|IT)$', '', column_name)
    
    # Create a mapping of original column names to translated names
    translation_map = {}
    for col in df.columns:
        # Remove language postfix
        base_name = remove_language_postfix(col)
        
        # Look for a translation
        if base_name in column_translations and language in column_translations[base_name]:
            translation_map[col] = column_translations[base_name][language]
        else:
            # If no translation found, keep the base name without language postfix
            translation_map[col] = base_name
    
    # Rename the columns in the DataFrame
    df.rename(columns=translation_map, inplace=True)
    print(df.columns)
    
    return df


def export_with_custom_widths(df, column_widths, language, VERSION):
    data_path = get_data_path(VERSION)
    
    if f'FileName{language}' in df.columns:
        unique_filenames = df[f'FileName{language}'].dropna().unique()

        # Construct the file path using get_data_path()
        output_file_path = data_path / f'Elementplan_{language}_{VERSION}.xlsx'

        with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
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

            for filename in unique_filenames:
                filtered_df = df[df[f'FileName{language}'] == filename]
                filtered_df['Sort'] = range(1, len(filtered_df) + 1)
                
                filtered_df = translate_column_names(filtered_df, language)


                filtered_df.to_excel(writer, sheet_name=filename[:31], index=False, startrow=0)  # Start writing data from row 1
                
                worksheet = writer.sheets[filename[:31]]

                for col_num, col_name in enumerate(filtered_df.columns):
                    width = column_widths[col_num] if col_num < len(column_widths) else default_column_width
                    
                    if 11 <= col_num <= 22 or col_name == 'Sort':
                        worksheet.set_column(col_num, col_num, width, centered_format)
                    else:
                        worksheet.set_column(col_num, col_num, width, default_format)

                worksheet.autofilter(0, 0, len(filtered_df), len(filtered_df.columns) - 1)

                # Freeze panes at C2
                worksheet.freeze_panes(1, 3)

                # Apply a thin top border and black text starting from column C if column C is different from above
                worksheet.conditional_format(1, 2, len(filtered_df), len(filtered_df.columns) - 1, {
                    'type': 'formula',
                    'criteria': '=$C2<>$C1',
                    'format': black_text_format
                })

                # Apply a line across all cells if column A is different from above
                worksheet.conditional_format(1, 0, len(filtered_df), len(filtered_df.columns) - 1, {
                    'type': 'formula',
                    'criteria': '=$A2<>$A1',
                    'format': black_text_format
                })

                # Apply a line from column F onward, even if the cells are empty
                worksheet.conditional_format(1, 5, len(filtered_df), len(filtered_df.columns) - 1, {
                    'type': 'formula',
                    'criteria': '=$F2<>$F1',
                    'format': black_text_format
                })

                # Always apply a thin line starting from column G onward, including empty cells
                worksheet.conditional_format(1, 6, len(filtered_df), len(filtered_df.columns) - 1, {
                    'type': 'no_errors',
                    'format': black_text_format
                })

                # Apply grey text formatting to columns A to F where the value is the same as the row above
                for col in range(6):
                    col_letter = chr(65 + col)
                    worksheet.conditional_format(1, col, len(filtered_df), col, {
                        'type': 'formula',
                        'criteria': f'=${col_letter}2=${col_letter}1',
                        'format': grey_text_format
                    })

        return output_file_path
    else:
        return "FileName column not found in the DataFrame"

def create_filtered_df(df, language):
    filtered_columns = [
        col.replace('*', language) if '*' in col else col for col in column_order
    ]
    return df[filtered_columns]


def create_formated_excel_export():
    VERSION = os.environ.get('VERSION')
    if not VERSION:
        raise ValueError("VERSION environment variable is not set")

    data_dir = get_data_path(VERSION)
    excel_file_path = data_dir / f'Elementplan_{VERSION}_raw_data.xlsx'
    df = pd.read_excel(excel_file_path)

    languages = get_available_languages(df)
    print('YYY')
    print(languages)
    first_lang = languages[0]
    print('XXX')
    print(first_lang)
    column_lang = f'ProjectPhase{first_lang}'
    print('AAA')
    print(column_lang)
    
    
    df = explode_phases_to_matrix(df, column_lang, first_lang)
    df_sorted = sort_dataframe(df)
    df = rename_phase_columns(df_sorted)  # Assumes this function exists
    column_widths = [15, 20, 20, 55, 20, 35, 45, 20, 15, 20, 45, 25, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]

    

    for language in languages:
        filtered_df = create_filtered_df(df, language)
        #filtered_df = translate_column_names(filtered_df, language)
        output_file_path = export_with_custom_widths(filtered_df, column_widths, language, VERSION) #test
        print(output_file_path)

