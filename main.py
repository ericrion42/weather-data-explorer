import requests
import os
import csv

# Configuration
URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/USW00013874.csv"
FILENAME = "weather_data.csv"

def download_data():
    print("Downloading weather data...")
    response = requests.get(URL)  
    with open(FILENAME, "w") as f:
        f.write(response.text)
    print("Download complete!")

def read_data():
    records = []
    with open(FILENAME, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = {
                    "date": row["DATE"],
                    "tmax": (float(row["TMAX"]) / 10) * 9/5 + 32,  # Convert to Fahrenheit
                    "tmin": (float(row["TMIN"]) / 10) * 9/5 + 32,  # Convert to Fahrenheit
                    "prcp": float(row["PRCP"]) / 10 if row["PRCP"] else 0.0
                }
                records.append(record)
            except (ValueError, KeyError):
                continue
    return records

def display_records(records):
    print(f"\n{'DATE':<12} {'HIGH (F)':<12} {'LOW (F)':<12} {'PRECIP (in)'}")
    print("-" * 48)
    for r in records:
        print(f"{r['date']:<12} {r['tmax']:<12.1f} {r['tmin']:<12.1f} {r['prcp']:.2f}")
        
def delete_data():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print("Temporary data file deleted.")

def get_user_filter(records):
    print("\nHow would you like to filter the data?")
    print("1. Filter by year")
    print("2. Filter by temperature (show days above a high temp)")
    print("3. Filter by precipitation (show days it rained)")
    print("4. Show all records")   
    print("5. Quit")

    while True:
        choice = input("Enter your choice (1-5): ")
        if choice in ["1", "2", "3", "4", "5"]:
            break
        print("Invalid choice, please enter a number between 1 and 5.")

    if choice == "1":
        year = input("Enter a year (e.g. 2023):")
        return [r for r in records if r["date"].startswith(year)]
    elif choice == "2":
        temp = float(input("Show days where high temp exceeded (F):"))
        return [r for r in records if r["tmax"] > temp]
    elif choice == "3":
        return [r for r in records if r["prcp"] > 0.0]
    elif choice == "4":
        return records
    elif choice == "5":
        print("Goodbye!")
        exit()

def main():
    try:
        download_data()
        records = read_data()
        while True:
            filtered = get_user_filter(records)
            display_records(filtered)
            input("\nPress Enter to continue...")
    finally:
        delete_data()

main()