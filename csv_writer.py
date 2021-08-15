import csv


def get_csv_writer(file_name):
    with open(file_name, 'w', newline='') as csv_file:
        fieldnames = ['business', 'comment']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        return writer
