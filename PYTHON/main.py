import numpy as np
from functions import collect_intresting_data, filter_by_choice, save_to_csv
import pickle
import csv
from ismember import ismember
"""
#****** TO COLLECT DATA FROM AN ADDRESS *******
#Set the parameters for visulazation
#address = '1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW'
address = '1LaNXgq2ctDEa4fTha6PTo8sucqzieQctq'

# Request counter for hourly/daily limit
hourly_requests = 0
daily_requests = 0

# Number of steps in data retrival 
number_of_step = 4

data = collect_intresting_data(address, number_of_step, hourly_requests, daily_requests)

# Store data in pickle inorder to filter
with open('./collected_data/data_pickle.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

"""
#****** Filter the collected data ******

filter_data = 0 # 0 for no, 1 for yes

# filter parameters
threshold = 10000 #Money value or transaction threshold
choice = 1 # 1 for filter by money, 2 for filter by number of transactions

# Load data into pickle
with open('./collected_data/data_pickle.pickle', 'rb') as handle:
    unfiltered_data = pickle.load(handle)

#Save unfiltered data into data.csv
if(filter_data == 0):
    save_to_csv('./collected_data/data.csv', unfiltered_data)
    
# Filter data and save into filtered_data.csv
elif(filter_data == 1):
    removed_transactions = []
    filtered_data = []
    for data in unfiltered_data:
        if(data.get('source') not in removed_transactions):
            filt_set, removed_transactions = filter_by_choice(data, choice, threshold, removed_transactions)
            filtered_data.append(filt_set)
    
    save_to_csv('./collected_data/filtered_data.csv',  filtered_data)
