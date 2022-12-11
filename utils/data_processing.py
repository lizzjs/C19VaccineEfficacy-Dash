import os
 
import pandas as pd 

def init_data():
    df = pd.read_csv(os.path.join("data", "VaccineData.csv"))
    df.drop(df.loc[df['Country'] == 'European Union'].index, inplace=True, axis=0)
    df = get_manufacturer_country(df)
    eff_df = init_efficacy_df(df)
    perc_df = pd.read_csv(os.path.join("data", "share-people-vaccinated-covid.csv"))

    return df, eff_df, perc_df

'''
#COMMENTED OUT CODE 
# Really bad function to fill in missing data for time series - Allen
def fill_missing_data(test):
    dataframes =[]
    for country in test['Country'].unique():
        df = test[test['Country']==country]
        manuflist = list(df['Vaccine_Manufacturer'].unique())
        for manuf in manuflist:
            df_sm = df[df['Vaccine_Manufacturer']==manuf]
            df_expanded = pd.DataFrame({'Date':pd.date_range(start=df_sm.loc[df_sm.Date.idxmin()]['Date'], end=df.loc[df.Date.idxmax()]['Date'])})
            df_expanded = pd.merge(df_expanded,df_sm,how='left',on=['Date'])
            df_expanded = df_expanded.ffill()
            dataframes.append(df_expanded)
    return pd.concat(dataframes)
'''


## ALLEN ## 
# Function to fill in non-existent dates for manufacturers for each country
# Assumption: For non-existent dates, it is assumed that the vaccinations given is constant
def fill_missing_data(df_in):
    dataframes =[]
    for country in df_in['Country'].unique():
        df = df_in[df_in['Country']==country]
        manuflist = list(df['Vaccine_Manufacturer'].unique())
        for manuf in manuflist:
            df_sm = df[df['Vaccine_Manufacturer']==manuf]
            df_expanded = pd.DataFrame({'Date':pd.date_range(start=df_sm.loc[df_sm.Date.idxmin()]['Date'], end=df.loc[df.Date.idxmax()]['Date'])})
            df_expanded = pd.merge(df_expanded,df_sm,how='left',on=['Date'])
            df_expanded = df_expanded.ffill()
            dataframes.append(df_expanded)
    return pd.concat(dataframes)


## ALLEN ## 
# Function to collapse expanded dataframe such that it only includes the dates of the original dataframe 
def collapse(df,df_expanded):
    dataframes =[]
    for country in df_expanded['Country'].unique():
        d_f = df_expanded[df_expanded['Country']==country]
        dates = df[df['Country']==country]['Date']
        d_f = d_f[d_f['Date'].isin(dates)]
        dataframes.append(d_f)
    return pd.concat(dataframes)


