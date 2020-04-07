import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
import matplotlib.mlab as mlab
plt.style.use("fivethirtyeight")


def show_a_row(df, index):
    '''

    '''
    lst = []
    for i in range(len(df.columns)):
        lst.append(df.iloc[index,i])
    return lst



def build_rename_dict(old, new):
    '''

    '''
    mapper = {k:v for (k,v) in zip(old, new)}
    return mapper



def transpose_and_relabel(df):
    '''


    '''
    df = df.T
    new_headers = df.iloc[0]
    df = df[1:]
    df.columns = new_headers
    return df

def convert_data_types(df, cols, target):
        '''
        Parameters: df: a Pandas DataFrame
                    cols: a list of columns to be changed
                    type: the target datatype

        Returns: Nothing, this function makes changes to a df in place.


        '''
        for i in cols:
            df[i] = df[i].astype(target)

def merge_and_average_dfs(df1, df2, cols, new_index):
    new_df = pd.DataFrame(index=new_index, columns=cols)
    for i in cols:
        new_df[i] = (df1[i] + df2[i]) / 2

    return new_df





if __name__ == "__main__":

# Initialize dfs
    rent = pd.read_csv('data/rent.csv', skiprows=1)
    single_fem = pd.read_excel('data/femaleinc.xlsx', skiprows=2)
    single_male = pd.read_excel('data/maleinc.xlsx', skiprows=2)
    mortgage = pd.read_csv('data/mortgage.csv')
    all_singles_average = pd.DataFrame(columns=['Food', 'Housing', 'Healthcare', "Transportation"])
    
# Cleaning and Organizing (Rent)
    # removing placeholder string chrs
    rentcols = ['id', 'name', 'average', 'average_moe', 'studio', 'studio_moe', '1bed', '1bed_moe', '2bed', '2bed_moe', '3bed', '3bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
    rent.replace({'-': np.NaN, '**': np.NaN, '3,500+':3500, '***':np.NaN, '100-':100}, inplace=True)
    #rename columns
    rent.rename(columns=build_rename_dict(rent.columns, rentcols), inplace=True)
    
    # converting datatypes
    change_cols = ['studio', 'studio_moe', '1bed', '1bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
    convert_data_types(rent, change_cols, float)

    #fillna with average of each column
    rent = rent.iloc[:,2:].apply(lambda x: x.fillna(x.mean()),axis=0)

# Cleaning and Organizing (Single Expenses)
    #drop blank lines (from excel formatting)
    single_fem.dropna(how='all', inplace=True)
    single_male.dropna(how='all', inplace=True)
    
    #transpose df and relabel columns
    single_fem = transpose_and_relabel(single_fem)
    #same for male
    single_male = transpose_and_relabel(single_male)

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

# The Plot Thickens
    #Rent
    fig, ax = plt.subplots(figsize=(6,6.8))
    ax.hist(rent['1bed'], bins=40, alpha=.75, density=1)
    ax.set_xlabel('Average Rent (Dollars)')
    ax.set_title("Average 1BR Rent (normalized)")
    ax.axvline(np.mean(rent['1bed']), color='coral', linewidth=1, label='Mean ($769)')
    plt.tight_layout()
    ax.legend()

    plt.savefig('images/rent_hist.png')

    #fitting a line
    x = np.linspace(0,2300, len(rent['1bed']))
    mu, sigma = stats.norm.fit(rent['1bed'])
    pdf_g = stats.norm.pdf(x, mu, sigma)
    ax.plot(x,pdf_g, 'r--', linewidth=1.5)

    
    plt.savefig('images/rent_hist_with_dist.png')
    plt.close()

    #Mortgage
    fig, ax = plt.subplots(figsize=(10,5))
    labels = [list(mortgage.columns)[i] for i in list(range(0,22,2))]
    data = [int(i) for i in mortgage.iloc[0].iloc[list(range(0,19,2))]]  # every other entry from the first row
    width = 1.8
    ticklocations = np.array([1,3,5,7,9,11,13,15,17,19])
    ax.bar(ticklocations, list(data), width, alpha=.8)
    ax.set_xticklabels(labels, fontsize=14, rotation=60)
    ax.set_title("Mortgage Rates ($/month)")
    ax.set_yscale("linear")
    plt.tight_layout()
    plt.savefig('images/mortgage_hist.png')
    plt.close()
    # plt.show()

    #Expenses
    food_male = single_male['Food'].iloc[1:-2]
    healthcare_male = single_male['Healthcare'].iloc[1:-2]
    housing_male = single_male['Housing'].iloc[1:-2]
    transportation_male = single_male['Transportation'].iloc[1:-2]

    food_fem =single_fem['Food'].iloc[1:-1]
    



