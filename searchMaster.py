#  Author : Albert Wang
#  ID     : 331793
#

"""
  
"""

import nltk,re, pprint 

if __name__ == "__main__":
    f = open('turgenev.txt')
    #print f.read()
    raw = f.read()
    #tokens = nltk.word_tokenize(raw)
    #for w in tokens:    
	#    w.lower()
    raw.lower()
    p = re.compile('[^a-z ]')
#    p.search(raw)
    r = re.sub(p,'',raw)    
    #print r
    tokens = nltk.word_tokenize(r)
    output_file = open('processedFile.txt','w')
    for w in tokens:
        output_file.write(w + '\n')


def searchByEditDistance(query):
    """Search the query by using Edit distance"""
    