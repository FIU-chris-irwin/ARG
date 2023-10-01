import random

num_transactions = 100
num_items_per_transaction = random.randint(1,40) 

with open('small.txt', 'w') as f:

    for transaction_id in range(1, num_transactions+1):
        
        for item_id in range(num_items_per_transaction):
            
            f.write(str(transaction_id) + ' ' + str(random.randint(1,999)).zfill(3) + '\n')
        
        num_items_per_transaction = random.randint(1,40)