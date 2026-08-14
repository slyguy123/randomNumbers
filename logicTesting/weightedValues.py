#!/usr/bin/env python3

#######################################################################
## Reads the cells of a csv file and outputs most common values found##
#######################################################################

import csv
import os
import datetime
import getpass
import random
from collections import Counter

# Combines the results from two consecutive rows in the given column
# to simulate accumulation of results

def combine_lists(filename, colNum):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row_index in range(1, len(rows) - 1):
        current_row = rows[row_index]
        next_row = rows[row_index + 1]
        column_index = colNum

        current_list = current_row[column_index].split('\n')
        next_list = next_row[column_index].split('\n')

        combined_list = current_list + next_list
        next_row[column_index] = ','.join(combined_list)

    return combined_list

# Cleans up a list by splitting entries with a given separator

def clean_list(mylist, separator):
    new_list = []
    for item in mylist:
        cur_list = item.split(str(separator))
        new_list += cur_list
    return new_list

# Extracts ball numbers from cleaned list segments

def getballnumbers(lst, segment_size):
    segments = [lst[i:i+segment_size] for i in range(0, len(lst), segment_size)]
    ball_numbers_list = []
    for segment in segments:
        ball_numbers_list += segment
    return ball_numbers_list

# Gets current timestamp for random seed

def get_current_time():
    return datetime.datetime.now()

def datetime_to_timestamp(dt):
    epoch_time = datetime.datetime(1970, 1, 1)
    return (dt - epoch_time).total_seconds()

# Returns weighted random sample from a number list using frequency weighting

def weighted_sample(numbers, frequency_dict, k, power=1.0):
    weighted_pool = []
    for num in numbers:
        freq = frequency_dict.get(num, 0)
        weight = (freq + 1) ** power  # +1 to avoid zero-weighting
        weighted_pool.extend([num] * int(weight))
    return random.sample(weighted_pool, k)

# Removes matches between two lists

def remove_matches(list1, list2):
    return [x for x in list1 if x not in list2]

# Filters index from tuple list

def filterTuples(list_of_tuples, index):
    return [t[index] for t in list_of_tuples]

# Replaces duplicates in a number list using frequency sorted replacements

def replace_duplicates(numbers, full_pool, counter):
    seen = set()
    duplicates = []

    for num in numbers:
        if num in seen:
            duplicates.append(num)
        else:
            seen.add(num)

    sorted_candidates = [num for num, _ in counter.most_common() if num not in seen]

    for dup in duplicates:
        if sorted_candidates:
            replacement = sorted_candidates.pop(0)
            idx = numbers.index(dup)
            numbers[idx] = replacement
            seen.add(replacement)

    return sorted(numbers)

# === FILE PATH ===
curDir = os.getcwd()
fName = "euromillions_results.csv"
filename = os.path.join(curDir, fName)

# === CLEANING AND PREP ===
ball_numbers = combine_lists(filename, 1)
lucky_numbers = combine_lists(filename, 2)

corrected_list = clean_list(ball_numbers, ",")
corrected_lucky_list = clean_list(lucky_numbers, ",")

gBallNumbers = getballnumbers(corrected_list, 5)
gLuckyStars = getballnumbers(corrected_lucky_list, 2)

# === FREQUENCY ANALYSIS ===
ball_counts = Counter(gBallNumbers)
star_counts = Counter(gLuckyStars)

most_common_balls = ball_counts.most_common(25)
most_common_stars = star_counts.most_common(2)

least_common_balls = ball_counts.most_common()[-5:]
least_common_stars = star_counts.most_common()[-2:]

highBalls_list = filterTuples(most_common_balls, 0)
highLowBalls_list = filterTuples(least_common_balls, 0)
remainingBalls = remove_matches(set(gBallNumbers), set(highLowBalls_list))

gLuckyStars_list = filterTuples(least_common_stars, 0)
remainingStars = remove_matches(set(gLuckyStars), set(gLuckyStars_list))

# === RANDOM SEED SETUP ===
current_time = get_current_time()
mySeed = float(datetime_to_timestamp(current_time))
random.seed(mySeed)

# === RANDOM WEIGHTED SELECTIONS ===
random_common_balls = weighted_sample(highBalls_list, ball_counts, 3, power=1.5)
random_remaining_balls = weighted_sample(list(remainingBalls), ball_counts, 2, power=0.5)
random_lucky_stars = weighted_sample(list(set(gLuckyStars)), star_counts, 2, power=1.0)

final_balls = sorted(random_common_balls + random_remaining_balls)
final_stars = sorted(random_lucky_stars)

# === DUPLICATE HANDLING ===
final_balls = replace_duplicates(final_balls, list(set(gBallNumbers)), ball_counts)
final_stars = replace_duplicates(final_stars, list(set(gLuckyStars)), star_counts)

# === OUTPUT ===
print("\nGenerated Numbers (Weighted & Deduplicated):")
print(f"Core Numbers: {final_balls}")
print(f"Lucky Stars:  {final_stars}")

print("\nMost Common Ball Numbers:")
for number, count in most_common_balls:
    print(f"{number}: {count}")

print("\nMost Common Lucky Stars:")
for number, count in most_common_stars:
    print(f"{number}: {count}")

print("\nLeast Common Ball Numbers:")
for number, count in least_common_balls:
    print(f"{number}: {count}")

print("\nLeast Common Lucky Stars:")
for number, count in least_common_stars:
    print(f"{number}: {count}")

print("\nSuccess!")
