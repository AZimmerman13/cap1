import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


def show_a_row(df, index):
    lst = []
    for i in range(len(df.columns)):
        lst.append(df.iloc[index,i])
    return lst



def build_rename_dict(old, new):
    mapper = {k:v for (k,v) in zip(old, new)}
    return mapper



if __name__ == "__main__":

# Initialize dfs
    rentcols = ['id', 'name', 'average', 'average_moe', 'studio', 'studio_moe', '1bed', '1bed_moe', '2bed', '2bed_moe', '3bed', '3bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
    rent = pd.read_csv('data/rent.csv', skiprows=1)
    
# Cleaning and Organizing
    # removing placeholder string chrs
    rent.replace({'-': np.NaN, '**': np.NaN, '3,500+':3500, '***':np.NaN, '100-':100}, inplace=True)
    #rename columns
    
    rent.rename(columns=build_rename_dict(rent.columns, rentcols), inplace=True)
    #converting datatypes
    rent['studio'] = rent['studio'].astype(float)
    rent['studio_moe'] = rent['studio_moe'].astype(float)
    rent['1bed'] = rent['1bed'].astype(float)
    rent['1bed_moe'] = rent['1bed_moe'].astype(float)
    rent['4bed'] = rent['4bed'].astype(float)
    rent['4bed_moe'] = rent['4bed_moe'].astype(float)
    rent['5bed'] = rent['5bed'].astype(float)
    rent['5bed_moe'] = rent['5bed_moe'].astype(float)
    #fillna with average of each column
    rent = rent.iloc[:,2:].apply(lambda x: x.fillna(x.mean()),axis=0)