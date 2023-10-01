import random

num_transactions = 100

with open('small.txt', 'w') as f:

  for transaction_id in range(1, num_transactions+1):

    num_items = random.randint(1, 40)
    
    for i in range(num_items):
    
      item_id = random.randint(1,999)
      f.write(f"{transaction_id} {item_id}\n")