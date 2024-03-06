import tweepy
import time

# Authentication details (to be filled by the user)
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

def twitter_bot():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)

    while True:
        try:
            tweets = api.mentions_timeline()
            for tweet in tweets:
                if '#hello' in tweet.text.lower():
                    print(f'Replying to {tweet.user.name}')
                    api.update_status(f'@{tweet.user.screen_name} Hello back to you!', in_reply_to_status_id=tweet.id)
            time.sleep(60)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break

# Example usage
# twitter_bot()
