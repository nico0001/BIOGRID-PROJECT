from dash import html, dcc
from dash.dependencies import Input, Output


rightBar = html.Div(
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
)
