from math import log

def createDataSet():
    dataset = [[1,1,'y'],[1,1,'y'],[1,0,'n'],[0,1,'n'],[0,1,'n']]#, [0,0,'may']]
    dataset1 = [[1,1,'y'],[1,1,'y'],[1,0,'n'],[0,1,'n'],[0,1,'n'], [2,0,'may']]
    labels = ['no surfacing', 'fippers']
    return dataset, dataset1, labels


def calcShannonEnt(dataset):
    length = len(dataset)
    classlist = {}
    ent = 0.0
    for featvec in dataset:
        if featvec[-1] not in classlist:
             classlist[featvec[-1]] = 0
        classlist[featvec[-1]] += 1

    for key in classlist:
        prob = float(classlist[key])/length
        ent -= prob * log(prob, 2)

    return ent

def splitDataSet(dataset, axis, value):
    retvec = []
    retset = []
    for featvec in dataset:
        if featvec[axis] == value:
            retvec = featvec[:axis]
            retvec.extend(featvec[axis+1:])
            retset.append(retvec)
    return retset

def chooseBestFeature(dataset, labels):
    numfeature = len(dataset[0]) - 1
    baseent = calcShannonEnt(dataset)
    bestgain = 0.0
    bestfeat = -1
    
    for i in range(numfeature):
        newent = 0.0
        feat_values = [example[i] for example in dataset]
        uniquevals = set(feat_values)
        for value in uniquevals:
            ret = splitDataSet(dataset, i, value)
            prob = float(feat_values.count(value))/len(feat_values)
            newent += prob * calcShannonEnt(ret)
        infogain = baseent-newent
        if (infogain > bestgain):
            bestgain = infogain
            bestfeat = i
    return bestfeat

def majorityCnt(col):
    length = len(col)
    uniquevals = set(col)
    probdic = {}
    for value in uniquevals:
        probdic[value] = float(col.count(value))/length

    sorteddic = sorted(probdic.items(), key=lambda e:e[1], reverse=True)
    return sorteddic[0][0]


def createDecisionTree(dataset, labels):
    classlist = [example[-1] for example in dataset]
    if len(dataset[0]) is 1:
        return majorityCnt(dataset[0])
    if classlist.count(classlist[0]) is len(dataset):
        return classlist[0]

    bestfeat = chooseBestFeature(dataset, labels)
    bestlabel = labels[bestfeat]
    del(labels[bestfeat])
    dTree = {bestlabel:{}}

    bestcol = [example[bestfeat] for example in dataset]
    uniquevals = set(bestcol)
    for value in uniquevals:
        subset = splitDataSet(dataset, bestfeat, value)
        sublabels = labels
        dTree[bestlabel][value] = createDecisionTree(subset, sublabels)

    return dTree

dataset, dataset1, labels = createDataSet()
#print createDecisionTree(dataset, labels) # {'no surfacing': {0: 'n', 1: {'fippers': {0: 'n', 1: 'y'}}}}
print createDecisionTree(dataset1, labels)

#testcol = [1,0,2,1,2,3,1,4,0,2,1]
#print majorityCnt(testcol)
#bestfeat = chooseBestFeature(dataset, labels)
#print bestfeat
#ent = calcShannonEnt(dataset)
#print ent
#retset = splitDataSet(dataset, 0, 1)
#print retset

