#!/usr/bin/env python3
from scraper import fetch_page, parse_mirrors, save_data

# URL of the Launchpad Ubuntu Archive Mirrors page
ARCHIVE_MIRRORS_URL = "https://launchpad.net/ubuntu/+archivemirrors"
CD_MIRRORS_URL = "https://launchpad.net/ubuntu/+cdmirrors"


def scrape_and_save(url, base_directory, table_id):
    print(f"\n--- Scraping {url} ---")
    html_content = fetch_page(url)
    if html_content:
        mirrors_data = parse_mirrors(html_content, table_id)
        if mirrors_data:
            save_data(mirrors_data, base_directory)
        else:
            print(f"No mirror data found for {url}.")
    else:
        print(f"Could not fetch content from {url}.")


if __name__ == "__main__":
    # Scrape Archive Mirrors
    scrape_and_save(ARCHIVE_MIRRORS_URL, "archive", "mirrors_list")

    # Scrape CD Mirrors
    scrape_and_save(CD_MIRRORS_URL, "cd", "mirrors_list")
