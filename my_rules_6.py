# Phase 1:
# Read input - done 
# Generate - done
# Create skeleton code
# Create functions to generate output files - done
# Write code needed for plots
# Initial Report & Current Draft

import argparse
import matplotlib.pyplot as plt

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
    NOTE: This function is deprecated. Use generate_itemsets() instead
    takes a dictionary of items with support counts, and a minimum support count;  returns a sorted dictionary of items that meet minsup 
    """
    
    
    f1_items = {}
    for item, count in item_counts.items():
        if count >= minsup:
            f1_items[item] = count
    
    return dict(sorted(f1_items.items()))\
    

def generate_itemsets(item_counts, minsup, transactions, output):
    """
    Takes the item counts and minsup as a paramter and generates candidate itemsets using the k-1 x k-1 method
    """

    def generate_1_itemsets(item_counts, minsup):
        # create F to hold the itemsets. The key will be k and the value will be a dictionary that holds the k-itemset
        F = {}

        # 1-itemset is the base case and is generated through comparison between support count and minsup
        f1_items = {}

        for item, count in item_counts.items():
            if count >= minsup:
                f1_items[(item)] = count
        
        # sort the dictionary and add to F at F[1]
        f1_items = dict(sorted(f1_items.items()))
        F[1] = f1_items
        return F


    def generate_2_itemsets(frequent_items):
        
        two_item_candidates = {}

        for item_1 in F[1].keys():
            for item_2 in F[1].keys():
                #prevent backtracking in combining items to generate candidates
                if item_1 < item_2:
                    key = (int(item_1), int(item_2))

                    two_item_candidates[key] = 0
    
        F[2] = two_item_candidates
        return(F)
    
    def prune_candidates(candidate, k):
        pass
    
    def generate_candidate_itemsets(k_minus_1_itemset):
        k = len(list(k_minus_1_itemset.keys())[0]) + 1 if k_minus_1_itemset else 2
        candidates = {}

        items = sorted(k_minus_1_itemset.keys())
        
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                # Check if the first k-2 items are the same
                if items[i][:k-2] == items[j][:k-2] and items[i][k-2] < items[j][k-2]:
                    candidate = items[i] + (items[j][k-2],)
                    candidates[candidate] = 0
        return candidates
    

    def support_count(itemsets, transactions):
        # creates dictionary with support count and eliminates candidates under minsup
        support_counts = {}
        for itemset in itemsets:
            count = 0
            for transaction in transactions.values():
                if all(item in transaction for item in itemset):
                    count += 1

            if count >= minsup:
                support_counts[itemset] = count
        return support_counts

    yval_items = []

    F = generate_1_itemsets(item_counts, minsup)
    generate_2_itemsets(F)
    F[2] = support_count(F[2],transactions)
    k_count = 3
    F[k_count] = generate_candidate_itemsets(F[2])
    F_k_sup = support_count(F[k_count - 1], transactions)

    yval_items.append(len(F[1]))
    yval_items.append(len(F_k_sup))

    while F_k_sup: # loop that finds F[k] until it is empty
        F_k = generate_candidate_itemsets(F[k_count - 1])
        F_k_sup = support_count(F_k, transactions)
        yval_items.append(len(F_k_sup))
        F[k_count] = F_k_sup
        
        k_count += 1
    
    xval_items = list(range(1,k_count-1))
    yval_items.pop()

    plt.bar(xval_items, yval_items)
    plt.xlabel("k")
    plt.ylabel("Number of frequent k-itemsets")
    plt.title("Plot items")
    plt.xticks(xval_items)
    plt.yticks(yval_items)
    plt.savefig(f"{output}_plot_items_6.png")

    # F[3] = generate_candidate_itemsets(F[2])
    # suptest = support_count(F[2],transactions)
    # print(suptest)


    return F



    # candidate pruning
        # prunes the candidates. Takes the candidate dictionary k_plus_one_candidates as a parameter. Returns k_plus_one_candidates.
    # support counting
        # assigns the support counts to the candidate itemsets. Takes the candidate dictionary k_plus_one_candidates and the transactions as parameters. 
        # Adds the support count to the value in k_plus_one_candidates 
        # e.g., k_plus_one_candidates = {
        #   '12': 3,
        #   '13': 4,
        #   '23': 11
        # }

    # candidate elimination
        # deletes candidates below the support count from the k_plus_one_candidates dictionary and adds the dictionary to F[k+1]. 
        # takes the k_plus_one_candidates dictionary and minsup as paramters.

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

    # test = generate_itemsets(item_counts, minsup, transactions, output)
    # test.popitem()
    # print(test)


if __name__ == "__main__":
    main()
