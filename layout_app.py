import dash
import dash_bootstrap_components as dbc
from assets.styling import *
from dash import dcc, html, Dash

from dash.dependencies import Input, Output
from utils.layout_utils import build_tabs, build_banner, build_quick_stats_panel, build_graph_div, build_eff_table_div
from tab_layout import tab1_layout
from utils.build_components import generate_section_banner
from utils.generate_visualizations import plot_world_map, line_area_breakout_graph, generate_percent_vaccinated_graph, generate_tree_map, protected_over_time_agg
from utils.data_processing import init_data


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
app.title = "Covid-19 Vaccine Efficacy Dashboard"
server = app.server
banner_title = "COVID 19 Vaccine Efficacy Dashboard"
banner_credits = "DSE I2700 - Lizzette Salmeron, Allen Lau, Analee Graig"

df, eff_df, perc_df = init_data()

countries = list(df.Country.unique())
manufacturers = list(df.Vaccine_Manufacturer.unique())
infections = ['Alpha (Infection)','Alpha (Severe)', 'Delta (Infection)', 'Delta (Severe)', 'Omnicron (Infection)', 'Omnicron (Severe)']

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(banner_title, banner_credits),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        html.Br(),
        html.Hr()
    ],
)
# Tab Callback functions 

@app.callback(
    Output('map-graphic', 'figure'),
    Input('manufacturer-select', 'value')
)
def update_world_map(manufacturer):
    '''This callback function produces the world map that depicts where vaccine manufacturers were distributed globally/geographically'''
    fig = plot_world_map(manufacturer, df)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    return fig 

@app.callback(
    Output('breakout-line-graph', 'figure'),
    Input('countries-select-single', 'value')
)
def update_breakout_graph(country):
    '''This callback function prodices the Total Vaccines in Country graph'''
    return line_area_breakout_graph(eff_df, country)

@app.callback(
    Output('percent-vaccinated-graph', 'figure'),
    Input('countries-select', 'value')
)
def update_percent_vaccinated_graph(countries):
    '''This callback function produces the Percentage of people vaccinated over time line graph'''
    return generate_percent_vaccinated_graph(perc_df, countries)

#Allen Code 
@app.callback(
    Output('protected_over_time_agg','figure'),
    Input('countries-select-single','value')
)
def update_protected_over_time_agg(country):
    return protected_over_time_agg(eff_df,country)


#Layout Callback functions

@app.callback(
    [Output("app-content", "children")],
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return (
            html.Div(
                id="status-container",
                children=[
                    build_quick_stats_panel(),
                    html.Div(
                        id="graphs-container",
                        children=[
                                build_graph_div(fig='map-graphic', 
                                    section_header="World Map Graphic",
                                    dropdown_id='manufacturer-select', 
                                    dropdown_options=manufacturers, 
                                    dropdown_label='select manufacturer'),
                                build_graph_div(fig=generate_tree_map(df),section_header="Tree Map Test"),
                                build_graph_div(fig='protected_over_time_agg',
                                    section_header='Percentage of Total Doses not Protecting Against Infection',
                                    dropdown_id='countries-select-single',
                                    dropdown_options=countries,
                                    dropdown_label='select country'),
                                html.Div(children=[
                                    generate_section_banner(title="Table"),
                                    build_eff_table_div(eff_df, max_rows=10)          
                                ]),       
                            ],
                    ),
                ],
            ),
            # generate_section_banner("Efficacy Table"),
            # build_eff_table_div(eff_df)
        )
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                build_graph_div(fig=generate_tree_map(df),section_header="THIS IS A PLACEHOLDER"), 
            ],
        ),
    )

if __name__ == '__main__':
    app.run_server(debug=True)
