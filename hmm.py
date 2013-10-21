""" hmm.py - Example of use of NLTK's Hidden Markov Model for the ALTA 2013 shared task

Author: Diego Molla-Aliod (dmollaaliod@gmail.com)
        http://web.science.mq.edu.au/~diego/

Date: 11 July 2013
"""

import nltk

def readWikiData(filenames):
    "Read Wikipedia data and return a structure for use by NLTK"
    data = list()
    for filename in filenames:
        f = open(filename)
        sentence = list()
        l = f.readline()
        for l in f.readlines():
            if l == "\n":
                data.append(sentence)
                sentence = list()
                continue
            (cap,punct,token) = l.split()
            label = str(cap)[0]+str(punct)[0]
            sentence.append((token,label))
        f.close()
        if sentence != []:
            data.append(sentence)
    return data

def readCaseData(filename,test=False):
    "Read data and return a structure for use by NLTK"
    f = open(filename)
    l = f.readline()
    sentence = list()
    for l in f.readlines():
        items = l.strip().split()
        if test:
            if len(items) != 2:
                print "Warning: Wrong format in input line", l
                continue
            (pos,token) = items
            sentence.append(token)
        else:
            if len(items) != 3:
                print "Warning: Wrong format in input line", l
                continue
            (pos,label,token) = items
            sentence.append((token,label))
    f.close()
    return [sentence]

if __name__ == "__main__":
    print "Reading data"
    train1 = readWikiData(('wikidata/train/split0.txt',
                          'wikidata/train/split1.txt',
                          'wikidata/train/split2.txt',
                          'wikidata/train/split3.txt',
                          'wikidata/train/split4.txt',
                          'wikidata/train/split5.txt',
                          'wikidata/train/split6.txt',
                          'wikidata/train/split7.txt',
                          'wikidata/train/split8.txt',
                          'wikidata/train/split9.txt',
                          'wikidata/train/split10.txt',
                          'wikidata/train/split11.txt',
                          'wikidata/train/split12.txt',
                          'wikidata/train/split13.txt',
                          'wikidata/train/split14.txt',
                          'wikidata/train/split15.txt',
                          'wikidata/train/split16.txt',
                          'wikidata/train/split17.txt'))
    train2 = readCaseData('casepunct/train.csv')
    train = train1+train2
    test = readCaseData('casepunct/testdata.csv',test=True)

    print "Training HMM"
    hmm = nltk.tag.HiddenMarkovModelTagger.train(train)

    print "Computing result of test"
    result = {'Case':list(), 'Punct':list()}
    offset = 0
    for s in test:
        tokens = s
        labels = hmm.tag(tokens)
        for i in range(len(tokens)):
            if labels[i][1][0]=='T':
                result['Case'].append(str(offset+i+1))
            if labels[i][1][1]=='T':
                result['Punct'].append(str(offset+i+1))
        offset += len(tokens)

    print "Writing result to file submission.csv"
    f = open('submission.csv','w')
    f.write("Id,documents\n")
    for k in result.keys():
        f.write(k+","+" ".join(result[k])+"\n")
    f.close()
