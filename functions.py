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
    while(address_info.get("hasMore") and morevalues < 150): #TODO:Get good programming practice here
        morevalues = morevalues + 50
        print("hasMore is : ", address_info.get("hasMore"))
        print("morevalue is : " , morevalues)
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
        address_info = get_address_full(address=input_address, txn_limit=50,before_bh=morevalues)
   
    print("this is number of transactions:", n_tx)
    print("number of transactions: ", nr_txs)
    return dict(addresses=arr,count=count,transaction_value=values) #When an address does not send any move to other addresses dict is empty