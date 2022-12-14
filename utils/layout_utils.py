
from dash import dcc, html, Dash, dash_table
import dash_daq as daq
import dash_bootstrap_components as dbc

from utils.data_processing import init_data
from assets.tab1_markdown import dashboard_desc_md, section_1_md, section_2_md, perc_total_doses_by_manufacturer_md, protected_over_time_agg_md, breakthrough_over_time_md, section_3_md, efficacy_md


df, eff_df, perc_df, vac_eff_df = init_data()
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
                        label="",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    # dcc.Tab(
                    #     id="Control-chart-tab",
                    #     label="Breakthrough Case Study for (Country)",
                    #     value="tab2",
                    #     className="custom-tab",
                    #     selected_className="custom-tab--selected",
                    # ),
                ],
            )
        ],
    )

def build_quick_stats_LED(label, value):
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P(label),
                    daq.LEDDisplay(
                        id="operator-led",
                        value=value, 
                        color="#9575cd",
                        backgroundColor="#1d202d",
                        size=50,
                    ),
                ],
            ),
        ],
    )

def build_markdown_container():
    return html.Div(
        children=[
            build_markdown_section(markdown_text=dashboard_desc_md, section_header='Dashboard Description'),
            build_markdown_section(markdown_text=section_1_md),
            build_markdown_section(markdown_text=section_2_md),
            build_markdown_section(markdown_text=efficacy_md),
            build_markdown_section(markdown_text=section_3_md),
            build_markdown_section(markdown_text=perc_total_doses_by_manufacturer_md), 
            build_markdown_section(markdown_text=protected_over_time_agg_md),
            build_markdown_section(markdown_text=breakthrough_over_time_md),
            html.Br()
        ]
    ) 

def build_quick_stats_container():
    return dbc.Row([
                build_quick_stats_LED(label="Vaccine Manufacturers", value="13"),
                build_quick_stats_LED(label="Covid Variants Considered", value="3"),
                build_quick_stats_LED(label="Total Doses Given (Billions)", value="2.482"),
                build_quick_stats_LED(label="Total Number of Countries", value="43"),
            ])

def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            build_markdown_container()
        ],
    )

def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)

def build_graph_div(fig, section_header, **kwargs):
    '''
    docs.md
    '''
    div_children = []
    if fig == 'map-graphic':
        div_children.append(generate_section_banner(section_header))

    if isinstance(fig, str):
        graph_object = dcc.Graph(id=f"{fig}")
    else: 
        graph_object = dcc.Graph(figure=fig)
    
    enable_dropdown = kwargs.pop('enable_dropdown', False)
    enable_radio = kwargs.pop('enable_radio', False)

    if enable_dropdown:
        dropdown_id = kwargs.pop('dropdown_id', '')
        dropdown_options = kwargs.pop('dropdown_options', [])
        multi_dropdown = kwargs.pop('multi_dropdown', False)
        dropdown_label = kwargs.pop('dropdown_label', '')
    if enable_radio:
        radio_id = kwargs.pop('radio_id', '')
        radio_options = kwargs.pop('radio_options', [])
        multi_radio = kwargs.pop('multi_radio', False)
        radio_label = kwargs.pop('radio_label', '')
    pass 

    if enable_dropdown:
        if multi_dropdown:
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
        dropdown_div = html.Div([
                        html.Label(children=str(dropdown_label)),
                        dropdown_object
                    ])
        
        div_children.append(dropdown_div)
    
    if enable_radio:
        if multi_radio:
            radio_object = dcc.Checklist(
                options = radio_options,
                value = radio_options[0],
                id = radio_id
            )
        else:
            radio_object = dcc.RadioItems(
                options = radio_options,
                value = radio_options[0],
                id = radio_id
            )
        radio_div = html.Div([
                        html.Label(children=str(radio_label)),
                        radio_object,
                    ]
                )
        div_children.append(radio_div)
        
    # if fig != 'map-graphic':
    # div_children.append(generate_section_banner(section_header))
    div_children.append(graph_object)
    
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=div_children
    )

def build_eff_table_div(df, max_rows=10):
    df = df[["Vaccine_Manufacturer", "Eff Severe Disease Alpha", "Eff Infection Alpha", 
    "Eff Severe Disease delta", "Eff Infection Delta", "Eff Severe Disease Omicron", "Eff Infection Omicron"]]
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

def build_markdown_section(markdown_text, section_header=None):
    div_children = []
    if section_header:
        div_children.append(generate_section_banner(section_header))
    div_children.append(dcc.Markdown(markdown_text, dedent=False))
    return (
        html.Div(
            id="markdown-container",
            # className="twelve columns", 
            children = html.Div(
                children = div_children
            )
        )
    )