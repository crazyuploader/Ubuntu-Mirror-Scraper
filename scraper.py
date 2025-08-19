import csv
import datetime
import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def fetch_page(url):
    """Fetches the HTML content of a given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully fetched the page from {url}.")
        return response.content
    else:
        print(
            f"Failed to fetch the page from {url}. Status code: {response.status_code}"
        )
        return None


def parse_mirrors(html_content, table_id):
    """Parses the HTML content to extract mirror data from a specified table ID."""
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table", {"id": table_id})

    if not table:
        print(f"No table with id '{table_id}' found.")
        return []

    mirrors_data = []
    rows = table.find_all("tr")

    country = None
    country_speed = None

    for row in rows:
        if "head" in row.get("class", []):
            th_elements = row.find_all("th")
            if len(th_elements) >= 2:
                country = th_elements[0].text.strip()
                country_speed = th_elements[1].text.strip()
            else:
                country = "Unknown"
                country_speed = "Unknown"
            continue

        cols = row.find_all("td")
        # For CD mirrors, there are 3 columns. For archive mirrors, there are 4.
        # We'll handle both cases by checking for at least 3 columns.
        if len(cols) < 3:
            continue

        # Skip rows that are clearly malformed or summary lines
        if country == "Unknown" and not cols[0].text.strip():
            continue

        mirror_name = cols[0].text.strip()
        protocols = [a["href"] for a in cols[1].find_all("a")]
        mirror_speed = cols[2].text.strip()

        # Status column is only present for archive mirrors, not CD mirrors.
        # If it exists, extract it, otherwise set to 'N/A'.
        status = cols[3].text.strip() if len(cols) > 3 else "N/A"

        hostnames = []
        for href in protocols:
            parsed_url = urlparse(href)
            hostname = parsed_url.hostname
            if hostname:
                hostnames.append(hostname)

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
    return mirrors_data


def save_data(mirrors_data, base_directory):
    """Saves the extracted mirror data into CSV, JSON, and TXT formats."""
    if not os.path.exists(f"data/mirrors/{base_directory}"):
        os.makedirs(f"data/mirrors/{base_directory}")

    # CSV
    csv_file = f"data/mirrors/{base_directory}/servers.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
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

    # JSON
    json_file = f"data/mirrors/{base_directory}/servers.json"
    now = datetime.datetime.now(datetime.timezone.utc)
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

    # TXT
    text_file = f"data/mirrors/{base_directory}/servers.txt"
    unique_hostnames = set()
    for mirror in mirrors_data:
        for hostname in mirror["hostnames"]:
            unique_hostnames.add(hostname)
    with open(text_file, mode="w") as file:
        for hostname in unique_hostnames:
            file.write(hostname + "\n")
    print(f"Data saved to {text_file}")
