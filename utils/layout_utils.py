
from dash import dcc, html, Dash, dash_table
import dash_daq as daq

from utils.data_processing import init_data

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
        
    if fig != 'map-graphic':
        div_children.append(generate_section_banner(section_header))

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
            id="control-chart-container",
            className="twelve columns", 
            children = html.Div(
                children = div_children
            )
        )
    )