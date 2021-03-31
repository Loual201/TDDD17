import numpy as np
from functions import visualization_of_data, collect_intresting_data
import pickle

#****** TO COLLECT DATA FROM A ADDRESS *******
#Set the parameters for visulazation
address = '1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW'
threshold = 0
choice = 1
number_of_step = 2

# data = collect_intresting_data(address, number_of_step, choice, threshold)


# Save data TODO: test that it works and how it looks
#       np.savetxt("data_csv.csv",data,delimiter=",")
# Store data (serialize)
# with open('data_pickle.pickle', 'wb') as handle:
#     pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Load data (deserialize)
with open('data_pickle.pickle', 'rb') as handle:
    unpacked_data = pickle.load(handle)

print(unpacked_data)
visualization_of_data(unpacked_data)