#!/usr/bin/env python3

##########################################################################
## This file will scrape the results pages from the euromillions website## 
## and save them to a csv file ###########################################                                      
##########################################################################


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

