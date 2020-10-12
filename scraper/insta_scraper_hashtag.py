import urllib
from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup as soup
import os
import requests
import time
import json
import csv

posts = []

####SCRAPE WITH DATA, IIIT will block you otherwise##########

end_cursor = ''
tag = 'lifestyle' #the tag you want to scrape the posts with.
# person = 'kendalljenner' #have to look at scraping users
page_count = 5 #each page roughly corresponds to 60-70 posts, add an exception if you're scraping using obscure tags

for i in range(page_count):
	##dont change this part##
	url = "https://www.instagram.com/explore/tags/{0}/?__a=1&max_id={1}".format(tag, end_cursor) #this url converts annoying infinite scrolling to lovable pages
	# url = "https://www.instagram.com/{0}/?__a=1&max_id={1}".format(person, end_cursor)

	try:
		r = requests.get(url)
	except urllib.error.HTTPError as err:
		print("Error", err.code, err)
		print(url)
		continue
	data = json.loads(r.text)
	end_cursor = data['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor'] # value for the next page
	# print(end_cursor)
	#########################
	#next few lines are standard json parsing, edit as per requirements
	edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges']
	for item in edges:
		if(item['node']['shortcode'] not in posts):
			posts.append(item['node']['shortcode'])
	time.sleep(1) # insurance to not reach a time limit
print(len(posts))

########################################

DIR = 'pictures'
if not os.path.isdir(f'{DIR}'):
		os.makedirs(f'{DIR}')

######task specific part#################
with open('data.csv', 'w') as csvfile:
	csvwriter = csv.writer(csvfile)
	title = ['id', 'text', 'text_hashtag','comment_1','comment_2','comment_3','comment_4','comment_5']
	csvwriter.writerow(title)
	for i in range(1, len(posts)):
		post = posts[i]
		image_DIR = os.path.join(DIR, str(i+1) + ".jpg")
		post_url = "https://www.instagram.com/p/"+str(post)+"/"
		time.sleep(1)
		if i%25 == 0:
		   time.sleep(5)
		#print(url)
		try:
			postClient = urlopen(post_url)
		except urllib.error.HTTPError as err:
			print(url)
			print("Error", err.code, err)
			continue
		post_html = postClient.read()
		# time.sleep(1)
		# if i%25 == 0:
		#    time.sleep(5)
		post_html = post_html.decode("utf8")
		postClient.close()
		post_soup = soup(post_html, "html.parser")
		post_script = post_soup.find('script', text=lambda t: t.startswith('window._sharedData'))
		post_json = post_script.text.split(' = ', 1)[1].rstrip(';')
		post_data = json.loads(post_json)
		#print(post_data)
		try:
			text_data = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
		except:
			text_data = ""
		text_data = text_data.split('#')
		hashtags = ""
		image_url = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['display_url']
		for j in range(len(text_data)):
			if(j > 0):
				tmp = text_data[j]
				tmp = tmp.split(' ')
				if(len(tmp) <= 2):
					hashtags += str(" ") + text_data[j]
				else:
					text_data[0] += str(' ') + text_data[j]
		text = text_data[0]
		try:
			#comment_count = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['count']
			comment_list = post_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_parent_comment']['edges']
			comment_count = len(comment_list)
		except:
			comment_count = 0
			comment_list = []
		#print(comment_list[0]['node']['text'])
		#print(comment_count)
		comments = ['N/A','N/A','N/A','N/A','N/A']
		for j in range(min(comment_count, 5)):
			#tmp = comment_list[i]['node']['text'].split('#')
			#tmp = ' '.join(tmp)
			comments[j] = comment_list[j]['node']['text']
			#comments[i] = tm
		try:
			urlretrieve(str(image_url),image_DIR)

		except IOError as e:
			print("IOError Failed to get image", e)
		except Exception as e:
			print('Exception Failed to get image', e)
		image_id = post

		# print(text) #add try and except for no text
		# print(hashtags)
		# print(comments)
		print("post_num:", i)
		fields = [str(i+1), text, hashtags]
		for j in comments:
			fields.append(j)
		# creating a csv writer object
		csvwriter.writerow(fields)
