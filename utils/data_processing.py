import os
 
import pandas as pd 

def init_data():
    df = pd.read_csv(os.path.join("data", "VaccineData.csv"))
    df.drop(df.loc[df['Country'] == 'European Union'].index, inplace=True, axis=0)
    df = get_manufacturer_country(df)
    eff_df = init_efficacy_df(df)
    perc_df = pd.read_csv(os.path.join("data", "share-people-vaccinated-covid.csv"))

    return df, eff_df, perc_df

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
