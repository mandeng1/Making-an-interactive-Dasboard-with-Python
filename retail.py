import dash
import dash_core_components as dcc 
import dash_html_components as html 
import plotly
import plotly.graph_objs as go 
from dash.dependencies import Input, Output
import dash_table
import pandas as pd 
import numpy as np 
import folium
import os
from operator import itemgetter
import base64

#import dataset
df=pd.read_excel("https://raw.githubusercontent.com/mandeng1/Retail_Dasboad/master/test_data.csv")
df_infos=pd.read_csv("https://raw.githubusercontent.com/mandeng1/Retail_Dasboad/master/df_infos.csv")
df_geo=pd.read_csv("https://raw.githubusercontent.com/mandeng1/Retail_Dasboad/master/df_geo.csv")
#create some data set 
#df1=df.groupby('Country')['StockCode','Customer ID'].nunique().reset_index()
#df2=df.groupby('Country')['InvoiceDate'].max().reset_index()
#df3=df.groupby('Country')['InvoiceDate'].min().reset_index()
#df4 = pd.merge(df1,df2, on='Country')
#df4.columns=['Country', 'Number of product', 'Number of Customer ', 'Last transaction']
#df5=pd.merge(df4,df3, on='Country')
#df5.columns=['Country', 'Number of products', 'Number of Customers ', 'Last transaction','First Transaction']
#dropdown
Countries = [{'label': Country, 'value' : Country} for Country in df['Country'].unique()]

app = dash.Dash(__name__)
app.layout=html.Div([
    html.Div([
        html.H4("Choose a Country"),
        dcc.Dropdown(
            id='Country-picker',
            options=Countries,
            value="France"
        )
    ],style={
        "width":'25%',
        "border":'1px solid #eee',
        "padding":'30px 30px 30px 120px',
        "box-shadow":'0 2px 2px #ccc',
        "display": 'inline-block',
        "verticalAlign":'top'

    } ),
    html.Div([
        dcc.Tabs(id='tabs',value='tab-1',children=[
            # General windows
            dcc.Tab(label="Data Overview",children=[
                html.Div([
                    html.H1("Data Overview")
                ],style={'background':'#2F0346', 'color':'white', 'textAlign':'center','padding':'10px 0px 10px 0px'}),
                html.Div([
                    dash_table.DataTable(
                        id="table-info",style_cell = {'font-family': 'Montserrat'},
                        style_data_conditional = [
                            {
                                'if' : {'column_id' : 'intitule'},
                                'textAlign' : 'left'
                            }] + [
                            {
                                'if': {'row_index' : 'odd'},
                                'backgroundColor' : 'rgb(248, 248, 248)'
                            }
                        ],
                        style_header = {
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight' : 'bold'
                        }
                    )
                ], style= {'width':'40%','border':'1px solid #eee','box-shadow':'0 2px 2px #ccc', 'display':'inline-block', 
                            'verticalAlign' : 'top', 'padding' : '60px 30px 60px 30px'}),
                html.Div(id = "map", style= {'display':'inline-block','verticalAlign':'top','width':'50%', 
                                            'padding':'15px 0px 15px 10px'}),
            ]),
            #dataviz windows
             dcc.Tab(label="Data Visualization"),
            #predictions windows
             dcc.Tab(label="Predictions"),
             dcc.Tab(label="Clustering")

        ])
    ])
])

#plot Generale informations
@app.callback([Output('table-info','data'), Output('table-info','columns')],[Input('Country-picker','value')])
def update_generales(chosen_country):
    colonnes = df_infos.columns
    colonnes_off = ['Country']
    listeInfos = [info for info in colonnes if info not in colonnes_off]
    infos = {
        'intitule': listeInfos,
        'donnee' : [df_infos[df_infos['Country'] == chosen_country][col].iloc[0] for col in listeInfos]
    }

    table = pd.DataFrame(infos)
    data = table.to_dict("rows")

    entete = {'id': 'intitule', 'name': " Informations "}, {'id': 'donnee', 'name': chosen_country}

    return data, entete

@app.callback(Output('map', 'children'), [Input('Country-picker','value')])
def update_location(chosen_country):
    longitude = df_geo[df_geo['Country'] == chosen_country]['Long'].iloc[0]
    latitude = df_geo[df_geo['Country'] == chosen_country]['Lat'].iloc[0]

    carte = folium.Map(location= (latitude, longitude), zoom_start=6)
    marker = folium.Marker(location = [latitude, longitude])
    marker.add_to(carte)

    fichier = "locations\\localisation_" + chosen_country + ".html"

    if not os.path.isfile(fichier):
        carte.save(fichier)

    return html.Iframe(srcDoc = open(fichier, 'r').read(), width='100%', height = '600')

server = app.server
if __name__ == "__main__":
    app.run_server()
