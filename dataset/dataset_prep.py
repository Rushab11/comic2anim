
import os
import csv

image_folder = './images/'

image_names = sorted([os.path.splitext(f)[0] for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))],
                     key=lambda x: os.path.getmtime(os.path.join(image_folder, x + ".jpg")))

# Define the path for the CSV file


csv_file = 'dataset_prep.csv'

with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['image_name', 'image_description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for image_name in image_names:
        writer.writerow({'image_name': image_name, 'image_description': ''})

print(f'CSV file "{csv_file}" has been created with image names.')
