import pandas as pd

def _convert_to_numeric(x):
    if pd.api.types.is_numeric_dtype(x):
        return x
    return pd.to_numeric(x.str.replace(',', '.'), errors='coerce')

def sort_dataframe(df):
    # Convert sorting columns to numeric
    for col in ['SortModels', 'SortElement', 'SortAttribut']:
        df[col] = _convert_to_numeric(df[col])

    # Sort by SortModels, then SortElement, then SortAttribut
    df_sorted = df.sort_values(
        by=['SortModels', 'SortElement', 'SortAttribut']
    )
    return df_sorted