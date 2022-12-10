
import os
import pathlib
import pandas as pd

from dash import dcc, html, Dash
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from utils.data_processing import get_manufacturer_country
from utils.build_components import build_world_map_graphic
from utils.generate_visualizations import generate_tree_map
from utils.data_processing import init_data

df, eff_df, perc_df = init_data()
manufacturers = list(df.Vaccine_Manufacturer.unique())


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
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="github"),
                        href="https://github.com/lizzjs/C19VaccineEfficacy-Dash",
                    )
                ],
            ),
        ],
        # className="p-3 rounded-3",
        # style={'background-image':'url("/assets/covid-banner.jpeg")', 'background-repeat':'no-repeat'} 
        style={'background-image':'url("/assets/Covid-19-Banner.png")', 'background-repeat':'no-repeat'} 
    )
        

def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="TAB 1",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Breakthrough Case Study for (Country)",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def build_tab_1(df): # NEED TO FIX THIS 
    manufacturer = list(df['Vaccine_Manufacturer'].unique())
    country = list(df['Country'].unique())
    
    return [
        # Manually select metrics
        html.Div(
            id="set-specs-intro-container",
            children=html.P(
                "Select manufacturer to view geographic availability"
            ),
        ),
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="manufacturer-select-menu",
                    children=[
                        html.Label(id="manufacturer-select-title", children="Select Manufacturer"),
                        html.Br(),
                        dcc.Dropdown(
                            id="manufacturer-select-dropdown",
                            options=manufacturer,
                            # value=manufacturer[1],
                        ),
                    ],
                ),
                html.Div(
                    id="country-select-menu",
                    # className='five columns',
                    children=[
                        html.Label(id="country-select-title", children="Select Country"),
                        html.Br(),
                        dcc.Dropdown(
                            id="country-select-dropdown",
                            options=country,
                            # value=country[1]
                        ),
                    ],
                ),
                html.Div(
                    id="value-setter-menu",
                    # className='six columns',
                    children=[
                        html.Div(id="value-setter-panel"),
                        html.Br(),
                        html.Div(
                            id="button-div",
                            children=[
                                # html.Button(
                                #     "Update", 
                                #     # id="value-setter-set-btn",
                                #     id=""
                                # ),
                                html.Button(
                                    "Recenter Map",
                                    # id="recenter-map-btn",
                                    id="",
                                    n_clicks=0,
                                ),
                            ],
                        ),
                        html.Div(
                            # id="value-setter-view-output", className="output-datatable",
                            id="graphs-container",
                            children=[
                                dcc.Graph(
                                    id="vaccination-avail-map",
                                    # figure=plot_world_map("Novamax", df)
                                )
                            ]
                        ),
                    ],
                ),
            ],
        ),
    ]

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Total # Of Vaccinations"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value="1704",
                        color="#9575cd",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
            html.Div(
                id="card-2",
                children=[
                    html.P("# of Countries"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value="43",
                        color="#e8bcf0",
                        backgroundColor="#1e2130",
                        size=50,
                    ),
                ],
            ),
        ],
    )

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def build_top_panel():
    return html.Div(
        id="top-section-container",
        # id="control-chart-container",
        # className="twelve columns",
        # className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    # generate_section_banner("Process Control Metrics Summary"),
                    html.Div(
                        id="metric-div",
                        children=[
                            # generate_metric_list_header(), # Dont need this
                            html.Div(
                                id="metric-rows",
                                children=[
                                    build_world_map_graphic(manufacturers),
                                    # generate_metric_row_helper(stopped_interval, 1),   #Replace this with a graph
                                    # generate_metric_row_helper(stopped_interval, 2),
                                    # generate_metric_row_helper(stopped_interval, 3),
                                    # generate_metric_row_helper(stopped_interval, 4),
                                    # generate_metric_row_helper(stopped_interval, 5),
                                    # generate_metric_row_helper(stopped_interval, 6),
                                    # generate_metric_row_helper(stopped_interval, 7),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # # Piechart                                                           #Maybe remove this 
            # html.Div(
            #     id="ooc-piechart-outer",
            #     className="four columns",
            #     children=[
            #         generate_section_banner("% OOC per Parameter"),
            #         # generate_piechart(), #
            #     ],
            # ),
        ],
    )

def build_top_panel_tab1():
     return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("testing"),
            html.Div([
                html.Label(children="Select Manufacturer"),
                dcc.Dropdown(
                    manufacturers,
                    manufacturers[0],
                    id='manufacturer-select'
                )
                ], #style={'width': '48%', 'display': 'inline-block'}
            ),
        # html.Div([html.H5(children='', id='map-title')]),
        html.Br(),
        dcc.Graph(id='map-graphic'),
        # html.Br(),
        # html.Hr(),
        ]
    )

def build_graph_panel(graph, title): # Can use this over and over for any graphs 
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner(title),
            dcc.Graph(
                id="control-chart-live",
                figure=graph,
            ),
        ],
    )
