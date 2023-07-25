#!/usr/bin/env python3

#######################################################################
#######################################################################
## Reads the cells of a csv file and outputs most common values found##
#######################################################################
#######################################################################

import csv
from collections import Counter

import datetime
import getpass

def combine_lists(filename):
    # Read the results from the CSV file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    # Assuming all rows have the same number of columns
    num_columns = len(rows[0])  
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

def get_current_user():
    current_user = getpass.getuser()
    return current_user

def get_current_time():
    current_time = datetime.datetime.now()
    return current_time

# set file name for csv file
filename = "/home/slyguy/Downloads/euromillions_results.csv"

# Sample the cells and flatten the ball numbers into a single list
ball_numbers = combine_lists(filename)

# clean up list and remove spaces and strange entries
corrected_list = clean_list(ball_numbers, ",")
#print(corrected_list)

# split into numbers and stars
gBallNumbers = getballnumbers(corrected_list, 7)
gLuckyStars = getluckystars(corrected_list, 7)
#print(gBallNumbers)
#print(gLuckyStars)

# Calculate the top 6 most common ball numbers
most_common_balls = Counter(gBallNumbers).most_common(5)
most_common_stars = Counter(gLuckyStars).most_common(2)

# Calculate the 6 least common ball numbers
least_common_balls = Counter(gBallNumbers).most_common()[-5:]
least_common_stars = Counter(gLuckyStars).most_common()[-2:]

#########################################################################
## Creating lists from numbers not found in most or least common lists ##
#########################################################################

def remove_matches(list1, list2):
    new_list = [x for x in list1 if x not in list2]
    return new_list

def filterTuples(list, index):
    filtered_list = [t[index] for t in list]
    return filtered_list

# isolate numbers that are not in the most or least common lists
highLowBalls_list = filterTuples(most_common_balls, 0) +  filterTuples(least_common_balls, 0)
remainingBalls = remove_matches(set(gBallNumbers), set(highLowBalls_list))

gLuckyStars_list = filterTuples(most_common_stars, 0) +  filterTuples(least_common_stars, 0)
remainingStars = remove_matches(set(gLuckyStars), set(gLuckyStars_list))


#########################################################################
#########################################################################
##################### Randomly generate numbers #########################
##################### from the remaining numbers ########################
#########################################################################
#########################################################################

import random
import datetime
import getpass

def get_current_time():
    current_time = datetime.datetime.now()
    return current_time

def datetime_to_timestamp(dt):
    epoch_time = datetime.datetime(1970, 1, 1)
    time_difference = dt - epoch_time
    timestamp = time_difference.total_seconds()
    return timestamp

def generate_random_numbers(num, seed):
    random.seed(seed)
    random_numbers = []
    for _ in range(num):
        random_number = random.randint(1, 50)
        random_numbers.append(random_number)
    return random_numbers

def generate_additional_numbers(num, seed):
    random.seed(seed)
    additional_numbers = []
    for _ in range(num):
        additional_number = random.randint(1, 12)
        additional_numbers.append(additional_number)
    return additional_numbers

# get current time and use it as a seed value
current_time = get_current_time()
current_time_as_float = float(datetime_to_timestamp(current_time))
mySeed = current_time_as_float

random.seed(mySeed)

random_balls = random.sample(remainingBalls, 5)
random_stars = random.sample(remainingStars, 2)

print("Random balls to play: " + str(random_balls))
print("Random stars to play: " + str(random_stars))

###############################################################
###############################################################
################### OUT NUMBERS TO THE TERMINAL ###############
###############################################################
###############################################################

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

print("\n Sucess!!")
