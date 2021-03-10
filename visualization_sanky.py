import plotly.graph_objects as go
import numpy as np
import pickle
from functions import filter_by_choice



with open('first_address.pickle', 'rb') as handle:
    first= pickle.load(handle)

with open('second_address.pickle', 'rb') as handle:
    second= pickle.load(handle)

with open('third_address.pickle', 'rb') as handle:
    third= pickle.load(handle)

dataset = second

# #Filtered by money
filt_by_money = filter_by_choice(dataset,1,100000)
output = filt_by_money.get('addresses')
value = filt_by_money.get('transaction_value')
color =filt_by_money.get('color')

#Filtered by transactions
# filt_by_transaction = filter_by_choice(first,2,1)
# output = filt_by_transaction.get('addresses')
# value = filt_by_transaction.get('transaction_value')
# color =filt_by_transaction.get('color')


#source = first.get('source') TODO
source = dataset.get('source')
source_arr = np.zeros(len(output))
target_arr = np.arange(1,len(output)+1,1)
output.insert(0,source)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = output,
      color = "blue"
    ),
    link = dict(
      source = source_arr, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = target_arr, 
      value = value,
      color = color
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()