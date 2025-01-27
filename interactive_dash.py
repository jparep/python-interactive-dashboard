from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
from dash_bootstrap_components import Table
from dash_bootstrap_templates import ThemeSwitchAIO
import pandas as pd
import numpy as np

# Example datasets (replace these with real train and test datasets)
train_df = pd.DataFrame({
    'Age': np.random.randint(1, 80, 500),
    'Fare': np.random.randint(5, 100, 500),
    'Survived': np.random.choice([0, 1], 500)
})
test_df = pd.DataFrame({
    'Age': np.random.randint(1, 80, 200),
    'Fare': np.random.randint(5, 100, 200),
    'Survived': np.random.choice([0, 1], 200)
})

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, dbc.themes.FLATLY])

# App Layout
app.layout = dbc.Container(
    [
        # Theme Switcher
        ThemeSwitchAIO(aio_id="theme", themes=[dbc.themes.CYBORG, dbc.themes.FLATLY]),
        
        # Dashboard Header
        dbc.Row(
            dbc.Col(html.H1("Titanic Interactive Dashboard", className="text-center text-light mb-4")),
        ),
        
        # Dropdown Row for Dataset and Chart Type
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id='dataset-dropdown',
                        options=[
                            {'label': 'Train Dataset', 'value': 'train'},
                            {'label': 'Test Dataset', 'value': 'test'}
                        ],
                        value='train',
                        placeholder="Select Dataset",
                        clearable=False,
                        className="mb-3"
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='chart-type-dropdown',
                        options=[
                            {'label': 'Histogram', 'value': 'histogram'},
                            {'label': 'Box Plot', 'value': 'box'},
                            {'label': 'Scatter Plot', 'value': 'scatter'}
                        ],
                        value='histogram',
                        placeholder="Select Chart Type",
                        clearable=False,
                        className="mb-3"
                    ),
                    width=6
                ),
            ]
        ),
        
        # Row for Filters
        dbc.Row(
            [
                dbc.Col(
                    dcc.RangeSlider(
                        id='age-slider',
                        min=0,
                        max=80,
                        step=5,
                        value=[10, 60],
                        marks={i: f"{i}" for i in range(0, 81, 10)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    width=12,
                )
            ],
            className="mb-4"
        ),
        
        # Row for Graphs
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='age-chart'), width=6),
                dbc.Col(dcc.Graph(id='fare-chart'), width=6),
            ]
        ),
        
        # Row for Key Metrics
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            html.H4("Key Metrics", className="card-title"),
                            html.P(id="metrics", className="card-text"),
                        ],
                        body=True,
                        color="info",
                        inverse=True,
                    ),
                    width=12,
                )
            ]
        ),
    ],
    fluid=True
)

# Callbacks

@app.callback(
    Output('age-chart', 'figure'),
    Output('fare-chart', 'figure'),
    [
        Input('dataset-dropdown', 'value'),
        Input('chart-type-dropdown', 'value'),
        Input('age-slider', 'value'),
        ThemeSwitchAIO.ids.switch("theme")  # Dynamic theming
    ]
)
def update_charts(selected_dataset, chart_type, age_range, theme):
    # Select dataset
    data = train_df if selected_dataset == 'train' else test_df
    filtered_data = data[(data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1])]
    
    # Chart generators
    chart_types = {
        'histogram': lambda col: px.histogram(filtered_data, x=col, nbins=20, color='Survived'),
        'box': lambda col: px.box(filtered_data, y=col, color='Survived'),
        'scatter': lambda _: px.scatter(filtered_data, x='Age', y='Fare', color='Survived')
    }

    # Generate charts
    age_fig = chart_types[chart_type]('Age')
    fare_fig = chart_types[chart_type]('Fare') if chart_type != 'scatter' else chart_types[chart_type](None)
    
    # Apply theming
    for fig in [age_fig, fare_fig]:
        fig.update_layout(template='plotly_dark' if theme == dbc.themes.CYBORG else 'plotly_white')
    
    return age_fig, fare_fig

@app.callback(
    Output('metrics', 'children'),
    [
        Input('dataset-dropdown', 'value'),
        Input('age-slider', 'value')
    ]
)
def update_metrics(selected_dataset, age_range):
    # Select dataset
    data = train_df if selected_dataset == 'train' else test_df
    filtered_data = data[(data['Age'] >= age_range[0]) & (data['Age'] <= age_range[1])]

    # Compute metrics
    total_passengers = len(filtered_data)
    avg_age = round(filtered_data['Age'].mean(), 2) if total_passengers > 0 else 0
    avg_fare = round(filtered_data['Fare'].mean(), 2) if total_passengers > 0 else 0
    survival_rate = round(filtered_data['Survived'].mean() * 100, 2) if total_passengers > 0 else 0

    return f"Total Passengers: {total_passengers}, Avg Age: {avg_age}, Avg Fare: {avg_fare}, Survival Rate: {survival_rate}%"

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
