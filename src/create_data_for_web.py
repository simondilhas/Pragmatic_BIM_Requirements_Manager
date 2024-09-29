
import pandas as pd
from src.load_data import load_file, store_file
from src.sort import sort_dataframe

#Is currently not really necessary but might become useful

def create_data_for_web(version:str):
    df = load_file(version, f'RawData_{version}.xlsx')
    sorted_df = sort_dataframe(df)
    store_file(sorted_df.to_csv(index=False), version, "data_for_web.csv")