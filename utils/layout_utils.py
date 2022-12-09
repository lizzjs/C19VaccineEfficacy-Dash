
import os
import pathlib
import pandas as pd

from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

from utils.data_processing import get_manufacturer_country


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
                        href="https://www.github.com",
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
                        label="TAB 2",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

def build_tab_1(path, params):
    df = get_manufacturer_country(path)
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
