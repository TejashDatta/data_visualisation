import plotly, json
import plotly.graph_objs as go
import pandas as pd

FILENAME = 'data_sets/statewise_elementary.csv'
STATE_NAME_FIELD = 'STATNAME'
COLORING_FIELD = 'OVERALL_LI'
COLOR_MIN = (123, 173, 252)
COLOR_MAX = (0, 33, 86)


df = pd.read_csv(FILENAME)

with open('./resources/states.geojson') as f:
    state_data = json.load(f)

MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoidW5jaGFydGVkbWFwcGVyIiwiYSI6ImNqc2plamlmbjFmYnUzeXFndjcwdTk3ZWYifQ.PV4-cwpuY1PQ2u0HfI8GPg'


state_layers = []


#creating dict used for json of each state

state_jsons = {}
max_cd = max(df[COLORING_FIELD])
min_cd = min(df[COLORING_FIELD])
color_difference = tuple(COLOR_MIN[i] - COLOR_MAX[i] for i in range(3))

for state in state_data['features']:
    state_json_template = {
    "type": "FeatureCollection",
    "features": []
    }
    state_json_template['features'] = [state]
    state_name = state['properties']['NAME_1']
    state_jsons[state_name]=state_json_template
    found = 0
    for state_index, csv_state in enumerate(df[STATE_NAME_FIELD]):
        if state_name.lower() == csv_state.replace('&', 'and').lower():
            found = 1
            break
    if found:
        coloring_data = df[COLORING_FIELD][state_index]
        color = tuple(COLOR_MAX[i] + (max_cd - coloring_data) / (max_cd - min_cd) * color_difference[i] for  i in range(3))
        state_layer = dict(
                    sourcetype = 'geojson',
                    source = state_json_template,
                    type = 'fill',
                    color = 'rgb' + str(color)
                )
        state_layers.append(state_layer)
    

scl = [ [0,'rgb' + str(COLOR_MIN)], [1,'rgb' + str(COLOR_MAX)] ]

data = [
    go.Scattermapbox(
        lat=['45.5017'],
        lon=['-73.5673'],
        mode='markers',
        marker = dict(
            color = [min_cd],
            colorscale = scl,
            cmin = min_cd,
            cmax = max_cd,
            colorbar=dict(
                    title=COLORING_FIELD
                )
        )
    )
]

layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        layers = state_layers,
        accesstoken=MAPBOX_ACCESS_TOKEN,
        bearing=0,
        center=dict(
            lat=22.000046, 
            lon=78.615276
        ),
        pitch=0,
        zoom=3.5,
    ),
)

figure = dict(data=data, layout=layout)

plotly.offline.plot(figure, validate=True, filename='graphs/chloropleth.html')
