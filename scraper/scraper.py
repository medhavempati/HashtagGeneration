import instaloader
import pandas as pd
import sys
import os
import re

class InstaloaderException(Exception):
	'''Copied from source code to hadnle error'''
	pass

class QueryReturnedNotFoundException(InstaloaderException):
	'''Copied from source code to hadnle error'''
	pass

def scraper(username = None, maxPostLimit = None, maxCommentLimit = None):
    L = instaloader.Instaloader(sleep = False,max_connection_attempts = 10)
    profile = instaloader.Profile.from_username(L.context, username)
    colName = ['ID','shortcode','text','hashtags','comments','likes']
    df = pd.DataFrame(columns = colName)
    seq = 1
    for post in profile.get_posts():
        postid,shortcode,caption,likes,hashtagList = '','','',0,''
        listOfComments = ''
        try:
            allComments = post.get_comments()
            caption = post.caption
            i = 0
            for itr in allComments:
                listOfComments = '|'.join([listOfComments.replace(',',''),itr[2]])	# comment text
                if i > maxCommentLimit:
                    break
            likes = post.likes
            hashtagList = ' '.join([hashtag for hashtag in post.caption_hashtags])
			# print(hashtagList)
            if listOfComments and hashtagList:
                df.loc[seq] = ['','',caption.replace(',',''),hashtagList,listOfComments,likes]
                if seq % 10 == 0:
                    print(seq)
                seq += 1
            if seq == maxPostLimit:
                break
        except QueryReturnedNotFoundException:
            continue
        except Exception as e:
            print(e)
    
    if not os.path.isdir('./data'):
        os.mkdir('./data')

    df.to_csv(f'data/{username}.csv', sep =',',encoding = 'utf-8')


if __name__ == '__main__':


	user,maxPostLimit,maxCommentLimit,seedHashtag = '',0,0,[]

	try:
		user = sys.argv[1]							# Mandatory argument
	except IndexError:
		print('Error: Scraper Needs a User Name')
		sys.exit(1)

	try:
		maxPostLimit = int(sys.argv[2])				# Optional argument
	except IndexError:
		maxPostLimit = 100
	except:
		raise

	try:
		maxCommentLimit = int(sys.argv[3])			# Optional argument
	except IndexError:
		maxCommentLimit = 10
	except:
		raise

	scraper(user,maxPostLimit,maxCommentLimit)