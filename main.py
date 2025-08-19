#!/usr/bin/env python3

import csv
import datetime
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# URL of the Launchpad Ubuntu Archive Mirrors page
url = "https://launchpad.net/ubuntu/+archivemirrors"

# Fetch the page content
response = requests.get(url)
if response.status_code == 200:
    print(f"Successfully fetched the page from {url}.")
    print("")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")
    exit()

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find the table with id "mirrors_list"
table = soup.find("table", {"id": "mirrors_list"})

# Ensure the table exists before proceeding
if table:
    # Initialize list to store mirror data
    mirrors_data = []

    # Find all rows in the table
    rows = table.find_all("tr")

    # Variables to keep track of the current country and its total speed
    country = None
    country_speed = None

    # Loop through each row and extract relevant information
    for row in rows:
        # Check if the row is a country header (with class="head")
        if "head" in row.get("class", []):
            # Extract country name from the first <th>
            th_elements = row.find_all("th")
            if len(th_elements) >= 2:
                country = th_elements[0].text.strip()  # Country name
                # Country's total speed
                country_speed = th_elements[1].text.strip()
            else:
                country = "Unknown"
                country_speed = "Unknown"
            continue  # Move to the next row for mirror data

        # For mirror details rows, check if the row has the expected number of <td> elements
        cols = row.find_all("td")
        if len(cols) < 4:  # Make sure the row has enough columns (i.e., 4 columns)
            continue

        # Extract mirror name
        mirror_name = cols[0].text.strip()  # Mirror name

        # Extract protocols (URLs)
        protocols = [a["href"] for a in cols[1].find_all("a")]  # Protocol URLs

        # Extract mirror speed
        mirror_speed = cols[2].text.strip()  # Individual mirror speed

        # Extract mirror status
        status = cols[3].text.strip()  # Mirror status

        # Extract hostnames from protocols (http, https, rsync)
        hostnames = []
        for href in protocols:
            parsed_url = urlparse(href)
            hostname = parsed_url.hostname
            if hostname:
                hostnames.append(hostname)

        # Add the extracted data to the mirrors_data list
        mirrors_data.append(
            {
                "country": country,
                "country_speed": country_speed,
                "mirror_name": mirror_name,
                "protocols": protocols,
                "hostnames": list(set(hostnames)),
                "mirror_speed": mirror_speed,
                "status": status,
            }
        )

    # Output the extracted data
    for mirror in mirrors_data:
        print(f"Country: {mirror['country']}")
        print(f"Country Speed: {mirror['country_speed']}")
        print(f"Mirror Name: {mirror['mirror_name']}")
        print(f"Protocols: {', '.join(mirror['protocols'])}")
        print(f"Hostnames: {', '.join(mirror['hostnames'])}")
        print(f"Mirror Speed: {mirror['mirror_speed']}")
        print(f"Status: {mirror['status']}")
        print("-" * 40)

    if not os.path.exists("data/mirrors"):
        os.makedirs("data/mirrors")

    # Define the file path where the CSV will be saved
    csv_file = "data/mirrors/ubuntu_mirrors.csv"

    # Open the file in write mode and save the data
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(
            [
                "Country",
                "Country Speed",
                "Mirror Name",
                "Protocols",
                "Hostnames",
                "Mirror Speed",
                "Status",
            ]
        )

        # Write the mirror data
        for mirror in mirrors_data:
            writer.writerow(
                [
                    mirror["country"],
                    mirror["country_speed"],
                    mirror["mirror_name"],
                    ", ".join(mirror["protocols"]),
                    ", ".join(mirror["hostnames"]),
                    mirror["mirror_speed"],
                    mirror["status"],
                ]
            )

    print(f"Data saved to {csv_file}")

    # Define the file path where the JSON will be saved
    json_file = "data/mirrors/ubuntu_mirrors.json"

    # Current time
    now = datetime.datetime.now(datetime.timezone.utc)

    # Open the file in write mode and save the data as JSON
    with open(json_file, mode="w") as file:
        json.dump(
            {
                "mirrors": mirrors_data,
                "count": len(mirrors_data),
                "last_updated": now.isoformat(),
            },
            file,
            indent=4,
        )

    print(f"Data saved to {json_file}")

    # Define the file path where the text file will be saved
    text_file = "data/mirrors/ubuntu_mirrors.txt"
    unique_hostnames = set()

    # Collect all unique hostnames from mirrors_data
    for mirror in mirrors_data:
        for hostname in mirror["hostnames"]:
            unique_hostnames.add(hostname)

    # Open the file in write mode and save the data as a text file
    with open(text_file, mode="w") as file:
        for hostname in unique_hostnames:
            file.write(hostname + "\n")

    print(f"Data saved to {text_file}")
else:
    print("No table with id 'mirrors_list' found.")
