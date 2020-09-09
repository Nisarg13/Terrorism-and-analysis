# Map changes with the changes in the dropdow

#importing the libraries
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, State, Output 
import dash_core_components as dcc
import plotly.graph_objects as go  
import plotly.express as px


# Global variables
app = dash.Dash()

def load_data():
  global token
  token='<Enter your token>'
  dataset_name = "global_terror.csv"

  #this line we use to hide some warnings which gives by pandas
  #pd.options.mode.chained_assignment = None
  
  global df
  df = pd.read_csv(dataset_name)
  #pd.set_option("display.max_rows", None)
  #pd.set_option('display.max_columns', None)
  #print(df.head(5))
  #print(df.tail(5))


  global month_list
  month = {
         "January":1,
         "February": 2,
         "March": 3,
         "April":4,
         "May":5,
         "June":6,
         "July": 7,
         "August":8,
         "September":9,
         "October":10,
         "November":11,
         "December":12
         }
  month_list= [{"label":key, "value":values} for key,values in month.items()]
  print(month_list)
  global date_list
  date_list = [{"label":x, "value":x} for x in range(1, 32)] 


  global region_list
  region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  #region_list.insert(0, {"label":"All", "value":"All"} )

  #print(region_list)  
  # Total 12 Regions

  #global country_list
  #country_list = [{"label": str(i), "value": str(i)}  for i in sorted(df['country_txt'].unique().tolist())]
  #print(country_list)
  # Total 205 Countries
  #df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()


  #global state_list
  #state_list = [{"label": str(i), "value": str(i)}  for i in df['provstate'].unique().tolist()]
  #print(state_list)
  # Total 2580 states

  #global city_list
  #city_list = [{"label": str(i), "value": str(i)}  for i in df['city'].unique().tolist()]
  #print(city_list)
  # Total 39489 cities

  global attack_type_list
  attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  #print(attack_type_list)


  global year_list
  year_list = sorted ( df['iyear'].unique().tolist()  )

  global year_dict
  year_dict = {str(year): str(year) for year in year_list}
  #print(year_dict)
  global chart_dropdown_values
  chart_dropdown_values = {"Terrorist Organisation":'gname', 
                             "Target Nationality":'natlty1_txt', 
                             "Target Type":'targtype1_txt', 
                             "Type of Attack":'attacktype1_txt', 
                             "Weapon Type":'weaptype1_txt', 
                             "Region":'region_txt', 
                             "Country Attacked":'country_txt'
                          }
                              
  chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]

def open_browser():
  # Open the default web browser
  webbrowser.open_new('http://127.0.0.1:8050/')


