from bs4 import BeautifulSoup
import requests
from datetime import date
import re

def scrapeMajorLeagueHacking(year:int):
    pass

def scrapeHackathonsUk(year:int) -> None:
    siteContents = requests.get("https://www.hackathons.org.uk/events/{currYear}".format(currYear=year))
    soup = BeautifulSoup(siteContents.content,"html.parser")
    rawText = soup.get_text()
    

        
def main() -> None:
    scrapeHackathonsUk(date.today().year)

if __name__ == "__main__":
    main()