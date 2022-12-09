from dash import dcc 
from dash import html 

from utils.generate_visualizations import generate_tree_map

def build_banner(title, credits):
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5(f"{title}"),
                    html.H6(f"{credits}"),
                ],
            )
        ],
    )

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def build_world_map_graphic(manufacturers):
    '''This function returns an HTML div that includes a drop down menu for vaccine manufacturer and returns a world map that highlights countries where the vaccine was available'''
    return html.Div(
        children=[
            html.Div([
            html.Div([
                html.H5(children='Select manufacturer'),
                html.Label(children="Select Manufacturer"),
                dcc.Dropdown(
                    manufacturers,
                    manufacturers[0],
                    id='manufacturer-select'
                )
            ], style={'width': '48%', 'display': 'inline-block'}),
        ]),
        html.Div([html.H5(children='', id='map-title')]),
        html.Br(),
        dcc.Graph(id='map-graphic'),
        html.Br(),
        html.Hr(),
        ]
    )

def build_total_vaccinations_country(countries):
    '''This function returns an HTML div that includes a drop down menu for country and returns a line plot that depicts the total number of vaccines over times in the select country'''
    return html.Div(children=[
        html.Div(children=[
            html.H5(children="Total Vaccinations in Country"),
            html.Label('Select Country'),
            dcc.Dropdown(
                countries, 
                countries[-2],
                id='countries-select-single'
            )
        ],style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='breakout-line-graph'),
        html.Br()
    ])

def build_perc_vaccinated_graphic(countries):
    '''This function returns an HTML div that includes a multi-selection drop down for countries and returns a line plot that depicts the percentage of people/population vaccinated over time'''
    return html.Div(children=[
            html.Div([
                    html.H5(children='Percentage of people vaccinated over time'),
                    html.Label(children="Select Countries"),
                    dcc.Dropdown(
                        countries, 
                        countries[-5:],
                        multi=True,
                        id='countries-select'
                    )
                ], style={'width': '48%', 'display': 'inline-block'}),
                html.Br(),
                dcc.Graph(id='percent-vaccinated-graph'),
                html.Br()
        ])

