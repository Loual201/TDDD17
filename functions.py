from blockcypher import get_address_full, get_address_details
import numpy as np
from ismember import ismember
import randomcolor
import time 
import plotly.graph_objects as go
import plotly

# Count number of requests, because of limitations from API
global number_of_requests_done

def collect_intresting_data(address,numb_of_step, filter_choice, threshold):
    # Initilze to zero
    global number_of_requests_done
    number_of_requests_done = 0

    # Array that stores all data to be visualized
    arr_vis = []

    # Array that stores the step the dictionary belongs to
    arr_step = []

    # Insert interesing address
    interesting_address = address

    # Get all the transactions for the interesting address
    int_add_txs = get_addresses(interesting_address)

    # Filter transactions based on either the amout of money or the number of transactions to an address
    filtered_addresses = filter_by_choice(int_add_txs,filter_choice, threshold)

    # Add the first dictionary to the visualization array
    # We only want to see the interesting addresses
    arr_vis.append(filtered_addresses)
    # This is the first (0) step in the money flow
    arr_step.append(0)
    current_step = 0
    arr_index = 0
    # Get all transactions for all interesting addresses, repeat for desired amout of times
    while(numb_of_step > current_step): #TODO: THIS IS MESSED UP
        # For every address in the dictionary, get their transactions

        # Get the number of address to look at 
        number_of_add_in_step = len(arr_vis[arr_index].get("addresses"))
      #  print("this is arr_vis ", arr_vis)
        # Loop for every address (to be dict in slot in vis array) 
        for j in range(number_of_add_in_step):
            # Get the dictionary we want to look at
            current_addresses = arr_vis[j].get("addresses")
            
            # Get the number of transactions in the current dictionary
            #num_txs_curr_dict = len(current_addresses)
          #  print("this is the current address ", current_addresses)
            for one_address in current_addresses:
             #   print("in loop, one_addresss is ", one_address)
                # get transactions for current address in current dictionary
                next_step_addresses = get_addresses(one_address)
                # filter transactions 
                filtered_addresses = filter_by_choice(next_step_addresses,filter_choice, threshold)

                # add to array for visualization
                arr_vis.append(filtered_addresses)
                arr_step.append(current_step+1)
            #Move in array to avoid duplicates
            arr_index = arr_index + 1
        #Increment for next step
        current_step = current_step + 1

    # Combine arr_vis and arr_step 
    combined_arr = np.vstack((arr_vis, arr_step))
    return combined_arr

def get_addresses(input_address):
    #TODO: Remove input address from output addresses
    address_info = get_address_full(address=input_address, txn_limit=5)
    global number_of_requests_done
    number_of_requests_done = number_of_requests_done + 5
    arr = []
    count = []
    values = []
    morevalues = 0
    nr_txs = 0
    n_tx = address_info.get('n_tx')
    test = True
    while(address_info.get("hasMore") and test): #TODO:Get good programming practice here
        test = False
        if(number_of_requests_done <200): # this is for one hour limit, need one day limit too
            morevalues = morevalues + 5
            #print("hasMore is : ", address_info.get("hasMore"))
            #print("morevalue is : " , morevalues)
            txs = address_info.get('txs')
            # Times sent to address (output)
            for t in txs: 
       
                nr_txs = nr_txs + 1
                addresses = t.get('outputs')[0].get('addresses')
                print('addresses: ', addresses[0])
                print('input address: ', input_address)

                if(addresses[0] != input_address): #This probably works, but if too many empty arr = [], here is the problem
                    [a, b] = ismember(addresses, arr)
                    print('arr: ', arr)
                    print('a: ', a, ' b: ', b)
                    if a:
                        count[b[0]] = count[b[0]] + 1
                        values[b[0]] = values[b[0]] + t.get('outputs')[0].get('value')
                    else:
                        arr.append(addresses[0])
                        c = 1
                        count.append(c)
                        values.append(t.get('outputs')[0].get('value'))

            address_info = get_address_full(address=input_address, txn_limit=5,before_bh=morevalues)
            number_of_requests_done = number_of_requests_done + 5
        else:
            time.sleep(60*60*1) 
   
    #print("this is number of transactions:", n_tx)
    #print("number of transactions: ", nr_txs)
    
    return dict(addresses=arr,count=count,transaction_value=values,source=input_address) #When an address does not send any move to other addresses dict is empty


def filter_by_choice(dataset, choice, threshold):
    value = dataset.get("transaction_value")
    transaction = dataset.get('count')
    output = dataset.get('addresses')
    filtered_transaction = []
    filtered_value = []
    filtered_output = []
    color = []
    if choice == 1:
        # Look at total amount of transaction value
        for i, val in enumerate(value):
            if(val > threshold):
                filtered_transaction.append(transaction[i])
                filtered_output.append(output[i])
                filtered_value.append(val)
                rand_color = randomcolor.RandomColor()
                col = rand_color.generate()
                color.append(col[0])
    if choice == 2:
        # Look at number of transaction 
        for i, tran in enumerate(transaction):
            if(tran > threshold):
                filtered_transaction.append(tran)
                filtered_output.append(output[i])
                filtered_value.append(value[i])
                rand_color = randomcolor.RandomColor()
                col = rand_color.generate()
                color.append(col[0])

        
    return dict(addresses=filtered_output,count=filtered_transaction,transaction_value=filtered_value, color=color, source= dataset.get('source'))

def visualization_of_data(arr_data):
    #Split the data again
    [datasets, step_order] = np.vsplit(arr_data,2) #TODO: Do we need step_order
    output = []
    value = []
    color = []
    source_arr = []
    target_arr = []
    first_loop = True
    #print("this is the dataset ", datasets)
    for i, dataset in enumerate(datasets):
        #print(dataset[i])
        source = dataset[0].get('source')
        #print("this is the source" , source)
        output_dataset = dataset[0].get('addresses')
        #print("this is the ouput add ", output_dataset)
        value_dataset = dataset[0].get('transaction_value')
        color_dataset = dataset[0].get('color')
        if(first_loop):
            output = output + [source]
            first_loop = False

        [member, index] = ismember(output_dataset, source)
        #print('member: ', member, 'index: ', index)
        for i, m in enumerate(member):
            if m:
                del output_dataset[i]
                del value_dataset[i]
                del color_dataset[i]

        output = output + output_dataset
        value = value + value_dataset
        color = color + color_dataset

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