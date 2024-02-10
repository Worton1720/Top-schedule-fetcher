# Top Schedule Fetcher

Top Schedule Fetcher is a Python program designed to retrieve schedules from the TOP Academy server. It offers functionalities to fetch daily or weekly schedules, display them neatly, and save them in JSON format.

![Screenshot](https://github.com/Worton1720/Top-schedule-fetcher/assets/124402406/39330841-6252-4a77-a52a-243c38a3123e)


## Features
- Fetch schedules for a specific day or the current week.
- Display schedules with colorful formatting.
- Save schedules to JSON files for future reference.

## Installation
1. Clone the repository: `git clone <repository-url>`
2. Navigate to the project directory: `cd top-schedule-fetcher`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
Run the program with Python:
Python main.py

Follow the on-screen instructions to choose the action and input dates if needed.

## Options
- `--date`: Specify a date in the format YYYY-MM-DD to fetch the schedule for a specific day.
- `--url`: Customize the URL for requests to the server.
- `--headers`: Provide custom headers for requests to the server.

## Dependencies
- requests
- argparse
- colorama
- tabulate
