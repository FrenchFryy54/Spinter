import sys; args=sys.argv[1:]
from random import random
from math import exp
def weightloader(struct):
    """numimputs, *layercounts, numoutputs"""
    weightlist = []
    while len(struct) > 1:
        weightrow = [random()*4-2 for _ in range(struct[1] * struct[0])]
        weightlist.append(weightrow)
        struct.pop(0)
    weightrow = [random()*4-2 for _ in range(struct[0])]
    weightlist.append(weightrow)
    return weightlist
def dot(list1, list2):
    return sum(v1 * list2[idx] for idx, v1 in enumerate(list1))
def feed_forward(inputs, weightfile):
    for weightline in weightfile[:-1]:
        newvals = []
        numinputs = len(inputs)
        for num in range(0, len(weightline), numinputs):
            newvals.append(dot(inputs, weightline[num: num + numinputs]))
        inputs = [*map(activation, newvals)]
    stored_y = [v1 * inputs[idx] for idx, v1 in enumerate(weightfile[-1])]
    return stored_y
activation = lambda x: 1 / (1 + exp(-x))
#Michael Rodriguez, Period 2, 2025    