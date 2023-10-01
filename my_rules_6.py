# Phase 1:
# Read input
# Generate F1
# Create skeleton code
# Create functions to generate output files
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

def main():
    parser = argparse.ArgumentParser(description="Association Rule Generator")
    parser.add_argument("--minsup", required=True, help="minimum support count")
    parser.add_argument("--minconf", required=True, help="minimum confidence")
    parser.add_argument("--input", required=True, help="input file name")
    parser.add_argument("--output", required=True, help="output file name")

    args = parser.parse_args()

    minsup = int(args.minsup)
    minconf = float(args.minconf)
    input_file = args.input
    output_file = args.output
    
    if minconf == -1:
        print('Minconf is -1;exiting without writing file')
        exit()

    item_counts, transactions = read_input(input_file)

    # FOR TESTING - write output file 
    with open(output_file, 'w') as output:
        output.write(f"minsup: {minsup} \n")
        output.write(f"minconf: {minconf} \n")
        output.write(f"input file: {input_file} \n")
        output.write(f"output name: {output_file} \n")
        output.write(f"number of items: {len(item_counts)}\n")
        output.write(f"number of transactions: {len(transactions)}\n")
        for transaction, list in transactions.items():
             output.write(f"Transaction {transaction}: {list}\n")
        for item, count in item_counts.items():
             output.write(f"Item {item}: {count} times\n")

if __name__ == "__main__":
    main()
