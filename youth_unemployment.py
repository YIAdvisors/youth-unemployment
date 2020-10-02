import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import heroku3
from dash.dependencies import Input, Output

#Ensure dash capabilities are enabled.
#This allows the code to be deployed on an online server.
app = dash.Dash(__name__)
server = app.server


################################################################################
#This code creates a data visualization of the unemployment rate for age groups.
#The plotly package is used to create the visualization.
#The dash package is used to create an interactive web app.
#################################################################################


# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
# Create separate data frames for the unemployment rate by race and by age
df = pd.read_csv("unemployment_by_race.csv")
df2 = pd.read_csv("unemployment_by_age.csv")

# ------------------------------------------------------------------------------
# App layout (create app layout for the web app)
app.layout = html.Div([

    #Create title.
    html.H1("Monthly Unemployment Rate for Young Adults Ages 18-34", style={'text-align': 'center', 'fontFamily':'Arial, serif'}),

    #Create drop down that enables the user to select the displayed statistic.
    html.Div(children='''
            Select Characteristic of Interest:
        ''', style={'text-align': 'left', 'margin-left': '2%', 'fontFamily':'Arial, serif'}),

    dcc.Dropdown(id="slct_statistic",
                 options=[
                     {"label": "Race", "value": "Race"}, #creates a list with the options
                     {"label": "Age", "value": "Age"},],
                 multi=False,
                 value="Race",
                 style={'width': "40%", 'margin-left': '2%'}
                 ),
    html.Br(),

    #Create drop down that enables the user to select the displayed year.
    html.Div(children='''
            Select Year:
        ''', style={'text-align': 'left', 'margin-left': '2%', 'fontFamily':'Arial, serif'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020}],
                 multi=False,
                 value=2020,
                 style={'width': "40%", 'margin-left': '2%'}
                 ),

    #Creates a Plotly bar chart graph.
    dcc.Graph(id='unemploymentGraph', figure={},config={
                'displayModeBar': False}),

    #Adds a link to the data source.
    dcc.Link(
        href='https://cps.ipums.org/cps/',
        refresh=True,
        children=[html.Div(children='Source: Current Population Survey', style={'text-align': 'right','margin-right': '5%', 'color':'#3c90ce', 'fontFamily':'Arial, serif'})]
    ),

    #Display the option from the dropdowns that the user selected.  (It is currently disabeled. to enable, change the code in the app.callback so that container = "option_slctd")
    html.Div(id='output_container', children=[])


])


#------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='unemploymentGraph', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'), #Note the second input used here. This is so the graph can update both the year and the statistic displayed.
    Input(component_id='slct_statistic', component_property='value')]
)

def update_graph(option_slctd, stat_slctd):
    #Print the option selected i.e. the year selected.
    print(option_slctd)

    #Print the stat selected i.e. either race or age group.
    print(stat_slctd)

    #######
    #Code to dynamically display the selected option is in the comment below:
    #container = "selected year: {}".format(option_slctd)
    #OR
    #container = "selected statistic: {}".format(stat_slctd)
    #######

    #Create a visualization for when the "race" option is selected.
    if stat_slctd == "Race":
        container = ""

        #Create a dataframe that only contains the selected year.
        dfCopy = df[df["Year"] == option_slctd]
        dff = pd.DataFrame(
            {'Month': dfCopy['Month'],
             'Unemployment': dfCopy['Unemployment Rate'],
             'Group': dfCopy['Group']
            })

        #Create separate dataframes for each race.
        dffWhite = dff[dff["Group"] == "White"]
        dffBlack = dff[dff["Group"] == "Black"]
        dffAsian = dff[dff["Group"] == "Asian"]
        dffLatinx = dff[dff["Group"] == "Latinx"]

        #Create a barchart, with a colorcoded bar for each racial group.
        fig = go.Figure(data=[
            go.Bar(name='White', x=dffWhite['Month'], y=dffWhite['Unemployment'], marker_color='#2c3e65'),
            go.Bar(name='Black', x=dffBlack['Month'], y=dffBlack['Unemployment'], marker_color='#3c90ce'),
            go.Bar(name='Hispanic/Latinx', x=dffLatinx['Month'], y=dffLatinx['Unemployment'], marker_color='#dd3430'),
            go.Bar(name='Asian', x=dffAsian['Month'], y=dffAsian['Unemployment'], marker_color='#1c2d4f')
        ])

        #Update the hover menu to only display the unemployment rate.
        fig.update_traces(hovertemplate='Unemployment Rate: %{y:.02%}')
        fig.update_traces(hoverinfo='none')

        #Set the aesthetic characteristics of the barchart.
        fig.update_layout(xaxis_title="Month", yaxis_title="Unemployment Rate", showlegend=True, hoverlabel=dict(
            font_size=10,
            font_family="Arial, serif"
        ))
        fig.layout.yaxis.tickformat = ',.0%'
        fig.update_layout(font=dict(
            family="Arial, serif",
            size=14,
        ))


    #Create a visualization for when the "age" option is selected.
    else:
        container = ""

        #Create a dataframe that only contains the selected year.
        dfCopy = df2[df2["Year"] == option_slctd]
        dff = pd.DataFrame(
            {'Month': dfCopy['Month'],
             'Unemployment': dfCopy['Unemployment Rate'],
             'Group': dfCopy['Group']
            })

        #Create separate dataframes for each age group.
        dff18up = dff[dff["Group"] == "Total 18+"]
        dff18_26 = dff[dff["Group"] == "Youth 18-26"]
        dff27_34 = dff[dff["Group"] == "Youth 27-34"]

        #Create a barchart, with a colorcoded bar for each age group.
        fig = go.Figure(data=[
            go.Bar(name='Youth 18-26', x=dff18_26['Month'], y=dff18_26['Unemployment'], marker_color='#2c3e65'),
            go.Bar(name='Youth 27-34', x=dff27_34['Month'], y=dff27_34['Unemployment'], marker_color='#3c90ce'),
            go.Bar(name='Adults 35-65', x=dff18up['Month'], y=dff18up['Unemployment'], marker_color='#dd3430')
        ])

        #Update the hover menu to only display the unemployment rate.
        fig.update_traces(hovertemplate='Unemployment Rate: %{y:.02%}', )
        fig.update_traces(hoverinfo='none')

        #Set the aesthetic characteristics of the barchart.
        fig.update_layout(xaxis_title="Month", yaxis_title="Unemployment Rate", showlegend=True, hoverlabel=dict(
            font_size=10,
            font_family="Arial, serif"
        ))
        fig.layout.yaxis.tickformat = ',.0%'
        fig.update_layout(font=dict(
            family="Arial, serif",
            size=14,
        ))


    return container, fig

#Command that ensures dash capabilities are enabled.
#This allows the code to be deployed on an online server.
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
