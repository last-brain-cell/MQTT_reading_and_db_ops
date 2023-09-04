import os
import time
import openpyxl
from pymongo import MongoClient

# Define file paths
excel_file_path = "HHDG - SpareInventory - excel.xlsx"
timestamp_file_path = "last_modified.txt"

# Connect to MongoDB
db_client = MongoClient("mongodb://127.0.0.1:27017/")
db = db_client["Product_Management"]
collection = db["products"]


def check_for_excel_updates():
    # Get the current modification timestamp of the Excel file
    current_timestamp = os.path.getmtime(excel_file_path)

    try:
        # Read the stored timestamp from the file
        with open(timestamp_file_path, 'r') as file:
            stored_timestamp = float(file.read())
    except FileNotFoundError:
        # If the timestamp file doesn't exist, consider it as the first run
        stored_timestamp = None

    # If the file has been modified or it's the first run
    if stored_timestamp is None or current_timestamp > stored_timestamp:
        print("Excel file has been modified. Updating the database...")

        try:
            # Load the Excel workbook
            workbook = openpyxl.load_workbook(excel_file_path)

            # Your logic to update the database goes here

            # Update the stored timestamp with the current timestamp
            with open(timestamp_file_path, 'w') as file:
                file.write(str(current_timestamp))

            print("Database updated successfully.")
        except Exception as e:
            print(f"An error occurred while updating the database: {str(e)}")


if __name__ == "__main__":
    # Run the update check every 10 sec
    while True:
        check_for_excel_updates()
        time.sleep(10)  # Sleep for 10 sec before the next check
