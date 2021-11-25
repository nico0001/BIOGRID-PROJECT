import dash
from dash import dcc
from dash import html
import dash_cytoscape as cyto
import networkx as nx
import plotly.graph_objs as go
import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import plotly.graph_objs as go
import json
from reader import *

# Initialization of the dash app

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
app.title = "BIOGRID PROJECT"


# division de l'appli en plusieurs div

app.layout = html.Div([
    html.Div([dcc.Upload(html.A('Import File'))],
             className="row",
             ),
             html.Hr(),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="two columns",
                children=[
                    html.I("Select a layout"),
                    dcc.RadioItems(
                        id='radio-update-layout',
                        options=[
                            {'label': name.capitalize(), 'value': name}
                            for name in ['grid', 'random', 'circle', 'cose', 'concentric']
                        ],
                        value='grid'
                    )
                ]
            ),
            html.Div(
                className="eight columns",
                children=[
                    cyto.Cytoscape(
                    id='cytoscape-update-layout',
                    layout={'name': 'grid'},
                    style={'width': '100%', 'height': '1000px'},
                    elements=elements,
                    responsive=True, 
                    style={'height': '800px'}
                ),
                html.Div(
                    className='twelve columns',
                    children=[
                        html.I("Place for the style modification etc"),
                    ],
                    style={'height': '100px'})],
            ),
            html.Div(
                className="two columns",
                children=[
                    html.Div(
                        className='twelve columns',
                        children=[
                            html.I("Network metric"),
                            html.Pre(id='hover-data')
                        ],
                        style={'height': '400px'}),
                ]
            )
        ]
    )
])


def display_selected_data(selectedData):
    num_of_nodes = len(selectedData['points'])
    text = [html.P('Num of nodes selected: '+str(num_of_nodes))]
    for x in selectedData['points']:
        material = int(x['text'].split('<br>')[0][10:])
        text.append(html.P(str(material)))
    return text


if __name__ == '__main__':
    app.run_server(debug=True)
