# Phase 1:
# Read input - done 
# Generate - done
# Create skeleton code
# Create functions to generate output files - done
# Write code needed for plots
# Initial Report & Current Draft

import argparse
import matplotlib.pyplot as plt
from itertools import combinations
import time


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
    

def generate_itemsets(item_counts, minsup):
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
        subsets = combinations(candidate, k-1)
        for subset in subsets:
            if subset not in F[k-1]:
                return False
        return True
    
    def generate_candidate_itemsets(k_minus_1_itemset):
        k = len(list(k_minus_1_itemset.keys())[0]) + 1 if k_minus_1_itemset else 2
        candidates = {}

        items = sorted(k_minus_1_itemset.keys())
        
        for i in range(len(items)):
            for j in range(i+1, len(items)):
                # Check if the first k-2 items are the same
                if items[i][:k-2] == items[j][:k-2] and items[i][k-2] < items[j][k-2]:
                    candidate = items[i] + (items[j][k-2],)
                    if prune_candidates(candidate, k):
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



def generate_association_rules(frequent_itemset, transactions, minconf):
    association_rules = []
    
    for i in range(1, len(frequent_itemset)):
        for combo in combinations(frequent_itemset, i):
            left = set(combo)
            right = frequent_itemset - left
            rule = (left, right)
            confidence = calculate_confidence(rule, transactions)
            if confidence >= minconf:
                association_rules.append((rule,confidence))

    return association_rules

def format_rule(rule):
    left, right = rule
    return f"{' '.join(map(str, left))}|{' '.join(map(str, right))}"

def calculate_support(itemset, transactions):
    count = 0
    for transaction in transactions.values():
        if all(item in transaction for item in itemset):
            count += 1
    return count

def calculate_confidence(rule, transactions):
    left, right = rule
    itemset_union = left.union(right)
    support_itemset_union = calculate_support(itemset_union, transactions)
    support_left = calculate_support(left, transactions)
    if support_left == 0:
        return 0  # Avoid division by zero
    confidence = support_itemset_union / support_left
    return confidence




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

def write_output(f1_items, minsup, minconf, input_file, output, item_counts, transactions, test, itemset_time):
    """
    writes three different output files that describe various aspects of the association rules
    """
    f1_items, minsup, minconf, input_file, output, item_counts, transactions, test = f1_items, minsup, minconf, input_file, output, item_counts, transactions, test
    
    confcount, maxconf = 0, 0

    def convert_to_str(key):
        if isinstance(key, tuple):
            return ' '.join(map(str, key))
        return str(key)

    # write {output}_items_6.txt
    with open(f'{output}_items_6.txt', 'w') as items:
        for outer_key, inner_dict in test.items():
            for inner_key, value in inner_dict.items():
                inner_key_str = convert_to_str(inner_key)
                items.write(f'{inner_key_str}|{value}\n')
    
    # write {output}_rules_6.txt
    hiconf_count = 0
    k_rule = 0
    maxrule = 0
    rule_time = 0
    k_list, rule_list = [], []
    if minconf != -1:
        with open(f'{output}_rules_6.txt', 'w') as rules:
            start = time.time()
            for outer_key, inner_dict in test.items():
                hiconf_count = 0
                k_rule += 1
                k_list.append(k_rule)
                for inner_key, value in inner_dict.items():
                    if isinstance(inner_key,int):
                        continue
                    frequent_itemset = set(inner_key)
                    support = value/len(transactions)
                    support = str(round(support, 2))
                    start = time.time()
                    association_rules = generate_association_rules(frequent_itemset,transactions,minconf)
                    hiconf_count += (len(association_rules))
                    for rule, confidence in association_rules:
                        confcount += 1
                        rules.write(f"{format_rule(rule)}|{support}|{round(confidence,2)}\n")
                        maxconf = max(confidence,maxconf)
                        if confidence == maxconf:
                            maxrule = format_rule(rule)
                rule_list.append(hiconf_count)
            end = time.time()
            rule_time = end - start
            k_list.pop(0)
            rule_list.pop(0)

    if minconf != -1:
        plt.clf()
        plt.bar(k_list, rule_list)
        plt.xlabel("k")
        plt.ylabel("Number of high-confidence rules")
        plt.title("Plot rules")
        plt.xticks(k_list)
        plt.yticks(rule_list)
        plt.savefig(f"{output}_plot_rules_6.png")



    # write {output}_info_6.txt
    
    with open(f'{output}_info_6.txt', 'w') as info:
        info.write(f"minsup: {minsup} \n")
        info.write(f"minconf: {minconf} \n")
        info.write(f"input file: {input_file} \n")
        info.write(f"output name: {output} \n")
        info.write(f"Number of items: {len(item_counts)}\n")
        info.write(f"Number of transactions: {len(transactions)}\n")
        info.write(f"The length of the largest frequent k-itemset: {list(test)[-1]}\n")
        totalfrequent = 0
        for outer_key, inner_dict in test.items():
            info.write(f"Number of frequent {outer_key}-itemsets: {len(inner_dict)}\n")
            totalfrequent += len(inner_dict)
        info.write(f"Total number of frequent itemsets: {totalfrequent}\n")
        info.write(f"Number of high confidence rules: {confcount}\n")
        info.write(f"The rule with the highest confidence: {maxrule}\n")
        info.write(f"Time in seconds to find the frequent itemsets: {itemset_time}\n")
        info.write(f"Time in seconds to find the confident rules: {rule_time}\n")
        # for transaction, list in transactions.items():
        #      info.write(f"Transaction {transaction}: {list}\n")
        # for item, count in item_counts.items():
        #      info.write(f"Item {item}: {count} times\n")
    

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
    # if minconf == -1:
    #     print('Minconf is -1;exiting without writing file')
    #     exit()

    item_counts, transactions = read_input(input_file)

    #f1_items = generate_f1(item_counts, minsup)

    write_output(f1_items, minsup, minconf, input_file, output, item_counts, transactions)


if __name__ == "__main__":
    main()
