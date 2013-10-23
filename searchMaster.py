#  Author : Albert Wang
#  ID     : 331793
#

"""
Reference: 1, http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python/11015381#11015381
           2, http://en.wikipedia.org/wiki/Levenshtein_distance
           3, http://www.stanford.edu/class/cs124/lec/med.pdf
           4, Trie: http://en.wikipedia.org/wiki/Trie
           5, Smith Waterman alogrithm: http://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm

"""

import nltk,re, pprint,time,sys 

#Helper method
def equal(char1, char2):
    """ Smith-Waterman algorithm/local edit distance
       match = 2
       mismatch = -1  
    """
    if char1 == char2:
        return  2
    else:
        return -1


def localEditDistance(query,word):
    """ Return a tuple, (local distance, word) """  
    matrix = [ [0 for elem in xrange(len(word)+1)] for elem in xrange(len(query)+1) ] 
    maxI,maxJ = 0,0
    highestScore = 0
    for i in xrange(1,len(query)+1):
        for j in xrange(1,len(word)+1):
            matrix[i][j] = max(matrix[i-1][j]-1, matrix[i][j-1]-1,matrix[i-1][j-1] + equal(query[i-1],word[j-1]),0) 
            if highestScore <= matrix[i][j]:
                highestScore = matrix[i][j]
                maxI = i
                maxJ = j
    #  Start trace back from matrix[maxI][maxJ]
    #  Trace back
    return highestScore, word #localAlignString
 


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
    """Return the most matched string."""   
    mismatchString = ""
    mismatchScore  = 9999
  
    for k in trie.iterkeys():
        tempScore = findMismatchScore(word,k)
        if tempScore <= mismatchScore:
             mismatchScore = tempScore
             mismatchString = k
    if( len(trie[mismatchString]) == 0): 
        return mismatchString,mismatchScore
    else:
        return findMostMatchString(word,trie[mismatchString])
                 
	
def searchQueryFromTrie(word,trie):
    """Recursively search an query from the trie, 
       return a tuple (result, score), 
       Score is the number of mismatch"""
    #  For loop is trying to find a match, if reach the end of file,the most matched one is returned.
    currentMismatches = 9999
    for k in trie.iterkeys():
        if word == k:
            return k,0
        elif word.startswith(k):
            if len(trie[k])!= 0:
                return searchQueryFromTrie(word,trie[k])
            else: #End of trie
                currentMismatches = findMismatchScore(word,k)
        else: 
            tempScore = findMismatchScore(word,k)
            if  tempScore <= 2:
                return k, tempScore    
                # else:
                #     return "NO", 2
    return k, currentMismatches
  

def findMostMatchString(word,trie):
    mostMatchKey = "NO"
    mismatches = 2

    for k in trie.iterkeys():
        if len(trie[k]) == 0 :
            tempScore = findMismatchScore(word,k)
            if tempScore <= mismatches:
               mostMatchKey = k
               mismatches = tempScore     
            return mostMatchKey,mismatches
        else:
            tempScore = findMismatchScore(word,k)
            if tempScore <= mismatches:
               mismatches = tempScore
               mostMatchKey = k
               return findMostMatchString(word,trie[k])
            else:   
                newSearch = findMostMatchString(word,trie[k])
                if newSearch[1] <= 2:
                    mostMatchKey = newSearch[0]
                    mismatches   = newSearch[1]

    return mostMatchKey,mismatches


def findMismatchScore(word,candidate):
    """return the mismatch score of two strings"""
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
    output = open('trieOutput.txt','a')
    for line in f:
        word = line.strip()
        startTime = time.time()
        result = searchQueryFromTrie(word,trie)
        if result[1] > 2:
            result = findMostMatchString(word,trie)
        endTime   = time.time()
        usedTime  = endTime - startTime
        print word + ': result: ' + result[0]  + ' score: ' + str(result[1]) + ' time: ' + str(usedTime) 
        output.write(word + ': result: ' + result[0]  + ' score: ' + str(result[1]) + ' time: ' + str(usedTime) + '\n')

def searchByEditDistance(*words):

    f = open('surnames.txt')
    output = open('editDistanceOutput.txt','a')
    for line in f:
        query = line.strip()
        localDistance = 0
        bestMatchKey = "placeholder"
        startTime = time.time()
        for elem in words:
            result = localEditDistance(query,elem)
            if result[0] >= localDistance:
                localDistance = result[0]
                bestMatchKey = result[1]        
        endTime = time.time()
        usedTime = endTime - startTime
        print query + ' : result : ' + bestMatchKey + ' : score : ' + str(localDistance) + ' time: ' + str(usedTime)
        output.write(query + ' : result : ' + bestMatchKey + ' : score : ' + str(localDistance) + ' time: ' + str(usedTime) + '\n') 


if __name__ == "__main__":
    f = open('turgenev.txt')
    raw = f.read()
    raw.lower()
    p = re.compile('[^a-z ]')
    r = re.sub(p,'',raw)    
    print "Preprocessing file..."
    tokens = nltk.word_tokenize(r)
    print "Tokenized."
    print "Start building Trie"
    trie = buildTrieFromWords(*tokens)
    print "Trie size: " + str(sys.getsizeof(trie)) + " bytes"
    print "Finished building Trie"
    output = open('trie.txt','w')
    output.write(str(trie))
    print "Start searching by Trie."
    searchByTrie(trie)
    print "Searching by Trie is done."
    print "Searching by edit distance."
    searchByEditDistance(*tokens)
    print "Searching by edit distance is done."

       
     