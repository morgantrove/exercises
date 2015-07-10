# my_helpers.py

import sys
import math
import random
import time
from trove.curation.tools.chanifier.importer import ModelViewer
from collections import defaultdict

def cos_sim(x,y):
    tot = 0
    keys = set(x.keys()) | set(y.keys())
    for k in keys:
        tot += x.get(k,0) * y.get(k,0)
    return tot

def dot(x,y):
    return cos_sim(x.y)

def get_cos_similarity(u,v, mv):
    # u,v are the integer IDs
    u_ = mv.read_model(u)
    v_ = mv.read_model(v)
    return cos_sim(u_, v_)

def get_mean(l): # for a uniform list
    return float(sum(l)) / len(l)

def get_E(d):
    tot = sum(d.values())
    E = 0
    for entry in d:
        E += entry * d[entry]
    return E / tot

def get_var(d):
    tot = sum(d.values())
    var = 0
    for entry in d:
        var += entry * entry * d[entry]
    return var / tot


def shuffle(l) :
    random.seed(time.time())
    random.shuffle(l)
    return l

# mv = ModelViewer('20150616-050011', env='prod')
# channel_names = dict(mv.model_channels())
# models = dict((id, mv.read_model(id)) for id in shuffle(channel_names.keys())[:1000])
# e.g.
# ordered(compare(models, channel_names, 500), 5)

def compare(models, names, limit=50):
    """
    create a dict[(i,j)] of similarities
    """
    result = {}
    ids = shuffle(models.keys())[:limit]
    for i, id in enumerate(ids):
        for idj in ids[i+1:]:
            (x, y) = sorted((id, idj))
            result[((x, names[x]), (y, names[y]))]=dot(models[x], models[y])
    return result

def ordered(dists, limit=None):
    """
    dists : a dict[(i,j)] of similarities
    limit : shortens the list of closest matches
    create a list of channels paired with their nearest other channels.
    """
    result = []
    ids = set([k for i, j in dists.keys() for k in i, j])
    for i in ids:
        row = []
        for j in ids:
            if i==j:
                continue
            row.append((j, dists[tuple(sorted((i, j)))]))
        row.sort(reverse=True, key = lambda x : x[1])
        if limit:
            row = row[:limit]
        result.append((i, row))
    result.sort(reverse=True, key = lambda x : x[1][0][1])
    return result
