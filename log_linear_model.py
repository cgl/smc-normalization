k = 10


def calculate_best_target_tweet(tweet,index_list):
    T = []
    W = []
    for n in index_list:
        calculate_T(T,tweet,n)
        calculate_W(W,T,tweet,n)
        result = find_best_target_tweet(T,tweet)
        return result

def calculate_T(T,tweet,ind):
    find_all_possible_candidates()
    pass

def calculate_W(W,T,tweet,n):
    pass

def find_best_target_tweet(T,tweet):
    return

def find_all_possible_candidates(tweet,ind):

    for i in xrange(lm.vocab.max_interned() + 1):
        logprob = lm.logprob(i, context)
        if logprob > best_logprob:
                best_idx = i
                best_logprob = logprob
        if logprob > -3:
            probs.append((i,logprob))
