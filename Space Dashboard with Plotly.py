# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                  dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                ],
                                                value='ALL',
                                                placeholder="Select a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),  
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        # counts = spacex_df['class'].value_counts()
        # Create a pie chart of launch outcomes for the selected site
        # fig = px.pie(
        #     values=counts, 
        #     names=counts.index, 
        #     title=f'Launch Outcomes for {entered_site}')
        fig = px.pie(spacex_df, values='class', names='Launch Site', title='Total Successful Launchs by site')
        # fig = px.pie(spacex_df, values='class', 
        # names='pie chart names', 
        # title='Total successful Launch for all sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        # Count the number of successful and failed launches for the selected site
        counts = filtered_df['class'].value_counts()
        # Create a pie chart of launch outcomes for the selected site
        fig = px.pie(
            values=counts, 
            names=counts.index, 
            title=f'Total successful Launch for site: {entered_site}')
        
        return fig
        # return the outcomes piechart for a selected site


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(site_dropdown, payload_range):
    if site_dropdown == 'ALL':
        # Create a scatter plot for all launch sites
        fig = px.scatter(spacex_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        # Create a scatter plot for a specific launch site
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for Site {site_dropdown}')
    
    # Set the x-axis range based on the selected payload range
    fig.update_layout(xaxis_range=payload_range)

    return fig
# Run the app
if __name__ == '__main__':
    app.run_server()

    
    
    
# 
# 
# Finding Insights Visually
# Now with the dashboard completed, you should be able to use it to analyze SpaceX launch data, and answer the following questions:

# 1. Which site has the largest successful launches?
#     KSC LC-39A
# 2. Which site has the highest launch success rate?
#     CCAFS SLC-40
# 3. Which payload range(s) has the highest launch success rate?
#     3000 kg - 4000 kg
# 4. Which payload range(s) has the lowest launch success rate?
#     6000 kg - 9000 kg
# 5. Which F9 Booster version (v1.0, v1.1, FT, B4, B5, etc.) has the highest launch success rate?
#     FT
# 
