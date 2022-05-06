from import_lib import *

class TwitterClient(object):

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = '3XwgFgsXucaFXOrkZtlwvxV5O'
        consumer_secret = 'LNnTcxibKalylVImljDsKfkRqb6WHD8I7hdSYt7Pm7VaCetqZm'
        access_token = '608048932-AM21gcwLORlm5j0514DwPL850byLb7Gs04bPZ6Mn'
        access_token_secret = 'QtnJ8mV75peV7L7Kd4DZKogMRIxzjk5XFOPtZiz62NoM3'

        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        #Utility function to clean tweet text by removing links, special characters using simple regex statements.
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(
                    tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except Exception  as e:
            # print error (if any)
            print("Error : " + str(e))


def get_analysis(query, count):
    try:
        # os.remove('./static/sentiment_analysis/sentiment.jpg')
        # creating object of TwitterClient Class
        api = TwitterClient()
        # calling function to get   tweets
        tweets = api.get_tweets(query=query, count=count)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        # print("Positive tweets percentage: {} %".format(
            # 100*len(ptweets)/len(tweets)))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        # print("Negative tweets percentage: {} %".format(
            # 100*len(ntweets)/len(tweets)))
        # percentage of neutral tweets
        # print("Neutral tweets percentage: {} % \
            # ".format(100*(len(tweets) - (len(ntweets)+len(ptweets)))/len(tweets)))

        # printing first 5 positive tweets
        # print("\n\nPositive tweets:")
        # for tweet in ptweets[:10]:
        # 	print(tweet['text'])

        # # printing first 5 negative tweets
        # print("\n\nNegative tweets:")
        # for tweet in ntweets[:10]:
        # 	print(tweet['text'])

        y = np.array([(100*len(ptweets)/len(tweets)), (100*len(ntweets)/len(tweets)),
                    (100*(len(tweets)-(len(ntweets)+len(ptweets)))/len(tweets))])
        mylabels = ["Positive", "Negative", "Neutral"]
        myexplode = [0.2, 0, 0]
        plt.clf()
        plt.pie(y, labels=mylabels, explode=myexplode,  autopct='%1.1f%%')
        plt.savefig('./static/sentiment_analysis/sentiment.jpg')
        return 1
    except Exception as e:
        print(e)
        return 0

# print(get_analysis("biden", 100))
