import twitter,json,csv

#Twitter keys
api_key = ""
api_key_secret = ""
oauth_key = ""
oauth_key_secret = ""

#Connect to the Twitter API
auth = twitter.oauth.OAuth(oauth_key, oauth_key_secret,
                           api_key, api_key_secret)
twitter_api = twitter.Twitter(auth=auth, retry=True)

#Creates a CSV file and writes Tweet information into it
csvfile = open('.csv', 'w')
csvwriter = csv.writer(csvfile, delimiter='|')

#Tidying - get rid of the lines that start with \r and \n that have percentages and random characters in
def getVal(val):
    clean = ""
    if val:
        val = val.replace('|', ' ')
        val = val.replace('\n', ' ')
        val = val.replace('\r', ' ')
        clean = val
    return clean

#Search terms
q = ""

#Searches for the search terms through the conenction with the Twitter API
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=q)

#Truncation handling - Andy's fix
for tweet in stream:
    if tweet['truncated']:
        tweet_text = tweet['extended_tweet']['full_text']
    else:
        tweet_text = tweet['text']
    if 'retweeted_status' in tweet: #Fix to retweeted_status issue in previous attempts
        rt_prefix = 'RT @' + tweet['retweeted_status']['user']['screen_name'] + ': '
        if tweet['retweeted_status']['truncated']:
            tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
        else:
            tweet_text = tweet['retweeted_status']['text']
            tweet_text = rt_prefix +  tweet_text
    if ('quoted_status' in tweet):
        quote_suffix =  tweet['quoted_status_permalink']['url']
        tweet_text = tweet_text + ' ' + quote_suffix
        if ('quoted_status' in tweet) and ('retweeted_status' not in tweet) :
            quote_suffix =  tweet['quoted_status_permalink']['url']
            tweet_text = tweet_text + ' ' + quote_suffix

#Elements being retrieved
    csvwriter.writerow([
        tweet['id_str'],
        tweet['created_at'],
        tweet['truncated'], #For testing purposes
        tweet['is_quote_status'], #For testing purposes
        tweet['source'],
        tweet['lang'],
        tweet['place'],
        tweet['user']['geo_enabled'],
        getVal(tweet['user']['screen_name']),
        getVal(tweet_text).encode('utf-8'),
        getVal(tweet['user']['location']),
        tweet['user']['verified'],
        tweet['user']['statuses_count'],
        tweet['user']['favourites_count'],
        tweet['user']['followers_count'],
        tweet['user']['friends_count'],
        tweet['user']['created_at']
        ])
