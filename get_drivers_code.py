import fastf1

# Enable cache for fast loading
fastf1.Cache.enable_cache('cache/')  # Adjust the cache directory as needed

# Specify the season you want to fetch
season = 2023  # Example: 2023 season

# Load the schedule of the given season
schedule = fastf1.get_event_schedule(season)

# Filter out testing sessions
grand_prix_schedule = schedule[schedule['EventFormat'] != 'testing']

# Extract Grand Prix names
grand_prix_names = grand_prix_schedule['EventName'].tolist()
print(f"Grand Prix Names in {season} season:")
for gp in grand_prix_names:
    print(gp)

# Extract driver names and codes
driver_info_list = set()  # Use a set to avoid duplicates
for _, event in grand_prix_schedule.iterrows():
    race = fastf1.get_session(season, event['RoundNumber'], 'R')
    race.load(weather=False, telemetry=False, messages=False)  # Load the session to access driver data
    for driver in race.drivers:
        driver_info = race.get_driver(driver)
        driver_name = f"{driver_info['FirstName']} {driver_info['LastName']}"
        driver_code = driver_info['Abbreviation']
        driver_info_list.add((driver_name, driver_code))

print(f"\nDrivers in {season} season:")
for driver_name, driver_code in sorted(driver_info_list):
    print(f"{driver_name} ({driver_code})")
