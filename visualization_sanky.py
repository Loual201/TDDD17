import plotly.graph_objects as go
import numpy as np
import pickle

with open('first_address.pickle', 'rb') as handle:
    first= pickle.load(handle)

with open('second_address.pickle', 'rb') as handle:
    second= pickle.load(handle)

with open('third_address.pickle', 'rb') as handle:
    third= pickle.load(handle)

f_len = first.get('addresses')
f_zero = np.zeros(len(f_len))

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = first.get('addresses'),
      color = "blue"
    ),
    link = dict(
      source = f_zero, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = first.get('addresses'),
      value = first.get("transaction_value")
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()