import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs import Layout
import pandas as pd

from utils.data_processing import color_in

def plot_world_map(manufacturer, df):
    df['Vaccine'] = df.apply (lambda row: color_in(row, manufacturer), axis=1)
    fig = px.choropleth(df,
                       locations=df.Code,
                       color='Vaccine',
                       color_discrete_map={
                           f"{manufacturer}": df.Colors.iloc[1]
                       },
                        projection='natural earth',
                        # hover_data = ['Country'],
                        # hover_label=dict(bgcolor="#161a28")
                        )
    fig.update_traces(hovertemplate=None)           
    fig.update_layout(font_color='white', plot_bgcolor="#6379bf", paper_bgcolor="#1e2130")
    fig.update_layout(titlefont=dict(size =16, color='white'))
    fig.update_traces(showlegend=False)
    return fig

def generate_tree_map(df):
    fig = px.treemap(
        df.loc[df.groupby(['Country','Vaccine_Manufacturer']).Date.idxmax()],
        path=["Country", "Vaccine_Manufacturer"],
        color='Total_Vaccinations',
        color_continuous_scale=px.colors.sequential.Purp,
        # hover_data=['Total_Vaccinations']
    )
    fig.update_traces(hovertemplate='Number of Doses: <br>%{customdata[0]}')
    fig.update_layout(title_text="<b>Number of Vaccine Variants<br></b><i>by Country</i>" ,title_x=0.05, 
                        font_color='white', plot_bgcolor="#6379bf", paper_bgcolor="#1e2130", 
                        hoverlabel=dict(font_size=12))
    fig.data[0].hovertemplate = (
        '<b>%{label}</b>'
        '<br>' +
        '%{value}' + 
        '<br>' 
    )   
    # fig.data[0].hovertemplate = ('<b>%{label}</b>'
    #     '<br>' +
    #     '<br>' +
    #     'Number of Vaccine Doses: <br>%{customdata[0]}') 

    return fig 

