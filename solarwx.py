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
while not year:
    requested_year = int(input(
        f"Enter the year between {min_year} and {max_year} for which you'd like information: "))
    if requested_year == 0:
        exit()
    elif requested_year in [*range(min_year, max_year + 1, 1)] and type(
            requested_year) == int:
        year = requested_year

available_historical_months = historical_dates.get(requested_year)

print(f"Make a selection from the available months for {requested_year} by "
      f"selecting the leading number.\nFor example, enter 1 for January")

month_counter = 0
month_name = None
for historical_month in available_historical_months:
    month_name = months[month_counter]
    print(f"{month_counter + 1}\t{month_name}")
    month_counter += 1

month = None
requested_month = None

while not month:
    requested_month = input("Month selection: ").zfill(2)
    print(requested_month)
    if requested_month == str(00):
        exit()
    elif requested_month in [str(month).zfill(2) for month in
                             available_historical_months]:
        month = requested_month

search_string = f"{requested_year}-{requested_month}"

results = historical_solar_cycles.get(search_string)
historical_intl_ssn = results[0]
historical_intl_smoothed_ssn = results[1]
historical_swpc_ssn = results[2]
historical_swpc_smoothed_ssn = results[3]
historical_f10_7 = results[4]
historical_smoothed_f10_7 = results[5]
print("\n")
print("================================================")
print(f"Solar report for {month_name}, {requested_year}")
print(f"International SSN:\t\t\t{historical_intl_ssn}")
print(f"International Smoothed SSN:\t\t{historical_intl_smoothed_ssn}")
print(f"SWPC SSN:\t\t\t\t{historical_swpc_ssn}")
print(f"SWPC smoothed SSN:\t\t\t{historical_swpc_smoothed_ssn}")
print(f"Historical F10.7 cm emissions:\t\t{historical_f10_7}")
print(f"Historical smoothed F10.7 cm emissions:\t{historical_smoothed_f10_7}")
print("================================================")
