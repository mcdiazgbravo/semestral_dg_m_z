#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from markupsafe import escape
#from jupyter_dash import JupyterDash  # pip install dash
#import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import pkg_resources
#pkg_resources.require("numpy==1.23.1")
import numpy as np
from dash.dependencies import Output, Input
from dash import no_update

import psycopg2
import textwrap
import geopandas
import warnings
import plotly.express as px
import plotly.graph_objects as go

#Conección Heroku
con = psycopg2.connect(database="d336iu9egej1ot", user="cvofatnojoxawg", password="54c370f6f702d93001ddbf870a5c5fe58868f4b021db069f258ae5b1353e1552", host="ec2-54-86-224-85.compute-1.amazonaws.com", port = "5432")
cur = con.cursor() 
print("Conexión exitosa\n\n")

#Queries
sql2="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos)"
sqlpma="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Panamá'"
sqlchiriqui="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Chiriquí'"
sqlcocle="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Coclé'"
sqlherrera="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Herrera'"
sqlls="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Los Santos'"
sqlpmaoeste="with centros as (select nombre, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select  r.nombre as nombre, pr.name_1 as provincia,r.puntos from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) AND pr.name_1='Panamá Oeste'"
sqlace = "with centros as (select clasificac, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajeaceite) select pr.name_1 as provincia, count(r.clasificac) as cantidad_centros from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) group by pr.name_1;"
sqlbat = "with centros as (select clasificac, (ST_SetSRID(ST_MakePoint(longitud, latitud), 4326)) as puntos from reciclajebaterias) select pr.name_1 as provincia, count(r.clasificac) as cantidad_centros from centros r, pan_adm1 pr where ST_Contains(pr.geom, r.puntos) group by pr.name_1;"

lugares = []

#Provincias
with warnings.catch_warnings():
  warnings.simplefilter('ignore', UserWarning)
  dft = geopandas.GeoDataFrame.from_postgis(sql2, con,geom_col='puntos')
  dftpa = geopandas.GeoDataFrame.from_postgis(sqlpma, con,geom_col='puntos')
  dftch = geopandas.GeoDataFrame.from_postgis(sqlchiriqui, con,geom_col='puntos')
  dftc = geopandas.GeoDataFrame.from_postgis(sqlcocle, con,geom_col='puntos')
  dfth = geopandas.GeoDataFrame.from_postgis(sqlherrera, con,geom_col='puntos')
  dftls = geopandas.GeoDataFrame.from_postgis(sqlls, con,geom_col='puntos')
  dftpo = geopandas.GeoDataFrame.from_postgis(sqlpmaoeste, con,geom_col='puntos')

#Aceite y Baterias
dftace = pd.read_sql(sqlace, con)
dftbat = pd.read_sql(sqlbat, con)

#Graficas iniciales
fig= px.scatter_geo(dft, lat = dft.geometry.y, lon = dft.geometry.x, color="provincia", size_max=1, hover_name="provincia",title="Centros de Reciclaje de Baterías por Provincia") #Todas las provincias
fig.update_layout(geo=dict(projection_scale=50, center=dict(lat=8.5, lon=-81)))

fig2 = px.bar(dftace, x="provincia", y="cantidad_centros") #Aceite

#DASH
app = dash.Dash(__name__, prevent_initial_callbacks=True, external_stylesheets=[dbc.themes.MORPH])
app.title = "Centros de reciclaje de aceite y baterías en Panamá"

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

