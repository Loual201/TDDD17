import numpy as np
from ismember import ismember
from blockcypher import get_address_full, get_address_details
from functions import get_addresses
import pickle

# First address 
add_dict = get_addresses('1MDAu9H2FiMchME58AafRwoAJLo2CbEGb9')

# loopas
int_txs = filter_interesting_txs(add_dict)

second_step_add = get_addresses()




# address_info = get_address_full(address='1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW', txn_limit=50)

# Store data (serialize)
with open('third_address.pickle', 'wb') as handle:
    pickle.dump(add_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Load data (deserialize)
with open('third_address.pickle', 'rb') as handle:
    unserialized_data = pickle.load(handle)

print(add_dict == unserialized_data)

# txs = address_info.get('txs')
# n_tx = address_info.get('n_tx')
# print(np.shape(txs))

# # Times sent to address (output)
# arr = []
# count = []
# values = []
# for t in txs:
#     addresses = t.get('outputs')[0].get('addresses')

#     [a, b] = ismember(addresses, arr)
#     if a:
#         count[b[0]] = count[b[0]] + 1
#         values[b[0]] = values[b[0]] + t.get('outputs')[0].get('value')
#     else:
#         arr.append(addresses[0])
#         c = 1
#         count.append(c)
#         values.append(t.get('outputs')[0].get('value'))


# print('Number of transactions: ' )
# print(n_tx)

# val = dict(addresses=arr,count=count,transaction_value=values)
# add = val.get('addresses')
# print(add)


   




