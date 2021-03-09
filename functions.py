from blockcypher import get_address_full, get_address_details
import numpy as np
from ismember import ismember

def get_addresses(input_address):
    address_info = get_address_full(address=input_address, txn_limit=50)
    arr = []
    count = []
    values = []
    morevalues = 0
    nr_txs = 0
    n_tx = address_info.get('n_tx')
    while(morevalues < 150): #address_info.get("hasMore")): #TODO:Get good programming practice here
        address_info = get_address_full(address=input_address, txn_limit=50,after_bh=morevalues)
        morevalues = morevalues + 50
        print(address_info.get("hasMore"))
        txs = address_info.get('txs')

        # Times sent to address (output)
        for t in txs:
            nr_txs = nr_txs + 1
            addresses = t.get('outputs')[0].get('addresses')

            [a, b] = ismember(addresses, arr)
            if a:
                count[b[0]] = count[b[0]] + 1
                values[b[0]] = values[b[0]] + t.get('outputs')[0].get('value')
            else:
                arr.append(addresses[0])
                c = 1
                count.append(c)
                values.append(t.get('outputs')[0].get('value'))
    
   
    print("this is number of transactions:", n_tx)
    print(nr_txs)
    return 0