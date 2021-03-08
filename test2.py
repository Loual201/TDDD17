
from blockcypher import get_address_full, get_address_details
import json

address_info = get_address_full(address='1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW')

txs = address_info.get('txs')

for one_tx in txs:
    print('---------- New transaction --------')
    print('This is inputs: ')
    print(one_tx.get('inputs')[0].get('addresses'))
    print('This is outputs: ')
    print(one_tx.get('outputs')[0].get('addresses'))
    print('Output value: ')
    print(one_tx.get('outputs')[0].get('value')/10000000)