def line_area_breakout_graph(df, country):
    fig = px.line(df[df['Country']==str(country)].sort_values(['Vaccine_Manufacturer','Date']),
                    x="Date",
                    y="Total_Vaccinations",
                    color='Vaccine_Manufacturer', 
                    labels=dict(Date="Date", Total_Vaccinations="Total Vaccinations", Vaccine_Manufacturer="Manufacturer")
                )
    fig.update_layout(margin=dict(l=5, r=5, t=20, b=20), paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    return fig

def generate_percent_vaccinated_graph(data, countries_selected):
    fog = go.Figure(layout=dict(template='plotly')) # don't remove or change this, unless you want to die it's a bugfix/workaround for Dash lol
    if isinstance(countries_selected, list):
        filtered_df = data[data["Entity"].isin(countries_selected)]
        fig = px.line(filtered_df, 
                            x = "Day",
                            y = "people_vaccinated_per_hundred",
                            color="Entity",
                            labels=dict(Day="Date", people_vaccinated_per_hundred="Percentage Vaccinated (%)", Entity="Country/Countries"))
    else:
        filtered_df = data[data["Entity"] == countries_selected]
        fig = px.line(filtered_df,
                        x = "Day",
                        y = "people_vaccined_per_hundred",
                        labels=dict(x="Date", y="Percentage Vaccinated (%)"))
    fig.update_layout(margin=dict(l=5, r=5, t=20, b=20), paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285", range=[0,100])
    return fig 


#ALLEN CODE 
def protected_over_time_agg(df, country):
    # Generate dataframe
    agg_df= df[df['Country'] == country][['Country',
                                               'Date',
                                               'Vaccine_Manufacturer', 
                                               'perc of manuf vacc not prot alpha',
                                               'perc of manuf vacc not prot delta',
                                               'perc of manuf vacc not prot omicron']].melt(id_vars = ['Country', 'Vaccine_Manufacturer', 'Date'],
                                                                                            var_name = 'Variant',
                                                                                            value_name = 'perc of manuf vacc not prot')

    # Map column values for readibility
    agg_df['Variant'] = agg_df['Variant'].map({'perc of manuf vacc not prot alpha': '% Alpha Not Protected',
                                               'perc of manuf vacc not prot delta': '% Delta Not Protected',
                                               'perc of manuf vacc not prot omicron': '% Omicron Not Protected'})
    
    # # Define backdrop
    # layout = Layout(
    # paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='rgba(0,0,0,0)')
    
    # Generate lineplot
    fig = px.line(agg_df.groupby(['Variant', 'Date']).sum().reset_index(),
                  x = 'Date',
                  y = 'perc of manuf vacc not prot',
                  range_y = [0, 100],
                  color = 'Variant',
                  labels = {'perc of manuf vacc not prot': '% of Total Doses'})
                #   title="layout.hovermode='x unified'")
    fig.update_layout(paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    
    fig.update_layout(title_text = "<b>"+country+"</b>" +": <b>Percentage of Total Doses Administered not Protected from Infection<br></b><i>over Time, by Variant</i>", 
                      title_x = 0.05,
                      titlefont=dict(size =16, color='white'),
                      yaxis = dict(tickformat = "0.0f"),margin=dict(t=105))
    fig.update_xaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC')
    fig.update_yaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC')
    fig.update_traces(line = dict(width=3))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    
    return fig



def total_vacc_admin(df):
    # Subset Dataframe
    df_perc = df.loc[df.groupby(['Country',
                       'Vaccine_Manufacturer']).Date.idxmax()].sort_values('Total')[['Country', 
                                                                                     'Vaccine_Manufacturer',
                                                                                     'Total_Vaccinations',
                                                                                     'perc of manuf vacc']].sort_values(['Country', 
                                                                                                                         'perc of manuf vacc'],
                                                                                                                         ascending = [True, False])
    # Create Top 2 + Others Dataframe
    df_others = (
                df_perc.groupby('Country').apply(
                    lambda x: pd.concat(
                                        [x.iloc[:2],
                                         x.iloc[2:].groupby('Country', as_index=False)
                                         .agg({'perc of manuf vacc': sum})
                                         .assign(Vaccine_Manufacturer='Others')]))
                .reset_index(drop=True)
    )

    # Create visualization
    fig = px.bar(df_others.sort_values('Total_Vaccinations', ascending = False),
             x = 'Country',
             y = 'perc of manuf vacc',
             color = 'Vaccine_Manufacturer',
             color_discrete_sequence = px.colors.qualitative.Safe,
             labels = {'perc of manuf vacc': '% of Total Doses', 'Vaccine_Manufacturer': 'Vaccine Manufacturer'},
            )


    # Adjust formatting
    fig.update_layout(title_text = "<b>Percentage of Total Doses by Manufacturer<br></b><i>by Country</i>", 
                      title_x = 0.03,
                      titlefont=dict(size =16, color='white'),
                      yaxis = dict(tickformat = "0.0f"),
                      paper_bgcolor = "#1d202d", 
                      plot_bgcolor = "rgba(0,0,0,0)",
                      hoverlabel=dict(bgcolor="#161a28"))
    fig.update_traces(hovertemplate = None)
    fig.update_layout(hovermode = "x unified",
                      legend_font_color = 'white')
    fig.update_xaxes(showline = False, linewidth = 0, linecolor = '#DCDCDC', mirror = True,
                     showgrid = False, gridwidth = 1, gridcolor = '#161a28',
                     title = '', zeroline=False)
    fig.update_yaxes(title_font_color="white",
                     color = 'white', zeroline=False, mirror = True, gridcolor = '#161a28')
    fig.update_xaxes(title_font_color="white",
                     color = 'white')
    # fig.update_layout(paper_bgcolor="#1d202d")

    # Display graph
    return fig



def create_area_graph(df, country):
    # Create dataframe
    df_rolling = df[['Country', 'Vaccine_Manufacturer', 'Date', 'perc of manuf vacc']]

    # Filter on country
    df_rolling = df_rolling[df_rolling['Country'] == country]
    
    # Create visual
    fig = px.area(df_rolling,
             x = 'Date',
             y = 'perc of manuf vacc',
             color = 'Vaccine_Manufacturer',
             labels = {'perc of manuf vacc': '% of Total Doses', 'Vaccine_Manufacturer': 'Vaccine Manufacturer'},
             hover_data = ['Vaccine_Manufacturer', 'perc of manuf vacc'],
             title = "layout.hovermode='x unified'",
             color_discrete_sequence = px.colors.qualitative.Safe)
    
    # Adjust formatting
    fig.update_layout(title_text="<b>"+country+"</b>" +": <b>Percentage of Total Doses by Manufacturer<br></b><i>over Time</i>",
                        yaxis = dict(tickformat = "0.0f"),
                      paper_bgcolor = "rgba(0,0,0,0)", 
                      plot_bgcolor = "rgba(0,0,0,0)")
    fig.update_traces(hovertemplate = None)
    fig.update_layout(hovermode = "x unified")
    fig.update_layout(paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")

    return fig

def create_bubble_plot(df):
    # Define efficacy table
    df_efficacy = df.groupby('Vaccine_Manufacturer')[['Vaccine_Manufacturer', 'Eff Severe Disease Alpha', 
                                                      'Eff Infection Alpha', 'Eff Severe Disease delta', 
                                                      'Eff Infection Delta', 'Eff Severe Disease Omicron', 
                                                      'Eff Infection Omicron']].mean().reset_index()
    
    # Collapse efficacy columns to rows
    df_efficacy = df_efficacy.melt(id_vars = ['Vaccine_Manufacturer'],
                                   var_name = 'Type of Efficacy',
                                   value_name = 'People out of 100').sort_values('Vaccine_Manufacturer')
    # Extract variant name
    df_efficacy['Variant'] = [val.split().pop().capitalize() for val in df_efficacy['Type of Efficacy']]
    
    # Extract type of protection
    df_efficacy['Type of Protection'] = [val.rsplit(' ', 1)[0] for val in df_efficacy['Type of Efficacy']]
    
    # Remap column values for better readability
    df_efficacy['Type of Protection'] = df_efficacy['Type of Protection'].map({'Eff Severe Disease': 'Severe Disease',
                                                                               'Eff Infection': 'Infection'})    
    # Generate visual
    fig = px.scatter(df_efficacy.sort_values('Type of Protection'), 
                 x="Vaccine_Manufacturer",
                 y="Variant",
                 size="People out of 100", 
                 color="People out of 100",
                 size_max = 30,
                 animation_frame = 'Type of Protection',
                 hover_name='People out of 100',
                 hover_data = ['Variant', 'People out of 100'],
                 title="layout.hovermode='closest'")
    
    # Format visual
    fig.update_layout(title_text = "<b>Vaccine Efficacy**<br></b><i>by Variant, Manufacturer</i>", 
                          title_x = 0.05,
                          titlefont=dict(size =16, color='white'),
                          yaxis = dict(tickformat = "0.0f"))
    fig.update_xaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC',
                     title = '')
    fig.update_yaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC',
                     title = '')
    fig.update_traces(hovertemplate=None)
    fig.update_layout(hovermode="closest")

    fig.update_layout(margin=dict(t = 105), paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    #fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    #ig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285", range=[0,100])
    
    # Display visual
    return fig 




def breakthrough_agg(df, country):
    # Generate dataframe
    agg_df= df[df['Country'] == country][['Country',
                                               'Date',
                                               'Vaccine_Manufacturer', 
                                               'breakthrough alpha',
                                               'breakthrough delta',
                                               'breakthrough omicron']].melt(id_vars = ['Country', 'Vaccine_Manufacturer', 'Date'],
                                                                                            var_name = 'Variant',
                                                                                            value_name = 'Breakthrough')

    # Map column values for readibility
    agg_df['Variant'] = agg_df['Variant'].map({'breakthrough alpha': 'Alpha Breakthrough',
                                               'breakthrough delta': 'Delta Breakthrough',
                                               'breakthrough omicron': 'Omicron Breakthrough'})
    
    # Define backdrop
    # layout = Layout(
    # paper_bgcolor='rgba(0,0,0,0)',
    # plot_bgcolor='rgba(0,0,0,0)')
    
    # Generate lineplot
    fig = px.line(agg_df.groupby(['Variant', 'Date']).sum().reset_index(),
                  x = 'Date',
                  y = 'Breakthrough',
                  range_y = [0, 100],
                  color = 'Variant',
                  labels = {'Breakthrough': 'Breakthrough per 100 people'},
                  title="layout.hovermode='x unified'",
                  color_discrete_sequence = px.colors.qualitative.Safe)
    fig.update_layout(paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    
    fig.update_layout(title_text = "<b>"+country+"</b>" +": <b>Breakthrough Rate per 100 People<br></b><i>over Time, by Variant</i>", 
                      title_x = 0.05,
                      titlefont=dict(size =16, color='white'),
                      yaxis = dict(tickformat = "0.0f"))
    fig.update_xaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC')
    fig.update_yaxes(showline = True, linewidth = 1, linecolor = '#DCDCDC', mirror = True,
                     showgrid = True, gridwidth = 1, gridcolor = '#DCDCDC')
    fig.update_traces(line = dict(width=3))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x unified")
    
    return fig 