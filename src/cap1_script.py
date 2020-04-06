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

def convert_data_types():
    pass


if __name__ == "__main__":

# Initialize dfs
    rent = pd.read_csv('data/rent.csv', skiprows=1)
    single_fem = pd.read_excel('data/femaleinc.xlsx', skiprows=2)
    single_male = pd.read_excel('data/maleinc.xlsx', skiprows=2)
    
# Cleaning and Organizing (Rent)
    # removing placeholder string chrs
    rentcols = ['id', 'name', 'average', 'average_moe', 'studio', 'studio_moe', '1bed', '1bed_moe', '2bed', '2bed_moe', '3bed', '3bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
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

# Cleaning and Organizing (Single Expenses)
    #drop blank lines (from excel formatting)
    single_fem.dropna(how='all', inplace=True)
    single_male.dropna(how='all', inplace=True)
    
    #transpose df and relabel columns
    single_fem = single_fem.T
    new_header = single_fem.iloc[0]
    single_fem = single_fem[1:]
    single_fem.columns = new_header
    #same for male
    single_male = single_male.T
    new_header = single_male.iloc[0]
    single_male = single_male[1:]
    single_male.columns = new_header

    # cut down the df to necessary columns only