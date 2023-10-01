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

    output_file = args.output
    minconf = int(args.minconf)
    if minconf == -1:
        print('Minconf is -1;exiting without writing file')
        exit()
        
    
    with open(output_file, 'w') as f:
        f.write(f"output test\n")

if __name__ == "__main__":
    main()
