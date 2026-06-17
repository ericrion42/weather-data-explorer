# Weather Data Explorer

A Python command-line program that automatically downloads historical weather data from NOAA and lets you filter and explore it interactively. Baby's second python program.

---

## About

This project was written by **ericrion42** with the assistance of [Claude.ai](https://claude.ai) as part of a structured Python learning journey. It is intended as a learning project and should not be taken as solely the author's independent work.

---

## Features

- Automatically downloads historical weather data for Atlanta Hartsfield-Jackson International Airport directly from NOAA on startup
- Interactive filter menu lets you search by year, temperature threshold, or precipitation
- Paginated results display 20 rows at a time for readability
- Summary statistics after every filtered result set, including hottest day, coldest day, average high, average low, total precipitation, and number of rainy days
- Dynamic color coding in the summary — temperatures above 90°F display in red, temperatures at or below 32°F display in blue
- Automatically deletes the downloaded CSV when the program exits, leaving no temporary files behind

---

## Requirements

- Python 3.x
- `requests` library

Install the required library with:

```bash
pip install requests
```

---

## How to Run

1. Clone the repository:

```bash
git clone https://github.com/ericrion42/weather-data-explorer.git
```

2. Navigate into the project folder:

```bash
cd weather-data-explorer
```

3. Run the program:

```bash
python main.py
```

---

## How to Use

When the program starts it will automatically download the weather data. You will then see a menu with the following options:

1. **Filter by year** — enter a four digit year to see only records from that year
2. **Filter by temperature** — enter a temperature in Fahrenheit to see all days where the high exceeded that value
3. **Filter by precipitation** — shows only days where measurable rainfall was recorded
4. **Show all records** — displays the full dataset
5. **Quit** — exits the program and deletes the temporary data file

After each filtered result set a summary is displayed showing key statistics for that subset of data. Press **Enter** to page through results or **Q** to return to the menu at any time.

---

## Data Source

Weather data is sourced from the **NOAA Global Historical Climatology Network Daily (GHCN-Daily)** dataset for station **USW00013874** (Atlanta Hartsfield-Jackson International Airport).

Data is fetched directly from:

```
https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access/USW00013874.csv
```

Temperatures are recorded by NOAA in tenths of a degree Celsius and converted to Fahrenheit by the program.

---

## Project Structure

```
weather-data-explorer/
├── main.py        # Main program
└── README.md      # This file
```

---

_Built as part of a personal Python learning project — 2026_