# Layout of your page
def create_app_ui():
  # Create the UI of the Webpage here
  main_layout = html.Div([
  html.H1('Terrorism Analysis with Insights', id='Main_title',style={'textAlign': 'center','color':'white','font-size':'50px'}),
  html.Div(html.Div(id='my_hidden')),
  dcc.Tabs(id="Tabs", value="tab-1",style={
        'width': '50%',
        'font-size': '150%',
        'height': '25%',
        'margin-left': '50%',
        'margin-right': '25%'
        
    },children=[
      dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
      dcc.Tabs(id = "subtabs", value = "tab-1",style={
        'width': '50%',
        'font-size': '150%',
        'height': '25%',
        'margin-left': '50%',
        'margin-right': '25%'
        
    },children = [
              dcc.Tab(label="World Map tool", id="World", value="tab-1",selected_className='custom-tab--selected' ,children = [html.Div(),
              dcc.Dropdown(
        id='month', 
        options=month_list,
        placeholder='Select Month',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%', 
       }
  ),
  dcc.Dropdown(
        id='date', 
        placeholder='Select Day',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='region-dropdown', 
        options=region_list,
        placeholder='Select Region',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='country-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select Country',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='state-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select State or Province',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='city-dropdown', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select City',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='attacktype-dropdown', 
        options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
        placeholder='Select Attack Type',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),

  html.H5('Select the Year', id='year_title',style={'color':'black','font-size':'35px','font-weight':'bold'}),
  dcc.RangeSlider(
        id='year-slider',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict,
     
  ),
  #dcc.Graph(id='graph-object', children = ["World Map is loading"]),
  html.Br(),
  html.Div(
        dcc.Loading(
            id='graph-object',
            type="default",
            #children=html.Div(id="loading-output-1",)
            children = ["World Map is loading"]
        ),
      #id='graph-object', 
      )
              ]),
              dcc.Tab(label="India Map tool", id="India", value="tab-2", children =[html.Div(),
              dcc.Dropdown(
        id='month1', 
        options=month_list,
        placeholder='Select Month',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='date1', 
        placeholder='Select Day',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='region-dropdown1', 
        options=region_list,
        placeholder='Select Region',
        value=['South Asia'],
        disabled=True,
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='country-dropdown1', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select Country',
        value=['India'],
        disabled=True,
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='state-dropdown1', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select State or Province',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='city-dropdown1', 
        options=[{'label': 'All', 'value': 'All'}],
        placeholder='Select City',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),
  dcc.Dropdown(
        id='attacktype-dropdown1', 
        options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
        placeholder='Select Attack Type',
        value=[],
        multi=True,
        style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }
  ),

  html.H5('Select the Year', id='year_title1',style={'color':'black','font-size':'35px','font-weight':'bold'}),
  dcc.RangeSlider(
        id='year-slider1',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict
  ),
  #dcc.Graph(id='graph-object1', children = ["India Map is loading"]),
  html.Br(),
  
  html.Div(
        dcc.Loading(
            id='graph-object1',
            type="default",
            #children=html.Div(id="loading-output-1",)
            children = ["India Map is loading"]
        ),
      #id='graph-object', 
      #dcc.Graph(id='graph-object1', children = ["India Map is loading"])
      )
              ])
              ]
              )
              ]),
      
      dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
      dcc.Tabs(id = "subtabs2", value = "WorldChart",style={
        'width': '50%',
        'font-size': '150%',
        'height': '25%',
        'margin-left': '50%',
        'margin-right': '25%'
        
    },children = [
              dcc.Tab(label="World Chart tool", id="WorldC",selected_className='custom-tab--selected' ,value="WorldChart",children=[
                  html.Br(),
                  dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt",style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }), 
                  html.Br(),
                  
                  dcc.Input(id="search", placeholder="Search Filter",style={'height': '50px',
	'width': '250px',
	'text-align': 'center',
	
	'position': 'relative',
    'margin-left': '67%',
    'margin-right': 'auto',}),
                  
                  html.Br(),
                  html.H5('Select the Year', id='year_title2',style={'color':'black','font-size':'35px','font-weight':'bold'}),
  dcc.RangeSlider(
        id='year-slider2',
        min=min(year_list),
        max=max(year_list),
        value=[min(year_list),max(year_list)],
        marks=year_dict
  ),
                  html.Div(id = "graph-object3", children ="Graph will be shown here")]),
              dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart",children=[
                  html.Br(),
                  dcc.Dropdown(id="Chart_Dropdown1", options = chart_dropdown_values, placeholder="Select option", value = "region_txt",style={'width': '500px',
    'height': 'auto',
	'text-align-last': 'center',
	'text-align': 'center !important',
	'display': 'block',
	'position': 'relative',
    'margin-left': '50%',
    'margin-right': '25%',    }), 
                  html.Br(),
                  dcc.Input(id="search1", placeholder="Search Filter",style={'height': '50px',
	'width': '250px',
	'text-align': 'center',
	'display': 'block',
	'position': 'relative',
    'margin-left': '67%',
    'margin-right': 'auto',}),
                  html.Br(),
                  html.H5('Select the Year', id='year_title3',style={'color':'black','font-size':'35px','font-weight':'bold'}),
                    dcc.RangeSlider(
                            id='year-slider3',
                            min=min(year_list),
                            max=max(year_list),
                            value=[min(year_list),max(year_list)],
                            marks=year_dict
                    ),
                  html.Div(id = "graph-object4", children ="Graph will be shown here")
              ])]),
              html.Div(),
              
              ])
    ]),
  
  ],
    style = {
'backgroundImage':'url("/assets/indianarmy3.jpg")',
'backgroundSize':'cover',
'width':'100%',
'height':'1000px',
'margin': 'auto'
}
  )
  
  return main_layout

fig=None
# Callback of your page
@app.callback(
    dash.dependencies.Output('graph-object', 'children'),
    [
    dash.dependencies.Input('month', 'value'),
    dash.dependencies.Input('date', 'value'),
    dash.dependencies.Input('region-dropdown', 'value'),
    dash.dependencies.Input('country-dropdown', 'value'),
    dash.dependencies.Input('state-dropdown', 'value'),
    dash.dependencies.Input('city-dropdown', 'value'),
    dash.dependencies.Input('attacktype-dropdown', 'value'),
    dash.dependencies.Input('year-slider', 'value'),
    dash.dependencies.Input('Tabs','value'),
    dash.dependencies.Input('subtabs','value'),
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input('subtabs2','value'),
    ]
    )

