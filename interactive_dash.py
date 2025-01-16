from dash import Dash, dcc, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np

# Load data
train_df = pd.read_csv('/data/train.csv')
test_df  = pd.read_csv('/data/test.csv')

# Initalize Dash app with a modern Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
