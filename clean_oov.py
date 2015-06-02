import re
import codecs
import langid

def get_reduced(word,count=2):
    replace = r'\1\1'
    if count == 1:
        replace = r'\1'
    return re.sub(r'(.)\1+', replace, word.lower())

with open("oov_words.txt") as oov_file:
    lines = oov_file.readlines()
    
print len(lines)
oovset = set([get_reduced(line.strip().lower().decode('utf-8').encode('ascii',"ignore")) for line in lines])
print len(oovset)
oovset = set([line.strip('!^+%&/()?_-=-<>:;,.~|\}][{$#') for line in oovset])

print len(oovset)


with open("oov_file.txt","w") as oov_file:
    oov_file.write("\n".join(oovset))
    
#with codecs.open('oov_words_2.txt','w','utf-8') as outfile:
#    outfile.write("\n".join(list(oovset)))
