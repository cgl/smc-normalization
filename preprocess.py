# coding: utf-8
import CMUTweetTagger
import langid, enchant, codecs, re, os

file_path = os.path.dirname(os.path.realpath(__file__))
RUN_TAGGER_CMD = "java -XX:ParallelGCThreads=2 -Xmx500m -jar " + file_path + "/ark-tweet-nlp-0.3.2.jar"
dic = enchant.Dict("en_US")

def main():
    tweets_filtered = []
    elenenler = []

    for tweet in read_file_direct("tweets06.txt"):
        flag = True
        wo_punc = re.sub('[!$,().-:;=%&/^?]', ' ', tweet)
        for kel in wo_punc.split(' '):
            if kel and not (dic.check(kel) or not kel.startswith('@') or not kel.startswith('#') ):
                flag = False
                if flag:
                    tweets_filtered.append(tweet)
                else:
                    elenenler.append(tweet)

    with codecs.open('filtered_tweets.txt','w','utf-8') as outfile:
            outfile.write("\n".join(tweets_filtered))

    with codecs.open('elenenler.txt','w','utf-8') as outfile:
            outfile.write("\n".join(elenenler))

def main2(filename,write=False,outfilename="output.txt"):
    lot_tokenized = []; lot =[] ;
    tweets_iter = read_file_direct(filename)
    for ind,tweet in enumerate(tweets_iter):
        if (ind+1) % 1000 != 0:
            lot.append(tweet)
        else:
            tokenized = tokenize_tweets(lot)
            filtered = [tweet for tweet,org_tweet in tokenized if filter_tweet(clean_tweet(tweet))]
            print(len(filtered))
            lot =[]
            if write:
                with codecs.open(outfilename,'w','utf-8') as outfile:
                    outfile.write("\n".join(filtered))
            lot_tokenized.extend(filtered)
    return lot_tokenized


def clean_tweet(tweet):
    URLless_string = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', tweet)
    return URLless_string
    #" ".join([token.strip() for token in URLless_string.split(" ") if len(token) > 1 and not ispunct(token)])

def ispunct(some_string):
    return not any(char.isalnum() for char in some_string)

def filter_tweet(tweet,debug=False):
    for token in tweet.split(" "):
        #print token.decode("utf-8"), token ,"-"
        if not token or token.isdigit() or dic.check(token) or token.startswith('@') or token.startswith('#'):
            if debug:
                print "[%s] is passed" %token
            pass
        else:
            return False
    return True

def read_file_direct( infile, lang='en'):
    with open(infile) as tweet_file:
        W = None
        for line in tweet_file:
            if line.split('\t')[0] == 'W':
                W = line.split('\t')[1].strip('\n').decode('utf-8')
                if not (W is None) | (W == 'No Post Title'):
                    if langid.classify(W)[0] == lang:
                        yield W

def tokenize_tweets(tweets):
    tokenized = CMUTweetTagger._call_runtagger_tokenize(tweets,run_tagger_cmd = RUN_TAGGER_CMD)
    return tokenized
