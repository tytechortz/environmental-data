### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
## Navbar
from navbar import Navbar
df = pd.read_csv('https://raw.githubusercontent.com/jayohelee/dash-tutorial/master/data/population_il_cities.csv')
df.set_index(df.iloc[:,0], drop = True, inplace = True)
df = df.iloc[:,1:]