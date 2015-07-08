import random
import sys
from trove.curation.tools.chanifier.importer import ModelViewer
import requests

class BestMatches:
    mv = ModelViewer()
    model_map = {} # A mapping of channel pairs to a _short_ list (usually size 1) which contains
                   #   (identical) cop(ies) of the pairs' corresponding similarity measures.
    simil_map = {} # A map of each pair of channels and their respective similaries.

    def __init__(self, nchannels=50):
        if nchannels < 2: 
            raise ValueError("Improper number of random channels")
        self.mc = self.mv.model_channels()
        self.tot_num_chs = len(self.mc)
        self.nchs = nchannels
        if nchannels > self.tot_num_chs:
            raise ValueError("Improper number of random channels")
        print 'successful initialization. [01]'

    def makeTuple(self, ch_id):
        # gets the channel's label, using the Trove API (since mc doesn't have it)
        api_call = requests.get("http://internal-api.trove.com/channels/"+str(ch_id))
        if not api_call.status_code == 200:
            raise IOError("Trove API does not recognize channel "+str(ch_id))
        label = api_call.text[api_call.text.find("displayName")+15:]
        label = label[:label.find('", "id":')]
        return (ch_id, label)

 

    # If repetitions is True, then there is a nchs/len(mc) probability of repeated entries.
    def setup(self, repetitions = True): 
        self.model_map = {} # <- model map gets wiped!
        if repetitions:
            for i in range(self.nchs):
                ch = self.makeTuple(self.mc[random.randrange(0,self.tot_num_chs-1)][0])
                if not ch in self.model_map.keys():
                    self.model_map[ch] = []
                    d1 = self.mv.read_model(ch[0])
                    d2 = {}
                    for a,b in d1: d2[b] = d1[(a,b)]
                    self.model_map[ch].append(d2)
        else:
            counter = self.nchs
            ch = self.makeTuple(self.mc[random.randrange(0,self.tot_num_chs-1)][0])
            while counter > 0:
                if not ch in self.model_map.keys():
                    self.model_map[ch] = []
                    d1 = self.mv.read_model(ch[0])
                    d2 = {}
                    for a,b in d1: d2[b] = d1[(a,b)]
                    self.model_map[ch].append(d2)
                    counter -= 1
                ch = self.makeTuple(self.mc[random.randrange(0,self.tot_num_chs-1)][0])

    def dump(self):
        for k,v in self.model_map: # hack city hack hack city
            print k
            print v
            print self.model_map[(k,v)], self.model_map[(k,v)][0]
            return

    def cos_sim(self, x,y):
        tot = 0
        keys = set(self.model_map[x][0].keys()) | set(self.model_map[y][0].keys())
        for k in keys:
            tot += self.model_map[x][0].get(k,0) * self.model_map[y][0].get(k,0)
        return tot

    def compute(self):
        if len(self.model_map) == 0: return
        for ch1 in self.model_map:
            """print type(ch1)
            print type(self.model_map)
            print type(self.model_map[ch1])
            print type(self.model_map[ch1][0])"""
            l = []
            for ch2 in self.model_map:
                if not ch1 == ch2: 
                    l.append((ch1, ch2, self.cos_sim(ch1, ch2))) # a list of 3-tuples
            l.sort(key = lambda x : -x[2])
            self.simil_map[ch1] = l

    def render(self):
        all_cmp = []
        for k in self.simil_map.keys():
            for tup in self.simil_map[k]: 
                all_cmp.append((tup[0][1], tup[1][1], tup[2]))
        all_cmp.sort(key = lambda x: -x[2])
        print str(self.nchs)+" randomly chosen channels, ranked by similarity:"
        for x in all_cmp:
            print "'"+str(x[0])+"' & '"+str(x[1])+"' :  "+str(x[2])


