### Data
import pandas as pd
import numpy as np
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

import time
from datetime import datetime
from pandas import Series
from scipy import stats 
from numpy import arange,array,ones 
from scipy.stats import norm
from pandas import DatetimeIndex

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

pd.options.display.float_format = '{:,}'.format

value_range = [0, 365]

# Read data
df = pd.read_csv('ftp://sidads.colorado.edu/DATASETS/NOAA/G02186/masie_4km_allyears_extent_sqkm.csv', skiprows=1)

# Format date and set indext to date
df['yyyyddd'] = pd.to_datetime(df['yyyyddd'], format='%Y%j')
df.set_index('yyyyddd', inplace=True)
df.columns = ['Total Arctic Sea', 'Beaufort Sea', 'Chukchi Sea', 'East Siberian Sea', 'Laptev Sea', 'Kara Sea',\
     'Barents Sea', 'Greenland Sea', 'Bafin Bay Gulf of St. Lawrence', 'Canadian Archipelago', 'Hudson Bay', 'Central Arctic',\
         'Bering Sea', 'Baltic Sea', 'Sea of Okhotsk', 'Yellow Sea', 'Cook Inlet']

count_row = df.shape[0]
days = count_row

# Dropdown year selector values
year_options = []
for YEAR in df.index.year.unique():
    year_options.append({'label':(YEAR), 'value':YEAR})

# Dropdown month selector values
month_options = [
{'label':'JAN', 'value':1},
{'label':'FEB', 'value':2},
{'label':'MAR', 'value':3},
{'label':'APR', 'value':4},
{'label':'MAY', 'value':5},
{'label':'JUN', 'value':6},
{'label':'JUL', 'value':7},
{'label':'AUG', 'value':8},
{'label':'SEP', 'value':9},
{'label':'OCT', 'value':10},
{'label':'NOV', 'value':11},
{'label':'DEC', 'value':12}
]

# Dropdown sea selector values
sea_options = []
for sea in df.columns.unique():
    sea_options.append({'label':sea, 'value':sea})


# Change dataframe to 5 day trailing average
df_fdta = df.rolling(window=5).mean()

startyr = 2006
presentyr = datetime.now().year
last_year = presentyr-1
year_count = presentyr-startyr
presentday = datetime.now().day
dayofyear = time.strftime("%j")
dayofyear = int(dayofyear)

arctic = df['Total Arctic Sea']
years = []

year_dict = {}
keys = []


for i in df.index.year.unique():
    keys.append(i)

def dictionary_maker():
    for i in keys:
        year_dict[i] = 0
keys = [str(i) for i in keys]
dictionary_maker()



m = 1
d = 1

arctic_r = arctic[(arctic.index.month == m) & (arctic.index.day == d)]
sort_arctic_r = arctic_r.sort_values(axis=0, ascending=True)


nav = Navbar()

header = html.H3(
    'Select the name of an Illinois city to see its population!'
)


def ice_App():
    return html.Div(
        [
            nav,
            html.Div([
                html.H2(
                    'Arctic Sea Ice Extent',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    '2006-Present',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.H6(
                    'Data From National Snow and Ice Data Center',
                    className='twelve columns',
                    style={'text-align': 'center'}
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Label('Select Product', style={'text-align': 'center'}),
                    html.Div([
                        dcc.RadioItems(
                        id='product',
                        options=[
                            {'label':'Ice Exent By Year', 'value':'years-graph'},
                            {'label':'Avg Monthy Extent', 'value':'monthly-bar'},
                            {'label':'Extent On Current Date', 'value':'extent-date'},
                            {'label':'Extent Rankings', 'value':'extent-stats'},
                        ],
                        # value='temp-graph',
                        labelStyle={'display': 'block'},
                    ),
                    ],
                        className='pretty_container'
                    ),
                ],
                    className='three columns',
                ),
                html.Div([
                    html.Div(id='sea-selector'),
                ],
                    className='two columns'
                ),
                html.Div([
                    html.Div(id='month-selector'),
                ],
                    className='two columns'
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
                    html.Div(id='stats-n-stuff')
                ],
                    className='four columns'
                ), 
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.Div(
                        id='stats'
                    ), 
                ],
                    className='twelve columns'
                ),
            ],
                className='row'
            ),
            
            html.Div(id='df-monthly', style={'display': 'none'}),
            html.Div(id='df-fdta', style={'display': 'none'}),
    ])

