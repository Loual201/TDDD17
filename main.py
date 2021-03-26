import numpy as np
from ismember import ismember
from blockcypher import get_address_full, get_address_details
from functions import get_addresses, filter_by_choice, visualization_of_data, collect_intresting_data

#Set the parameters for visulazation
address = '1MDAu9H2FiMchME58AafRwoAJLo2CbEGb9'
threshold = 10000
choice = 1
number_of_step = 2

data = collect_intresting_data(address, number_of_step, choice, threshold)

visualization_of_data(combined_arr)