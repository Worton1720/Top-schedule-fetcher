# Top Schedule Fetcher

Top Schedule Fetcher is a Python program designed to retrieve schedules from the TOP Academy server. It offers functionalities to fetch daily or weekly schedules, display them neatly, and save them in JSON format.

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
