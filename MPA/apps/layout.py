import dash_cytoscape as cyto
from dash import Dash,html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
import networkx as nx
import pandas as pd

from app import app

data_chemicals = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.csv', delimiter=";")
data_PTM = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.csv', delimiter=";")
data_genes = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', delimiter=";")
data_interactions = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv', delimiter=";")

# Graph construction
n_sample = 500
G = nx.from_pandas_edgelist(data_interactions[:][:n_sample], 'BioGRID ID Interactor A', 'BioGRID ID Interactor B', edge_attr=True)

# construction de nos nodes et edges pour le dash cytoscape
nodes = [
    {
        'data': {'id': str(node), 'size': G.degree[node]},
    }
    for node in G.nodes
]
edges = [
    {
        'data': {'id': str(data['#BioGRID Interaction ID']), 'source': str(source), 'target': str(target)}
    }
    for source, target, data in G.edges.data()
]
elements = nodes + edges


colorPick = html.Div([daq.ColorPicker(id='color-picker',
                                      label='Node color picker',
                                      value=dict(hex='#FEF122'))])

colorPick2 = html.Div([daq.ColorPicker(id='edgeColor',
                                      label='Edge color picker',
                                      value=dict(hex='#Fc2ed2'))])

# Visualisation pannel

default_stylesheet = [{'selector': 'node',
                       'style': {
                           'background-color': "black"
                       }},
                      {'selector': 'edge',
                       'style': {
                           'line-color': "blue",
                       }}
                      ]

mygraph = cyto.Cytoscape(
    id='cytoscape-update-layout',
    elements=elements,
    responsive=True,
    stylesheet=default_stylesheet
)

# Layout selection
dropdown = dcc.Dropdown(id="layout-drop", options=[{'label': name.upper(), 'value': name}
                                                   for name in ['grid', 'random', 'circle', 'cose', 'concentric']],
                        value='circle',
                        clearable=False)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([dropdown], width=4)], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=8),
        dbc.Col([colorPick], width=2),
        dbc.Col([colorPick2], width=2)
    ], justify='center'),
    dbc.Row(html.Div(html.P(id="nodeClick"))),
    dbc.Row(html.Div(html.P(id="edgeClick")))], fluid=True)

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
              Input('edgeColor', 'value'))
def update_layout(clr,clr2):

    new_styles = [{
        'selector': 'node',
        'style': {
            'background-color': clr["hex"]
        }
    },
        {
        'selector': 'edge',
        'style': {
            'line-color': clr2["hex"]
        }
    }]

    return default_stylesheet + new_styles


@app.callback(Output('nodeClick', 'children'),
              Input('cytoscape-update-layout', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        return "You recently clicked the gene with ID: " + str(data["id"]) + " and Degree:" + str(data["size"])


@app.callback(Output('edgeClick', 'children'),
              Input('cytoscape-update-layout', 'tapEdgeData'))
def displayTapEdgeData(data):
    if data:
        for edge in G.edges.data():
            check1 = (int(edge[0]) == int(
                data['source']))
            check2 = (int(edge[1]) == int(
                data['target']))
            check3 = (int(edge[0]) == int(
                data['target']))
            check4 = (int(edge[1]) == int(
                data['source']))
            if (check1 and check2) or (check3 and check4):
                return html.Table(
                            [html.Tr([html.Th("Attribute"), html.Th("Gene data")])] +
                            [html.Tr([
                                html.Td(
                                    i
                                ),
                                html.Td(
                                    edge[2][i]
                                )
                            ]) for i in edge[2]]
                        )
        return html.Table(
                [html.Tr([html.Th("Attribute"), html.Th("Information")])]
            )
