import tweepy
import time

print("This is My twitter bot")

CONSUMER_KEY = 'iB4pR66EnLnu9lnJANGn3TTE4'
CONSUMER_SECRET = 'gP17KMARYXNxIVq1gT1RCgxmzPZcIuRtan0dx150NQzezM60nX'
ACCESS_KEY = '1261596317211668480-F6dcZeFFfxuFDNNWnvTr9lMotge25R'
ACCESS_SECRET = 'szJaCZduFkJUEmOJQw0rw3vbRfQCFugQ9BzX0TlCnKJLP'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


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
		elif '#save' in mention.full_text.lower():
			print('found #save!')
			print('responding back...')
			api.update_status('@' + mention.user.screen_name + '  Save Confirmed!', mention.id)
			api.retweet(last_seen_id)
			reply_id = str(mention.in_reply_to_status_id)
			mention1 = api.get_status(reply_id)
			ogname = "@" + mention.in_reply_to_screen_name + "\n"
			textt = ogname  + mention1.text
			api.send_direct_message(recipient_id, textt ,quick_reply_type= None,attachment_media_id=None)

while True:
	reply_to_tweets()
	time.sleep(2)
