import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats as stats
import matplotlib.mlab as mlab
import seaborn as sns
plt.style.use("fivethirtyeight")


def show_a_row(df, index):
    '''
    shows a row, friendo
    '''
    lst = []
    for i in range(len(df.columns)):
        lst.append(df.iloc[index, i])
    return lst


def build_rename_dict(old, new):
    '''
    Parameters: old: a list of columns to be replaced
        new: new column list
                

    Returns: mapper, a dictionary that can be used by DF.rename()
        to rename columns in a df

    '''
    mapper = {k: v for (k, v) in zip(old, new)}
    return mapper


def transpose_and_relabel(df):
    '''
    Parameter: df, a dataframe to be manipulated

    Returns: df, the manipulated dataframe
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
    '''
    Takes in two DataFrames with the same shape and
    data type (int or float).  Creates a third DataFrame
    which contains the average values of the given DataFrames.

    Parameters: df1, df2: Two pandas DataFrames to be averaged
                cols: new column names
                new_index: new index names
    '''
    new_df = pd.DataFrame(index=new_index, columns=cols)
    for i in cols:
        new_df[i] = (df1[i] + df2[i]) / 2

    return new_df


def plot_dist(mu, sigma, xmin, xmax, title, xlabel, color):
    '''
    Plots a distribution with the given keyword parameters.

    '''
    fig, ax = plt.subplots()
    x = np.linspace(xmin, xmax, 500)
    ax.plot(x, stats.norm.pdf(x, mu, sigma), color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.axvline(mu, color='coral', label=(f'Mean ${int(mu)}'), linewidth=1)
    ax.axvline(mu + sigma, color='coral', label=f"1 Std: ${int(mu + sigma)}", linewidth=1, linestyle='--')
    ax.axvline(mu + 2*sigma, color='coral', label=f"2 Std: ${int(mu + 2*sigma)}", linewidth=2, linestyle=':')
    ax.legend()
    plt.tight_layout()


def aggregate_mean_and_std(mu_lst, sigma_lst):
    '''
    Given a list of mus and sigmas, create 3 lists:
    means = the mu values
    std1 = mu plus 1 std
    std2 = mu plus 2 std

    returns the sum of each list
    (great for plotting vlines in a series of distributions)
    '''
    means = [int(i) for i in mu_lst]
    std1 = [int(i + j) for (i, j) in zip(mu_lst, sigma_lst)]
    std2 = [int(i + 2*j) for (i, j) in zip(mu_lst, sigma_lst)]
    return np.sum(means), np.sum(std1), np.sum(std2)


def weighted_means(ref_df, search_df, col, which_total):
    '''
    Calculates weighted mean for a single-column pandas
    DataFrame.


    Paremeters: ref_df: pandas series with a single column,
                    for ease of reference.
                search_df: pandas dataframe to search for the bucket
                    totals that contains the column in ref_df
                col: the name of the column shown in ref_df, as it
                    appears in search_df
                which_total: A sample total for the denominator
                    when calculating weights

    Returns: the weighted mean of a series (ref_df).
    '''
    lst = []
    for i in ref_df:
        weight = search_df['Bucket Total'][search_df[col] == i] / which_total
        lst.append(weight)

    mean = weighted_means_helper(lst, ref_df)
    return mean


def weighted_means_helper(weights, targets):
    '''
    Helper function to reduce complexity of weighted_means

    '''
    total = 0
    for (i, j) in zip(weights, targets):
        total += float(i*j)
    return total


if __name__ == "__main__":

# Data Pipeline
   # Initialize dfs
    rent = pd.read_csv('data/rent.csv', skiprows=1)
    single_fem = pd.read_excel('data/femaleinc.xlsx', skiprows=2)
    single_male = pd.read_excel('data/maleinc.xlsx', skiprows=2)
    mortgage = pd.read_csv('data/mortgage.csv')

   # Cleaning and Organizing (Rent)
    # removing placeholder string chrs
    rentcols = ['id', 'name', 'average', 'average_moe', 'studio', 'studio_moe', '1bed', '1bed_moe', '2bed', '2bed_moe', '3bed', '3bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
    rent.replace({'-': np.NaN, '**': np.NaN, '3,500+': 3500, '***': np.NaN, '100-': 100}, inplace=True)
    # rename columns
    rent.rename(columns=build_rename_dict(rent.columns, rentcols), inplace=True)

    # converting datatypes
    change_cols = ['studio', 'studio_moe', '1bed', '1bed_moe', '4bed', '4bed_moe', '5bed', '5bed_moe']
    convert_data_types(rent, change_cols, float)

    rent1 = rent

    # fillna with average of each column
    rent = rent.iloc[:, 2:].apply(lambda x: x.fillna(x.mean()), axis=0)

    rent_greater_than_2_std_above_mean = rent1[rent1['1bed'] > np.mean(rent['1bed']) + 2 * np.std(rent['1bed'])]

    n_largest = rent1.nlargest(20, '1bed')
    n_largest_names = n_largest[['name', '1bed']]

   # Cleaning and Organizing (Single Expenses)
    # drop blank lines (from excel formatting)
    single_fem.dropna(how='all', inplace=True)
    single_male.dropna(how='all', inplace=True)

    # transpose df and relabel columns
    single_fem = transpose_and_relabel(single_fem)
    single_male = transpose_and_relabel(single_male)

    # cut down the df to necessary columns only
    single_fem = single_fem[['Food', 'Housing', 'Healthcare', 'Transportation', 'Number of consumer units (in thousands)']]
    single_fem = single_fem.iloc[:, [0, 2, 4, 6, 8]]
    single_fem.rename(columns={'Number of consumer units (in thousands)': 'Bucket Total'}, inplace=True)

    single_male = single_male[['Food', 'Housing', 'Healthcare', 'Transportation', 'Number of consumer units (in thousands)']]
    single_male = single_male.iloc[:, [0, 2, 4, 6, 8]]
    single_male.rename(columns={'Number of consumer units (in thousands)': 'Bucket Total'}, inplace=True)

    # Breaking into categories and thinning out asymmetrical rows (tried to make this a function but .iloc did NOT like that)
    food_male = single_male['Food'].iloc[1:-2]
    healthcare_male = single_male['Healthcare'].iloc[1:-2]
    housing_male = single_male['Housing'].iloc[1:-2]
    transportation_male = single_male['Transportation'].iloc[1:-2]

    food_fem = single_fem['Food'].iloc[1:-1]
    healthcare_fem = single_fem['Healthcare'].iloc[1:-1]
    housing_fem = single_fem['Housing'].iloc[1:-1]
    transportation_fem = single_fem['Transportation'].iloc[1:-1]

    # creating weighted means
    total_women = single_fem['Bucket Total'].iloc[0]
    total_men = single_male['Bucket Total'].iloc[0]

    food_mean = np.mean([weighted_means(food_fem, single_fem, 'Food', total_women), weighted_means(food_male, single_male, 'Food', total_men)])
    healthcare_mean = np.mean([weighted_means(healthcare_fem, single_fem, 'Healthcare', total_women), weighted_means(healthcare_male, single_male, 'Healthcare', total_men)])
    housing_mean = np.mean([weighted_means(housing_fem, single_fem, 'Housing', total_women), weighted_means(housing_male, single_male, 'Housing', total_men)])
    transportation_mean = np.mean([weighted_means(transportation_fem, single_fem, 'Transportation', total_women), weighted_means(transportation_male, single_male, 'Transportation', total_men)])

    # standard deviations
    food_std = np.mean([food_male.std(), food_fem.std()])
    healthcare_std = np.mean([healthcare_male.std(), healthcare_fem.std()])
    housing_std = np.mean([housing_male.std(), housing_fem.std()])
    transportation_std = np.mean([transportation_male.std(), transportation_fem.std()])

   # Cleaning and Organizing (Mortgage)
    # cut out extra info
    mortgage = mortgage.loc[:, 'S2506_C01_029E':'S2506_C02_039M']
    mortgage = mortgage.iloc[:, range(0, len(mortgage.columns), 2)]

    # rename cols and remove extra row
    mortcols = ['<200', 'percent_share_<200', '200_399', 'percent_share_200_399', '400_599', 'percent_share_400_599', '600_799', 'percent_share_600_799', '800_999', 'percent_share_800_999', "1000_1499", 'percent_share_1000_1499', '1500_1999', 'percent_share_1500_1999', '2000_2499', 'percent_share_2000_2499', '2500_2999', 'percent_share_2500_2999', '>3000', 'percent_share_>3000', 'median_cost', 'percent_share_median']
    mortgage.rename(columns=build_rename_dict(mortgage.columns, mortcols), inplace=True)
    mortgage = mortgage[1:]

# The Plot Thickens
   #  Rent

    # Seaborn distplot
    plt.figure()
    plt.axvline(np.mean(rent['1bed']), color='coral', linewidth=1, label='Mean ($769)')
    plt.axvline(np.mean(rent['1bed']) + np.std(rent['1bed']), color='coral', linewidth=1, linestyle='--', label=f"1 Std: ${int(np.mean(rent['1bed']) + np.std(rent['1bed']))}")
    plt.axvline(np.mean(rent['1bed']) + 2 * np.std(rent['1bed']), color='coral', linewidth=2, linestyle=':', label=f"2 Std: ${int(np.mean(rent['1bed']) + 2 * np.std(rent['1bed']))}")
    sns.distplot(rent['1bed'], axlabel="Monthly Rent ($)")
    plt.legend()
    plt.title('Average 1BR Rent (normalized)')
    plt.tight_layout()
    plt.savefig('images/rent_distplot.png')
    plt.close()

    # Mortgage (Not used)
    # fig, ax = plt.subplots(figsize=(10,5))
    # labels = [list(mortgage.columns)[i] for i in list(range(0,22,2))]
    # data = [int(i) for i in mortgage.iloc[0].iloc[list(range(0,19,2))]]  # every other entry from the first row
    # width = 1.8
    # ticklocations = np.array([1,3,5,7,9,11,13,15,17,19])
    # ax.bar(ticklocations, list(data), width, alpha=.8)
    # ax.set_xticklabels(labels, fontsize=14, rotation=60)
    # ax.set_title("Mortgage Rates ($/month)")
    # ax.set_yscale("linear")
    # plt.tight_layout()
    # plt.savefig('images/mortgage_hist.png')
    # plt.close()
    # # plt.show()

   # Expenses
    n = len(food_fem)  # for calculating standard error

    plot_dist(food_mean/12, food_std/np.sqrt(n), 0, 1600, "Average Monthly Food Cost", "Cost ($)", 'orange')
    plt.savefig('images/food_dist.png')
    # plt.show()
    plt.close()

    plot_dist(housing_mean/12, housing_std/np.sqrt(n), 0, 5500, "Average Monthly Housing Cost", "Cost ($)", 'violet')
    plt.savefig('images/housing_dist.png')
    # plt.show()
    plt.close()


    plot_dist(healthcare_mean/12, healthcare_std/np.sqrt(n), 0, 1300, "Average Monthly Healthcare Cost", "Cost ($)", 'yellowgreen')
    plt.savefig("images/healthcare_dist.png")
    # plt.show()
    plt.close()

    plot_dist(transportation_mean/12, transportation_std/np.sqrt(n), 0, 2900, "Average Monthly Transportation Cost", "Cost ($)", 'tan')
    plt.savefig("images/transportation_dist.png")
    # plt.show()
    plt.close()

   # Final Plot

    mu_lst = [food_mean/12, healthcare_mean/12, np.mean(rent['1bed']), transportation_mean/12]
    sigma_lst = [food_std/np.sqrt(n), healthcare_std/np.sqrt(n), np.std(rent['1bed'])/np.sqrt(n), transportation_std/np.sqrt(n)]
    total_mean, total_std1, total_std2 = aggregate_mean_and_std(mu_lst, sigma_lst)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    labels = ['Mean', '1 Std', '2 Std']
    data = [total_mean, total_std1, total_std2]
    width = 1.8
    y = np.arange(len(data))

    ax.barh(y, data, alpha=.8, align="center")
    ax.set_yticks(y)
    ax.xaxis.grid(True)
    ax.set_yticklabels(labels, fontsize=14)
    ax.set_title("Total Core Monthly Expenses Estimate")
    ax.axvline(1063, color='maroon', label='Federal Poverty Level ($1063)', linewidth=2)
    ax.axvline(1200, color='olive', label=f"COVID stimulus ($1200)", linewidth=2, linestyle='-.')
    ax.axvline(1257, color='deeppink', label=f"Federal Minimum Wage ($1257)", linewidth=1.4, linestyle='--')
    ax.axvline(2080, color='black', label=f"CO Minimum Wage ($2080)", linewidth=2, linestyle=':')
    ax.set_xlabel("Monthly Expense ($)")
    ax.legend()

    # get labels on the bars
    for i, v in enumerate(data):
        ax.text(v-10, i, f'${v}', color='blue', fontweight='bold', rotation=330)

    plt.tight_layout()
    plt.savefig('images/final_plot.png')
    plt.close()