#HTML
app.layout = html.Div([
    html.Div(
            children=[
                html.H1(
                    children="Centros de reciclaje de aceite y baterías en Panamá", className="header-title"
                ), 
                html.P(
                    children="El presente dashboard tiene como objetivo servir de herramienta a los ciudadanos para informarse sobre lugares que aceptan y reciclan aceite de cocina y baterías ya que estos son materiales que no son recolectados en los centros de acopio comunes, sin embargo requieren un proceso de disposición especial.",
                    className="header-description",
                ),
            ], style={'padding-top' : 70,   'height': 230, 'color': 'white', 'text-align': 'center', 'background-color':'#78C2AD'},
            className="header",
        ),                       
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Div(children="Provincia", className="menu-title"),
                        dcc.Dropdown( 
                            id="por-prov",
                                     options =[
                                               {"label": "Todas las provincias", "value": "todo"},
                                               {"label": "Panamá", "value": "panama" },
                                               {"label": "Chirquí", "value":  "chiriqui"},
                                               {"label": "Coclé", "value":  "cocle"},
                                               {"label": "Herrera", "value":  "herrera"},
                                               {"label": "Los Santos", "value":  "losantos"},
                                               {"label": "Panamá Oeste", "value":  "panamao"},
                                               ],
                                    multi = False,
                                    value="todo",
                                  ),
                      ],
                ),
                dbc.Col([
                        html.Div(children="Tipo", className="menu-title"),
                        dcc.Dropdown(
                            id="por-rec",
                                     options =[
                                               {"label": "Aceite", "value": "ace"},
                                               {"label": "Batería", "value": "bat" },
                                               ],
                                    multi = False,
                                    value="ace",                            
                        ),
                ],),
            ], align='center', 
            
            ), 
            html.Br(),
            dbc.Row([
                dbc.Col([
                  html.Div(
                          html.Div(
                              dcc.Graph(
                                  id="my-graph", figure = fig
                              ),
                          ),
                  ),
                ],),
                dbc.Col([
                  html.Div(
                          html.Div(
                              dcc.Graph(
                                  id="my-graph2", figure = fig2
                              ),
                          ),
                  ),                    
                ],),
            ], align='center'), 
            html.Br(),     
        ]), 
    )
])


@app.callback(
     Output(component_id="my-graph",component_property="figure"),
     Output(component_id="my-graph2", component_property="figure"),
     Input(component_id="por-prov", component_property= "value"),
     Input(component_id="por-rec", component_property="value"),
)

def display_choropleth(por_prov, por_rec):

  #Provincias
  if por_prov == "todo":
    fig= px.scatter_geo(dft, lat = dft.geometry.y, lon = dft.geometry.x, color="provincia", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías por Provincia")
    fig.update_layout(geo=dict(projection_scale=50, center=dict(lat=8.5, lon=-81)))

  if por_prov == "panama":
    fig= px.scatter_geo(dftpa, lat = dftpa.geometry.y, lon = dftpa.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Panamá")

  if por_prov == "chiriqui":
    fig= px.scatter_geo(dftch, lat = dftch.geometry.y, lon = dftch.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Chiriquí")

  if por_prov == "cocle":
    fig= px.scatter_geo(dftc, lat = dftc.geometry.y, lon = dftc.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Coclé")

  if por_prov == "herrera":
    fig= px.scatter_geo(dfth, lat = dfth.geometry.y, lon = dfth.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Herrera")

  if por_prov == "losantos":
    fig= px.scatter_geo(dftls, lat = dftls.geometry.y, lon = dftls.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Los Santos")

  if por_prov == "panamao":
    fig= px.scatter_geo(dftpo, lat = dftpo.geometry.y, lon = dftpo.geometry.x, color="nombre", size_max=1, hover_name="nombre",title="Centros de Reciclaje de Baterías en Panamá Oeste")

  #Aceite y Bateria
  if por_rec == "ace":
    fig2 = px.bar(dftace, x="provincia", y="cantidad_centros")
  if por_rec == "bat":
    fig2 = px.bar(dftbat, x="provincia", y="cantidad_centros")

  fig.update_layout(geo=dict(projection_scale=50, center=dict(lat=8.5, lon=-81)))

  return fig, fig2
  
print("Cerrando conexión")
con.close()


if __name__ == '__main__':
    app.run(debug=True)
