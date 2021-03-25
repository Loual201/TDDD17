import plotly.graph_objects as go
import plotly
import numpy as np
import pickle
from functions import filter_by_choice
from ismember import ismember

with open('first_address.pickle', 'rb') as handle:
    first= pickle.load(handle)

with open('second_address.pickle', 'rb') as handle:
    second= pickle.load(handle)

with open('third_address.pickle', 'rb') as handle:
    third= pickle.load(handle)

datasets = [first, second, third]
output = []
value = []
color = []
source_arr = []
target_arr = []
first_loop = True
for dataset in datasets:

  # #Filtered by money
  filt_by_money = filter_by_choice(dataset,1,100000)
  source = dataset.get('source') 
  output_dataset = filt_by_money.get('addresses')
  value_dataset = filt_by_money.get('transaction_value')
  color_dataset = filt_by_money.get('color')

  if(first_loop):
    output = output + [source]
    first_loop = False

  [member, index] = ismember(output_dataset, source)
  print('member: ', member, 'index: ', index)
  for i, m in enumerate(member):
    if m:
      del output_dataset[i]
      del value_dataset[i]
      del color_dataset[i]

  output = output + output_dataset
  value = value + value_dataset
  color = color + color_dataset


  #Filtered by transactions
  # filt_by_transaction = filter_by_choice(first,2,1)
  # output = filt_by_transaction.get('addresses')
  # value = filt_by_transaction.get('transaction_value')
  # color =filt_by_transaction.get('color')


  index = output.index(source)
 # skapa array med source index från output array, ett index ska repeteras lika många gånger som det finns transaktioner från en address
  source_arr = source_arr + [index]*len(output_dataset)
  target_arr = np.arange(1,len(output)+1,1)
#  output.insert(0,source)


fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = output,
      color = color
    ),
    link = dict(
      source = source_arr, # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = target_arr, 
      value = value,
      color = 'gray',
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
plotly.offline.plot(fig)