app.layout = ice_App

@app.callback(
    Output('stats-n-stuff', 'children'),
    [Input('product', 'value')])
def stats_n_stuff(product):
    if product == 'years-graph':
        return html.Div([
            html.Div([
                html.Div(id='year-selector')
            ],
                className='three columns'
            ), 
            html.Div([
                html.Div(id='current-stats')
            ],
                className='eight columns'
            ),
        ],
            className='twelve columns'
        ),
    elif product == 'monthly-bar':
        return html.Div([
            html.Div([
                html.Div(id='monthly-bar-stats')
            ],
                className='twelve columns'
            )
        ],
            className='twelve columns'
        ),
    elif product == 'extent-date':
        return html.Div([
            html.Div([
                html.Div([
                    html.Div(id='extent-date')
                ],
                    className='seven columns'
                ),
            ],
                className='row'
            ),
            
        ],
            className='twelve columns'
        ),

@app.callback(
    Output('stats', 'children'),
    [Input('product', 'value')])
def display_stats(value):
    
    if value == 'extent-stats':
        return html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='annual-max-table')
                    ],
                        className='three columns'
                    ),
                    html.Div([
                        html.Div(id='annual-min-table')
                    ],
                        className='three columns'
                    ),
                    html.Div([
                        html.Div(id='annual-rankings')
                    ],
                        className='three columns'
                    ),
                ])
        ],
            className='twelve columns'
        ),

@app.callback(
    Output('daily-rankings-graph', 'figure'),
    [Input('product', 'value'),
    Input('selected-sea', 'value'),
    Input('df-fdta', 'children')])
def update_figure_b(selected_product, selected_sea, df_fdta):
    if selected_product == 'extent-date':
        df_fdta = pd.read_json(df_fdta)
      
        dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
        dr_sea = dr[selected_sea]
        dr_sea.index = dr_sea.index.strftime('%Y-%m-%d')
        
        # trend line
        def fit():
            xi = arange(0,len(dr_sea))
            slope, intercept, r_value, p_value, std_err = stats.linregress(xi,dr_sea)
            return (slope*xi+intercept)

        data = [
            go.Bar(
                x=dr_sea.index,
                y=dr_sea,
                name=('Extent')
            ),
            go.Scatter(
                    x=dr_sea.index,
                    y=fit(),
                    name='trend',
                    line = {'color':'red'}
                ),
        ]
        layout = go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Ice Extent-Million km2'},
            title='{} Values on {}'.format(selected_sea, dr_sea.index[-1]),
            plot_bgcolor = 'lightgray',
        )
        return {'data': data, 'layout': layout}

@app.callback(
    Output('extent-date', 'children'),
    [Input('df-fdta', 'children'),
    Input('selected-sea', 'value'),
    Input('product', 'value')])
def daily_ranking(df_fdta, selected_sea, selected_product):
    if selected_product == 'extent-date':
    
        df_fdta = pd.read_json(df_fdta)
        dr = df_fdta[(df_fdta.index.month == df_fdta.index[-1].month) & (df_fdta.index.day == df_fdta.index[-1].day)]
        
        dr_sea = dr[selected_sea]
        sort_dr_sea = dr_sea.sort_values(axis=0, ascending=True)
        sort_dr_sea = pd.DataFrame({'km2':sort_dr_sea.values, 'YEAR':sort_dr_sea.index.year})
        sort_dr_sea = sort_dr_sea.round(0)
    
        return html.Div([
                html.Div('Current Day Values', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sort_dr_sea.YEAR[i]), style={'text-align': 'center'}) for i in range(10)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sort_dr_sea.iloc[i,0]), style={'text-align': 'left'}) for i in range(10)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            ),
    # else:
    #     return None

