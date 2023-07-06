#!/usr/bin/env python3

# This file will scrape the results pages from the euromillions website and save them to a csv file
# It will then count up the results and print out the 6 most and least common results drawn.

import requests
from bs4 import BeautifulSoup
import csv
from collections import Counter

# Function to scrape the EuroMillions results from a specific year
def scrape_results(year):
    url = f"https://www.lottery.co.uk/euromillions/results/archive-{year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results_table = soup.find("table", class_="table euromillions mobFormat")
    results_list = []

    for row in results_table.find_all("tr")[1:]:
        cells = row.find_all("td")
        date = cells[0].text.strip()
        #numbers = [cell.text.strip() for cell in cells[1:-1]]
        numbers = [cells[1].text.strip()]
        lucky_stars = [cells[-1].text.strip()]
        result = {"Date": date, "Numbers": numbers, "Lucky Stars": lucky_stars}
        results_list.append(result)

    return results_list

# Scrape the EuroMillions results for each year from 2016 to the present
start_year = 2016
current_year = 2023
results = []

for year in range(start_year, current_year + 1):
    results.extend(scrape_results(year))

# Save the results to a CSV file
filename = "euromillions_results.csv"

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Numbers", "Lucky Stars"])
    for result in results:
        writer.writerow([result["Date"], ", ".join(result["Numbers"]), ", ".join(result["Lucky Stars"])])
print(f"Results saved to {filename}")

# Read the results from the CSV file

def combine_lists(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    num_columns = len(rows[0])  # Assuming all rows have the same number of columns

    ##### Need to filter out lucky numbers
    for row_index in range(1, len(rows) - 1):
        current_row = rows[row_index]
        next_row = rows[row_index + 1]

        column_index = 1
        current_list = current_row[column_index].split(',')
        next_list = next_row[column_index].split('\n')

        combined_list = current_list + next_list
        next_row[column_index] = ','.join(combined_list)        

    return combined_list
    #with open(new_filename, 'w', newline='') as file:
    #    writer = csv.writer(file)
    #    writer.writerows(rows)
    #    writer.writerows(combined_list)

# Flatten the ball numbers into a single list
ball_numbers = combine_lists(filename)

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

print("\nLeast common ball numbers:")
for number, count in least_common:
    print(f"{number}: {count}")