def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,Tabs_value,subtabs_value,chart_dp_value, search,
                   subtabs2):
    global figure
    figure = go.Figure()

                # year_filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df = df[df["iyear"].isin(year_range)]
                

                # month_filter
    if month_value is None or month_value==[]:
                    pass
    else:
        if date_value is None or date_value==[]:
                        new_df = new_df[new_df["imonth"].isin(month_value)]

        else:
                        new_df = new_df[(new_df["imonth"].isin(month_value))&
                                        (new_df["iday"].isin(date_value))]
                
                
    # region, country, state, city filter
    if Tabs_value=='Map':
            if subtabs_value=='tab-1':
                    print("Data Type of month value = " , str(type(month_value)))
                    print("Data of month value = " , month_value)
                                    
                    print("Data Type of Day value = " , str(type(date_value)))
                    print("Data of Day value = " , date_value)
                                    
                    print("Data Type of region value = " , str(type(region_value)))
                    print("Data of region value = " , region_value)
                                    
                    print("Data Type of country value = " , str(type(country_value)))
                    print("Data of country value = " , country_value)
                                    
                    print("Data Type of state value = " , str(type(state_value)))
                    print("Data of state value = " , state_value)
                                    
                    print("Data Type of city value = " , str(type(city_value)))
                    print("Data of city value = " , city_value)
                                    
                    print("Data Type of Attack value = " , str(type(attack_value)))
                    print("Data of Attack value = " , attack_value)
                                    
                    print("Data Type of year value = " , str(type(year_value)))
                    print("Data of year value = " , year_value)
       
                    if region_value is None or region_value==[] :
                        pass
                    else:
                        if country_value is None or country_value==[]:
                            new_df = new_df[new_df["region_txt"].isin(region_value)]
                        else:
                            if state_value is None or state_value==[]:
                                new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                                (new_df["country_txt"].isin(country_value))]
                            else:
                                if city_value is None or city_value==[]:
                                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                                (new_df["country_txt"].isin(country_value)) &
                                                (new_df["provstate"].isin(state_value))]
                                else:
                                    new_df = new_df[(new_df["region_txt"].isin(region_value))&
                                                (new_df["country_txt"].isin(country_value)) &
                                                (new_df["provstate"].isin(state_value))&
                                                (new_df["city"].isin(city_value))]
    # Attack Type                    
                    if attack_value is None or attack_value==[]:
                        pass
                    else:
                        new_df = new_df[new_df["attacktype1_txt"].isin(attack_value)]
                    

                    # You should always set the figure for blank, since this callback 
                    # is called once when it is drawing for first time                          
                    if new_df.shape[0]:
                        pass
                        print("Shape-------------------------------->")
                    else: 
                        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                    'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
                        
                        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
                    
                    mapfigure = px.scatter_mapbox(new_df,
                                lat="latitude", 
                                lon="longitude",
                                color="attacktype1_txt",
                                hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                                zoom=1
                                )                       
                    mapfigure.update_layout(mapbox_style="dark",
                            mapbox_accesstoken=token,
                            autosize=True,
                            margin=dict(l=0, r=0, t=25, b=20),
                            )
                    figure=mapfigure
    
    return dcc.Graph(figure=figure)
      
    

@app.callback(
  Output("date", "options"),
                [Input("month", "value")])
def update_date(month):
    day1=False
    day2= False
    day3 = False
    date_list = [x for x in range(1, 32)]
    if month==[]:
        return []
    else:
        for i in month:
            if i in [1,3,5,7,8,10,12]:
                day1=True
            elif i in [4,6,9,11]:
                day2=True
            elif i==2:
                day3 = True
        if day1==True:
            return [{"label":m, "value":m} for m in date_list]
        elif day2==True:
            return [{"label":m, "value":m} for m in date_list[:-1]]
        else:
            return [{"label":m, "value":m} for m in date_list[:-2]]
        


@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
  # Making the country Dropdown data
  return[{"label": str(i), "value": str(i)}  for i in df[df['region_txt'].isin(region_value)] ['country_txt'].unique().tolist() ]

@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist() ]


@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist() ]

