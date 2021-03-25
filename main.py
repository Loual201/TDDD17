
# Count number of requests, because of limitations from API
number_of_requests_done = 0

# Array that stores all data to be visualized
arr_vis = []

# Array that stores the step the dictionary belongs to
arr_step = []

# Insert interesing address
interesting_address = ''

# Get all the transactions for the interesting address
int_add_txs = 

# Filter transactions based on either the amout of money or the number of transactions to an address
filtered_addresses = 

# Add the first dictionary to the visualization array
# We only want to see the interesting addresses
arr_vis.append(filtered_addresses)
arr_step.append(0)

slot_index = 0
# Get all transactions for all interesting addresses, repeat for desired amout of times
while(antal_steg)
    # For every address in the dictionary, get their transactions

    # Get the number of address to look at 
    number_of_add_in_step =

    # Loop for every address (to be dict in slot in vis array) 
    while(number_of_add_in_step)
        # Get the dictionary we want to look at
        current_dict = arr_vis[slot_index]

        # Get the number of transactions in the current dictionary
        num_txs_curr_dict = len(current_dict)

        for every transaction in current_dict
            # get transactions for current address in current dictionary

            # filter transactions 

            # add to array for visualization
            arr_vis.append()
            arr_step.append(the_step_number)
        
        # Go to next slot in array, 
        slot_index = slot_index + 1

# Combine arr_vis and arr_step 
combined_arr = np.vstack((arr_vis, arr_step)).T

visualize_data(combined_arr)