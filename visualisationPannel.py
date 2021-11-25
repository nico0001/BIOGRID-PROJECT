import dash
import dash_cytoscape as cyto
from dash import html, dcc
from dash.dependencies import Input, Output


def createPanel(elements):
    panel = html.Div(
        className="eight columns",
        children=[
            cyto.Cytoscape(
                id='cytoscape-update-layout',
                layout={'name': 'grid'},
                style={'width': '100%', 'height': '800px'},
                elements=elements,
                responsive=True,
            ),
            html.Div(
                className='twelve columns',
                children=[
                    html.I("Place for the style modification etc"),
                ],
                style={'height': '100px'})],
    )
    return panel
