import dash
import dash_cytoscape as cyto
from dash import html,dcc
from dash.dependencies import Input, Output
import json
import networkx as nx
import pandas as pd
from rightSide import *
from leftSide import *
from visualisationPannel import *

data_chemicals = pd.read_csv(
    'Data\\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.csv', delimiter=";")
data_PTM = pd.read_csv(
    'Data\\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.csv', delimiter=";")
data_genes = pd.read_csv(
    'Data\\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', delimiter=";")
data_interactions = pd.read_csv(
    'Data\\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv', delimiter=";")
# Graph construction

n_sample = 50
G = nx.from_pandas_edgelist(
    data_interactions[:][:n_sample], 'BioGRID ID Interactor A', 'BioGRID ID Interactor B', edge_attr=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "BIOGRID PROJECT"

# construction de nos nodes et edges pour le dash cytoscape

nodes = [
    {
        'data': {'id': str(node), 'label': str(node)},
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


app.layout = html.Div([
    html.Div([dcc.Upload(html.A('Import File'),accept='csv')],
             className="row",
             ),
    html.Hr(),
    html.Div(
        className="row",
        children=[
            rightBar,
            createPanel(elements),
            leftSide
        ]
    )
])

# fonctions de callback pour le changement dynamique de layout


@app.callback(Output('cytoscape-update-layout', 'layout'),
              Input('radio-update-layout', 'value'))
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


# @app.callback(Input('cytoscape-update-layout','element'),
#             Output('hover-data','children'))

# def display_gene_infos():
#     return json.dumps(hoverData,indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)
