import os
import glob
import re
import csv

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)',str(text)) ]

def create_tc_csv(thumbnail_path, output_path):
    data_file = []
    folder = glob.glob(os.path.join(thumbnail_path, '*.jpg'))
    print(folder)
    for file_name in folder:
        data_file.append([file_name.split("\\")[2]])
        print(file_name)
    
    with open(os.path.join(output_path,'container_list2.csv'), 'w') as fout:
        writer = csv.writer(fout)
        writer.writerows(sorted(data_file, key=natural_keys))
        fout.close()
    
    remove_empty_rows(os.path.join(output_path,'container_list2.csv'), os.path.join(output_path,'container_list.csv'))
    os.remove(os.path.join(output_path,'container_list2.csv'))

def remove_empty_rows(in_fnam, out_fnam):
    with open(in_fnam) as input, open(out_fnam, 'w', newline='') as output:
        writer = csv.writer(output)
        for row in csv.reader(input):
            if any(field.strip() for field in row):
                writer.writerow(row)
                