@app.callback(
    Output('annual-max-table', 'children'),
    [Input('selected-sea', 'value'),
    Input('product', 'value'),
    Input('df-fdta', 'children')])
def record_ice_table(selected_sea, selected_value, df_fdta, max_rows=10):
    df_fdta = pd.read_json(df_fdta)
    
    annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=True)
   
    sama = pd.DataFrame({'Extent km2':sorted_annual_max_all.values,'YEAR':sorted_annual_max_all.index.year})
    sama = sama.round(0)
    return html.Div([
                html.Div('Annual Max', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{:.0f}'.format(sama.iloc[y][1]), style={'text-align': 'center'}) for y in range(0,14)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sama.iloc[y,0]), style={'text-align': 'left'}) for y in range(0,14)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            )

@app.callback(
    Output('annual-min-table', 'children'),
    [Input('selected-sea', 'value'),
    Input('df-fdta', 'children')])
def record_ice_table_a(selected_sea, df_fdta, max_rows=10):
    df_fdta = pd.read_json(df_fdta)
    annual_min_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmin().iloc[:, 0]]
    sorted_annual_min_all = annual_min_all.sort_values(axis=0, ascending=True)
    sama = pd.DataFrame({'Extent km2':sorted_annual_min_all.values,'YEAR':sorted_annual_min_all.index.year})
    sama = sama.round(0)
    return html.Div([
                html.Div('Annual Min', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{:.0f}'.format(sama.iloc[y][1]), style={'text-align': 'center'}) for y in range(0,14)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,.0f}'.format(sama.iloc[y,0]), style={'text-align': 'left'}) for y in range(0,14)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            )

@app.callback(
    Output('annual-rankings', 'children'),
    [Input('product', 'value')])
def annual_ranking(selected_product):
   
    if selected_product == 'extent-stats':
        df1 = df['Total Arctic Sea']

        x = 0

        rankings = [['2006', 0],['2007', 0],['2008', 0],['2009', 0],['2010', 0],['2011', 0],['2012', 0],['2013', 0],['2014', 0],['2015', 0],['2016', 0],['2017', 0],['2018', 0],['2019', 0]]
        rank = pd.DataFrame(rankings, columns = ['Year','Pts'])
    
        while x < 366:
            dr1 = df1[(df1.index.month == df1.index[x].month) & (df1.index.day == df1.index[x].day)]
            dr_sort = dr1.sort_values(axis=0, ascending=True)
        
            rank.loc[rank['Year'] == str(dr_sort.index.year[0]), 'Pts'] += 10
            rank.loc[rank['Year'] == str(dr_sort.index.year[1]), 'Pts'] += 9
            rank.loc[rank['Year'] == str(dr_sort.index.year[2]), 'Pts'] += 8
            rank.loc[rank['Year'] == str(dr_sort.index.year[3]), 'Pts'] += 7
            rank.loc[rank['Year'] == str(dr_sort.index.year[4]), 'Pts'] += 6
            rank.loc[rank['Year'] == str(dr_sort.index.year[5]), 'Pts'] += 5
            rank.loc[rank['Year'] == str(dr_sort.index.year[6]), 'Pts'] += 4
            rank.loc[rank['Year'] == str(dr_sort.index.year[7]), 'Pts'] += 3
            rank.loc[rank['Year'] == str(dr_sort.index.year[8]), 'Pts'] += 2
            rank.loc[rank['Year'] == str(dr_sort.index.year[9]), 'Pts'] += 1
        
            rank.sort_values(by=['Pts'], ascending=True)
            x += 1

        sorted_rank = rank.sort_values('Pts', ascending=False)
    
        return html.Div([
                html.Div('Annual Ranks', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(sorted_rank.iloc[y][0]), style={'text-align': 'center'}) for y in range(0,14)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{:,}'.format(sorted_rank.iloc[y,1]), style={'text-align': 'left'}) for y in range(0,14)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            ),
                    
@app.callback(
    Output('df-fdta', 'children'),
    [Input('product', 'value')])
def clean_fdta(selected_product):
    df_fdta = df.rolling(window=5).mean()
    if selected_product == 'years-graph' or selected_product == 'extent-stats' or selected_product == 'extent-date':
        return df_fdta.to_json()

@app.callback(
    Output('monthly-bar-stats', 'children'),
    [Input('df-monthly', 'children'),
    Input('product','value')])
def display_graph_stats(ice, selected_product):

    if selected_product == 'monthly-bar':
        df_monthly = pd.read_json(ice)
        extent = df_monthly['data'].apply(pd.Series)
        extent['value'] = extent['value'].astype(float)
        extent = extent.sort_values('value')
        extent = extent[extent.value != -9999]

        return html.Div([
                html.Div('10 Lowest Selected Month', style={'text-align': 'center'}),
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div('{}'.format(extent.index[i]), style={'text-align': 'center'}) for i in range(10)
                        ],
                            className='eight columns'
                        ),
                        html.Div([
                            html.Div('{}'.format(extent.iloc[i,0]), style={'text-align': 'left'}) for i in range(10)
                        ],
                            className='four columns'
                        ),  
                    ],
                        className='row'
                    ),
                ],
                    className='round1'
                ),      
            ],
                className='round1'
            ),

