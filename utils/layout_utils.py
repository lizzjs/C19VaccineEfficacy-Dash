
import os
import pathlib
import pandas as pd

from dash import dcc, html, Dash, dash_table
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

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Total Vaccinations in Billions"),
                    daq.LEDDisplay(
                        id="operator-led",
                        value="2.482", #2482427113 
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
        children=[
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    html.Div(
                        id="metric-div",
                        children=[
                            html.Div(
                                id="metric-rows",
                                children=[
                                    build_world_map_graphic(manufacturers),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

def build_graph_div(fig, section_header, dropdown_options=[], dropdown_id='', dropdown_label='', multi_dropdown=False):
    '''
    params:
        - figure: plotly.figure object or a dcc.Graph id (str)
        - section_header (str): Title for the graph div section
        - dropdown_options (list):  List of options for dropdown menu 
        - dropdown_id (str): Callback Input of the dropdown object, this dropdown_id is what changes the plots
        - multi_dropdown (bool): True if multiple dropdown menu options are accepted 
    return: 
        - returns an dash.html.Div that renders the section header, dropdown menu (if available), and graph
    '''
    if isinstance(fig, str):
        graph_object = dcc.Graph(id=f"{fig}")
    else: 
        graph_object = dcc.Graph(figure=fig)
    
    # check for drop down 
    if len(dropdown_options):
        # this means it is NOT empty, we have a drop down 
        if multi_dropdown: 
            # this means it IS a multi-selection dropdown menu 
            dropdown_object = dcc.Dropdown(
                options=dropdown_options, 
                value=dropdown_options[-2:],
                multi=True,
                id=dropdown_id

            )
        else: 
            dropdown_object = dcc.Dropdown(
                options=dropdown_options, 
                value=dropdown_options[0],
                id=dropdown_id
            )
        
        return html.Div(
            id="control-chart-container",
            className="twelve columns",
            children=[
                generate_section_banner(section_header),
                html.Div([
                        html.Label(children=str(dropdown_label)),
                        dropdown_object,
                    ]
                ),
                graph_object
            ]
        )
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner(section_header),
            graph_object
        ]
    )
            

    
    # div_children.append(graph_object)
    # print(div_children)
    # return html.Div(
    #     id='control-chart-container',
    #     className="twelve columns", 
    #     children=div_children
    # )

# how to use this function
# build_graph_div (line_graph, "")

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

def build_eff_table_div(df, max_rows=10):
    return( 
        dash_table.DataTable(
            data=df.head(max_rows).to_dict('records'), 
            columns=[{'id': c, 'name': c} for c in df.columns],
            style_table={'overflowX': 'scroll'},
            style_header={
                'backgroundColor': '#1e2130',
                'color': 'white'
            },
            style_data={
                'backgroundColor': '#34394f',
                'color': 'white'
            },
            style_cell_conditional=[  # align text columns to left. By default they are aligned to right
                {"if": {"column_id": c}, "textAlign": "center"} for c in df.columns
            ]
        )
    )
