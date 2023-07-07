#!/usr/bin/env python3

#######################################################################
## Reads the cells of a csv file and outputs most common values found##
#######################################################################

import csv
from collections import Counter

# Read the results from the CSV file
def combine_lists(filename, new_filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    num_columns = len(rows[0])  # Assuming all rows have the same number of columns

    ##### Need to filter out lucky numbers
    for row_index in range(1, len(rows) - 1):
        current_row = rows[row_index]
        next_row = rows[row_index + 1]

        column_index = 1
        lucky_stars = []
        current_list = current_row[column_index].split(',')
        next_list = next_row[column_index].split('\n')
        ##!!!!! need to remove luckystars from next_list
        lucky_stars = next_list[-1:]

        combined_list = current_list + next_list
        next_row[column_index] = ','.join(combined_list)        

    final_list = combined_list + lucky_stars
    return final_list
    

# set file name for csv file
filename = "euromillions_results.csv"
new_filename = "tester.csv"
# Flatten the ball numbers into a single list
ball_numbers = combine_lists(filename, new_filename)

print(ball_numbers)
for i in range(1, 3):
    print("\n")
#with open(new_filename, 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerows(ball_numbers)

#######################

# This is not counting correctly. It is just returning the first and last set
# Calculate the top 6 most common ball numbers
most_common = Counter(ball_numbers).most_common(6)

###### need to print least common numbers
# Calculate the 6 least common ball numbers
least_common = Counter(ball_numbers).most_common()[:-1]

# Output the results
print("Most common ball numbers:\n")
#print(most_common)
for number, count in most_common:
    print(f"{number}: {count}")

#print("\nLeast common ball numbers:")
#for number, count in least_common:
#    print(f"{number}: {count}")
