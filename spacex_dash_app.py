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
								sites = spacex_df['Launchsite'].unique().tolist()
                                site1 = sites[0]
                                site2 = sites[1]
                                site3 = sites[2]
                                site4 = sites[3]
                                dcc.Dropdown(id='site-dropdown',
                                              options=[{'label': 'All Sites', 'value': 'ALL'},{'label': 'site1', 'value': 'site1'}, {'label': 'site2', 'value': 'site2'}, {'label': 'site3', 'value': 'site3'}, {'label': 'site4', 'value': 'site4'}],
                                              value = 'ALL',
                                              placeholder = 'Select a Launch Site here',
                                              searchable = True)
                                html.Br(),
								# TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
								# TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step = 1000, value = [min_payload, max_payload]),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

																								
# Function decorator to specify function input and output

		
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['Launchsite' == entered_site]]
    if entered_site == 'ALL':
        data = spacex_df[spacex_df['class']==1].groupby('Launchsite').count()
        fig = px.pie(spacex_df, values='data', 
        names='Launchsite', 
        title='Total Succes Launches')
        return fig
    else:
        # return the outcomes piechart for a selected site
        data = filtered_df.groupby('class').count()
        fig = px.pie(filtered_df, values='data', 
        names='class', 
        title='Succeded and Failed Launches by site')
        return fig
		
				
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def get_scatter_plot(entered_site, payload_range):
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    
    if entered_site == 'ALL':
        #data = spacex_df[spacex_df['class']==1].groupby('Launchsite').count()
        fig = px.scatter(mask, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                 title ='Correlation between Payload and Success for all Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = mask[mask['Launchsite' == entered_site]]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                 title ='Correlation between Payload and Success for all Sites')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()