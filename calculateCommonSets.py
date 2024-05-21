#!/usr/bin/env python3

###############################################################################
###############################################################################
###############################################################################
## Reads the cells of a csv file and outputs most common sets of values found##
###############################################################################
###############################################################################

import os
import csv
from itertools import combinations
from collections import Counter

def read_number_sets(csv_file, column):
    number_sets = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            # Split row by commas and strip whitespace, then convert to integers
            numbers = [int(num.strip()) for num in row[column].split(',')]
            number_sets.append(numbers)
    return number_sets

def count_triplets(number_sets, set_length):
    triplet_counter = Counter()
    for number_set in number_sets:
        # Get all possible combinations of 3 numbers in each set
        triplets = combinations(number_set, set_length)
        triplet_counter.update(triplets)
    return triplet_counter

def find_top_triplets(triplet_counter, top_n=6):
    # Get the top N triplets with the highest counts
    return triplet_counter.most_common(top_n)

if __name__ == "__main__":
    # set file name for csv file
    curDir = os.getcwd()
    fName = "euromillions_results.csv"
    csv_file = os.path.join(curDir, fName)
    # csv_file = 'lottery_data.csv'  # Replace with the path to your CSV file
    number_sets = read_number_sets(csv_file, 1)
    lucky_sets = read_number_sets(csv_file, 2)
    
    # define length of sets to search
    triplet_counter = count_triplets(number_sets, 2)
    lucky_counter = count_triplets(lucky_sets, 2)

    top_triplets = find_top_triplets(triplet_counter)
    lucky_triplets = find_top_triplets(lucky_counter)

    print("Top 3 Triplets that appear most often:")
    for triplet, count in top_triplets:
        print(f"Core Numbers: {triplet}, Count: {count}")

    for lucky, count in lucky_triplets:
        print(f"lucky: {lucky}, Count: {count}")

# adding to test
