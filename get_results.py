import log_linear_model
import values

sources,targets,inds = log_linear_model.get_tweets() ; oov_indexes = [[ind for ind,tag in enumerate(index_list) if not tag] for index_list in inds]

i = 50; tweet = sources[i] ; ind_list = oov_indexes[i]; answer = targets[i] ;n = oov_indexes[i][1]

answers = targets
results = []

count=0
for ind_answer in range(0, len(answers)):
    for ind_wrd in range(0, len(answers[ind_answer])):
        if targets[ind_answer][ind_wrd] == answers[ind_answer][ind_wrd]:
            count=count+1
    results.append(float(count)/len(answers[ind_answer]))
    count=0

    
