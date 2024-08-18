import pandas as pd
import os
from datetime import datetime
import numpy as np
import openpyxl
import sys

import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, Border, Side, Alignment, PatternFill



version = 'V16_05'
data_dir = os.path.join('..', 'data', version)

file_name_attributes = os.path.join(data_dir, 'Attributes-Export_All.csv')
file_name_elements = os.path.join(data_dir, 'Elements-Export_All.csv')
file_name_models = os.path.join(data_dir, 'Models-Export_All.csv')


attributes_df = pd.read_csv(file_name_attributes)
elements_df = pd.read_csv(file_name_elements)
models_df = pd.read_csv(file_name_models)


def colum_name_list(df):
    for column in df.columns:
        print(column)


def sort_by_colume(df, column_name):
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
    df = df.sort_values(by=[column_name], ascending=[True], na_position='last')
