
import pandas as pd
from src.load_data import load_file, store_file

#Is currently not really necessary

def create_data_for_web(version:str):
    df = load_file(version, f'RawData_{version}.xlsx')
    store_file(df.to_csv(index=False), version, "data_for_web.csv")