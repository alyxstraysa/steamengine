from requests import get
from bs4 import BeautifulSoup
import numpy as np
import json
import time

steam_id_list = []

with open('/Users/kitsundere/Documents/dscrape/steam_id list.json') as handle:
    steam_dict = json.loads(handle.read())

for app in steam_dict['applist']['apps']:
	steam_id_list.append(app['appid'])

scraped_info = []

for steam_id in steam_id_list[1:10]:

	#delay to avoid ban
	time_sleep = 1 + np.random.uniform()
	print("Sleeping for {}".format(time_sleep))
	time.sleep(time_sleep)

	url = 'https://store.steampowered.com/app/' + str(steam_id)
	response = get(url)
	response.text

	html_soup = BeautifulSoup(response.text, 'html.parser')

	game_description = html_soup.find(id='game_area_description') #get the description for the game

	game_description_str = game_description.get_text()
	scraped_info.append(game_description_str)

#replace tabs and new lines
stripped_review = [review.replace('\n', '').replace('\r', '').replace('\t', '') for review in scraped_info]

with open('reviewtext.txt', 'w') as f:
	for review in stripped_review:
	    	f.write(review)
	    	f.write("\n")
	    	f.write("\n")