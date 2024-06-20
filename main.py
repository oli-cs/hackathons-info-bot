from bs4 import BeautifulSoup
import requests
import discord
import os
from dotenv import load_dotenv
import re

#def scrapeMajorLeagueHacking(year:int):
#    pass

def scrapeHackathonsUk(year:int) -> str:
    siteContents = requests.get("https://www.hackathons.org.uk/events/{currYear}".format(currYear=year))
    soup = BeautifulSoup(siteContents.content,"html.parser")
    rawText = soup.get_text()
    return rawText

def getHacksArr(information:str) -> list:
    hackathons = []
    information = information.replace("Hackathons UK - Official Partner","")
    information = information.replace("website","")
    informationArray = information.split(">>")
    informationArray[0] = informationArray[0].split("Past Events")[1]
    informationArray = informationArray[0:-1]

    searchExpsDate = ["[0-9] [a-zA-Z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z]",#i.e. 1 jan - 2 jan
                      "[0-9] [a-zA-Z][a-z][a-z] - [0-3][0-9] [a-zA-Z][a-z][a-z]",#i.e. 9 jan - 10 jan
                      "[0-3][0-9] [a-zA-Z][a-z][a-z] - [0-3][0-9] [a-zA-Z][a-z][a-z]",#i.e. 23 jan - 24 jan
                      "[0-3][0-9] [a-zA-Z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z]",#i.e. 31 jan - 1 feb
                      "[0-9] [a-zA-Z][a-z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z][a-z]", #i.e. 1 sept - 2 sept
                      "[0-9] [a-zA-Z][a-z][a-z][a-z] - [0-3][0-9] [a-zA-Z][a-z][a-z][a-z]",#i.e. 9 sept - 10 sept
                      "[0-3][0-9] [a-zA-Z][a-z][a-z][a-z] - [0-3][0-9] [a-zA-Z][a-z][a-z][a-z]",#i.e. 23 sept - 24 sept
                      "[0-3][0-9] [a-zA-Z][a-z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z][a-z]",#i.e. 30 june - 1 july
                      "[0-3][0-9] [a-zA-Z][a-z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z]",#i.e. 30 sept - 1 oct
                      "[0-3][0-9] [a-zA-Z][a-z][a-z] - [0-9] [a-zA-Z][a-z][a-z][a-z]"]#i.e. 30 aug - 1 sept

    for info in informationArray:
        infoDict = {}
        name = ""
        strContainingDate = ""

        print(info)
        
        try:
            name =  info.split("In-Person")[0]
            strContainingDate = info.split("In-Person")[1]
        except:
            try:
                name =  info.split("Hybrid")[0]
                strContainingDate = info.split("Hybrid")[1]
            except:
                name =  info.split("Online")[0]
                strContainingDate = info.split("Online")[1]

        infoDict["name"] = name
        for expression in searchExpsDate:
            matchingStrObj = re.search(expression,strContainingDate)
            if matchingStrObj != None:
                infoDict["date"] = matchingStrObj.group()
                break
        
        hackathons.append(infoDict)

    return hackathons

def getMoreInfo(year:int) -> str:
    return "See https://www.hackathons.org.uk/events/{year} for more information".format(year = str(year))

def formatOutput(data:list,year:int) -> str:
    outputStr = "Here's a list of hackathons sponsored by Hackathons UK for the {year} season: \n".format(year = str(year))
    for row in data:
        outputStr += "- {name}, {date} \n".format(name = row["name"], date = row["date"])

    outputStr += getMoreInfo(year)

    return outputStr

load_dotenv()

hackBot = discord.Bot()

@hackBot.slash_command(name="hi",description="testing")#works
async def hi(sourceChannel:discord.ApplicationContext):
    await sourceChannel.respond("Hi!")

@hackBot.slash_command(name="hacks",desciption="returns scraped text from hackathons uk webpage")#works, but need to add explicit permission for channel
async def hacks(sourceChannel:discord.ApplicationContext,year:int):
    try:
        await sourceChannel.respond(formatOutput(getHacksArr(scrapeHackathonsUk(year)),year))
    except:
        await sourceChannel.respond("Something went wrong\n" + getMoreInfo(year))

hackBot.run(os.getenv("TOKEN"))