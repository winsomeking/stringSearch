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

def findMostMatchString (word, trie):
    """Allowing mismatch 2"""   
    mismatchString = ""
    mismatchScore  = 9999
  
    for k in trie.iterkeys():
        tempScore = findMismatchScore(word,k)
        if tempScore <= mismatchScore:
             mismatchScore = tempScore
             mismatchString = k
    if( len(trie[mismatchString]) == 0): 
        #print mismatchString + ':score: ' + str(mismatchScore) 
        return mismatchString,mismatchScore
    else:
        return findMostMatchString(word,trie[mismatchString])


    # return mismatchString,mismatchScore 
                
	
def searchQueryFromTrie(word,trie):
    """Recursively search an query from the trie, 
       return a tuple (result, score), 
       Score is the number of mismatch"""
    #  For loop is trying to find a match, if reach the end of file,the most matched one is returned.
    mostMatchKey = ""
    mismatches = 9999
    for k in trie.iterkeys():
        # print k
        if word == k:
            return k,0
        elif word.startswith(k):
            if len(trie[k])!= 0:
                return searchQueryFromTrie(word,trie[k])
            else:#End of trie
                return k, findMismatchScore(word,k)
        # else: #find the mismatch number,  
        #     tempScore = findMismatchScore(word,k)
        #     if tempScore < mismatches:
        #         mismatches = tempScore
        #         mostMatchKey = k
    #return mostMatchKey,mismatches
    for k in trie.iterkeys():
        if len(trie[k]) == 0 :
            tempScore = findMismatchScore(word,k)
            if tempScore < mismatches:
                mismatches = tempScore
                mostMatchKey = k
        else: 
            result = findMostMatchString(word,trie[k])
            tempMatchString = result[0]
            tempScore = result[1]
            if tempScore <= mismatches :
                mismatches = tempScore
                mostMatchKey = tempMatchString
    return mostMatchKey,mismatches


def findMismatchScore(word,candidate):
    """return the mismatch of two strings"""
    if len(word) > len(candidate):
        while len(candidate) != len(word):
            candidate = candidate + " "
    if len(word) < len(candidate):
        while len(candidate) != len(word):
            word = word + " "
    mismatch = 0
    for v in xrange(0,len(word)):
        if word[v] != candidate[v]:
            mismatch = mismatch + 1
    return mismatch   


    
def searchByTrie(trie):
    """Read from query file and search each query from trie, output query, result and time"""
    f = open('surnames.txt')
    output = open('outputNames.txt','a')
    for line in f:
        # print line
        word = line.strip()
        # print word
        startTime = time.time()
        result = searchQueryFromTrie(word,trie)
        endTime   = time.time()
        usedTime  = endTime - startTime
        print word + ': ' + result[0] + ' ' + str(result[1]) + ' ' + str(usedTime)
        output.write(word + ': ' + result[0]  + ' ' + str(result[1]) + ' ' + str(usedTime) + '\n')


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








      
            


