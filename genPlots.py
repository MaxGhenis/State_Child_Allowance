import datetime
import numpy as np
import pandas as pd

import plotly.graph_objects as go
import plotly.express as px

from ipywidgets import widgets

# data
raw_data = pd.read_csv('stateCAsummary.csv')
state_names = raw_data['state'].unique()
state_names.sort()
age_groups = raw_data['age_group'].unique()
x = raw_data['ca_monthly'].unique()

data_list = []
for state in state_names:
  state_list = []
  state_data = raw_data[raw_data['state']==state]
  for age in age_groups:
    state_list.append(state_data[state_data['age_group']==age]['poverty_rate'])
  data_list.append(state_list)

data = pd.DataFrame(data_list, columns = age_groups)
data['State'] = state_names
data = data.set_index('State')

# plotly setup]
fig = go.Figure()

# Add one ore more traces
legend_names = {'child': 'Child',
                'adult': 'Adult',
                'all': 'Overall'}
default = state_names[0]
for age in age_groups:
  fig.add_trace(go.Scatter(
      x=x, 
      y=data[age][default],
      name=legend_names[age]
))

buttons = []
for state in state_names:
  new_button = {'method': 'update',
                'label': state,
                'args': [{'y': data.loc[state]},]}
  buttons.append(new_button)

# construct menus
updatemenus = [{'buttons': buttons,
                'direction': 'down',
                'showactive': True,}]

# update layout with buttons, and show the figure
fig.update_layout(updatemenus=updatemenus)

fig.update_layout(
    title="Povery Impact of a Child Allowance by State",
    xaxis_title="Monthly Child Allowance Amount ($)",
    yaxis_title="Poverty Rate (%)",
    legend_title="Poverty Rates",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    )
)

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99
))

fig.write_html("html_plotly.html", full_html = False)

html_template = """
<html>
  <head>
    <title>UBI Poverty Line Explorer</title>
  </head>
  <body>
    <h1>Poverty Impact of a Child Allowance</h1>
    <p>Welcome to the UBI Poverty Line Explorer</p>
    <p>Created by the UBI Center</p>
    <p>Other stuff goes here!</p>
    {plot}
  </body>
</html>
"""

with open('html_plotly.html', 'r') as file:
    plot = file.read()
rendered_template = html_template.format(plot=plot)
with open('output.html', 'w') as fp:
    fp.write(rendered_template)









