import os
import json
import multiprocessing
import psutil

def map_file_system(root_path):
    file_system_map = {}

    for dirpath, dirnames, filenames in os.walk(root_path):
        parent_folder = os.path.relpath(dirpath, root_path)
        file_system_map[parent_folder] = {
            "directories": dirnames,
            "files": filenames
        }

    return file_system_map

def update_map(existing_map, root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        parent_folder = os.path.relpath(dirpath, root_path)

        if parent_folder in existing_map:
            existing_directories = existing_map[parent_folder]["directories"]
            existing_files = existing_map[parent_folder]["files"]
            new_directories = dirnames
            new_files = filenames

            existing_directories.extend(new_directories)
            existing_files.extend(new_files)

    return existing_map

def save_map_to_json(file_system_map, output_file):
    with open(output_file, "w") as json_file:
        json.dump(file_system_map, json_file, indent=4)

def sanitize_filename(filename):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in filename)

def create_individual_maps(partitions):
    with multiprocessing.Pool() as pool:
        results = pool.map(map_file_system, partitions)

    file_system_maps = {}
    for partition, file_system_map in zip(partitions, results):
        file_system_maps[partition] = file_system_map

    for partition, file_system_map in file_system_maps.items():
        output_file = f"file_system_map_{sanitize_filename(partition)}.json"
        save_map_to_json(file_system_map, output_file)
        print(f"Updated file system map for partition '{partition}' saved to {output_file}")

if __name__ == "__main__":
    partitions = [part.device for part in psutil.disk_partitions()]

    if partitions:
        create_individual_maps(partitions)
    else:
        print("No available partitions found.")