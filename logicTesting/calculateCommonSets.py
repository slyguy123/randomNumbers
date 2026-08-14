#!/usr/bin/env python3

###############################################################################
## Reads the cells of a CSV file and outputs the most common sets of values ##
###############################################################################

import os
import csv
import random
from itertools import combinations
from collections import Counter

def read_number_sets(csv_file, column):
    """Reads the number sets from a CSV file and returns a list of lists."""
    number_sets = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            # Split row by commas and strip whitespace, then convert to integers
            numbers = [int(num.strip()) for num in row[column].split(',')]
            number_sets.append(numbers)
    return number_sets

def count_combinations(number_sets, set_length):
    """Counts occurrences of number combinations of a given length."""
    combination_counter = Counter()
    for number_set in number_sets:
        combos = combinations(number_set, set_length)
        combination_counter.update(combos)
    return combination_counter

def find_top_combinations(combination_counter, top_n=6):
    """Finds the top N most common number combinations."""
    return combination_counter.most_common(top_n)

def get_random_numbers(all_numbers, top_combinations, selection_count=5, lucky_mode=False):
    """
    Returns a random selection of numbers that do not include the most common combinations.
    lucky_mode = True ensures selection is from 1-12.
    """
    # Flatten the top combinations into a set of numbers to avoid
    excluded_numbers = {num for combo, _ in top_combinations for num in combo}

    # Get all unique numbers available
    if lucky_mode:
        unique_numbers = set(range(1, 13))  # Only 1-12 for lucky numbers
    else:
        unique_numbers = set(all_numbers)

    # Remove the excluded numbers
    available_numbers = sorted(unique_numbers - excluded_numbers)

    # Ensure there are enough numbers to sample from
    if len(available_numbers) < selection_count:
        raise ValueError("Not enough unique numbers to generate a random selection.")

    # Select random numbers from the available pool
    return random.sample(available_numbers, selection_count)

if __name__ == "__main__":
    # Set file name for CSV file
    curDir = os.getcwd()
    fName = "euromillions_results.csv"
    csv_file = os.path.join(curDir, fName)

    # Read numbers from the CSV file
    number_sets = read_number_sets(csv_file, 1)
    lucky_sets = read_number_sets(csv_file, 2)

    # Define length of sets to search
    combination_counter = count_combinations(number_sets, 2)
    lucky_counter = count_combinations(lucky_sets, 2)

    # Find top occurring combinations
    top_combinations = find_top_combinations(combination_counter)
    lucky_top_combinations = find_top_combinations(lucky_counter)

    # Flatten all number sets into a unique list
    all_numbers = {num for sublist in number_sets for num in sublist}

    # Generate random numbers excluding the top combinations
    try:
        random_numbers = get_random_numbers(all_numbers, top_combinations, 5)
        random_lucky_numbers = get_random_numbers(all_numbers, lucky_top_combinations, 2, lucky_mode=True)
    except ValueError as e:
        print(f"Error: {e}")
        random_numbers, random_lucky_numbers = [], []

    # Print results
    print("Combinations that appear most often:")
    for combo, count in top_combinations:
        print(f"Core Numbers: {combo}, Count: {count}")

    for lucky, count in lucky_top_combinations:
        print(f"Lucky: {lucky}, Count: {count}")

    print("\nRandomly Selected Numbers (Excluding Common Combinations):")
    print(f"Core Numbers: {random_numbers}")
    print(f"Lucky Numbers: {random_lucky_numbers}")

    print(f" --- CSV file: {csv_file} ---")

    print(" ----- USE COMMON VALUES RATHER -----")
