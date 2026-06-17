import requests
import os

# Configuration
URL = "https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/USW00013874.csv"
FILENAME = "weather_data.csv"

def download_data():
    print("Downloading weather data...")
    response = requests.get(URL)  
    with open(FILENAME, "w") as f:
        f.write(response.text)
    print("Download complete!")

def delete_data():
    if os.path.exists(FILENAME):
        os.remove(FILENAME)
        print("Temporary data file deleted.")

def main():
    try:
        download_data()
        print("Program running! Features to come soon...")
    finally:
        delete_data()

main()