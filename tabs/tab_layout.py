from dash import Dash, dcc, html, Input, Output

from utils.data_processing import init_data
from utils.generate_visualizations import plot_world_map, line_area_breakout_graph, generate_percent_vaccinated_graph, generate_tree_map
from utils.build_components import build_banner, build_world_map_graphic, build_total_vaccinations_country, build_perc_vaccinated_graphic

app = Dash(__name__)
app.title = 'COVID-19 Vaccine Efficacy Dashboard'
app.config['suppress_callback_exceptions'] = True

df, eff_df, perc_df = init_data()

countries = list(df.Country.unique())
manufacturers = list(df.Vaccine_Manufacturer.unique())
infections = ['Alpha (Infection)','Alpha (Severe)', 'Delta (Infection)', 'Delta (Severe)', 'Omnicron (Infection)', 'Omnicron (Severe)']

banner_title = "COVID 19 Vaccine Efficacy Dashboard"
banner_credits = "DSE I2700 - Lizzette Salmeron, Allen Lau, Analee Graig"

tab1_layout = html.Div(
    children=[
        # world map - Chloropleth
        build_world_map_graphic(manufacturers), 
        # Tree Map - Tree Map (Interactive Static plot)
        html.Div(
            children=[html.Div([
                html.H5(children="Vaccine Maufacturer Tree Map")
            ]),
            dcc.Graph(id='tree-map-graphic', figure=generate_tree_map(df)),
            html.Br()
        ]),
        # Total Vaccinations in Country - Line Plot
        build_total_vaccinations_country(countries),
        # Percentage of People Vaccinated Over Time - Line Plot
        build_perc_vaccinated_graphic(countries)
    ]
)



