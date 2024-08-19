import pandas as pd
from pathlib import Path
import os

VERSION = 'SampleV.01'

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

def main():
    data_dir = get_data_path()
    print(data_dir)
    excel_file_path = data_dir / f'Elementplan_{VERSION}_raw_data.xlsx'
    df = pd.read_excel(excel_file_path)
    

    df = explode_phases_to_matrix(df, 'ProjectPhaseEN')
    print(df)

main()