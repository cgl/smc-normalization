from lib.stringcmp import editdist_edits, editdist, editex
from srilm import LM
k = 10
lm = LM("data/lm", lower=True)
import numpy as np
from math import exp
import difflib,string,re,mlpy

def calculate_best_target_tweet(tweet,index_list):
    Ws = np.ones(1,len(tweet))
    n_1 = -1
    for n in index_list:
        T,f_of_n,Q_prime,candidates,sorted_q_indexes  = calculate_T(tweet,n)
        W = calculate_W(T,tweet,n,1,Q_prime)
        result = find_best_target_tweet(T,tweet)
        n_1 = n
    return result

def calculate_T(tweet,ind):
    candidates,probs = find_all_possible_candidates(tweet,ind)
    source_word = tweet[ind]
    f_of_n = calculate_f_of_n(candidates,source_word)
    phi = np.ones((1,f_of_n.shape[1]))
    Q_prime = [np.sum(np.exp(phi * f_of_n[i])) * probs[i] for i in range(1,len(candidates))]
    Q = Q_prime/sum(Q_prime)
    sorted_q_indexes = np.argsort(Q)
    sorted_q_indexes[0:10]
    T = [candidates[j] for j in sorted_q_indexes[0:10]]
    return T,f_of_n,Q_prime,candidates,sorted_q_indexes

def calculate_W(T,tweet,n,W_k_n_1,Q_prime):
    Z = calculate_Z(T)
    W_k_n = W_k_n_1 * (np.sum(Q_prime)/Z)
    return  W_k_n

OOV= []
def calculate_Z(T):
    for oov in OOV:
        update_similarity_dict(oov,T)
    phi = []
    Z = []
    for target in T:
        f_of_n = np.empty((0,13), int)
        z_t_k_n = 0
        for oov in OOV:
            pairwise_features = calculate_pairwise_feautures(oov,target)
            sim_features = calculate_similarity_feautures(oov,target)
            f_of_n = np.append(f_of_n, np.array([np.concatenate([pairwise_features,sim_features])]),axis=0)
            print np.sum(np.exp(phi * f_of_n))
            z_t_k_n += np.sum(np.exp(phi * f_of_n))
        Z.append(z_t_k_n)
    return Z


SIMILARITY = {}
def calculate_f_of_n(candidates,source_word):
    update_similarity_dict(source_word,candidates)
    f_of_n = np.empty((0,13), int)
    for cand in candidates:
        pairwise_features = calculate_pairwise_feautures(source_word,cand)
        sim_features = calculate_similarity_feautures(source_word,cand)
        f_of_n = np.append(f_of_n, np.array([np.concatenate([pairwise_features,sim_features])]),axis=0)
    return f_of_n
    #return np.ones((len(candidates),2))

def update_similarity_dict(source_word,candidates):
    if not SIMILARITY.has_key(source_word):
        SIMILARITY[source_word] = {}
    for cand in candidates:
        if not SIMILARITY[source_word].has_key(cand):
            SIMILARITY[source_word][cand] = calculate_lcsr(source_word,cand)

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
    items_list = SIMILARITY[source_word].items()
    sorted_list = sorted(items_list, key=lambda item: item[1], reverse=True)
    similarity_index = next((i for i, v in enumerate(sorted_list) if v[0] == "diet"), None)
    return [int(similarity_index <= i-1) for i in [5,10,25,50,100,250,500,1000]]

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
