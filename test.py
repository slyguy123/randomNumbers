import csv

def combine_lists(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    num_columns = len(rows[0])  # Assuming all rows have the same number of columns

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

# Usage example
filename = "euromillions_results.csv"
new_filename = "tester.csv"

combine_lists(filename)
