import os
import subprocess
import json
import psutil

def load_file_system_maps(partitions):
    file_system_maps = {}

    for partition in partitions:
        sanitized_partition = "".join(c if c.isalnum() or c in "-_." else "_" for c in partition)
        file_path = f"file_system_map_{sanitized_partition}.json"
        with open(file_path, "r") as json_file:
            file_system_maps[partition] = json.load(json_file)

    return file_system_maps

def open_file(filename):
    subprocess.run(["start", filename], shell=True)

def prompt_user_for_file(files):
    if len(files) == 1:
        return files[0]

    print("Multiple files found with the same name:")
    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")

    while True:
        choice = input("Enter the number of the file you want to open: ")
        if choice.isdigit() and 1 <= int(choice) <= len(files):
            return files[int(choice) - 1]
        print("Invalid choice. Please enter a valid number.")

def process_open_command(command, file_system_maps):
    open_parts = command.split("open ")
    if len(open_parts) > 1:
        file_to_open = open_parts[1].strip()

        matching_files = []

        for partition, file_system_map in file_system_maps.items():
            for parent_folder, parent_data in file_system_map.items():
                if "files" in parent_data:
                    for file in parent_data["files"]:
                        file_name, _ = os.path.splitext(file)
                        if file_name == file_to_open and not file.endswith(".lnk"):
                            matching_files.append(os.path.join(partition, parent_folder, file))

        if matching_files:
            file_to_open = prompt_user_for_file(matching_files)
            open_file(file_to_open)
            return True

    return False

def main():
    partitions = [part.device for part in psutil.disk_partitions()]
    file_system_maps = load_file_system_maps(partitions)

    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() == "exit":
            break

        # Process "open" command
        if process_open_command(user_input, file_system_maps):
            continue

        # Handle other commands here

if __name__ == "__main__":
    main()
