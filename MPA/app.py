import dash
import plotly.express as px
import dash_uploader as du
import base64
import datetime
import io
import dash_cytoscape as cyto
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
import networkx as nx
import pandas as pd
import numpy as np
from sympy import Id

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server
app.config.suppress_callback_exceptions = True

du.configure_upload(app, r'E:\tmp\uploads')

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

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
        'data': {'id': str(data['#BioGRID Interaction ID']), 'source': str(source), 'target': str(target)}
    }
    for source, target, data in G.edges.data()
]

elements = nodes + edges


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

# Visualisation pannel


default_stylesheet = [{'selector': 'node',
                       'style': {
                           'background-color': "red"
                       }},
                      {'selector': 'edge',
                       'style': {
                           'line-color': "white",
                       }}
                      ]

mygraph = cyto.Cytoscape(
    id='cytoscape-update-layout',
    elements=elements,
    responsive=True,
    stylesheet=default_stylesheet
)

# Layout selection
controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Select a Layout"),
                dcc.Dropdown(id="layout-drop", options=[{'label': name.upper(), 'value': name}
                                                        for name in ['grid', 'circle', 'cose', 'concentric', 'breadthfirst']],
                             value='circle',
                             clearable=False)
            ]
        ),
        html.Div(
            [
                dbc.Label("Select a metric"),
                dcc.Dropdown(id="metric-drop", options=[{'label': name.upper(), 'value': name} for name in ['clustering coefficient', 'minimum spanning tree', 'betweenness centrality', 'community']],
                             placeholder="Select a metric",
                             clearable=False),
            ]
        ),
        html.Div(
            [
                dbc.Label("Filter nodes by degree"),
                dcc.Slider(min=1, max=10, step=1, value=1, marks={
                    1: {'label': '1', 'style': {'color': '#77b0b1'}},
                    2: {'label': '2'},
                    3: {'label': '3'},
                    4: {'label': '4'},
                    5: {'label': '5'},
                    6: {'label': '6'},
                    7: {'label': '7'},
                    8: {'label': '8'},
                    9: {'label': '9'},
                    10: {'label': '10', 'style': {'color': '#f50'}}
                }, id='filter-node'),
            ]
        ),
    ],
    body=True,
)
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand(
                            "Glioblastoma Gene Interaction Visualization Dashboard", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            )
        ]
    ),
    color="warning",
    dark=True,
)

app.layout = dbc.Container([
    navbar,
    dbc.Row(
        [
            dbc.Col(controls, md=4),
            dbc.Col([mygraph], md=8),
        ],
        align="center",
    ),
    dbc.Row(html.Div(html.P(id="metricOutput"))),
    dbc.Row(html.Div(html.P(id="nodeClick"))),
    dbc.Row(dbc.Col(html.P(id="edgeClick"), width=12)),
    dbc.Row(html.Div(html.P(id="output-data-upload")))],
    # dcc.Store(id="interaction-value")],
    fluid=True)

# fonctions de callback pour le changement dynamique de layout


@app.callback(Output('cytoscape-update-layout', 'layout'),
              [Input('layout-drop', 'value')]
              )
def update_layout(layout):
    return {
        'name': layout,
        'animate': True
    }


def parse_contents(contents, filename):
    print(contents)
    content_type, content_string = contents.split(',').items()

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


@app.callback(Output('button2', 'children'),
              Input('upload-edges', 'contents'),
              Input('upload-edges', 'filename'))
def upload_test(contents, filename):
    if contents is not None:
        print("test")
        children = [
            parse_contents(c, n) for c, n in
            zip(contents, filename)]
        return "essai"


@app.callback([Output('metricOutput', 'children'),
              Output('cytoscape-update-layout', 'stylesheet')],
              Input('metric-drop', 'value'),
              Input('cytoscape-update-layout', 'tapNodeData'))
