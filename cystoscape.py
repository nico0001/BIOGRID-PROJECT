import dash
import dash_cytoscape as cyto
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import matplotlib.pyplot as plt

data_chemicals = pd.read_csv('Data\\BIOGRID-PROJECT-glioblastoma_project-CHEMICALS.chemtab.csv', delimiter=";")
data_PTM = pd.read_csv('Data\\BIOGRID-PROJECT-glioblastoma_project-PTM.ptmtab.csv', delimiter=";")
data_genes = pd.read_csv('Data\\BIOGRID-PROJECT-glioblastoma_project-GENES.projectindex.csv', delimiter=";")
data_interactions = pd.read_csv('Data\\BIOGRID-PROJECT-glioblastoma_project-INTERACTIONS.tab3.csv', delimiter=";")

n_sample = 50
G = nx.from_pandas_edgelist(data_interactions[:][:n_sample],'BioGRID ID Interactor A','BioGRID ID Interactor B', edge_attr=True)
pos = nx.drawing.layout.spring_layout(G)
app = dash.Dash(__name__)
# 'Score' : { G.get_edge_data(source, target)["Score"]}
nodes = [
    {
        'data': {'id': str(node), 'label':str(node)},
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
    cyto.Cytoscape(
        id='cytoscape-layout-1',
        elements=elements,
        style={'width': '100%', 'height': '350px'},
        layout={'name': 'circle'},

    )
])

if __name__ == '__main__':
    app.run_server(debug=True)