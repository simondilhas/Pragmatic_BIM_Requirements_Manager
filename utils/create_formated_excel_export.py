import pandas as pd
from pathlib import Path
import os

VERSION = 'SampleV.01'
languages = ['DE', 'EN', 'FR', 'IT']

column_order = [
    'FileName*',
    'ModelName*',
    'ElementName*',
    'ElementDescription*',
    'IfcEntityIfc4.0Name',
    'Pset',
    'AttributDescription*',
    'AttributName',
    'Unit',
    'DataTyp',
    'AllowedValues*',
    'ContainedIn*',
]



def get_data_path() -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        return Path('/mount/src/pragmatic_bim_requirements_manager') / 'data' / VERSION
    else:
        return Path(__file__).parent.parent / 'data' / VERSION


def extract_phase_definitions(df, column):
    all_phases = set()
    for phases in df[column].str.split(','):
        all_phases.update([phase.strip() for phase in phases if isinstance(phases, list)])
    
    all_phases = sorted(all_phases)
    return all_phases

def explode_phases_to_matrix(df, column):
    
    all_phases = extract_phase_definitions(df, 'ProjectPhaseEN')
    
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

def export_with_custom_widths(df, column_widths, language):
    if f'FileName{language}' in df.columns:
        unique_filenames = df[f'FileName{language}'].dropna().unique()

        with pd.ExcelWriter(f'Elementplan_{language}_{VERSION}.xlsx', engine='xlsxwriter') as writer:
            workbook = writer.book

            default_format = workbook.add_format({
                'text_wrap': True,
                'valign': 'top',
            })
            default_column_width = 20

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
                print(filename)
                filtered_df['Sort'] = range(1, len(filtered_df) + 1)

                filtered_df.to_excel(writer, sheet_name=filename[:31], index=False, startrow=0)  # Start writing data from row 1

                worksheet = writer.sheets[filename[:31]]

                                # Add the new rows at the top
                #worksheet.write('A1', 'Elementplan BBL')
                #worksheet.write('A2', 'Version:')
                #worksheet.write('B2', version)
                #worksheet.write('A3', 'Datum:')
                #worksheet.write('B3', datetime.now().strftime('%Y-%m-%d'))  # Current date
                #worksheet.write('A4', "")
                # Row 3 is left empty


                for col_num, col_name in enumerate(filtered_df.columns):
                    width = column_widths.get(col_name, default_column_width)
                    
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

        output_file_by_filename = f'Elementplan_{language}_{VERSION}.xlsx'
    else:
        output_file_by_filename = "FileName column not found in the DataFrame"

    return output_file_by_filename



def create_filtered_df(df, language):
    filtered_columns = [
        col.replace('*', language) if '*' in col else col for col in column_order
    ]
    return df[filtered_columns]

def main():
    data_dir = get_data_path()
    print(data_dir)
    excel_file_path = data_dir / f'Elementplan_{VERSION}_raw_data.xlsx'
    df = pd.read_excel(excel_file_path)
    
    df = explode_phases_to_matrix(df, 'ProjectPhaseEN') #TODO #7 pick any column with ProjectPhase that is not empty
    column_widths = {col: 20 for col in df.columns}

    for language in languages:
        filtered_df = create_filtered_df(df, language)
        output_file_path = export_with_custom_widths(filtered_df, column_widths, language)
        print(output_file_path)

if __name__ == "__main__":
    main()