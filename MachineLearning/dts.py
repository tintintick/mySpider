from math import log
import sys
import pickle

def createDataSet():
    dataset = [[1, 1, 'y'], [1, 1, 'y'], [1, 0, 'n'],
               [0, 1, 'n'], [0, 1, 'n'], [1, 0, 'may']]#, [1, 0, 'may']]
    dataset1 = [[1, 1, 'y'], [1, 1, 'y'], [1, 0, 'n'],
                [0, 1, 'n'], [0, 1, 'n'], [0, 0, 'may']]
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
        prob = float(classlist[key]) / length
        ent -= prob * log(prob, 2)

    return ent


def splitDataSet(dataset, axis, value):
    retvec = []
    retset = []
    for featvec in dataset:
        if featvec[axis] == value:
            retvec = featvec[:axis]
            retvec.extend(featvec[axis + 1:])
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
            prob = float(feat_values.count(value)) / len(feat_values)
            newent += prob * calcShannonEnt(ret)
        infogain = baseent - newent
        if (infogain > bestgain):
            bestgain = infogain
            bestfeat = i
    return bestfeat


def majorityCnt(col):
    length = len(col)
    uniquevals = set(col)
    probdic = {}
    for value in uniquevals:
        probdic[value] = float(col.count(value)) / length

    sorteddic = sorted(probdic.items(), key=lambda e: e[1], reverse=True)
    return sorteddic[0][0]


def createDecisionTree(dataset, labels):
    classlist = [example[-1] for example in dataset]

    if classlist.count(classlist[0]) is len(dataset):  # Classes are equal
        #        print 'yezi:{}'.format(dataset)
        return classlist[0]

    if labels == []:  # All features are customed
        if len(dataset[0]) is not 1:
            print 'error dataset'
            sys.exit()
        else:
            #print 'major:{}'.format(dataset)
            return majorityCnt(dataset[0])

    bestfeat = chooseBestFeature(dataset, labels)
#    print 'bestfeat:{}'.format(bestfeat)

    if bestfeat is -1:  # Feature vectors are equal
        return majorityCnt([example[-1] for example in dataset])

    bestlabel = labels[bestfeat]
    del(labels[bestfeat])
    dTree = {bestlabel: {}}

    bestcol = [example[bestfeat] for example in dataset]
    uniquevals = set(bestcol)
    for value in uniquevals:
        subset = splitDataSet(dataset, bestfeat, value)
        #print subset
        sublabels = labels[:]
        dTree[bestlabel][value] = createDecisionTree(subset, sublabels)

    return dTree


def dtsclassify(dts, labels, testvec):
    curfeat = dts.keys()[0]
    curnode = dts[curfeat]
    featpos = labels.index(curfeat)
    featval = testvec[featpos]

    for value in curnode.keys():
        if value is featval:
            if type(curnode[value]) is dict:
                subtree = curnode[value]
                classlabel = dtsclassify(subtree, labels, testvec)
            else:
                classlabel = curnode[value]
    return classlabel

def storedts(dts, filename):
    fw = open(filename, "w")
    pickle.dump(dts, fw)
    fw.close

def loaddts(filename):
    fr = open(filename, "r")
    dts = pickle.load(fr)
    return dts


dataset, dataset1, labels = createDataSet()

featlabels=labels[:]
dts = createDecisionTree(dataset, featlabels)

path = '/home/redhat/Desktop/dts.log'
storedts(dts, path)
print loaddts(path)


#testvec = [0, 0]
#featlabels=labels[:]
#classval = dtsclassify(dts, featlabels, testvec)
#print 'class is: {}'.format(classval)

#testcol = [1,0,2,1,2,3,1,4,0,2,1]
# print majorityCnt(testcol)
#bestfeat = chooseBestFeature(dataset, labels)
# print bestfeat
#ent = calcShannonEnt(dataset)
# print ent
#retset = splitDataSet(dataset, 0, 1)
# print retset
