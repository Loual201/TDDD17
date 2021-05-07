import numpy as np
from functions import collect_intresting_data, filter_by_choice, save_to_csv
import pickle
import csv
from ismember import ismember
import pandas as pd

"""
#****** TO COLLECT DATA FROM AN ADDRESS *******
#Set the parameters for visulazation
#address = '1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW'
#address = 'bc1qwqdg6squsna38e46795at95yu9atm8azzmyvckulcc7kytlcckxswvvzej'
address = '1G47mSr3oANXMafVrR8UC4pzV7FEAzo3r9'

# Request counter for hourly/daily limit
hourly_requests = 0
daily_requests = 0

# Number of steps in data retrival 
number_of_step = 5

data = collect_intresting_data(address, number_of_step, hourly_requests, daily_requests)

# Store data in pickle inorder to filter
with open('./collected_data/data_pickle.pickle', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
"""

#****** Filter the collected data ******

filter_data = 1 # 0 for no, 1 for yes
number_of_step = 4
# filter parameters
threshold = 3 # Top money value or transaction threshold
choice = 0 # 0 for filter top transaction values, 1 for filter by money, 2 for filter by number of transactions

# Load data from pickle
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
        filt_set, removed_transactions = filter_by_choice(data, choice, threshold, removed_transactions)
        filtered_data.append(filt_set)

    
    save_to_csv('./collected_data/filtered_data.csv',  filtered_data)
    
    if(choice == 0):
        dataframe = pd.read_csv('./collected_data/data.csv')

        col_names =  ['source', 'target', 'value', 'count', 'step']
        final_data  = pd.DataFrame(columns = col_names)

        removed_targets =  []
        for i in range(number_of_step):
            step_order = dataframe.loc[dataframe['step'] == i]
            interesting_transactions = step_order['value'].nlargest(threshold)
            
            # Get index of top transactions
            data_top = interesting_transactions.head()
            rows_to_be_dropped = data_top.index

            # Save top transactions
            interesting_transactions = step_order.iloc[rows_to_be_dropped]

            # Remove the top transactions from step_order
            step_order = step_order.drop(labels=rows_to_be_dropped, axis=0)
            
            # Place all targets from step_order into removed_targets
            removed_targets = removed_targets + step_order['target'].to_list()

            # Change all targets in step_order from address to other
            step_order.loc[:,'target'] = 'other' + str(i)

            # Group to other
            step_order_combined  = pd.DataFrame(columns = col_names)

            # Change sources to other if it is in removed_targets
            step_order.loc[step_order['source'].isin(removed_targets), "source"] = "other" + str(i -1)
            interesting_transactions.loc[interesting_transactions['source'].isin(removed_targets), "source"] = "other" + str(i -1)

            # Combine the transactions
            step_order_combined = step_order_combined.append(step_order.groupby(['source','target']).agg({'value':'sum','count':'sum','step':'max'}).reset_index())
            all_data = pd.concat([ interesting_transactions,step_order_combined], axis=0)
            final_data = final_data.append(all_data, ignore_index = True)

        # Save data to csv
        final_data.to_csv('./collected_data/top_txs_data.csv')