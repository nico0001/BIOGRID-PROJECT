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


# App Layouts definition (pensez à faire des fonctions pour chacunes de nos layouts?)


# Relation interface/action

# @app.callback(
#     dash.dependencies.Output('my-graph', 'figure'),
#     [dash.dependencies.Input('my-range-slider', 'value'), dash.dependencies.Input('input1', 'value')])
# def update_output(value, input1):
#     YEAR = value
#     ACCOUNT = input1
#     return network_graph(value, input1)


# @app.callback(
#     dash.dependencies.Output('hover-data', 'children'),
#     [dash.dependencies.Input('my-graph', 'hoverData')])
# def display_hover_data(hoverData):
#     return json.dumps(hoverData, indent=2)


# @app.callback(
#     dash.dependencies.Output('click-data', 'children'),
#     [dash.dependencies.Input('my-graph', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)


# Creating network and trying to visualize it

G = nx.from_pandas_edgelist(
    data_interactions[:][:50], 'Entrez Gene Interactor A', 'Entrez Gene Interactor B')

# for key, node in data_genes.iterrows():
#      G.add_node(node[1])

pos = nx.layout.spiral_layout(G)
nx.set_node_attributes(G, pos, name="pos")
# Create Edges
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])


# creating the nodes

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line=dict(width=2)))
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])


# add color to node points
for node, adjacencies in enumerate(G.adjacency()):
    node_trace['marker']['color'] += tuple([len(adjacencies[1])])
    node_info = 'Name: ' + \
        str(adjacencies[0]) + '<br># of connections: '+str(len(adjacencies[1]))
    node_trace['text'] += tuple([node_info])


# Displaying to dash

fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                title='<br>BIOGRID PROJECT',
                titlefont=dict(size=16),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002)],
                xaxis=dict(showgrid=False, zeroline=False,
                           showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))


# creating the layout
elt = edge_trace
app.layout = html.Div([
    html.Div(dcc.Graph(id='Graph', figure=fig)),
    html.Div(className='row', children=[
        html.Div([html.H2('Overall Data'),
                  html.P('Num of nodes: ' + str(len(G.nodes))),
                  html.P('Num of edges: ' + str(len(G.edges)))],
                 className='three columns'),
        html.Div([
            html.H2('Selected Data'),
            html.Div(id='selected-data'),
        ], className='six columns')
    ]), html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-2',
            style={'width': '100%', 'height': '350px'},
            layout={
                'name': 'grid'
            }
        )
    ])

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
