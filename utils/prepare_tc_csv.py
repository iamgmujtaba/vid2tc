import os
import glob
import re
import csv

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [atoi(c) for c in re.split(r'(\d+)', text)]

def remove_empty_rows(in_fnam, out_fnam):
    with open(in_fnam) as input_file, open(out_fnam, 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for row in csv.reader(input_file):
            if any(field.strip() for field in row):
                writer.writerow(row)

def create_tc_csv(thumbnail_path, output_path):
    folder = glob.glob(os.path.join(thumbnail_path, '*.jpg'))
    # print(folder)
    data_file = [[os.path.basename(file_name)] for file_name in folder]
    # for file_name in folder:
        # print(file_name)
    temp_csv = os.path.join(output_path, 'container_list2.csv')
    final_csv = os.path.join(output_path, 'container_list.csv')

    with open(temp_csv, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(data_file, key=lambda x: natural_keys(x[0])))

    remove_empty_rows(temp_csv, final_csv)
    os.remove(temp_csv)
