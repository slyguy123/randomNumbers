import random

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

# Example usage: Generate 10 random numbers from 1 to 50 and 5 additional numbers from 1 to 12 with seed 123
mySeed = 12413.981267321
random_numbers = generate_random_numbers(5, mySeed)
additional_numbers = generate_additional_numbers(2, mySeed)

print("Random numbers from 1 to 50:", random_numbers)
print("Additional numbers from 1 to 12:", additional_numbers)
print("With the seed:", mySeed)