def update_metric(m, node):
    outTrigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if outTrigger == "metric-drop":
        if m == "clustering coefficient":
            out = dbc.Alert(
                [
                    "The Clustering Coefficient of the initial graph is ",
                    clustering_coefficient(G),
                ],
                color="success",
            )
            return (out, default_stylesheet)

        if m == "betweenness centrality":
            b_central = betweenness_centrality(G)
            min = np.min(list(b_central.values()))
            max = np.max(list(b_central.values()))
            newStyle = []
            for node, b_cent in b_central.items():
                color = (b_cent*230/max, b_cent*20/max, b_cent*28/max)
                newStyle.append({"selector": 'node[id*= "{}"]'.format(node),
                                 "style": {
                                "background-color": "rgb{}".format(color),
                                'z-index': 5000
                                }
                })
            out = dbc.Alert(
                [
                    "Betweenness centralities between {:.3f} (black) and {:.3f} (red) are shown on the graph".format(
                        min, max), 
                ],
                color="success",
            )

            return out, default_stylesheet+newStyle

        if (m == 'minimum spanning tree'):
            edges = minimum_spanning_tree(G)
            edges = np.array(list(edges))[:, :2]
            newStyle = []
            for edge in edges:
                for ed in G.edges.data():
                    check1 = edge[0] == ed[0]
                    check2 = edge[1] == ed[1]
                    check3 = edge[0] == ed[1]
                    check4 = edge[1] == ed[0]
                    if (check1 and check2) or (check3 and check4):
                        newStyle.append({
                            "selector": 'edge[id*= "{}"]'.format(ed[2]['#BioGRID Interaction ID']),
                            "style": {
                                "line-color": "blue",
                                'opacity': 0.9,
                                'z-index': 5000
                            }
                        })
            out = dbc.Alert(
                [
                    "Minimum spanning tree is shown on the graph"
                ],
                color="success",
            )

            return (out, default_stylesheet+newStyle)

        if m == "community":
            list_commu = community(G)
            newStyle = []
            for i, commu in enumerate(list_commu):
                random_color = tuple(np.random.choice(range(255), size=3))
                for node in commu:
                    newStyle.append({"selector": 'node[id*= "{}"]'.format(node),
                                     "style": {
                        "background-color": "rgb{}".format(random_color),
                        'z-index': 5000
                    }
                    })
            out = dbc.Alert(
                [
                    str(len(list_commu)), " communities are present on the initial graph"
                ],
                color="success",
            )
            return (out, default_stylesheet+newStyle)

        return " ", default_stylesheet
    elif outTrigger == "cytoscape-update-layout":
        if node:
            children_style = [{
                'selector': 'edge[source *= "{}"]'.format(node["id"]),
                'style': {
                    'line-color': 'green'
                }
            }]

            return (" ", default_stylesheet + children_style)
        return (" ", default_stylesheet)
    return (" ", default_stylesheet)


@app.callback(Output('nodeClick', 'children'),
              Input('cytoscape-update-layout', 'tapNodeData'))
def displayTapNodeData(data):
    if data:
        out = dbc.Alert(
            [
                "You recently clicked the gene with ID: " +
                str(data["id"]) + " and Degree:" + str(data["size"])
            ],
            color="warning",
        )
        return out


@app.callback(Output('cytoscape-update-layout', 'elements'), Input('filter-node', 'value'))
def filterNode(value):
    if value >= 1:
        test = G.copy()
        node = list(filter(lambda x: test.degree[x] < value, test.nodes))
        test.remove_nodes_from(node)
        nodes = [
            {
                'data': {'id': str(node), 'size': G.degree[node]},
            }
            for node in test
        ]

        edges = [
            {
                'data': {'id': str(data['#BioGRID Interaction ID']), 'source': str(source), 'target': str(target)}
            }
            for source, target, data in test.edges.data()
        ]
    return nodes + edges


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
                tmp = html.Table(
                    [html.Tr([html.Th("Attribute"), html.Th("Informations")])] +
                    [html.Tr([
                        html.Td(
                            i
                        ),
                        html.Td(
                            edge[2][i]
                        )
                    ]) for i in edge[2]]
                )
                return dbc.Table(tmp, bordered=True, hover=True, color="primary",
                                 responsive=True,
                                 striped=True,)
        return html.Table(
            [html.Tr([html.Th("Attribute"), html.Th("Information")])]
        )


if __name__ == '__main__':
    app.run_server(debug=True)
