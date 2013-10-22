#  Author : Albert Wang
#  ID     : 331793
#

"""
Reference: http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python/11015381#11015381
//FIX ME:
"""

import nltk,re, pprint,time 

def buildTrieFromWords(*words):
    """Build a trie data structure from a list of words. A dictionary is used."""
    trie = {}  #A dictionary 
    root = ""  #Root of the trie is a dummy node represented by empty string.
    for word in words:
        currentNode = trie
        parentKey = root
        for letter in word:
	        currentNode = currentNode.setdefault(parentKey+letter,{})
	        parentKey = parentKey+letter      
    return trie


def searchQueryFromTrie(word,trie):
    """Recursively search an query from the trie"""
    print word
    for k in trie.iterkeys():
        # print k
        if word == k:
            return k
        elif word.startswith(k):
            # print 'startswithk'
            if len(trie[k])!= 0:
                # print 'recursiveCall'
                return searchQueryFromTrie(word,trie[k])
            else:
                # print 'end of trie'
                return "NO"
    return "NO"    



def searchByTrie(trie):
    """Read from query file and search each query from trie, output query, result and time"""
    f = open('surnames.txt')
    output = open('outputNames.txt','a')
    # startTime = time.time()
    # result = searchQueryFromTrie("work",trie)
    # endTime   = time.time()
    # usedTime  = endTime - startTime
    # print word ' : ' + result + ' ' + str(usedTime)
    # output.write(result + ' ' + str(usedTime) + '\n')

    for line in f:
        print line
        word = line.strip()
        startTime = time.time()
        result = searchQueryFromTrie(word,trie)
        endTime   = time.time()
        usedTime  = endTime - startTime
        # print word + ' : ' result + ' ' + str(usedTime)
        output.write(word + ' : ' + result + ' ' + str(usedTime))



   

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
    #output_file = open('processedFile.txt','w')
    #for w in tokens:
    #    output_file.write(w + '\n')
    #print buildTrieFromWords(*tokens)
    trie = buildTrieFromWords(*tokens)
    #print trie
    searchByTrie(trie)
    
"""
def searchByEditDistance(query):
   
"""    








      
            


