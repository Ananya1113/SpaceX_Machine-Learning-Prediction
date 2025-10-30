# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# ----------------------------------------------------
# TASK 1: Add a Launch Site Drop-down Input Component
# ----------------------------------------------------
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),

    # ----------------------------------------------------
    # TASK 2: Add a Pie Chart for success count
    # ----------------------------------------------------
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    # ----------------------------------------------------
    # TASK 3: Add a Payload Range Slider
    # ----------------------------------------------------
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000',
               7500: '7500', 10000: '10000'},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # ----------------------------------------------------
    # TASK 4: Add a Scatter Chart for Payload vs Success
    # ----------------------------------------------------
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# ----------------------------------------------------
# TASK 2: Callback for success pie chart
# ----------------------------------------------------
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # Use all data to show total successful launches by site
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site',
                     title='Total Successful Launches by Site')
        return fig
    else:
        # Filter dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count success (class=1) and failure (class=0)
        fig = px.pie(filtered_df, names='class',
                     title=f'Success vs Failure for site {entered_site}')
        return fig

# ----------------------------------------------------
# TASK 4: Callback for scatter plot
# ----------------------------------------------------
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    # Filter by payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                            (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Payload vs. Launch Outcome for All Sites')
        return fig
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(site_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Payload vs. Launch Outcome for {entered_site}')
        return fig

# ----------------------------------------------------
# Run the app
# ----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8051)



