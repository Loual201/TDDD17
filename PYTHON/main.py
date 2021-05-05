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
        #print(final_data)
        removed_targets =  []
        for i in range(number_of_step):
            step_order = dataframe.loc[dataframe['step'] == i]
            step_order.to_csv('./collected_data/step_order.csv')
            interesting_transactions = step_order['value'].nlargest(threshold)
            
            # Get index of top transactions
            data_top = interesting_transactions.head()
            rows_to_be_dropped = data_top.index

            # Save top transactions
            interesting_transactions = step_order.iloc[rows_to_be_dropped]
            #print(interesting_transactions)

            # Remove the top transactions from step_order
            step_order = step_order.drop(labels=rows_to_be_dropped, axis=0)

            removed_targets = [i for i, si in enumerate(removed_targets) if np.char.startswith(si, 'other')]
            removed_targets = removed_targets + step_order['target'].to_list()
            print(removed_targets)

            step_order.loc[:,'target'] = 'other' + str(i)
            #print(removed_targets)
            # Group to other
            step_order_combined  = pd.DataFrame(columns = col_names)

            step_order.loc[step_order['source'].isin(removed_targets), "source"] = "other" + str(i -1)

        
            step_order_combined = step_order_combined.append(step_order.groupby(['source','target']).agg({'value':'sum','count':'sum','step':'max'}).reset_index())
            #print(step_order_combined)
            all_data = pd.concat([step_order_combined, interesting_transactions], axis=0)
     

            #print(all_data)
            #final_data = pd.concat([final_data,all_data ], axis = 0)
            final_data = final_data.append(all_data, ignore_index = True)
        #print(final_data)
        

        #interesting_transactions.to_csv('./collected_data/interesting_Data.csv')
        #step_order.to_csv('./collected_data/step_order2.csv')
        final_data.to_csv('./collected_data/final_data.csv')

            
        # print(step_order)
        # #duplicate_transactions = dataframe[dataframe.duplicated(['source','target'])]
        # test = dataframe.groupby(['source','target']).agg({'value':'sum','count':'sum','step':'max'})
        # #print(test)
        # test.to_csv('./collected_data/filtered_data.csv')