@app.callback(
    Output('year-selector', 'children'),
    [Input('product', 'value')])
def display_year_selector(product_value):
    if product_value == 'years-graph':
        return html.P('Select Years') , html.Div([
                html.Div([
                dcc.Checklist(
                id='selected-years',
                options=year_options,
                value=2019       
                )
            ],
                className='pretty_container'
            ),
        ],
         className='twelve columns'
        ),

@app.callback(
    Output('sea-selector', 'children'),
    [Input('product', 'value')])
def display_sea_selector(product_value):
    if product_value == 'years-graph' or product_value == 'extent-date' or product_value == 'extent-stats':
        return html.P('Select Sea', style={'text-align': 'center'}) , html.Div([
            dcc.Dropdown(
                id='selected-sea',
                options=sea_options,
                value='Total Arctic Sea'      
            ),
        ],
            className='pretty_container'
        ),

@app.callback(
    Output('month-selector', 'children'),
    [Input('product', 'value')])
def display_month_selector(product_value):
    if product_value == 'monthly-bar':
        return html.P('Select Month', style={'text-align': 'center'}) , html.Div([
            dcc.Dropdown(
                id='month',
                options=month_options,
                value=1     
            ),
        ],
            className='pretty_container'
        ),

@app.callback(
    Output('graph', 'children'),
    [Input('product', 'value')])
def display_graph(value):
    if value == 'years-graph':
        return dcc.Graph(id='ice-extent')
    elif value == 'monthly-bar':
        return dcc.Graph(id='monthly-bar')
    elif value == 'extent-date':
        return dcc.Graph(id='daily-rankings-graph')

@app.callback(
    Output('current-stats', 'children'),
    [Input('selected-sea', 'value'),
    Input('product', 'value'),
    Input('df-fdta', 'children')])
