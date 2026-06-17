import requests
import os
import csv

# Colors
YELLOW = "\033[93m" # Menus and inputs
RED = "\033[91m" # Errors
ORANGE = "\033[38;5;214m" # System notifications
GREEN = "\033[92m" # Success messages
BLUE = "\033[94m" # Reserved for coldest day
RESET = "\033[0m" # Reset color

# Configuration
URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/USW00013874.csv"
FILENAME = "weather_data.csv"

def download_data():
    print(f"{GREEN}Downloading weather data...{RESET}")
    response = requests.get(URL)  
    with open(FILENAME, "w") as f:
        f.write(response.text)
    print(f"{GREEN}Download complete!{RESET}")

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

def temp_color_high(temp):
    if temp >= 90:
        return RED
    return RESET

def temp_color_low(temp):
    if temp <= 32:
        return BLUE
    return RESET    

def display_summary(records):
    if len(records) == 0:
        return
    
    temps_max = [r["tmax"] for r in records]
    temps_min = [r["tmin"] for r in records]
    precip = [r["prcp"] for r in records]

    hottest = max(temps_max)              
    coldest = min(temps_min)             
    avg_high = sum(temps_max) / len(temps_max)
    avg_low = sum(temps_min) / len(temps_min)
    total_precip = sum(precip)
    rainy_days = len([p for p in precip if p > 0])

    hottest_day = next(r for r in records if r["tmax"] == hottest)
    coldest_day = next(r for r in records if r["tmin"] == coldest)

    print(f"\n{ORANGE}--- Summary ---{RESET}")
    print(f"{YELLOW}Hottest day:{RESET}       {RED}{hottest_day['date']} ({hottest:.1f}°F){RESET}")
    print(f"{YELLOW}Coldest day:{RESET}       {BLUE}{coldest_day['date']} ({coldest:.1f}°F){RESET}")
    print(f"{YELLOW}Average high:{RESET}      {temp_color_high(avg_high)}{avg_high:.1f}°F{RESET}")
    print(f"{YELLOW}Average low:{RESET}       {temp_color_low(avg_low)}{avg_low:.1f}°F{RESET}")
    print(f"{YELLOW}Total precip:{RESET}      {total_precip:.2f} in")
    print(f"{YELLOW}Rainy days:{RESET}        {rainy_days} days")

def display_records(records):
    page_size = 20
    total = len(records)

    if total == 0:
        print(f"\n{RED}No records found matching that filter.{RESET}")
        return
    
    for i in range(0, total, page_size):
        page = records[i:i + page_size]
        print(f"\n{'{YELLOW}DATE{RESET}':<12} {'HIGH (F)':<12} {'LOW (F)':<12} {'PRECIP (in)'}")
        print("-" * 48)
        for r in page:
            print(f"{r['date']:<12} {r['tmax']:<12.1f} {r['tmin']:<12.1f} {r['prcp']:.2f}")

        remaining = total - (i + page_size)
        if remaining > 0:
            print(f"\n{ORANGE}--- {remaining} more records ---{RESET}")
            cont = input(f"{YELLOW}Press Enter for next page or Q to return to menu: {RESET}")
            if cont.strip().upper() == "Q":
                return
        else:
            print(f"\n{ORANGE}--- End of results ({total} records total){RESET}")
    
    
    for r in records:
        print(f"{r['date']:<12} {r['tmax']:<12.1f} {r['tmin']:<12.1f} {r['prcp']:.2f}")
        
def delete_data():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print(f"{GREEN}Temporary data file deleted.{RESET}")

def get_user_filter(records):
    print(f"\n{YELLOW}How would you like to filter the data?{RESET}")
    print(f"{YELLOW}1.{RESET} Filter by year")
    print(f"{YELLOW}2.{RESET} Filter by temperature (show days above a high temp)")
    print(f"{YELLOW}3.{RESET} Filter by precipitation (show days it rained)")
    print(f"{YELLOW}4.{RESET} Show all records")
    print(f"{YELLOW}5.{RESET} Quit")

    while True:
        choice = input(f"{YELLOW}Enter your choice (1-5): {RESET}")
        if choice in ["1", "2", "3", "4", "5"]:
            break
        print(f"{RED}Invalid choice, please enter a number between 1 and 5.{RESET}")

    if choice == "1":
        year = input(f"{YELLOW}Enter a year (e.g. 2023):{RESET}")
        return [r for r in records if r["date"].startswith(year)]
    elif choice == "2":
        temp = float(input(f"{YELLOW}Show days where high temp exceeded (F):{RESET}"))
        return [r for r in records if r["tmax"] > temp]
    elif choice == "3":
        return [r for r in records if r["prcp"] > 0.0]
    elif choice == "4":
        return records
    elif choice == "5":
        print(f"{GREEN}Goodbye!{RESET}")
        exit()

def main():
    try:
        download_data()
        records = read_data()
        while True:
            filtered = get_user_filter(records)
            display_records(filtered)
            display_summary(filtered)
    finally:
        delete_data()

main()