## ALLEN ## 
# Function to initialize dataframe with efficacy, proportion, and breakthrough calculations
def init_efficacy_df(df):
    #Convert Date col to datetime type
    df['Date'] = pd.to_datetime(df['Date'])

    # drop European Union rows, since they are unneeded for this analysis
    df.drop(df.loc[df['Country'] == 'European Union'].index, inplace=True, axis=0)

    # drop columns that are not alpha, delta, or omnicrom 
    df.drop(df.columns[[4,5,8,9,10,11]], axis=1, inplace = True)

    #load and merge efficacy data 
    efficacy_path = os.path.join('data', 'Vaccine_Efficacy.csv')
    df_eff = pd.read_csv(efficacy_path)
    df_eff.drop(df_eff.columns[[1,2,5,6,7,8]], axis=1, inplace = True)
    df = pd.merge(df,df_eff,on='Vaccine_Manufacturer',how='left')

    #expanded dataframe with forward filled data for all dates in timeseries 
    df_expanded = fill_missing_data(df)

    #added column for total vaccine of all manuf for specific date and country for proportion calculations
    total_vacc = df_expanded.groupby(['Country','Date']).sum()[['Total_Vaccinations']].rename(columns={'Total_Vaccinations':'Total'})

    #merge total vaccination per day calculation to df_expanded 
    df_expanded = pd.merge(df_expanded,total_vacc,how='left',on=['Country','Date'])

    #path to share-people-vaccinated-covid csv file 
    share_people_path = os.path.join("data", "share-people-vaccinated-covid.csv")
    #merge number vaccined (at least one dose) per 100 people to dataframe
    df_proportions = pd.read_csv(share_people_path)
    df_proportions.drop(['Code','145610-annotations'],inplace=True,axis=1)
    df_proportions.columns = ['Country','Date','overall vacc per 100 ppl']
    df_proportions['Date'] = pd.to_datetime(df_proportions['Date'])
    df_expanded = pd.merge(df_expanded,df_proportions,on=['Country','Date'],how='left')

    ## proportion calculations 
    # percent of specific manuf vaccine out of the total vaccinations administered
    df_expanded['perc of manuf vacc'] = df_expanded['Total_Vaccinations'] / df_expanded['Total'] * 100
    # specific manuf vaccine administered per 100 ppl
    df_expanded['num manuf vacc per 100 ppl'] = df_expanded['perc of manuf vacc'] / 100 * df_expanded['overall vacc per 100 ppl']

    ## Alpha percentage of vaccinations not offereing protection
    # percent of specific manuf vaccine out of total administered on the date not offering protection
    df_expanded['perc of manuf vacc not prot alpha'] = df_expanded['perc of manuf vacc'] * (1 - df_expanded['Eff Infection Alpha']/100) 

    ## Delta percentage of vaccinations not offereing protection
    # percent of specific manuf vaccine out of total administered on the date not offering protection
    df_expanded['perc of manuf vacc not prot delta'] = df_expanded['perc of manuf vacc'] * (1 - df_expanded['Eff Infection Delta']/100)

    ## Omicron percentage of vaccinations not offereing protection
    # percent of specific manuf vaccine out of total administered on the date not offering protection
    df_expanded['perc of manuf vacc not prot omicron'] = df_expanded['perc of manuf vacc'] * (1 - df_expanded['Eff Infection Omicron']/100) 

    ## Alpha breakthrough calculations 
    # people who are not protected who were given the specific manuf vac per 100 ppl
    df_expanded['breakthrough alpha'] = df_expanded['num manuf vacc per 100 ppl'] * (1 - (df_expanded['Eff Infection Alpha']/100)) 

    ## Delta breakthrough calculations 
    # people who are not protected who were given the specific manuf vac per 100 ppl
    df_expanded['breakthrough delta'] = df_expanded['num manuf vacc per 100 ppl'] * (1 - (df_expanded['Eff Infection Delta']/100)) 

    # Omicron breakthrough calculations 
    # people who are not protected who were given the specific manuf vac per 100 ppl
    df_expanded['breakthrough omicron'] = df_expanded['num manuf vacc per 100 ppl'] * (1 - (df_expanded['Eff Infection Omicron']/100)) 

    #collapse datafarme 
    df = collapse(df, df_expanded)

    #drop na rows in collapse df due to missing data from share-people-vaccinated-covid.csv
    df = df.dropna()

    return df

