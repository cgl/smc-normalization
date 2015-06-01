import preprocess
import enchant
import ipdb
import codecs
import re

dic = enchant.Dict("en_US")

tweets_filtered = []
elenenler = []
for tweet in preprocess.read_file_direct("tweets09.txt"):
                flag = True
      #              ipdb.set_trace()
                wo_punc = re.sub('[!$,().-:;=%&/^?]', ' ', tweet)
      	        for kel in wo_punc.split(' '):
     #                          ipdb.set_trace()
                                if kel and not (dic.check(kel) or kel.find('@') == 1 or kel.find('#') == 1):
		                                flag = False
                if flag:
                                tweets_filtered.append(tweet)
    	        else:
                                elenenler.append(tweet)	
 #ipdb.set_trace()

with codecs.open('filtered_tweets.txt','w','utf-8') as outfile:
 
#with open("filtered_tweets.txt","w") as outfile:
	outfile.write("\n".join(tweets_filtered))
with codecs.open('elenenler.txt','w','utf-8') as outfile:
#with open("elenenler.txt","w","utf-8") as outfile:
	outfile.write("\n".join(elenenler))
