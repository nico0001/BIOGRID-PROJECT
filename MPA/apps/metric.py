import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from app import app
import dash_bootstrap_components as dbc
import dash_daq as daq
import networkx as nx
import pandas as pd

data_chemicals = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.csv', delimiter=";")
data_PTM = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.csv', delimiter=";")
data_genes = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', delimiter=";")
data_interactions = pd.read_csv(
    'Data\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv', delimiter=";")

# metric algo definitions


def betweenness_centrality(G):
    return nx.betweenness_centrality(G)


def clustering_coefficient(G):
    return nx.average_clustering(G)


def minimum_spanning_tree(G):
    return nx.algorithms.minimum_spanning_edges(G)


def has_path(G, source, target):
    return nx.algorithms.has_path(G, source, target)


def shortest_path(G, source, target):
    return nx.algorithms.shortest_path(G, source, target)


def community(G):
    return nx.algorithms.community.greedy_modularity_communities(G)



# Graph construction
n_sample = 50
G = nx.from_pandas_edgelist(
    data_interactions[:][:n_sample], 'BioGRID ID Interactor A', 'BioGRID ID Interactor B', edge_attr=True)

app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = "BIOGRID PROJECT"


# construction de nos nodes et edges pour le dash cytoscape
nodes = [
    {
        'data': {'id': str(node), 'size': G.degree[node]},
    }
    for node in G.nodes
]
edges = [
    {
        'data': {'id':str(data['#BioGRID Interaction ID']),'source': str(source), 'target': str(target)}
    }
    for source, target,data in G.edges.data()
]
elements = nodes + edges

# Visualisation pannel
mygraph = cyto.Cytoscape(
    id='cytoscape-update-layout',
    elements=elements,
    responsive=True,
    stylesheet=[{'selector': 'node',
                 'style': {
                     'background-color': "black"
                 }}]
)


metricLayout = cyto.Cytoscape(
    id='metric-layout',
    responsive=True,
)


# Metric selection
metric = dcc.Dropdown(id="metric-drop", options=[{'label': name.upper(), 'value': name} for name in ['betweenness centrality', 'clustering coefficient', 'minimum spanning tree', 'shortest path', 'community']],
                      placeholder="Select a metric",
                      clearable=False)

layout = dbc.Container([
    dbc.Row([
        dbc.Col([metric], width=4)], justify='center'),
    dbc.Row([
        dbc.Col([mygraph], width=8)
    ], justify='center')], fluid=True)

# fonctions de callback pour le changement dynamique de layout
