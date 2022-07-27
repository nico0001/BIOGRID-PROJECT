from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import metric, layout

navbar = dbc.NavbarSimple(
    children=[
        dbc.Button(
            "Import genes",
            color="primary",
            id="button",
            className="mb-3",
        ), dbc.Button(
            "Import interactions",
            color="primary",
            id="button2",
            className="mb-3",
        ),
        dbc.NavItem(dbc.NavLink("Metric", href="/apps/metric")),
    ],
    brand="BIOGRID PROJECT-INFORMATION VISUALISATION",
    brand_href="#",
    color="primary",
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content',children='/home')
])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/metric':
        return metric.layout
    elif pathname == '/apps/layout':
        return layout.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
