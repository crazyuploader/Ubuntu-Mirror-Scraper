# Ubuntu Mirrors Scraper

A Python program designed to automatically scrape and organize a comprehensive list of Ubuntu archive and CD (ISO) mirrors directly from the official Launchpad website. This tool helps users and systems identify and utilize up-to-date mirror servers for faster and more reliable access to Ubuntu packages and ISO images.

## Features

*   **Automated Scraping:** Automatically fetches mirror data from Launchpad.
*   **Dual Mirror Support:** Scrapes both archive (package) and CD (ISO) mirrors.
*   **Multiple Output Formats:** Generates mirror lists in CSV, JSON, and plain text formats for easy consumption by various applications and scripts.
*   **Organized Output:** Stores mirror data in a structured `data/mirrors` directory, separated by mirror type.

## Usage

To run this scraper and generate the mirror lists, follow these steps:

1.  **Install pipenv:** If you don't have `pipenv` installed, you can install it using pip:
    ```bash
    pip install --upgrade pipenv
    ```
2.  **Install Dependencies:** Navigate to the project root directory and install the required Python packages using pipenv:
    ```bash
    pipenv install
    ```
3.  **Run the Scraper:** Execute the `main.py` script using pipenv. This will initiate the scraping process and generate the mirror files in the `data/mirrors` directory.
    ```bash
    pipenv run python main.py
    ```

## Output Files

The scraper generates the following files, categorized by mirror type:

### Archive Mirrors

These files contain a list of mirrors for Ubuntu package archives.

*   [CSV File](data/mirrors/archive/servers.csv): Comma-separated values, suitable for spreadsheet applications or data analysis.
*   [JSON File](data/mirrors/archive/servers.json): JavaScript Object Notation, ideal for programmatic access and web applications.
*   [Txt File](data/mirrors/archive/servers.txt): Plain text file, with one mirror URL per line.

### CD Mirrors

These files contain a list of mirrors for Ubuntu CD/DVD (ISO) images.

*   [CSV File](data/mirrors/cd/servers.csv)
*   [JSON File](data/mirrors/cd/servers.json)
*   [Txt File](data/mirrors/cd/servers.txt)

## Technologies Used

*   [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/): For parsing HTML and XML documents.
*   [Requests](https://requests.readthedocs.io/en/latest/): For making HTTP requests to fetch web pages.