'''
#COMMENTED OUT CODE 
def init_efficacy_df(df):
    df['Date'] = pd.to_datetime(df['Date'])

    # drop European Union rows, since they are unneeded for this analysis
    df.drop(df.loc[df['Country'] == 'European Union'].index, inplace=True, axis=0)

    # drop columns that are not alpha, delta, or omnicrom 
    df.drop(df.columns[[4,5,8,9,10,11]], axis=1, inplace = True)

    # find number of unique vaccines giving by vaccine manufacturer
    df.groupby('Country')['Vaccine_Manufacturer'].nunique()

    efficacy_path = os.path.join('data', 'Vaccine_Efficacy.csv')
    df_eff = pd.read_csv(efficacy_path)
    df_eff.drop(df_eff.columns[[1,2,5,6,7,8]], axis=1, inplace = True)
    df = pd.merge(df,df_eff,on='Vaccine_Manufacturer',how='left')

    # Find latest date for each country/manuf pair
    df_latest = df.loc[df.groupby(['Country','Vaccine_Manufacturer']).Date.idxmax()]

    #expanded dataframe with forward filled data for all dates in timeseries 
    df_expanded = fill_missing_data(df)

    #added column for total vaccine of all manuf for specific date and country for proportion calculations
    total_vacc = df_expanded.groupby(['Country','Date']).sum()[['Total_Vaccinations']].rename(columns={'Total_Vaccinations':'Total'})

    #merge total vaccination per day calculation to df 
    df = pd.merge(df,total_vacc,on=['Country','Date'],how='left')

    share_people_path = os.path.join("data", "share-people-vaccinated-covid.csv")
    #merge number vaccined (at least one dose) per 100 people to dataframe
    df_proportions = pd.read_csv(share_people_path)
    df_proportions.drop(['Code','145610-annotations'],inplace=True,axis=1)
    df_proportions.columns = ['Country','Date','overall vacc perc']
    df_proportions['Date'] = pd.to_datetime(df_proportions['Date'])
    df_proportions['overall vacc perc'] = df_proportions['overall vacc perc'] 
    df = pd.merge(df,df_proportions,on=['Country','Date'],how='left')

    # percent of specific manuf vaccine out of the total vaccinations administered
    df['perc of manuf vacc'] = df['Total_Vaccinations'] / df['Total'] * 100

    # percent of the specific manuf vaccine that offers protection against infection based on efficacy 
    df['perc infection protected alpha'] = df['perc of manuf vacc'] / 100 * df['Eff Infection Alpha']
    df['perc infection protected delta'] = df['perc of manuf vacc'] / 100 * df['Eff Infection Delta']
    df['perc infection protected omicron'] = df['perc of manuf vacc'] / 100 * df['Eff Infection Omicron']

    # percent of the specific manuf vaccine that does not offer protection against infection based on efficacy 
    df['perc infection unprotected alpha'] = 100 - df['perc infection protected alpha']
    df['perc infection unprotected delta'] = 100 - df['perc infection protected delta']
    df['perc infection unprotected omicron'] = 100 - df['perc infection protected omicron']

    # breakthrough infection = percent of population that is succeptible to breakout infection based on vaccinations administered and efficacy rates
    df['breakthrough alpha'] = (100 - df['perc infection protected alpha']) * df['overall vacc perc'] / 100
    df['breakthrough delta'] = (100 - df['perc infection protected delta']) * df['overall vacc perc'] / 100
    df['breakthrough omicron'] = (100 - df['perc infection protected omicron']) * df['overall vacc perc'] / 100

    return df

'''

def assign_country_code (row, codes):
    try:
        return codes[row.Country] 
    except:
        return None

def assign_color(row, colors):
    try: 
        return colors[row.Vaccine_Manufacturer]
    except:
        return None

def color_in(row, manufacturer):
    if row.Vaccine_Manufacturer == manufacturer:
        return f"{manufacturer} administered"
        
def get_manufacturer_country(df):
    manufacturer = list(df['Vaccine_Manufacturer'].unique())
    country = list(df['Country'].unique())

    url="https://raw.githubusercontent.com/plotly/dash-sample-apps/f44f386e890c72846e39a871cde06a58f2367b5c/apps/dash-phylogeny/data/2014_world_gdp_with_codes.csv"
    c=pd.read_csv(url)

    df_countries = list(df.Country.unique())

    country_name, country_code = list(c.COUNTRY), list(c.CODE)

    country_codes = {}
    for name, code in zip(country_name, country_code):
        country_codes[name] = code
    country_codes['Czechia'] = 'CZE'

    colors = ["#2e0166", "#6e017a", "#4c017a", "#36017a", "#4c00b0", "#7600bc", "#8a00c2", "#a000c8", "#b100cd", "#be2ed6", "#ca5cdd", "#da8ee7", "#e8bcf0"]

    manufacturer_colors = {}
    for name, color in zip(manufacturer, colors):
        manufacturer_colors[name] = color

    df['Code'] = df.apply (lambda row: assign_country_code(row, country_codes), axis=1)
    df['Colors'] = df.apply (lambda row: assign_color(row, manufacturer_colors), axis=1)
    
    return df

def get_efficacy_data():
    pass 
