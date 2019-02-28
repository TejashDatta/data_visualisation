import plotly, json
import plotly.graph_objs as go

import pandas as pd

df = pd.read_csv('data_sets/education_statewise_elementary.csv')


# text_data = []
# for index, row in df.iterrows():
#     text = ''
#     for field in list(df):
#         text += f'{field}: {row[field]}\n'
#     text_data.append(text)

# print(text_data)

try:
    too = df[df['DISTRICTS']>0]
    print('found')

except Exception:
    print('not found')