import plotly.express as px
import plotly.graph_objects as go

from utils.data_processing import color_in

def plot_world_map(manufacturer, df):
    df['Availibility'] = df.apply (lambda row: color_in(row, manufacturer), axis=1)
    fig = px.choropleth(df,
                       locations=df.Code,
                       color='Availibility',
                       color_discrete_map={
                           f"{manufacturer} administered": df.Colors.iloc[1]
                       },
                        projection='natural earth'
                       )
    fig.update_layout(font_color='white', plot_bgcolor="#6379bf", paper_bgcolor="#1e2130")
    return fig

def generate_tree_map(df):
    fig = px.treemap(
        df,
        path=["Country", "Vaccine_Manufacturer"],
        color='Total_Vaccinations',
        color_continuous_scale=px.colors.sequential.Purp
    )

    fig.update_layout(width=1200, height=600, title_x=0.5, title_y=0.90, 
                        font_color='white', plot_bgcolor="#6379bf", paper_bgcolor="#1e2130", 
                        hoverlabel=dict(font_size=12))
    fig.data[0].hovertemplate = (
        '<b>%{label}</b>'
        '<br>' +
        '<br>' +
        '# of Vaccines: <br>%{value}' + 
        '<br>' +
        '<br>' 
    )   
    return fig 

def line_area_breakout_graph(df, country):
    fig = px.line(df[df['Country']==str(country)].sort_values(['Vaccine_Manufacturer','Date']),
                    x="Date",
                    y="Total_Vaccinations",
                    color='Vaccine_Manufacturer', 
                    labels=dict(Date="Date", Total_Vaccinations="Total Vaccinations", Vaccine_Manufacturer="Manufacturer")
                )
    fig.update_layout(margin=dict(l=5, r=5, t=20, b=20), paper_bgcolor="#1d202d", plot_bgcolor="#34394f", font_color="white")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
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
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285")
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, gridwidth=1, gridcolor="#5a6285", range=[0,100])
    return fig 