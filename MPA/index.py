from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from app import app
from apps import metric, layout


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Navigate to Layout', href='/apps/layout'),
    html.Br(),
    dcc.Link('Navigate to Metric', href='/apps/metric'),
    html.Div(id='page-content',children='/home')
])
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/metric':
        return metric.layout
    elif pathname == '/apps/layout':
        return layout.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
