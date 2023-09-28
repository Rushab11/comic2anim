import os
import csv


def create_csv(folder_name):
    image_folder = f'../images/{folder_name.lower()}/'

    if not os.path.exists(image_folder):
        print(f'Image folder does not exist: {image_folder}')
        exit(1)

    image_names = sorted([os.path.splitext(f)[0] for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))],
                         key=lambda x: os.path.getmtime(os.path.join(image_folder, x + ".jpg")))

    csv_file = f'{folder_name}.csv'

    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['image_name', 'image_description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for image_name in image_names:
            writer.writerow({'image_name': image_name, 'image_description': ''})

    print(f'CSV file "{csv_file}" has been created with image names.')


