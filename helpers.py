import random
import time

def shuffle(l) :
    random.seed(time.time())
    random.shuffle(l)
    return l

# mv = ModelViewer('20150616-050011', env='prod')

# channel_names = dict(mv.model_channels())

# models = dict((id, mv.read_model(id)) for id in shuffle(channel_names.keys())[:1000])

# e.g.
# ordered(compare(models, channel_names, 500), 5)

def dot(v1, v2):
    keys = set(v1.keys()) | set(v2.keys())
    sum = 0
    for k in keys:
        sum += v1.get(k,0) * v2.get(k,0)
    return sum
                                        
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
