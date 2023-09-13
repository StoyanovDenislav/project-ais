import os
import json
import psutil

def load_file_system_maps(partitions):
    file_system_maps = {}

    for partition in partitions:
        sanitized_partition = "".join(c if c.isalnum() or c in "-_." else "_" for c in partition)
        file_path = f"file_system_map_{sanitized_partition}.json"
        try:
            with open(file_path, "r") as json_file:
                file_system_maps[partition] = json.load(json_file)
        except FileNotFoundError:
            file_system_maps[partition] = {}

    return file_system_maps

def find_files_by_name(base_file_name):
    partitions = [part.device for part in psutil.disk_partitions()]
    file_system_maps = load_file_system_maps(partitions)

    matching_files = []

    for partition, file_system_map in file_system_maps.items():
        for contents in file_system_map.values():
            if "files" in contents:
                for file in contents["files"]:
                    file_name, file_extension = os.path.splitext(file)
                    if base_file_name == file_name:
                        matching_files.append(os.path.join(partition, file_name))

    return matching_files

if __name__ == "__main__":
    target_base_file_name = "AnimationGraphArea"  # Replace with the desired base file name

    # Find all files with the base file name
    matching_files = find_files_by_name(target_base_file_name)

    if matching_files:
        print(f"Files with base name '{target_base_file_name}' found:")
        for file in matching_files:
            print(file)
    else:
        print(f"No files with base name '{target_base_file_name}' found in the file system.")