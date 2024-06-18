from bs4 import BeautifulSoup
import requests
from datetime import date
import discord
import os
from dotenv import load_dotenv

#def scrapeMajorLeagueHacking(year:int):
#    pass

def scrapeHackathonsUk(year:int) -> str:
    siteContents = requests.get("https://www.hackathons.org.uk/events/{currYear}".format(currYear=year))
    soup = BeautifulSoup(siteContents.content,"html.parser")
    rawText = soup.get_text()
    information = rawText.split(">>")
    information[0] = information[0].split("Past Events")[1]
    information = information[0:-1]
    return str(information)

load_dotenv()

hackBot = discord.Bot()

@hackBot.slash_command(name="hi",description="testing")#works
async def hi(sourceChannel:discord.ApplicationContext):
    await sourceChannel.respond("Hi!")

@hackBot.slash_command(name="hacks",desciption="returns scraped text from hackathons uk webpage")#works, but need to add explicit permission for channel
async def hacks(sourceChannel:discord.ApplicationContext):
    await sourceChannel.respond(scrapeHackathonsUk(date.today().year))

hackBot.run(os.getenv("TOKEN"))