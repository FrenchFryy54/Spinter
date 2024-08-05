from random import random
import numpy as np
def weightloader(struct):
    """numimputs, *layercounts, numoutputs"""
    weightlist = []
    while len(struct) > 1:
        weightrow = np.array([[random()*4-2 for _ in range(struct[0])] for _ in range(struct[1])])
        weightlist.append(weightrow)
        struct.pop(0)
    weightrow = [random()*4-2 for _ in range(struct[0])]
    weightlist.append(weightrow)
    return weightlist
def loadbots(file):
    botweights = []
    with open(file) as f:
        weights = []
        for line in f.readlines():
            line = line.strip()
            if line == "SPLIT_HERE":
                wl2 = []
        
                ins = 10
                for wl in weights[:-1]:
                    formatted = [wl[num: num + ins] for num in range(0, len(wl), ins)]
                    wl2.append(np.array(formatted))
                    ins = len(wl) // ins
                wl2.append(weights[-1])
                botweights.append(wl2)
                weights = []
            else:
                weights.append([*map(float, line.split())])
    return botweights
def offspring(parent, childcount, alpha):
    children = [parent]
    for _ in range(childcount):
        child = []
        for layer in parent[:-1]:
            nlayer = np.array(layer, copy=True)
            for row in nlayer:
                for i in range(len(row)):
                    row[i] += (random() - 0.5) * alpha
            child.append(nlayer)
        newlist = [i for i in parent[-1]]
        for i in range(len(newlist)):
            newlist[i] += (random() - 0.5) * alpha
        child.append(newlist)
        children.append(child)
    return children
def export(bots, outfile):
    with open(outfile, 'w') as f:
        for weights in bots:
            for mat in weights[:-1]:
                print(*[item for row in mat for item in row], sep=' ', file=f)
            print(*weights[-1], sep=' ', file=f)
            print("SPLIT_HERE", file=f)
def sigmoid(m):
    return 1 / (1 + np.exp(-m))
def feed(inputs, weightfile):
    inputs = np.array([[i] for i in inputs])
    for mymat in weightfile[:-1]:
        inputs = np.matmul(mymat, inputs)
        inputs = sigmoid(inputs)
    stored_y = [v1 * inputs[idx][0] for idx, v1 in enumerate(weightfile[-1])]
    return stored_y
#Michael Rodriguez, Period 2, 2025    