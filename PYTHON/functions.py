from blockcypher import get_address_full, get_address_details
import numpy as np
from ismember import ismember
import randomcolor
import time 
import plotly.graph_objects as go
import plotly
import csv
import operator

def collect_intresting_data(address,numb_of_step, hourly_requests, daily_requests):
 
    # Array that stores all data to be visualized
    arr_vis = []

    # Array that stores the step the dictionary belongs to
    arr_step = []

    # Insert interesing address
    interesting_address = address

    # Get all the transactions for the interesting address
    [int_add_txs, hourly_requests, daily_requests] = get_addresses(interesting_address, hourly_requests, daily_requests)

    int_add_txs["step"] = 0
    # Add the first dictionary to the visualization array
    # This is the first (0) step in the money flow
    arr_vis.append(int_add_txs)
    arr_step.append(0)
    current_step = 0
    arr_index = 0
    
    # Get all transactions for all interesting addresses, repeat for desired amout of times
    while(numb_of_step > current_step): 
        # Get the number of address to look at 
        number_of_add_in_step = len(arr_vis[arr_index].get("addresses"))
        
        # Loop for every address, these will be their own dictonaries in arr_vis
        for j in range(number_of_add_in_step):
            # Get the dictionary we want to look at
            current_addresses = arr_vis[j].get("addresses")
            
            for one_address in current_addresses:
                # get transactions for current address in current dictionary
                [next_step_addresses, hourly_requests, daily_requests] = get_addresses(one_address, hourly_requests, daily_requests)

                next_step_addresses['step'] = current_step+1
                # add to array for visualization
                arr_vis.append(next_step_addresses)
                arr_step.append(current_step+1)
            #Move in array to avoid duplicates
            arr_index = arr_index + 1
        #Increment for next step
        current_step = current_step + 1

    print('You have made ', hourly_requests, ' requests this hour')
    print('You have made ', daily_requests, ' requests today')

    return arr_vis

def get_addresses(input_address, hourly_requests, daily_requests):
    arr = []
    count = []
    values = []
    morevalues = 0
    nr_txs = 0

    tx_limit = 50
    daily_limit_reached, hourly_requests = reached_limit(hourly_requests, daily_requests)

    if(not daily_limit_reached):
        address_info = get_address_full(address=input_address, txn_limit=tx_limit)
        n_tx = address_info.get('n_tx')

        hourly_requests = hourly_requests + 1
        daily_requests = daily_requests + 1
    else:
        return [dict(addresses=arr,count=count,transaction_value=values,source=input_address), hourly_requests, daily_requests]

    while(n_tx > 0 and daily_limit_reached == False):
     
        daily_limit_reached, hourly_requests = reached_limit(hourly_requests, daily_requests)

        if(not daily_limit_reached):
            n_tx = 0
            morevalues = morevalues + tx_limit
            txs = address_info.get('txs')

            for t in txs: 
                nr_txs = nr_txs + 1
                addresses = t.get('outputs')[0].get('addresses')
            
                if(addresses and addresses[0] != input_address):
                    [a, b] = ismember(addresses, arr)
                    if a:
                        count[b[0]] = count[b[0]] + 1
                        values[b[0]] = values[b[0]] + t.get('outputs')[0].get('value')
                    else:
                        arr.append(addresses[0])
                        c = 1
                        count.append(c)
                        values.append(t.get('outputs')[0].get('value'))
            
            if(address_info.get("hasMore")):
                address_info = get_address_full(address=input_address, txn_limit=tx_limit,before_bh=morevalues)
                n_tx = address_info.get('n_tx')
                
                hourly_requests = hourly_requests + 1
                daily_requests = daily_requests + 1
            
    return [dict(addresses=arr,count=count,transaction_value=values,source=input_address), hourly_requests, daily_requests] 

def reached_limit(hourly, daily):
    daily_limit_reached = False

    if(daily >= 1000): 
        daily_limit_reached = True
        print('You have reached your daily limit of requests, the program will exit and the fetched data is saved in a csv file') 
        return daily_limit_reached, hourly 
    elif(hourly >= 100 ):
        print('You have reached your hourly limit of requests, the program will pause for one hour. You have made ', daily, ' requests today')
        time.sleep(60*60*1) 
        hourly = 0
     
    return daily_limit_reached, hourly
           

def filter_by_choice(dataset, choice, threshold, removed_transactions):

    value = dataset.get("transaction_value")
    transaction = dataset.get('count')
    output = dataset.get('addresses')
    filtered_transaction = []
    filtered_value = []
    filtered_output = []
    
    #Filter to top transactions
    if choice == 0:
        other_value = 0
        other_transaction = 0
        step = dataset.get("step")
        filtered_step = []
        
        for i in range(threshold):
            if(len(value) != 0):
                index, max_val = max(enumerate(value), key=operator.itemgetter(1))
                filtered_transaction.append(transaction[index])
                filtered_output.append(output[index])
                filtered_value.append(max_val)
                del value[index]
                del output[index]
                del transaction[index]
        
        for i, val in enumerate(value):
            other_value = other_value + val
  #          print('other value: ', other_value)
            other_transaction = other_transaction + transaction[i]
            removed_transactions.append(output[i])
        if(other_value > 0):
            filtered_output.append("other" + str(step))
            filtered_step.append(step)
            filtered_transaction.append(other_transaction)
            filtered_value.append(other_value)
    #    print('filtered value: ', filtered_value)

        if(dataset.get("source") in removed_transactions):
            dataset['source'] = 'other' + str(step-1)
    
    if choice == 1:
       if(dataset.get('source') not in removed_transactions):
            # Look at total amount of transaction value
            for i, val in enumerate(value):
                
                if(val > threshold):
                    filtered_transaction.append(transaction[i])
                    filtered_output.append(output[i])
                    filtered_value.append(val)
                else:
                    removed_transactions.append(output[i])
    if choice == 2:
        if(dataset.get('source') not in removed_transactions):
            # Look at number of transaction 
            for i, tran in enumerate(transaction):
                if(tran > threshold):
                    filtered_transaction.append(tran)
                    filtered_output.append(output[i])
                    filtered_value.append(value[i])
                else:
                    removed_transactions.append(output[i])

    return dict(addresses=filtered_output,count=filtered_transaction,transaction_value=filtered_value, source= dataset.get('source'),step=dataset.get("step")), removed_transactions


def save_to_csv(filename, datasets):
    source_list = []
    with open(filename, 'w', newline='') as file:
        writer=csv.writer(file)
        writer.writerow(['source', 'target', 'value', 'count', 'step'])

        for dictionary in datasets:
            addresses_dict = dictionary.get('addresses')
            source_list.append(dictionary.get('source'))
            
            for i, address in enumerate(addresses_dict):
                if(not (address in source_list)):
                    writer.writerow([dictionary.get('source'), address, dictionary.get('transaction_value')[i], dictionary.get('count')[i], dictionary.get('step')])
