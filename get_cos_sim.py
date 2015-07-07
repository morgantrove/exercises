# get_cos_sim.py

import sys
import math
import random
from trove.curation.tools.chanifier.importer import ModelViewer
from collections import defaultdict

def cos_sim(x,y):
    tot = 0
    keys = set(x.keys()) | set(y.keys())
    for k in keys:
        tot += x.get(k,0) * y.get(k,0)
    return tot

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



def main(args):
    if len(args) > 1:
        print "Bad number of arguments. Exiting."; return

    mv = ModelViewer()
    all_channels = mv.model_channels()
    all_keys = []
    print all_channels[0]
    for channel in all_channels:
        all_keys.append(int(channel[0]))
    # print all_keys[0], all_channels[0], mv.read_model(all_keys[0]), len(all_keys), "channels."

    # Get a multiset//list of all keys choose 2.  To get a (bucketed, 
    # ie quasi-continuous) distribution of the similarities.
    assert(len(all_keys) < 6000)
    sims = []
    models = {}

    ### *** ###
    num_ex = 30
    ###  **  ###

    for i in range(num_ex):
        u = all_keys[random.randint(0, len(all_keys) - 1)]
        if not u in models.keys(): models[u] = mv.read_model(u) 
        # models maps ID u to its model.

    checked = []
    for x, x_v in models.iteritems():
        checked.append(x)
        for y, y_v in models.iteritems():
            if not y in checked:
                val = cos_sim(x_v, y_v)*100
                if math.floor(val) - val < 0.5: val = math.floor(val)
                else: val = math.ceil(val);
                sims.append(val)

    sim_counts = defaultdict(int) # <-  not sortable!
    for p in sims:
        sim_counts[p] += 1
    print len(sims), get_E(sim_counts), get_mean(sims), get_var(sim_counts)
    print "distribution dump:"
    for x in sim_counts.keys():
        for i in range(min(sim_counts[x], 75)): sys.stdout.write('-')
        if sim_counts[x]>75: sys.stdout.write(' ... ')
        sim_counts[x] = math.ceil(sim_counts[x] * 0.01)
        s = str(x*0.01)
        if x > 0.15:
            s = s + " , "
        s = s + "\n"
        sys.stdout.write(s)







if __name__ == "__main__":
    args = sys.argv[1:]
    main(args)

