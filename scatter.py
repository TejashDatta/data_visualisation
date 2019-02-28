import plotly, json
import plotly.graph_objs as go

import pandas as pd

BUBBLE_SIZE = 35
LAT_PARAM = 'Lat'
LONG_PARAM = 'Long'
COLOR_PARAM = 'Overall_Literacy'
SIZE_PARAM = 'Area_Sqkm'

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidW5jaGFydGVkbWFwcGVyIiwiYSI6ImNqc2plamlmbjFmYnUzeXFndjcwdTk3ZWYifQ.PV4-cwpuY1PQ2u0HfI8GPg'

df = pd.read_csv('data_sets/education_districtwise.csv')
scl = [ [0,"rgb(123, 173, 252)"], [1,"rgb(0, 33, 86)"] ]

text_data = []
for index, row in df.iterrows():
    text = ''
    for field in list(df):
        if field not in {LAT_PARAM, LONG_PARAM}:
            text += f"{str(field).replace('_',' ')}: {row[field]}<br>"
    text_data.append(text)

data = [go.Scattermapbox(
        lat = df[LAT_PARAM],
        lon = df[LONG_PARAM],
        mode='markers',
        marker = dict(

            size = df[SIZE_PARAM],
            sizeref = 2. * max(df[SIZE_PARAM]) / (BUBBLE_SIZE ** 2),
            sizemode = 'area',
            opacity = 0.8,

            reversescale = False,

            colorscale = scl,
            cmin = df[COLOR_PARAM].min(),
            color = df[COLOR_PARAM],
            cmax = df[COLOR_PARAM].max(),
            colorbar=dict(
                title=COLOR_PARAM
            )
        ),
        hoverinfo='text',
        text = text_data,
    )]

with open('./resources/india_district.geojson') as f:
    state_data = json.load(f)

layout = go.Layout(
    # autosize=True,
    hovermode='closest',
    title = 'Education in India',
    mapbox=dict(
        accesstoken=MAPBOX_ACCESS_TOKEN,
        layers = [dict(
                    sourcetype = 'geojson',
                    source = state_data,
                    type = 'line',
                    opacity = 0.5,
                    color = 'rgb(128,128,128)',
                    line = {'width': .5},
                )
            ],
        bearing=0,
        center=dict(
            lat=22.000046, 
            lon=78.615276
        ),
        pitch=0,
        zoom=3.5
    ),
)


figure = go.Figure(layout=layout, data=data)

plotly.offline.plot(figure, validate=False, filename='graphs/scatter.html')