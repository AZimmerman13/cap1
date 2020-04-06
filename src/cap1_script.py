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
    mortgage = pd.read_csv('data/mortgage.csv')
    
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
    single_fem = single_fem[['Food', 'Housing', 'Healthcare', 'Transportation']]
    single_fem = single_fem.iloc[:, [0,2,4,6]]
    #same for male
    single_male = single_male[['Food', 'Housing', 'Healthcare', 'Transportation']]
    single_male = single_male.iloc[:, [0,2,4,6]]

# Cleaning and Organizing (Mortgage)
    # cut out extra info
    mortgage = mortgage.loc[:,'S2506_C01_029E':'S2506_C02_039M']
    mortgage = mortgage.iloc[:, range(0,len(mortgage.columns), 2)]

    #rename cols and remove extra row
    mortcols = ['<200', 'percent_share_<200', '200_399', 'percent_share_200_399', '400_599', 'percent_share_400_599', '600_799', 'percent_share_600_799', '800_999', 'percent_share_800_999', "1000_1499", 'percent_share_1000_1499', '1500_1999', 'percent_share_1500_1999', '2000_2499', 'percent_share_2000_2499', '2500_2999', 'percent_share_2500_2999', '>3000', 'percent_share_>3000', 'median_cost', 'percent_share_median']
    mortgage.rename(columns=build_rename_dict(mortgage.columns, mortcols), inplace=True)
    mortgage = mortgage[1:]

    