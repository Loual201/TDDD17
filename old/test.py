from blockchain import blockexplorer
import numpy as np
# block = blockexplorer.get_block('000000000000000016f9a2c3e0f4c1245ff24856a79c34806969f5084f410680')
# transactions = block.transactions

# print(np.shape(transactions))
# print(transactions[0].inputs[0])

address = blockexplorer.get_address('1C1Ford5HUusymXqEQMY3TdWQtyZtsMZAW')
transactions = address.transactions

for t in transactions:
    inputs = t.outputs
    for i in inputs:
        print(i.value)

