import requests
from bs4 import BeautifulSoup
import csv

# Worldometers URL
url = "https://www.worldometers.info/geography/alphabetical-list-of-countries/"
headers = {"User-Agent": "Mozilla/5.0"}

# Request the page
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing countries
table = soup.find("table")

countries = []

# Loop through each row in the table
for row in table.find_all("tr")[1:]:  # skip header
    cols = row.find_all("td")
    if cols:
        country_name = cols[1].get_text(strip=True)  # 2nd column = country
        countries.append(country_name)

# Save to CSV
with open("countries_worldometers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Country"])
    for country in countries:
        writer.writerow([country])

print("Scraping complete! Total countries:", len(countries))
