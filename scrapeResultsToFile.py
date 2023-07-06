#!/usr/bin/env python3

import re
import requests
from bs4 import BeautifulSoup

# Send a GET request to the webpage
url = "https://www.lottery.co.uk/euromillions/results/past"
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the table containing the results
results_table = soup.find("table", class_="table euromillions mobFormat")

# Initialize a list to store the results
results_list = []

#print(results_table)

# Iterate over each row in the table (excluding the header row)
for row in results_table.find_all("tr")[1:]:
    # Extract the date and numbers from each row
    cells = row.find_all("td")
    date = cells[0].text.strip()
    numbers = [cell.text.strip() for cell in cells[1:-1]]
    lucky_stars = [cells[-1].text.strip()]

    # Append the result to the list
    result = {"Date": date, "Numbers": numbers, "Lucky Stars": lucky_stars}
    results_list.append(result)

# Save the results to a file
filename = "euromillions_results.csv"
with open(filename, "w", encoding="utf-8") as file:
    for result in results_list:
        file.write(f"Date: {result['Date']}\n")
        file.write(f"Numbers: {', '.join(result['Numbers'])}\n")
        file.write(f"Lucky Stars: {', '.join(result['Lucky Stars'])}\n")
        file.write("\n")

print(f"Results saved to {filename}")
