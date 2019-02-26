import plotly
import plotly.graph_objs as go

import pandas as pd

BUBBLE_SIZE = 35

df = pd.read_csv('data_sets/edu.csv')
scl = [ [0,"rgb(247, 195, 140)"], [1,"rgb(237, 122, 0)"] ]

data = [go.Scattermapbox(
        # type = 'scattergeo',
        # locationmode = 'country names',
        lon = df['LONG'],
        lat = df['LAT'],
        mode='markers',
        marker = dict(

            size = df['AREA_SQKM'],
            sizeref = 2. * max(df['AREA_SQKM']) / (BUBBLE_SIZE ** 2),
            sizemode = 'area',
            opacity = 0.8,

            reversescale = False,

            colorscale = scl,
            cmin = df['OVERALL_LIT'].min(),
            color = df['OVERALL_LIT'],
            cmax = df['OVERALL_LIT'].max(),
            colorbar=dict(
                title="Item"
            )
        )
    )]

layout = go.Layout(
    # autosize=True,
    hovermode='closest',
    title = 'Education in India',
    mapbox=dict(
        accesstoken=MAPBOX_ACCESS_TOKEN,
        bearing=0,
        center=dict(
            lat = (min(df['LAT']) + max(df['LAT']))/2,
            lon = (min(df['LONG']) + max(df['LONG']))/2
        ),
        pitch=0,
        zoom=3.5
    ),
)


figure = go.Figure(layout=layout, data=data)

plotly.offline.plot(figure, validate=False, filename='graphs/scatter.html')