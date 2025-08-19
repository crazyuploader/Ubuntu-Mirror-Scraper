# Ubuntu Mirrors Scraper

> Python program to scrape Ubuntu mirrors from https://launchpad.net/ubuntu/+archivemirrors

## Usage

```bash
pip install --upgrade pipenv
pipenv install
pipenv run ./main.py
```

## Mirrors

### Archive

- [CSV File](data/mirrors/archive/servers.csv)
- [JSON File](data/mirrors/archive/servers.json)
- [Txt File](data/mirrors/archive/servers.txt)

### CD (ISO)

- [CSV File](data/mirrors/cd/servers.csv)
- [JSON File](data/mirrors/cd/servers.json)
- [Txt File](data/mirrors/cd/servers.txt)

## Technologies Used

- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/en/latest/)
