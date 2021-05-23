import os
import tweepy
import time
from keep_alive import keep_alive

key1 = os.environ['CONSUMER_KEY']
key2 = os.environ['CONSUMER_SECRET']
key3 = os.environ['ACCESS_KEY']
key4 = os.environ['ACCESS_SECRET']


auth = tweepy.OAuthHandler(key1,key2)
auth.set_access_token(key3,key4)
api = tweepy.API(auth, wait_on_rate_limit=True)

print("This is My twitter bot") 

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
	f_write = open(file_name, 'w')
	f_write.write(str(last_seen_id))
	f_write.close()
	return

def reply_to_tweets():
	print('retrieving and replying to tweets...')
	last_seen_id = retrieve_last_seen_id(FILE_NAME)
	mentions = api.mentions_timeline(last_seen_id, tweet_mode='extended')


	for mention in reversed(mentions):
		print(str(mention.id) + ' - ' + mention.full_text)
		last_seen_id = mention.id
		store_last_seen_id(last_seen_id, FILE_NAME)
		user = api.get_user(mention.user.screen_name)
		recipient_id = user.id_str
		print("ID-",recipient_id)
		if '#helloworld' in mention.full_text.lower():
			print('found #helloworld!')
			print('responding back...')
			api.update_status('@' + mention.user.screen_name + '#HelloWorld back to you!', mention.id)
		elif '#retweet' in mention.full_text.lower():
			print('found #retweet!')
			print('responding back...')
			api.update_status('@' + mention.user.screen_name + '  retweeted Confirmed!', mention.id)
			api.retweet(last_seen_id)
		elif '#save' in mention.full_text.lower():
			print('found #save!')
			print('responding back...')
			reply_id = str(mention.in_reply_to_status_id)
			mention1 = api.get_status(reply_id)
			name = "@" + mention.in_reply_to_screen_name + "\n" + "\n"
			text = name + mention1.text
			api.send_direct_message(recipient_id, text , quick_reply_type=None, attachment_media_id=None)
			api.update_status('@' + mention.user.screen_name + ' save Confirmed!', mention.id)
      
keep_alive()      
while True:
	reply_to_tweets()
	time.sleep(10)


