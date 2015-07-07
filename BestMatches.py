import random
from trove.curation.tools.chanifier.importer import ModelViewer
import requests

class BestMatches:
    mv = ModelViewer()
    model_map = {}

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
                self.model_map[ch].append(self.mv.read_model(ch[0]))
        else:
            counter = self.nchs
            ch = self.makeTuple(self.mc[random.randrange(0,self.tot_num_chs-1)][0])
            while counter > 0:
                if not ch in self.model_map.keys():
                    self.model_map[ch] = []
                    self.model_map[ch].append(self.mv.read_model(ch[0]))
                    counter -= 1
                ch = self.makeTuple(self.mc[random.randrange(0,self.tot_num_chs-1)][0])

    def dump(self):
        for k,v in self.model_map: # hack city hack hack city
            print k
            print v
            print type(self.model_map[(k,v)])
            return

    def compute(self):
        for ch_pair in self.model_map:
            pass
        pass



