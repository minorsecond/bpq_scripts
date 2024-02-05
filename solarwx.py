#!/usr/bin/python3
# Get solar weather indices

import requests

print(f"Hello, {input()}, and welcome to the solar information application.")

solar_cycle_indices_url = "https://services.swpc.noaa.gov/json/solar-cycle/observed-solar-cycle-indices.json"
predicted_cycle_url = "https://services.swpc.noaa.gov/json/solar-cycle/predicted-solar-cycle.json"

solar_cycles_by_year = requests.get(solar_cycle_indices_url).json()

historical_solar_cycles = {}
historical_dates = {}

months = ("January", "February", "March",
          "April", "May", "June",
          "July", "August", "September",
          "October", "November", "December")

# Get into dictionary form
min_year = 9999
max_year = 0
for year_month in solar_cycles_by_year:
    year = int(year_month["time-tag"].split("-")[0])
    month = int(year_month["time-tag"].split("-")[1])

    if year in historical_dates:
        historical_dates[year].append(month)
    else:
        historical_dates[year] = [month]

    if year < min_year:
        min_year = year
    if year > max_year:
        max_year = year

    historical_solar_cycles[year_month["time-tag"]] = (year_month["ssn"],
                                                       year_month[
                                                           "smoothed_ssn"],
                                                       year_month[
                                                           "observed_swpc_ssn"],
                                                       year_month[
                                                           "smoothed_swpc_ssn"],
                                                       year_month["f10.7"],
                                                       year_month[
                                                           "smoothed_f10.7"])

year = None
requested_year = None
invalid_attempts = 0

year = None
requested_year = None

while not year:
    try:
        requested_year_input = input(
            f"Enter the year between {min_year} and {max_year} for which you'd like information or '0' to exit: ")

        if requested_year_input.strip() == '0':
            print("Exiting the program.", flush=True)
            exit()

        requested_year = int(requested_year_input)

        if min_year <= requested_year <= max_year:
            year = requested_year
        else:
            print(f"Invalid year. Please enter a year between {min_year} and {max_year}.", flush=True)
            invalid_attempts += 1

    except ValueError:
        print("Invalid input. Please enter a numeric year.", flush=True)
        invalid_attempts += 1

    if invalid_attempts >= 3:
        print("Too many invalid attempts. Exiting the program.", flush=True)
        exit()

available_historical_months = historical_dates.get(requested_year)

print(f"Make a selection from the available months for {requested_year} by "
      f"selecting the leading number.\nFor example, enter 1 for January", flush=True)

month_counter = 0
month_name = None
for historical_month in available_historical_months:
    month_name = months[month_counter]
    print(f"{month_counter + 1}\t{month_name}")
    month_counter += 1

month = None
requested_month = None
requested_month_padded = None
invalid_attempts = 0

while not month:
    if invalid_attempts >= 3:
        print("Too many invalid attempts. Exiting.", flush=True)
        exit()

    try:
        requested_month_int = int(input("Month selection (1-12): "))
        requested_month_padded = str(requested_month_int).zfill(2)

        if requested_month_int == 0:
            print("Exiting.", flush=True)
            exit()

        if requested_month_int in available_historical_months:
            month = requested_month_padded
        else:
            print(f"Invalid month. Please choose from the available months for {requested_year}.", flush=True)
            invalid_attempts += 1

    except ValueError:  # Non-integer input
        print("Please enter a valid number for the month.", flush=True)
        invalid_attempts += 1

search_string = f"{requested_year}-{requested_month_padded}"

results = historical_solar_cycles.get(search_string)
historical_intl_ssn = results[0]
historical_intl_smoothed_ssn = results[1]
historical_swpc_ssn = results[2]
historical_swpc_smoothed_ssn = results[3]
historical_f10_7 = results[4]
historical_smoothed_f10_7 = results[5]
print(flush=True)
print("=" * 50, flush=True)
print(f"Solar Report for {month_name}, {requested_year}", flush=True)
print("-" * 50, flush=True)
print(f"International SSN:                {historical_intl_ssn}", flush=True)
print(f"International Smoothed SSN:       {historical_intl_smoothed_ssn}", flush=True)
print(f"SWPC SSN:                         {historical_swpc_ssn}", flush=True)
print(f"SWPC Smoothed SSN:                {historical_swpc_smoothed_ssn}", flush=True)
print(f"Historical F10.7 cm Emissions:    {historical_f10_7}", flush=True)
print(f"Historical Smoothed F10.7 cm Emissions: {historical_smoothed_f10_7}", flush=True)
print("=" * 50, flush=True)

