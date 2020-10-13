import instaloader
import pandas as pd
import sys
import os
import re
import time

class InstaloaderException(Exception):
	'''Copied from source code to hadnle error'''
	pass

class QueryReturnedNotFoundException(InstaloaderException):
	'''Copied from source code to hadnle error'''
	pass

def scraper(username = None, maxPostLimit = None, maxCommentLimit = None, set_no = None):
    L = instaloader.Instaloader(sleep = False,max_connection_attempts = 10)
    profile = instaloader.Profile.from_username(L.context, username)
    colName = ['ID','shortcode','text','hashtags','comments','likes']
    df = pd.DataFrame(columns = colName)
    seq = 1
    for post in profile.get_posts():
        sleep(15)
        postid,shortcode,caption,likes,hashtagList = '','','',0,''
        listOfComments = ''
        try:
            allComments = post.get_comments()
            sleep(15)
            caption = post.caption
            i = 0
            for itr in allComments:
                listOfComments = '|'.join([listOfComments.replace(',',''),itr[2]])	# comment text
                if i > maxCommentLimit:
                    break
            likes = post.likes
            sleep(10)
            hashtagList = ' '.join([hashtag for hashtag in post.caption_hashtags])
			# print(hashtagList)
            if listOfComments and hashtagList:
                df.loc[f'{set_no}.{seq}'] = ['','',caption.replace(',',''),hashtagList,listOfComments,likes]
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

    username_list = ['narendramodi', 'the_hindu', 'ndtv']
    set_no = 7

    for u in username_list:

        print(f'|{u}|')

        user,maxPostLimit,maxCommentLimit,seedHashtag = '',0,0,[]

        try:
            user = u							# Mandatory argument
        except IndexError:
            print('Error: Scraper Needs a User Name')
            sys.exit(1)

        try:
            maxPostLimit = int(sys.argv[2])				# Optional argument
        except IndexError:
            maxPostLimit = 200
        except Exception as e:
            print(e)

        try:
            maxCommentLimit = int(sys.argv[3])			# Optional argument
        except IndexError:
            maxCommentLimit = 10
        except Exception as e:
            print(e)

        scraper(user,maxPostLimit,maxCommentLimit, set_no)

        set_no += 1
        sleep(20)