from requests import get
from bs4 import BeautifulSoup
import numpy as np
import json
import time
import csv
from selenium import webdriver
 
# prepare the option for the chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')

# start chrome browser
browser = webdriver.Chrome(options=options)
browser.get("https://store.steampowered.com/app/646570/Slay_the_Spire/") 
html = browser.page_source


cookies = { 'birthtime': '283993201', 'mature_content': '1' }

html_soup = BeautifulSoup(html, 'html.parser')

game_description = html_soup.find_all("div", {"class": "content"}) 

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

with open('review.csv','w') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(['steam_id','tags','review'])
    for row in scraped_info:
        csv_out.writerow(row)