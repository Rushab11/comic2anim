import os
import shutil
from dataset_prep import create_csv

source_folder = '../images/'

dest_name = input("Enter the name of the destination folder: ")

destination_folder = f'../images/{dest_name.lower()}'

num_files_to_move = int(input("Enter the number of files to move: "))

if not os.path.exists(source_folder):
    print(f"Source folder does not exist: {source_folder}")
    exit(1)

if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

files_to_move = sorted(os.listdir(source_folder), key=lambda x: os.path.getmtime(os.path.join(source_folder, x)))

num_available_files = len(files_to_move)
num_to_move = min(num_files_to_move, num_available_files)

for i in range(num_to_move):
    source_file = os.path.join(source_folder, files_to_move[i])
    destination_file = os.path.join(destination_folder, files_to_move[i])
    shutil.move(source_file, destination_file)

print(f"Moved {num_to_move} files to {destination_folder}")

create_csv(dest_name)
