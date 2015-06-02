from srilm import LM
k = 10
lm = LM("data/lm", lower=True)
import numpy as np
from math import exp

def calculate_best_target_tweet(tweet,index_list):
    T = []
    W = []
    for n in index_list:
        f_of_n,Q_prime,candidates,probs = calculate_T(T,tweet,n)
        calculate_W(W,T,tweet,n)
        result = find_best_target_tweet(T,tweet)
    return result

def calculate_T(T,tweet,ind):
    candidates,probs = find_all_possible_candidates(tweet,ind)
    phi = np.array([1,1])
    source_word = tweet[ind]
    f_of_n = calculate_f_of_n(candidates,source_word)
    Q_prime = [np.exp(phi * f_of_n[i]) * probs[i] for i in range(1,len(candidates))]
    return f_of_n,Q_prime,candidates,probs

def calculate_W(W,T,tweet,n):
    pass

def calculate_f_of_n(candidates,source_word):
    for cand in candidates:
        pairwise_features = calculate_pairwise_feautures(source_word,cand)
        sim_features = calculate_similarity_feautures(source_word,cand)
    return np.ones((len(candidates),2))

def calculate_pairwise_feautures(source_word,cand):
    return np.array([int(source_word[0] == cand[0]),int(source_word[-1] == cand[-1]),int(source_word[0:3] == cand[0:3]),int(len(source_word) == len(cand)),calculate_common_letters(source_word,cand)])

def calculate_common_letters(source_word,cand):
    leng = len(cand)
    cnt = 0
    for letter in source_word:
        if cand.find(letter)!=-1:
            cnt = cnt+1
    if float(cnt)/leng >= 0.5:
        return 1
    return 0
    

def calculate_similarity_feautures(source_word,cand):
    return np.array(int(source_word[0] == cand[0]),int(source_word[-1] == cand[-1]),int(source_word[0:3] == cand[0:3]),int(len(source_word) == len(cand)))

def find_best_target_tweet(T,tweet):
    return

def find_all_possible_candidates(tweet,ind):
    context = [lm.vocab.intern(w) for w in tweet[ind-1:ind]+tweet[ind+1:ind+2]]
    probs = []
    candidates = []
    best_logprob = -1e100
    for i in xrange(lm.vocab.max_interned() + 1):
        logprob = lm.logprob(i, context)
        if logprob > best_logprob:
            best_idx = i
            best_logprob = logprob
        if logprob > -3:
            probs.append(logprob)
            candidates.append(lm.vocab.extern(i))
    return candidates,probs

import han
def get_tweets():
    sources = []
    targets = []
    inds = []
    for tweet_tuples in han.RESULTS:
        source = []
        target = []
        ind = []
        for tweet_tuple in tweet_tuples:
            source.append(tweet_tuple[0])
            target.append(tweet_tuple[2])
            ind.append(tweet_tuple[1] != u"OOV")
        sources.append(source)
        targets.append(target)
        inds.append(ind)
    return sources,targets,inds

sources,targets,inds = get_tweets()
oov_indexes = [[ind for ind,tag in enumerate(index_list) if not tag] for index_list in inds]
