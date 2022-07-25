import dash_cytoscape as cyto
from dash import Dash,html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
import networkx as nx
import pandas as pd

from app import app

data_chemicals = pd.read_csv(
    'First session\Data\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.csv', delimiter=";")
data_PTM = pd.read_csv(
    'First session\Data\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.csv', delimiter=";")
data_genes = pd.read_csv(
    'E:\EPL_Master\Q1\Data visualization\BIOGRID-PROJECT\First session\Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', delimiter=";")
data_interactions = pd.read_csv(
    'First session\Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv', delimiter=";")

# Graph construction
n_sample = 50
G = nx.from_pandas_edgelist(
    data_interactions[:][:n_sample], 'BioGRID ID Interactor A', 'BioGRID ID Interactor B', edge_attr=True)

# construction de nos nodes et edges pour le dash cytoscape
nodes = [
    {
        'data': {'id': str(node), 'size': G.degree[node]},
    }
    for node in G.nodes
]
edges = [
    {
        'data': {'source': str(source), 'target': str(target)}
    }
    for source, target in G.edges
]
elements = nodes + edges

mytitle = dcc.Markdown(
    id="title", children='# BIOGRID PROJECT-INFORMATION VISUALISATION')

colorPick = html.Div([daq.ColorPicker(id='color-picker',
                                      label='Node color picker',
                                      value=dict(hex='#FEF122'))])

colorPick2 = html.Div([daq.ColorPicker(id='color-picker2',
                                      label='Edge color picker',
                                      value=dict(hex='#FFFFFF'))])

# Visualisation pannel
mygraph = cyto.Cytoscape(
    id='cytoscape-update-layout',
    elements=elements,
    responsive=True,
    stylesheet=[{'selector': 'node',
                 'style': {
                     'background-color': "black"
                 }},
                {'selector': 'edges',
                 'style': {
                     'background-color': "white"
                 }}
                 ]
)

# Layout selection
dropdown = dcc.Dropdown(id="layout-drop", options=[{'label': name.upper(), 'value': name}
                                                   for name in ['grid', 'random', 'circle', 'cose', 'concentric']],
                        value='circle',
                        clearable=False)

layout = dbc.Container([dbc.Row([
    dbc.Col([mytitle], width=10)], justify='center'),
    dbc.Row([
        dbc.Col([dropdown], width=4)], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=8),
        dbc.Col([colorPick], width=2),
        dbc.Col([colorPick2], width=2)
    ], justify='center')], fluid=True)

# fonctions de callback pour le changement dynamique de layout


@app.callback(Output('cytoscape-update-layout', 'layout'),
              [Input('layout-drop', 'value')]
              )
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


@app.callback(Output('cytoscape-update-layout', 'stylesheet'),
              Input('color-picker', 'value'),
              Input('color-picker2', 'value'))
def update_layout(clr,clr2):
    return [{
        'selector': 'node',
        'style': {
            'background-color': clr["hex"]
        }
    }]

