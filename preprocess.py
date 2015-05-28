import langid

def read_file_direct( infile, lang='en'):
    with open(infile) as tweet_file:
        W = None
        for line in tweet_file:
            if line.split('\t')[0] == 'W':
                W = line.split('\t')[1].strip('\n').decode('utf-8')
                if not (W is None) | (W == 'No Post Title'):
                    if langid.classify(W)[0] == lang:
                        yield W
