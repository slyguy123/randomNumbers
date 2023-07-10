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

    # Assuming all rows have the same number of columns
    num_columns = len(rows[0])  
    ##### Need to filter out lucky numbers
    for row_index in range(0, len(rows) - 1):
        if(row_index!=0):
            current_row = rows[row_index]
            next_row = rows[row_index + 1]

            column_index = 1
            
            current_list = current_row[column_index].split('\n')
            next_list = next_row[column_index].split('\n')

            combined_list = current_list + next_list
            next_row[column_index] = ','.join(combined_list)

    return combined_list
    
def clean_list(mylist,separator):
    new_list= []
    for index in range(0, len(mylist)):
        cur_list = mylist[index].split(str(separator))
        new_list = new_list+cur_list
    return new_list


# set file name for csv file
filename = "euromillions_results.csv"
new_filename = "tester.csv"

# Flatten the ball numbers into a single list
ball_numbers = combine_lists(filename, new_filename)

# clean up list and remove spaces and strange entries
corrected_list = clean_list(ball_numbers, ",")
#print(corrected_list)

# isolate the first 5 and list 2 elements of every result
def getballnumbers(lst, segment_size):
    segments = [lst[i:i+segment_size] for i in range(0, len(lst), segment_size)]
    ball_numbers_list = []
    for segs in range(0,len(segments)):
        gList = segments[segs] 
        ball_numbers_list += gList[:-2]
    return ball_numbers_list

def getluckystars(lst, segment_size):
    segments = [lst[i:i+segment_size] for i in range(0, len(lst), segment_size)]
    lucky_stars = []
    for segs in range(0,len(segments)):
        gList = segments[segs] 
        lucky_stars += gList[-2:]
    return lucky_stars

# Usage example
gBallNumbers = getballnumbers(corrected_list, 7)
gLuckyStars = getluckystars(corrected_list, 7)
#print(gBallNumbers)
#print(gLuckyStars)


#with open(new_filename, 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerows(ball_numbers)

#######################

# This is not counting correctly. It is just returning the first and last set
# Calculate the top 6 most common ball numbers
most_common_balls = Counter(gBallNumbers).most_common(5)
most_common_stars = Counter(gLuckyStars).most_common(2)

###### need to print least common numbers
# Calculate the 6 least common ball numbers
least_common_balls = Counter(gBallNumbers).most_common()[-5:]
least_common_stars = Counter(gLuckyStars).most_common()[-2:]


# Output the results
# Most common
print("Most common ball numbers:")
for number, count in most_common_balls:
    print(f"{number}: {count}")
print("Lucky stars:")
for number, count in most_common_stars:
    print(f"{number}: {count}")

print("\nLeast common ball numbers:")
#print(least_common_balls)
for number, count in least_common_balls:
    print(f"{number}: {count}")
print("Lucky stars:")
for number, count in least_common_stars:
    print(f"{number}: {count}")


