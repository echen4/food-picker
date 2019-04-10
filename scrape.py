import requests
import json
import random
from bs4 import BeautifulSoup


def searchCuisine(food, location):
    base = "https://www.yelp.com/search?find_desc={f}&find_loc={loc}"
    url = base.format(f=food, loc=location)
    resp = requests.get(url)
    
    if resp.status_code == 200:
        restDict = {}
        data = resp.text
        
        bsObj = BeautifulSoup(data, "html.parser")
        
        lemons = bsObj.find_all('div', class_='largerScrollablePhotos__373c0__3FEIJ')
        
        if len(lemons) < 1:
            return (False, "There was an issue with your search. Please try again or try a different cuisine/location")
        # Choose the restaurant
        lemon = random.choice(lemons)
        restaurant = lemon.find_all('a', class_='lemon--a__373c0__IEZFH')[0]
        
        # get restaurant name
        restDict['name'] = restaurant.get_text()
        
        # get restaurant URL
        restDict['url'] = 'https://www.yelp.com' + restaurant['href']
        
        # get restaurant telephone + address
        details = lemon.find_all('div', class_='u-space-b1')
        restDict['phone'] = details[0].get_text()
        restDict['address'] = details[1].get_text()
        restDict['area'] = details[2].get_text()
        
        return (True, restDict)
        
    else:
        return (False, "There was an issue with your search. Please try again or try a different cuisine/location")



searchCuisine("Burger", "Boston")