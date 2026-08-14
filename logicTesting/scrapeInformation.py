#!/usr/bin/env python3

import os
import datetime
import csv
import random
from collections import Counter
import requests
from bs4 import BeautifulSoup

# === FILE PATH ===
curDir = os.getcwd()
fName = "euromillions_results.csv"
filename = os.path.join(curDir, fName)

def check_and_remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"# File {file_path} was already present and has been removed. #")
    else:
        print(f"# First time running. File {file_path} does not exist. #")

def scrape_results(year):
    url = f"https://www.lottery.co.uk/euromillions/results/archive-{year}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results_table = soup.find("table", class_="table euromillions mobFormat")
    results_list = []

    for row in results_table.find_all("tr")[1:]:
        cells = row.find_all("td")
        date = cells[0].text.strip()
        numbers = [cells[1].text.strip()]
        current_list = numbers[0].split('\n')
        frontNums = current_list[0:5]
        lucky_stars = current_list[5:]
        payouts = [cells[-1].text.strip()]
        result = {"Date": date, "Numbers": frontNums, "Lucky Stars": lucky_stars, "Payouts": payouts}
        results_list.append(result)

    return results_list

def scrape_and_save(start_year=2020):
    """
    Scrapes Euromillions data from start_year to current year,
    removes old CSV if exists, and saves fresh results.
    """
    current_year = datetime.datetime.now().year

    check_and_remove_file(filename)

    all_results = []
    for year in range(start_year, current_year + 1):
        all_results.extend(scrape_results(year))
        print(f"Scraped year {year}")

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Numbers", "Lucky Stars", "Payouts"])
        for result in all_results:
            writer.writerow([
                result["Date"], 
                ", ".join(result["Numbers"]), 
                ", ".join(result["Lucky Stars"]), 
                ", ".join(result["Payouts"])
            ])
    print(f"## New results saved to {filename} ##")

# --- Your existing functions for weighted picking ---
# ... include your combine_lists, clean_list, getballnumbers, weighted_sample, replace_duplicates etc here

# Example of generate_custom_draw (updated to raise error if CSV missing)
def generate_custom_draw(common_power=1.5, rare_power=0.5, core_count=5, star_count=2):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Data file {filename} not found. Please run scraping first.")
    # Your existing logic to load CSV and generate numbers
    # ...
    # Return final_balls, final_stars
    pass  # <-- your implementation here
