import pandas as pd

def _convert_to_numeric(x):
    if pd.api.types.is_numeric_dtype(x):
        return x
    return pd.to_numeric(x.str.replace(',', '.'), errors='coerce')

def sort_dataframe(df):
    # Convert sorting columns to numeric
    for col in ['SortModels', 'SortElement', 'SortAttribute']:
        df[col] = _convert_to_numeric(df[col])

    # Sort by SortModels, then SortElement, then SortAttribute
    df_sorted = df.sort_values(
        by=['SortModels', 'SortElement', 'SortAttribute']
    )
    return df_sorted