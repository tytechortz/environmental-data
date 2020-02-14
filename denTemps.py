import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from datetime import datetime, date, timedelta
import json, csv, dash_table, time, operator
from connect import norm_records, rec_lows, rec_highs, all_temps
import pandas as pd
import numpy as np
from numpy import arange,array,ones
from scipy import stats 
# from index import d_max_max, d_max_min

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

server = app.server

df_all_temps = pd.DataFrame(all_temps,columns=['dow','sta','Date','TMAX','TMIN'])
last_day = df_all_temps.iloc[-1, 2] + timedelta(days=1)
ld = last_day.strftime("%Y-%m-%d")

df_norms = pd.DataFrame(norm_records)

df_rec_lows = pd.DataFrame(rec_lows)
# print(rec_lows)

df_rec_highs = pd.DataFrame(rec_highs)

current_year = datetime.now().year
today = time.strftime("%Y-%m-%d")
startyr = 1950
year_count = current_year-startyr


def temp_App():
    return html.Div(
        [
            html.Div([
                html.H4(
                    'DENVER TEMPERATURE RECORD',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(
                    'NOAA Stapleton Station Data',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    id='title-date-range',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Label('Select Product'),
                    dcc.RadioItems(
                        id='product',
                        options=[
                            {'label':'Temperature graphs', 'value':'temp-graph'},
                            {'label':'Climatology for a day', 'value':'climate-for-day'},
                            {'label':'Full Record Bar Graphs', 'value':'frbg'},
                            {'label':'5 Year Moving Avgs', 'value':'fyma-graph'},
                            {'label':'Full Record Heat Map', 'value':'frhm'},
                        ],
                        # value='temp-graph',
                        labelStyle={'display': 'block'},
                    ),
                ],
                    className='three columns',
                ),
                html.Div([
                    html.Div(
                        id='year-picker'
                    ),
                    html.Div(
                        id='date-picker'
                    ),
                ],
                    className='four columns',
                ),
                html.Div([
                    html.Button('Update Data', id='data-button'),
                ]),
                html.Div([
                    html.Div(id='output-data-button')
                ]),

            ],
                className='row'
            ),
            html.Div([
                html.Div(
                    [
                        html.Div(id='period-picker'),
                    ],
                ),
    
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='graph'
                    ),
                ],
                    className='eight columns'
                ),
                html.Div([
                    html.Div([
                        html.Div(id='graph-stats'
                        ),
                    ],
                    ),
                    html.Div([
                        html.Div(id='frs-bar-controls'
                        ),
                    ],
                    ),
                    html.Div([
                        html.Div(id='frs-heat-controls'
                        ),
                    ],
                    ),
                    html.Div([
                        html.Div(id='fyma-stats'
                        ),
                    ],
                    ),
                ],
                    className='four columns'
                ),    
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='climate-day-table'
                    ),
                ],
                    className='five columns'
                ),
                html.Div([
                    html.Div([
                        html.Div(
                            id='bar'
                        ),
                    ],
                        className='twelve columns'
                    ),
                ],
                    className='seven columns'
                ),     
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                        html.Div(id='daily-max-t'),
                    ],
                        className='six columns'
                    ),
                    html.Div([
                        html.Div(id='daily-min-t'),
                    ],
                        className='six columns'
                    ), 
            ],
                className='row'
            ),
            
            html.Div(id='all-data', style={'display': 'none'}),
            html.Div(id='rec-highs', style={'display': 'none'}),
            html.Div(id='rec-lows', style={'display': 'none'}),
            html.Div(id='norms', style={'display': 'none'}),
            html.Div(id='temp-data', style={'display': 'none'}),
            html.Div(id='df5', style={'display': 'none'}),
            html.Div(id='max-trend', style={'display': 'none'}),
            html.Div(id='min-trend', style={'display': 'none'}),
            html.Div(id='d-max-max', style={'display': 'none'}),
            html.Div(id='avg-of-dly-highs', style={'display': 'none'}),
            html.Div(id='d-min-max', style={'display': 'none'}),
            html.Div(id='d-min-min', style={'display': 'none'}),
            html.Div(id='avg-of-dly-lows', style={'display': 'none'}),
            html.Div(id='d-max-min', style={'display': 'none'}),
            html.Div(id='temps', style={'display': 'none'}),
        ]
    )


app.layout = temp_App

# if __name__ == "__main__":
#     app.run_server(port=8025, debug=False)