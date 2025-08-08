#!/usr/bin/env python3

#######################################################################
## Reads CSV lottery results and generates weighted random numbers   ##
## Now supports filtering out rollover draws (Column D in CSV)       ##
#######################################################################

import csv
import os
import datetime
import random
from collections import Counter
import requests
from bs4 import BeautifulSoup

# === FILE PATH ===
curDir = os.getcwd()
fName = "euromillions_results.csv"
filename = os.path.join(curDir, fName)

# === GLOBAL TOGGLE FOR ROLLOVER FILTER ===
FILTER_ROLLOVERS = False  # Set True to only use draws that are NOT rollovers

##############################
# --- Scraper Functions --- #
##############################

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
    current_year = datetime.datetime.now().year

    check_and_remove_file(filename)

    all_results = []
    for year in range(start_year, current_year + 1):
        print(f"Scraping results for year: {year}")
        all_results.extend(scrape_results(year))

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

##############################
# --- Filter Functions ---  #
##############################

def filter_non_rollover_numbers(filename):
    """
    Reads the CSV file and returns only numbers from rows
    where the 'Payouts' column does NOT contain 'Rollover'.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Data file {filename} not found. Please scrape first.")

    filtered_balls = []
    filtered_stars = []

    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # skip header

        for row in reader:
            if len(row) < 4:
                continue

            payouts_col = row[3].strip().lower()
            if "rollover" not in payouts_col:
                balls = [n.strip() for n in row[1].split(",") if n.strip()]
                stars = [n.strip() for n in row[2].split(",") if n.strip()]
                
                filtered_balls.extend(balls)
                filtered_stars.extend(stars)

    return filtered_balls, filtered_stars

##############################
# --- Helper Functions ---  #
##############################

def combine_lists(filename, colNum):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row_index in range(1, len(rows) - 1):
        current_row = rows[row_index]
        next_row = rows[row_index + 1]
        current_list = current_row[colNum].split('\n')
        next_list = next_row[colNum].split('\n')
        combined_list = current_list + next_list
        next_row[colNum] = ','.join(combined_list)

    return combined_list

def clean_list(mylist, separator):
    new_list = []
    for item in mylist:
        cur_list = item.split(str(separator))
        new_list += cur_list
    return new_list

def getballnumbers(lst, segment_size):
    segments = [lst[i:i+segment_size] for i in range(0, len(lst), segment_size)]
    ball_numbers_list = []
    for segment in segments:
        ball_numbers_list += segment
    return ball_numbers_list

def weighted_sample(numbers, frequency_dict, k, power=1.0):
    weighted_pool = []
    for num in numbers:
        freq = frequency_dict.get(num, 0)
        weight = (freq + 1) ** power
        weighted_pool.extend([num] * int(weight))
    if len(weighted_pool) < k:
        weighted_pool = numbers * k
    return random.sample(weighted_pool, k)

def remove_matches(list1, list2):
    return [x for x in list1 if x not in list2]

def filterTuples(list_of_tuples, index):
    return [t[index] for t in list_of_tuples]

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

##############################
# --- Core Data Prep ---    #
##############################

def prepare_data():
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Data file {filename} not found. Please run scraping first.")

    if FILTER_ROLLOVERS:
        print("Applying rollover filter...")
        gBallNumbers, gLuckyStars = filter_non_rollover_numbers(filename)
    else:
        ball_numbers = combine_lists(filename, 1)
        lucky_numbers = combine_lists(filename, 2)
        corrected_list = clean_list(ball_numbers, ",")
        corrected_lucky_list = clean_list(lucky_numbers, ",")
        gBallNumbers = getballnumbers(corrected_list, 5)
        gLuckyStars = getballnumbers(corrected_lucky_list, 2)

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

    return {
        "gBallNumbers": gBallNumbers,
        "gLuckyStars": gLuckyStars,
        "ball_counts": ball_counts,
        "star_counts": star_counts,
        "most_common_balls": most_common_balls,
        "most_common_stars": most_common_stars,
        "least_common_balls": least_common_balls,
        "least_common_stars": least_common_stars,
        "highBalls_list": highBalls_list,
        "highLowBalls_list": highLowBalls_list,
        "remainingBalls": remainingBalls,
        "gLuckyStars_list": gLuckyStars_list,
        "remainingStars": remainingStars
    }

##############################
# --- Number Generation --- #
##############################

def generate_custom_draw(common_power=1.5, rare_power=0.5, core_count=5, star_count=2):
    data = prepare_data()
    ball_counts = data["ball_counts"]
    star_counts = data["star_counts"]

    highBalls_list = data["highBalls_list"]
    remainingBalls = data["remainingBalls"]
    gBallNumbers = data["gBallNumbers"]
    gLuckyStars = data["gLuckyStars"]

    common_pick_count = min(3, core_count)
    random_common_balls = weighted_sample(highBalls_list, ball_counts, common_pick_count, power=common_power)

    remaining_pick_count = core_count - common_pick_count
    random_remaining_balls = []
    if remaining_pick_count > 0:
        random_remaining_balls = weighted_sample(list(remainingBalls), ball_counts, remaining_pick_count, power=rare_power)

    random_lucky_stars = weighted_sample(list(set(gLuckyStars)), star_counts, star_count, power=1.0)

    final_balls = sorted(random_common_balls + random_remaining_balls)
    final_stars = sorted(random_lucky_stars)

    final_balls = replace_duplicates(final_balls, list(set(gBallNumbers)), ball_counts)
    final_stars = replace_duplicates(final_stars, list(set(gLuckyStars)), star_counts)

    return final_balls, final_stars

##############################
# --- Main Execution ---    #
##############################

def main():
    scrape_and_save(start_year=2020)
    final_balls, final_stars = generate_custom_draw()
    data = prepare_data()

    print("\nGenerated Numbers (Weighted & Deduplicated):")
    print(f"Core Numbers: {final_balls}")
    print(f"Lucky Stars:  {final_stars}")

    print("\nMost Common Ball Numbers:")
    for number, count in data["most_common_balls"]:
        print(f"{number}: {count}")

    print("\nMost Common Lucky Stars:")
    for number, count in data["most_common_stars"]:
        print(f"{number}: {count}")

    print("\nLeast Common Ball Numbers:")
    for number, count in data["least_common_balls"]:
        print(f"{number}: {count}")

    print("\nLeast Common Lucky Stars:")
    for number, count in data["least_common_stars"]:
        print(f"{number}: {count}")

if __name__ == "__main__":
    main()
