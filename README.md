# Google Maps Data Extraction

This Python script automates the extraction of place data from Google Maps. It retrieves information about places based on location and search keywords, handles pagination, and saves results to a CSV file for easy analysis.

## Overview

The script performs the following tasks:
1. Fetches place data from Google Maps using location and search keywords.
2. Handles pagination to retrieve multiple pages of search results.
3. Extracts relevant details such as place names, addresses, websites, phone numbers, and opening hours.
4. Saves the extracted data into a CSV file.

## Features

- **Location-Based Search**: Retrieves data based on latitude, longitude, and zoom level.
- **Keyword Search**: Searches for places matching a specified keyword (e.g., "restaurants", "colleges").
- **Pagination Support**: Handles multiple pages of results.
- **Data Extraction**: Extracts details including names, addresses, websites, phone numbers, and opening times.
- **CSV Export**: Saves the collected data in a CSV file for further analysis.

## Requirements

- Python 3.x
- Required Python libraries:
  - `requests`
  - `pandas`
  - `re` (standard library)
  - `json` (standard library)
  - `math` (standard library)

Install the required libraries using pip:

```bash
pip install requests pandas
