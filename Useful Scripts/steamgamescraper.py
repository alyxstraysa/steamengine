from requests import get
from bs4 import BeautifulSoup
import numpy as np
import json
import time
import csv

steam_id_list = []

with open('/Users/kitsundere/Documents/dscrape/steam_id list.json') as handle:
    steam_dict = json.loads(handle.read())

for app in steam_dict['applist']['apps']:
	steam_id_list.append(app['appid'])

scraped_info = []
iteration = 0

cookies = { 'birthtime': '283993201', 'mature_content': '1' }

#setseed
np.random.seed(123)

#sample 10,000 indices : to be implemented
random_ids = np.random.choice(76026, 10000, replace=False)  

#for steam_id in steam_id_list:
#edit this when you want to use the whole set

for steam_id in steam_id_list:

	try:
		#delay to avoid ban
		time_sleep = 0.01 + np.random.uniform()/2
		print("Sleeping for {}".format(time_sleep))

		#100 iterations
		if (iteration % 100 == 0):
			print("Iteration {}".format(iteration))
		time.sleep(time_sleep)
		print("Finished Analyzing")

		url = 'https://store.steampowered.com/app/' + str(steam_id)
		response = get(url, cookies=cookies)
		response.text

		html_soup = BeautifulSoup(response.text, 'html.parser')

		game_description = html_soup.find(id='game_area_description') #get the description for the game
		#html_soup.find_all(lambda tag: tag.name =='div' and tag.get('class') == 'game_area_description')  
		
		try:
			#get the steamID tags
			tags = html_soup.find_all('a', {'class':'app_tag'})
			output_tags = []

			for tag in tags:
				st = tag.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
				output_tags.append(st)
		except:
			pass

		game_description_str = game_description.get_text().replace('\n', '').replace('\r', '').replace('\t', '')
		scraped_info.append((steam_id, ','.join(output_tags), game_description_str))
		
	except:
		pass

	iteration += 1

#replace tabs and new lines

#with open('reviewtext.txt', 'w') as f:
#	for review in stripped_review:
#	    	f.write(review)
#	    	f.write("\t")

with open('review.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['steam_id','tags','review'])
    for row in scraped_info:
        csv_out.writerow(row)