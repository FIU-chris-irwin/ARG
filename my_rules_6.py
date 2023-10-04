# Phase 1:
# Read input - done 
# Generate - done
# Create skeleton code
# Create functions to generate output files - done
# Write code needed for plots
# Initial Report & Current Draft

import argparse

def read_input(input_file):
    """
    takes a text file that contains transaction IDs and item numbers in the transaction and returns 
    a dictionary with item numbers as keys and their support counts as the value
    """
 
    # hash table for item counts
    item_counts = {}
    
    # hash table for transactions
    transactions = {}

    with open(input_file, 'r') as file:
        for line in file:
            # split into list of that contains [transaction ID, item number]
            transaction_datum = line.split()
            transaction_id, item_number = map(int, transaction_datum)
            # update item count hash table
            if item_number in item_counts:
                item_counts[item_number] += 1
            else:
                item_counts[item_number] = 1
            # update transaction hash table
            if transaction_id in transactions:
                transactions[transaction_id].append(item_number)
            else:
                transactions[transaction_id] = [item_number]
    
    return item_counts, transactions

def generate_f1(item_counts, minsup):
    """
    takes a dictionary of items with support counts, and a minimum support count;  returns a sorted dictionary of items that meet minsup 
    """
    f1_items = {}
    for item, count in item_counts.items():
        if count >= minsup:
            f1_items[item] = count
    
    return dict(sorted(f1_items.items()))

def write_output(f1_items, minsup, minconf, input_file, output, item_counts, transactions):
    """
    writes three different output files that describe various aspects of the association rules
    """
    f1_items, minsup, minconf, input_file, output, item_counts, transactions = f1_items, minsup, minconf, input_file, output, item_counts, transactions
    
    # write {output}_items_6.txt
    with open(f'{output}_items_6.txt', 'w') as items:
        for itemset, count in f1_items.items():
            items.write(f'item{itemset}|{count}\n')
    
    # write {output}_rules_6.txt
    if minconf != -1:
        with open(f'{output}_rules_6.txt', 'w') as rules:
            rules.write('Dummy text. Will contain LHS|RHS|SUPPORT|CONFIDENCE\n')

    # write {output}_info_6.txt
    
    with open(f'{output}_info_6.txt', 'w') as info:
        info.write(f"minsup: {minsup} \n")
        info.write(f"minconf: {minconf} \n")
        info.write(f"input file: {input_file} \n")
        info.write(f"output name: {output} \n")
        info.write(f"number of items: {len(item_counts)}\n")
        info.write(f"number of transactions: {len(transactions)}\n")
        for transaction, list in transactions.items():
             info.write(f"Transaction {transaction}: {list}\n")
        for item, count in item_counts.items():
             info.write(f"Item {item}: {count} times\n")
    

def main():
    # Get the arguments from terminal and assign to variables
    parser = argparse.ArgumentParser(description="Association Rule Generator")
    parser.add_argument("--minsup", required=True, help="minimum support count")
    parser.add_argument("--minconf", required=True, help="minimum confidence")
    parser.add_argument("--input", required=True, help="input file name")
    parser.add_argument("--output", required=True, help="output file name")

    args = parser.parse_args()

    minsup = int(args.minsup)
    minconf = float(args.minconf)
    input_file = args.input
    output= args.output
    
    # Do not generate rules when minconf = -1
    if minconf == -1:
        print('Minconf is -1;exiting without writing file')
        exit()

    item_counts, transactions = read_input(input_file)

    f1_items = generate_f1(item_counts, minsup)

    write_output(f1_items, minsup, minconf, input_file, output, item_counts, transactions)

if __name__ == "__main__":
    main()
