# Phase 1:
# Read input
# Generate F1
# Create skeleton code
# Create functions to generate output files
# Write code needed for plots
# Initial Report & Current Draft

import argparse

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
        
    # hash table for item counts
    item_counts = {}

    with open(input_file, 'r') as file:
        for line in file:
            # spit into list of that contains [transaction ID, item number]
            transaction_datum = line.split()
            transaction_id, item_number = map(int, transaction_datum)
            # update hash table
            if item_number in item_counts:
                    item_counts[item_number] += 1
            else:
                    item_counts[item_number] = 1
    
    with open(output_file, 'w') as output:
        for item, count in item_counts.items():
             output.write(f"Item {item}: {count} times\n")

if __name__ == "__main__":
    main()
