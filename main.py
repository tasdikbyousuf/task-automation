import os
import shutil
from send2trash import send2trash
import schedule
import time
from datetime import datetime


def organize_files(path):
    """
    Organizes files into folders based on their types.

    Args:
    path (str): The path to the directory to organize.
    """
    # Dictionary mapping file extensions to folder names
    file_types = {
        ".txt": "TextFiles",
        ".doc": "Documents",
        ".docx": "Documents",
        ".pdf": "Documents",
        ".jpg": "Images",
        ".jpeg": "Images",
        ".png": "Images",
        ".gif": "Images",
        ".mp4": "Videos",
        ".avi": "Videos",
        ".mkv": "Videos",
        ".mp3": "Music",
        ".wav": "Music",
        ".flac": "Music",
        ".zip": "Archives",
        ".rar": "Archives",
        ".exe": "Executables",
        ".py": "Scripts",
        ".java": "Scripts",
        ".cpp": "Scripts",
        ".c": "Scripts"
    }

    # Create folders for each file type if they don't exist
    for folder_name in file_types.values():
        folder_path = os.path.join(path, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    # Organize files into folders
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in file_types:
                dest_folder = file_types[file_ext]
                dest_path = os.path.join(path, dest_folder)
                shutil.move(file_path, dest_path)
                print(f"Moved '{file}' to '{dest_folder}' folder")


def recycle_files(path):
    """
    Recycles files and directories in a drive.

    Args:
    path (str): The path to the drive to recycle.
    """
    print(f"Recycling started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for drive {path}")

    for root, _, files in os.walk(path):
        for item in files:
            item_path = os.path.join(root, item)
            send2trash(item_path)
            print(f"Moved '{item_path}' to recycle bin")

        for directory in os.listdir(root):
            directory_path = os.path.join(root, directory)
            if os.path.isdir(directory_path):
                send2trash(directory_path)
                print(f"Removed directory '{directory_path}'")

    print(f"Recycling completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} for drive {path}")


def schedule_recycle_drive(drive_path, interval_minutes):
    """
    Schedules recycling for a drive at intervals.

    Args:
    drive_path (str): The path to the drive to recycle.
    interval_minutes (int): The interval in minutes for recycling.
    """
    print(f"Scheduling recycling for drive {drive_path} every {interval_minutes} minutes.")
    schedule.every(interval_minutes).minutes.do(recycle_files, drive_path)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    print("1. Organize files")
    print("2. Recycle files")
    print("3. Organize and recycle files")

    choice = input("Enter your choice: ").strip()

    # Add initial action at the start
    drive_path = input("Enter the path to the drive to perform initial action (e.g., C:/, D:/): ").strip()
    if choice == "2" or choice == "3":  # Check if recycling is chosen
        recycle_files(drive_path)  # For example, performing initial recycling

    if choice == "1":
        organize_files(drive_path)
    elif choice == "2":
        interval_minutes = int(input("Enter the interval in minutes: ").strip())
        schedule_recycle_drive(drive_path, interval_minutes)
    elif choice == "3":
        organize_files(drive_path)
        interval_minutes = int(input("Enter the interval in minutes for recycling: ").strip())
        schedule_recycle_drive(drive_path, interval_minutes)
    else:
        print("Invalid choice. Please choose a valid option.")
