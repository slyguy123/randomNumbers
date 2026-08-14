import os 
import csv
from collections import Counter
import matplotlib.pyplot as plt

def calculate_probabilities(csv_file):
    numbers_count = Counter()

    # Read the CSV file and count the occurrences of each number
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if exists
        for row in reader:
            numbers = row[1:]  # Assuming numbers are in columns 1 onwards
            numbers_count.update(numbers)

    # Total number of draws
    total_draws = sum(numbers_count.values())

    # Calculate probabilities
    probabilities = {number: count / total_draws for number, count in numbers_count.items()}
    return probabilities

def visualize_probabilities(probabilities):
    sorted_probabilities = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    numbers, probs = zip(*sorted_probabilities)

    plt.figure(figsize=(10, 6))
    plt.bar(numbers, probs)
    plt.xlabel('Number')
    plt.ylabel('Probability')
    plt.title('Probability of Numbers Being Drawn')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()



if __name__ == "__main__":
    # set file name for csv file
    curDir = os.getcwd()
    fName = "euromillions_results.csv"
    csv_file = os.path.join(curDir, fName)
    probabilities = calculate_probabilities(csv_file)
    print("Probabilities:", probabilities)
    visualize_probabilities(probabilities)