def update_current_stats(selected_sea, selected_product, df_fdta):
    df_fdta = pd.read_json(df_fdta)
    annual_max_all = df_fdta[selected_sea].loc[df_fdta.groupby(pd.Grouper(freq='Y')).idxmax().iloc[:, 0]]
    sorted_annual_max_all = annual_max_all.sort_values(axis=0, ascending=True)
    today_value = df_fdta[selected_sea][-1]
    daily_change = today_value - df_fdta[selected_sea][-2]
    week_ago_value = df_fdta[selected_sea].iloc[-7]
    weekly_change = today_value - week_ago_value
    record_min = df_fdta[selected_sea].min()
    record_min_difference = today_value - record_min
    record_low_max = sorted_annual_max_all[-1]
    record_max_difference = today_value - record_low_max
  
    if selected_product == 'years-graph':
        return html.Div([
                    html.Div('Current Extent', style={'text-align': 'center'}),
                    html.Div([
                        html.Div([
                            html.Div('{:,.0f}'.format(today_value), style={'text-align': 'center'}), 
                        ],
                            className='round1'
                        ),  
                    ]),
                    html.Div([
                        html.Div('Daily Change', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.Div('{:,.0f}'.format(daily_change), style={'text-align': 'center'}), 
                            ],
                                className='round1'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.Div('Weekly Change', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.Div('{:,.0f}'.format(weekly_change), style={'text-align': 'center'}), 
                            ],
                                className='round1'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.Div('Diff From Rec Low Min', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.Div('{:,.0f}'.format(record_min_difference), style={'text-align': 'center'}), 
                            ],
                                className='round1'
                            ),  
                        ]),      
                    ]),
                    html.Div([
                        html.Div('Diff From Rec Low Max', style={'text-align': 'center'}),
                        html.Div([
                            html.Div([
                                html.Div('{:,.0f}'.format(record_max_difference), style={'text-align': 'center'}), 
                            ],
                                className='round1'
                            ),  
                        ]),      
                    ]),      
                ],
                    className='round1'
                ),
                    
@app.callback(
    Output('ice-extent', 'figure'),
    [Input('selected-sea', 'value'),
    Input('selected-years', 'value'),
    Input('df-fdta', 'children')])
def update_figure(selected_sea, selected_year, df_fdta):
    traces = []
    df_fdta = pd.read_json(df_fdta)
    # selected_years = [selected_year1,selected_year2,selected_year3,selected_year4]
    for x in selected_year:
        sorted_daily_values=df_fdta[df_fdta.index.year == x]
        traces.append(go.Scatter(
            y=sorted_daily_values[selected_sea],
            mode='lines',
            name=x
        ))
    return {
        'data': traces,
        'layout': go.Layout(
                title = '{} Ice Extent'.format(selected_sea),
                xaxis = {'title': 'Day', 'range': value_range},
                yaxis = {'title': 'Ice extent (km2)'},
                hovermode='closest',
                )  
    }

@app.callback([
    Output('monthly-bar', 'figure'),
    Output('df-monthly', 'children')],
    [Input('month', 'value')])
def update_figure_c(month_value):
    df_monthly = pd.read_json('https://www.ncdc.noaa.gov/snow-and-ice/extent/sea-ice/N/' + str(month_value) + '.json')
    df_monthly = df_monthly.iloc[5:]
    ice = []
    for i in range(len(df_monthly['data'])):
        ice.append(df_monthly['data'][i]['value'])
    ice = [14.42 if x == -9999 else x for x in ice]
    ice = list(map(float, ice))
    
    # trend line
    def fit():
        xi = arange(0,len(ice))
        slope, intercept, r_value, p_value, std_err = stats.linregress(xi,ice)
        return (slope*xi+intercept)

    data = [
        go.Bar(
            x=df_monthly['data'].index,
            y=ice
        ),
        go.Scatter(
                x=df_monthly['data'].index,
                y=fit(),
                name='trend',
                line = {'color':'red'}
            ),

    ]
    layout = go.Layout(
        xaxis={'title': 'Year'},
        yaxis={'title': 'Ice Extent-Million km2', 'range':[(min(ice)-1),(max(ice)+1)]},
        title='{} Avg Ice Extent'.format(month_options[int(month_value)- 1]['label']),
        plot_bgcolor = 'lightgray',
    )
    return {'data': data, 'layout': layout}, df_monthly.to_json()