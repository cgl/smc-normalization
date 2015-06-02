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
    f_of_n = calculate_f_of_n(candidates,phi)
    Q_prime = [np.exp(phi * f_of_n[i]) * probs[i] for i in range(1,len(candidates))]
    return f_of_n,Q_prime,candidates,probs

def calculate_W(W,T,tweet,n):
    pass

def calculate_f_of_n(candidates,phi):
    return np.ones((len(candidates),len(phi)))

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