@app.callback(
    dash.dependencies.Output('graph-object1', 'children'),
    [
    dash.dependencies.Input('month1', 'value'),
    dash.dependencies.Input('date1', 'value'),
    dash.dependencies.Input('region-dropdown1', 'value'),
    dash.dependencies.Input('country-dropdown1', 'value'),
    dash.dependencies.Input('state-dropdown1', 'value'),
    dash.dependencies.Input('city-dropdown1', 'value'),
    dash.dependencies.Input('attacktype-dropdown1', 'value'),
    dash.dependencies.Input('year-slider1', 'value'),
    dash.dependencies.Input('Tabs','value'),
    dash.dependencies.Input('subtabs','value'),
    dash.dependencies.Input('subtabs2','value'),
    ]
)
def update_app_ui(month_value, date_value,region_value,country_value,state_value,city_value,attack_value,year_value,Tabs_value,subtabs_value,subtabs2_value):
      
    
  
    df1=df.loc[df["country_txt"]=='India']
    global figure
    figure = go.Figure()
    # year_filter
    year_range = range(year_value[0], year_value[1]+1)
    new_df1 = df1[df1["iyear"].isin(year_range)]
    

    # month_filter
    if month_value is None or month_value==[]:
        pass
    else:
        if date_value is None or date_value==[]:
            new_df1 = new_df1[new_df1["imonth"].isin(month_value)]

        else:
            new_df1 = new_df1[(new_df1["imonth"].isin(month_value))&
                             (new_df1["iday"].isin(date_value))]
              
              
    # region, country, state, city filter
    if Tabs_value=='Map':
            if subtabs_value=='tab-2':
                    print("Data Type of month value = " , str(type(month_value)))
                    print("Data of month value = " , month_value)
                    
                    print("Data Type of Day value = " , str(type(date_value)))
                    print("Data of Day value = " , date_value)
                    
                    print("Data Type of region value = " , str(type(region_value)))
                    print("Data of region value = " , region_value)
                    
                    print("Data Type of country value = " , str(type(country_value)))
                    print("Data of country value = " , country_value)
                    
                    print("Data Type of state value = " , str(type(state_value)))
                    print("Data of state value = " , state_value)
                    
                    print("Data Type of city value = " , str(type(city_value)))
                    print("Data of city value = " , city_value)
                    
                    print("Data Type of Attack value = " , str(type(attack_value)))
                    print("Data of Attack value = " , attack_value)
                    
                    print("Data Type of year value = " , str(type(year_value)))
                    print("Data of year value = " , year_value)
                
                    if region_value is None or region_value==[] :
                        pass
                    else:
                        if country_value is None or country_value==[]:
                            new_df1 = new_df1[new_df1["region_txt"].isin(region_value)]
                        else:
                            if state_value is None or state_value==[]:
                                new_df1 = new_df1[(new_df1["region_txt"].isin(region_value))&
                                                (new_df1["country_txt"].isin(country_value))]
                            else:
                                if city_value is None or city_value==[]:
                                    new_df1 = new_df1[(new_df1["region_txt"].isin(region_value))&
                                                (new_df1["country_txt"].isin(country_value)) &
                                                (new_df1["provstate"].isin(state_value))]
                                else:
                                    new_df1 = new_df1[(new_df1["region_txt"].isin(region_value))&
                                                (new_df1["country_txt"].isin(country_value)) &
                                                (new_df1["provstate"].isin(state_value))&
                                                (new_df1["city"].isin(city_value))]
                
                
    
    # Attack Type                    
                        if attack_value is None or attack_value==[]:
                            pass
                        else:
                            new_df1 = new_df1[new_df1["attacktype1_txt"].isin(attack_value)]
                        

                        # You should always set the figure for blank, since this callback 
                        # is called once when it is drawing for first time                          
                        if new_df1.shape[0]:
                            pass
                            print("Shape-------------------------------->")
                        else: 
                            new_df1 = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
                        'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
                            
                            new_df1.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
                        
                        figure = px.scatter_mapbox(new_df1,
                                    lat="latitude", 
                                    lon="longitude",
                                    color="attacktype1_txt",
                                    hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                                    zoom=1
                                    )                       
                        figure.update_layout(mapbox_style="dark",
                            mapbox_accesstoken=token,
                                autosize=True,
                                margin=dict(l=0, r=0, t=25, b=20),
                                )
                    
    return dcc.Graph(figure=figure)
@app.callback(
  Output("date1", "options"),
  [Input("month1", "value")])
