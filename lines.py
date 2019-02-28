import plotly
import plotly.graph_objs as go

import pandas as pd

Y_PARAM = 'hum'
TIME = 'time'
DATE = 'date'
MONTH = 'month'
YEAR = 'year'

df = pd.read_csv('data_sets/air_quality_delhi.csv')

data = []
for year in df[YEAR].unique():
    wf = df[df[YEAR] == year]
    datum = go.Scatter(
        visible=False,
        x = [f'{r[TIME]}-{r[DATE]},{r[MONTH]}' for index, r in wf.iterrows()],
        y = wf[Y_PARAM],
        line= dict(
            color = 'blue',
            width = .5
        ),
    )
    data.append(datum)

data[0]['visible'] = True

steps = []
for i in range(len(data)):
    step = dict(
        method = 'restyle',  
        label = min(df[YEAR]) + i,
        args = ['visible', [False] * len(data)],
    )
    step['args'][1][i] = True # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active = 0,
    currentvalue = {"prefix": "Year: "},
    pad = {"t": 200},
    steps = steps
)]



layout = go.Layout(
    sliders=sliders,
    title = 'Air Quality Delhi',
    xaxis = dict(
        title = 'Date and Time', 
        range = [0,len(df[df[YEAR] == min(df[YEAR])][df[MONTH] == min(df[MONTH])])],
        rangeslider=dict(
            visible = True
        ),
    ),
    yaxis = dict(
        title = Y_PARAM,
        autorange=True,
    ),
)


figure = go.Figure(layout=layout, data=data)

plotly.offline.plot(figure, validate=False, filename='graphs/lines.html')