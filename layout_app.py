import dash
import dash_bootstrap_components as dbc
from assets.styling import *
from dash import dcc, html, Dash

from dash.dependencies import Input, Output
from utils.layout_utils import build_tabs, build_banner, build_tab_1, build_quick_stats_panel, build_top_panel, build_graph_panel, build_world_map_graphic, build_top_panel_tab1
from tab_layout import tab1_layout
from utils.generate_visualizations import plot_world_map, line_area_breakout_graph, generate_percent_vaccinated_graph, generate_tree_map
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
    ],
)
# Tab Callback functions 

@app.callback(
    Output('map-graphic', 'figure'),
    # Output('map-title', 'children'),
    Input('manufacturer-select', 'value')
)
def update_world_map(manufacturer):
    '''This callback function produces the world map that depicts where vaccine manufacturers were distributed globally/geographically'''
    fig = plot_world_map(manufacturer, df)
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')
    # title = f"{manufacturer} Vaccine - Global Distribution"
    return fig #, title

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

#Layout Callback functions

# @app.callback(Output('app-content', 'children'),
#               [Input('app-tabs', 'value')])
# def render_content(tab):
#     if tab == 'tab1':       
#         return tab1_layout
#     elif tab == 'tab2':
#         pass

@app.callback(
    [Output("app-content", "children")], #Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")]
    # [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        # return build_tab_1(df)
        return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[
                        # build_top_panel(),
                        build_top_panel_tab1(),
                        build_graph_panel(generate_tree_map(df), title='Vaccine Manufacturer Tree Map')
                    ],
                ),
            ],
        ),
    )
    
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[
                        build_top_panel(), 
                        build_graph_panel(graph=generate_tree_map(df), title='Vaccine Manufacturer Tree Map')
                    ],
                ),
            ],
        ),
    )

if __name__ == '__main__':
    app.run_server(debug=True)