def update_date(month):
    day1=False
    day2= False
    day3 = False
    date_list = [x for x in range(1, 32)]
    if month==[]:
        return []
    else:
        for i in month:
            if i in [1,3,5,7,8,10,12]:
                day1=True
            elif i in [4,6,9,11]:
                day2=True
            elif i==2:
                day3 = True
        if day1==True:
            return [{"label":m, "value":m} for m in date_list]
        elif day2==True:
            return [{"label":m, "value":m} for m in date_list[:-1]]
        else:
            return [{"label":m, "value":m} for m in date_list[:-2]]
        


@app.callback(
    Output('country-dropdown1', 'options'),
    [Input('region-dropdown1', 'value')])
def set_country_options(region_value):
  # Making the country Dropdown data
  return[{"label": str(i), "value": str(i)}  for i in df[df['region_txt'].isin(region_value)] ['country_txt'].unique().tolist() ]

@app.callback(
    Output('state-dropdown1', 'options'),
    [Input('country-dropdown1', 'value')])
def set_state_options(country_value):
  # Making the state Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['country_txt'].isin(country_value)] ['provstate'].unique().tolist() ]


@app.callback(
    Output('city-dropdown1', 'options'),
    [Input('state-dropdown1', 'value')])
def set_city_options(state_value):
  # Making the city Dropdown data
  return [{"label": str(i), "value": str(i)}  for i in df[df['provstate'].isin(state_value)] ['city'].unique().tolist() ]
# Flow of your Project
@app.callback(
    dash.dependencies.Output('graph-object3', 'children'),
    [
    dash.dependencies.Input('Tabs','value'),
    dash.dependencies.Input('subtabs2','value'),
    dash.dependencies.Input("Chart_Dropdown", "value"),
    dash.dependencies.Input("search", "value"),
    dash.dependencies.Input("year-slider2", "value"),
    ]
)

def update_app_ui(Tabs_value,subtabs2,chart_dp_value, search,year_value):
        if Tabs_value=="Chart":
            global fig
            fig=go.Figure()
            year_range = range(year_value[0], year_value[1]+1)
            new_df = df[df["iyear"].isin(year_range)]
            if subtabs2 == "WorldChart":
                if chart_dp_value is not None:
                    if search is not None: 
                        chart_df = new_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name = "count")
                        chart_df  = chart_df[chart_df[chart_dp_value].str.contains(search, case = False)]
                    else:
                        chart_df = new_df.groupby("iyear")[chart_dp_value].value_counts().reset_index(name="count")
                else:
                    raise PreventUpdate
                chartFigure = px.area(chart_df, x= "iyear", y ="count", color = chart_dp_value)
                fig = chartFigure
            else:
                return None
        return dcc.Graph(figure = fig)
@app.callback(
    dash.dependencies.Output('graph-object4', 'children'),
    [
    dash.dependencies.Input('Tabs','value'),
    dash.dependencies.Input('subtabs2','value'),
    dash.dependencies.Input("Chart_Dropdown1", "value"),
    dash.dependencies.Input("search1", "value"),
    dash.dependencies.Input("year-slider3", "value"),
    ]
)

def update_app_ui(Tabs_value,subtabs2,chart_dp_value1, search1,year_value):
        if Tabs_value=="Chart":
            global fig
            fig=go.Figure()
            year_range = range(year_value[0], year_value[1]+1)
            new_df = df[df["iyear"].isin(year_range)]
            if subtabs2 == "IndiaChart":
                chart_df = new_df[(new_df["region_txt"]=="South Asia") &(new_df["country_txt"]=="India")]
                if chart_dp_value1 is not None:
                    if search1 is not None: 
                        chart_df = chart_df.groupby("iyear")[chart_dp_value1].value_counts().reset_index(name = "count")
                        chart_df  = chart_df[chart_df[chart_dp_value1].str.contains(search1, case = False)]
                    else:
                        chart_df = chart_df.groupby("iyear")[chart_dp_value1].value_counts().reset_index(name="count")
                else:
                    raise PreventUpdate
                chartFigure = px.area(chart_df, x= "iyear", y ="count", color = chart_dp_value1)
                fig = chartFigure
            else:
                return None
        return dcc.Graph(figure = fig)

def main():
  load_data()
  
  open_browser()
  
  global app
  app.layout = create_app_ui()
  app.title = "Terrorism Analysis with Insights"
  # go to https://www.favicon.cc/ and download the ico file and store in assets directory 
  app.run_server() # debug=True

  print("This would be executed only after the script is closed")
  df = None
  app = None



if __name__ == '__main__':
    main()
