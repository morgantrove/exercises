import random
from trove.curation.tools.chanifier.importer import ModelViewer

class BestMatches:
    mv = ModelViewer()

    def __init__(self, nchannels=50):
        if nchannels < 2: 
            raise ValueError("Improper number of random channels")
        self.mc = self.mv.model_channels()
        self.tot_num_chs = len(self.mc)
        self.nchs = nchannels
        if nchannels > self.tot_num_chs:
            raise ValueError("Improper number of random channels")
        print 'successful initialization. [01]'

    model_map = {}
    # If repetitions is True, then there is a nchs/len(mc)
    def setup(self, repetitions = True): 
        for i in range(self.nchs):
            x = random.randrange(0,5002)
            if not repetitions:
                while x in self.model_map.keys():
                    x = random.random(0,5002)
            
