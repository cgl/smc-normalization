from srilm import LM
k = 10
lm = LM("data/lm", lower=True)
import numpy as np
from math import exp
from lib.stringcmp import editdist_edits, editdist, editex
import difflib,string,re

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
    f_of_n = np.empty((0,8), int)
    for ind,cand in enumerate(candidates):
        pairwise_features = calculate_pairwise_feautures(source_word,cand)
        sim_features = calculate_similarity_feautures(source_word,cand)
        f_of_n[ind] = np.append(f_of_n, np.array([np.concatenate([pairwise_features,sim_features])]))
    return f_of_n
    #return np.ones((len(candidates),2))

def calculate_pairwise_feautures(source_word,cand):
    return np.array([int(source_word[0] == cand[0]),
                     int(source_word[-1] == cand[-1]),
                     int(source_word[0:3] == cand[0:3]),
                     int(len(source_word) == len(cand)),
                     calculate_common_letters(source_word,cand)])

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

    return np.array([int(source_word[0] == cand[0]),int(source_word[-1] == cand[-1]),int(source_word[0:3] == cand[0:3]),int(len(source_word) == len(cand))])

vowels = ('a', 'e', 'i', 'o', 'u', 'y')
chars = string.lowercase + string.digits + string.punctuation
char_ind = [ord(x) for x in chars]
char_map = dict(zip(chars,char_ind))

def calculate_lcsr(ovv,cand):
    ovv = get_reduced(ovv)
    lcs = longest(ovv,cand)
    max_length = max(len(ovv),len(cand))
    lcsr = float(lcs)/max_length
    def remove_vowels(word):
        for vowel in vowels:
            word = word.replace(vowel, '')
    ed = editex(remove_vowels(ovv),remove_vowels(cand))
    simcost = lcsr/ed
    return simcost

def longest(ovv,cand):
    try:
        ovv_int = [char_map[x] for x in ovv.encode('ascii',"ignore").lower()]
        cand_int = [char_map[y] for y in cand.encode('ascii',"ignore").lower()]
        lcs = mlpy.lcs_std(ovv_int,cand_int)[0]
    except Exception, e:
        print(ovv,cand,e)
        lcs = difflib.SequenceMatcher(None, ovv,cand).find_longest_match(0, len(ovv), 0, len(cand))[2]
    return lcs

def get_reduced(word,count=2):
    replace = r'\1\1'
    if count == 1:
        replace = r'\1'
    return re.sub(r'(.)\1+', replace, word.lower())

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
