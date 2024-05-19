#!/usr/bin/env python3

##########################################################################
## This file will scrape the results pages from the euromillions website## 
## and save them to a csv file ###########################################                                      
##########################################################################


import os
import datetime
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

    #for row in results_table.find_all("tr")[1:]:
    #    cells = row.find_all("td")
    #    date = cells[0].text.strip()
    #    #numbers = [cell.text.strip() for cell in cells[1:-1]]
    #    numbers = [cells[1].text.strip()]
    #    lucky_stars = [cells[-1].text.strip()]
    #    result = {"Date": date, "Numbers": numbers, "Lucky Stars": lucky_stars}
    #    results_list.append(result)

    # Adding lucky stars and payouts colum. 
    # TO DO - need to adjust coloum lookups in extract commonValues to match.
    # also need to check that the commas are supported in the text.
    for row in results_table.find_all("tr")[1:]:
        cells = row.find_all("td")
        date = cells[0].text.strip()
        numbers = [cells[1].text.strip()]

        current_list = numbers[0].split('\n')
        frontNums = current_list[0:5]
        #lucky_stars = [cells[-1].text.strip()]
        lucky_stars = current_list[5:]
        payouts = [cells[-1].text.strip()]
        result = {"Date": date, "Numbers": frontNums, "Lucky Stars": lucky_stars, "Payouts": payouts}
        results_list.append(result)
        print(frontNums)
        print(lucky_stars)
    return results_list

# Scrape the EuroMillions results for each year from 2016 to the present
start_year = 2016
current_year = datetime.datetime.now().year
results = []

for year in range(start_year, current_year + 1):
    results.extend(scrape_results(year))

# Save the results to a CSV file
curDir = os.getcwd()

#filename = "/home/slyguy/Downloads/euromillions_results.csv"
fName = "euromillions_results.csv"
filename = os.path.join(curDir, fName)



with open(filename, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Date", "Numbers", "Lucky Stars", "Payouts"])
    for result in results:
        writer.writerow([result["Date"], ", ".join(result["Numbers"]), ", ".join(result["Lucky Stars"]), ", ".join(result["Payouts"])])
print(f"Results saved to {filename}")

