from dash import html, dcc
from dash.dependencies import Input, Output

leftSide = html.Div(
    className="two columns",
    children=[
        html.Div(
            className='twelve columns',
            children=[
                html.I("Network metric and filters"),
                html.Pre(id='hover-data')
            ],
            style={'height': '400px'}),
    ]
)
