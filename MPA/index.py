from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from apps import metric, layout

navbar = dbc.NavbarSimple(
    children=[
        dcc.Upload(id="upload-node",
            children=dbc.Button(
            "Import genes",
            color="danger",
            id="button",
            className="me-1",
        ),accept="CSV"), dcc.Upload(id="upload-edge",
            children=dbc.Button(
            "Import interactions",
            color="danger",
            id="button2",
            className="me-1",
        ), accept="CSV")
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
    return layout.layout

if __name__ == '__main__':
    app.run_server(debug=True)
