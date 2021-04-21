import numpy as np
from functions import visualization_of_data, collect_intresting_data, filter_by_choice
import pickle
import csv
from ismember import ismember

#****** TO COLLECT DATA FROM A ADDRESS *******
#Set the parameters for visulazation
address = '1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW'

filter_data = 0 # 0 for no, 1 for yes

# filter parameters
threshold = 0
choice = 1 # 1 for filter by money, 2 for filter by number of transactions
number_of_step = 2

# Request counter for hourly/daily limit
hourly_requests = 0
daily_requests = 0

data = collect_intresting_data(address, number_of_step, choice, threshold, hourly_requests, daily_requests)

# Store data in pickle inorder to filter
with open('data_pickle.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

source_list = []
if(filter_data == 0):
    # Save data TODO: test that it works and how it looks
    with open('data.csv', 'w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['source', 'target', 'value'])

        for dictionary in data:
            addresses_dict = dictionary.get('addresses')
            value = dictionary.get('transaction_value')
            # print('Addresses_dict ', addresses_dict)
            # print('value ', value)
            # print('source ', dictionary.get('source'))
            source_list.append(dictionary.get('source'))
            for i, address in enumerate(addresses_dict):
                [a,b] = ismember(address, source_list)
                if(not a):
                    writer.writerow([dictionary.get('source'), address, dictionary.get('transaction_value')[i]])

elif(filter_data == 1):
    # Load data (deserialize)
    with open('data_pickle.pickle', 'rb') as handle:
        unpacked_data = pickle.load(handle)

    filtered_data = filter_by_choice(unpacked_data, choice, threshold)
    # Save data TODO: test that it works and how it looks
    with open('filtered_data.csv', 'w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['source', 'target', 'value'])

        for dictionary in data:
            addresses_dict = dictionary.get('addresses')
            value = dictionary.get('transaction_value')
            # print('Addresses_dict ', addresses_dict)
            # print('value ', value)
            # print('source ', dictionary.get('source'))

            for i, address in enumerate(addresses_dict):
                [a,b] = ismember(address, source_list)
                if(not a):
                    writer.writerow([dictionary.get('source'), address, dictionary.get('transaction_value')[i]])
