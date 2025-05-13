from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from GetResponseCode import get_response_code
from selenium import webdriver
import pandas as pd
import math, re

#Establish website path and path to chromedriver
web = "https://steamcharts.com/top"
path = ".../chromedriver.exe"

#Setting up to get response code from website...
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--headless")

#Setting up more capabilities for getting the response code...
caps = DesiredCapabilities.CHROME.copy()
caps['goog:loggingPrefs'] = {'performance': 'ALL'}

for key, value in caps.items():
    chrome_options.set_capability(key, value)


def games(totalGames):    
    games = []
    counts = []
    
    #Service takes driver path, driver connects to driver.exe, then .get to open website
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(web)
    driver.set_page_load_timeout(10)
    
    #Get the response code from scraped page...
    logs = driver.get_log("performance")
    response_code = get_response_code(logs, web)

    if (response_code == 200) or (response_code == 301):
        #After find the html element containing what we need, let driver find these elements
        gameNames = driver.find_elements(by='xpath', value='//td[@class="game-name left"]')
        for game in gameNames:
            games.append(game.text)
            
        playerCounts = driver.find_elements(by='xpath', value='//td[@class="num"]')
        for players in playerCounts:
            counts.append(players.text)
    
    print(games)
    print(counts)


    #Got first page, now get the next 19 pages
    newWeb = (web + "/p.")
    print(newWeb)

    startingPage = 2
    
    if totalGames > 25:
        maxPages = float(totalGames/25)
        maxPages = math.ceil(maxPages)
        maxPages = maxPages + 1
        for x in range(startingPage, maxPages):
            #Get new URL, initiate driver, and check for response code.
            newWeb = (newWeb+str(x))
            service = Service(executable_path=path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(newWeb)
            
            print(newWeb)
            driver.set_page_load_timeout(20)
            
            #Get the response code from scraped page...
            logs = driver.get_log("performance")
            response_code = get_response_code(logs, newWeb)
                
            if (response_code == 200) or (response_code == 301):
                #Getting game names into array...
                gameNames = driver.find_elements(by='xpath', value='//td[@class="game-name left"]')
                for game in gameNames:
                    games.append(game.text)
                    
                #Getting player counts into array...
                playerCounts = driver.find_elements(by='xpath', value='//td[@class="num"]')
                for players in playerCounts:
                    counts.append(players.text)
                newWeb = re.sub(str(x), '', newWeb)
                
                totalArray = [games, counts]
                print(totalArray)
                dataframe = pd.DataFrame({'Game': games, 'Player Counts': counts})
                dataframe.to_csv('PlayerCounts.csv', mode='a', index = False, header=False)
                games = []
                counts = []
    
    

    
    
games(2000)