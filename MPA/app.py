import dash
import dash_bootstrap_components as dbc
import plotly.express as px


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
server = app.server
app.config.suppress_callback_exceptions = True
