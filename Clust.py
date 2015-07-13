# Clust.py

import time, random, os, os.path, math, sys
# from collections import defaultdict
# import pydot
import pyparsing as pp
# import pygraphviz
# import graphs
# import BestMatches as bm
import my_helpers
# from trove.curation.tools.chanifier.importer import ModelViewer

# some of the code in this class was adapted from/inspired by 
# http://blog.teamtreehouse.com/operator-overloading-python .

##########
# Clust: An overarching class to 1) hold Graph, Node, Edge, and Cluster objects and
#  2) to provide most of the utility functions as needed by the clustering process.
class Clust(object):
    G = None
    def __init__(self, filename='graph_file.txt'):
        if filename:
            f = open(filename, 'r')
            self.G = self.Graph(self.read_dict_from_file(f))
            f.close()


    ##########
    # Cluster has two purposes: 1) be a collection of Nodes and provide functions on/for
    # them and 2) simplify the process of determining what edges are and are not within 
    # the cluster itself (ie, all e for which both e.src and e.dest are in cluster.V)
    class Cluster(object):
        pass

    ##########
    # Graph: a glorified, 'robust-ified' dictionary of verticies (as Nodes) to lists of 
    # each such vertex's outgoing Edges.  The class usage is much better over the simple dict
    # usage due mainly to the trouble you'd have to go through iterating through Node objs, etc.
    class Graph(object):
        graph = {}
        nodenames = []

        def __init__(self, in_graph):
            self.graph = in_graph  # maps named Nodes to list of Edges 
            

        # returns the str name of the node specified by n if it exists; else, returns None.
        def getN(self, n): 
            if isinstance(n, str):
                if self.existNode(n): return n
                else: return None
            elif isinstance(n, type(self.graph.keys()[0])):
                if self.existNode(n.name): return n
                else: return None
            else:
                return None

        # returns T/F : if sname is the name of a node in the dict
        def getNode(self, sname):
            if sname in self.NodeNames(): return True; return False

        # returns a list of the names of each node in the graph.
        def NodeNames(self):
            if len(self.nodenames) == 0:
                for k in self.graph.keys():
                    if k.name not in nodenames:
                        nodenames.append(k.name)
            return list(nodenames)


    ##########
    # Node: an object wrapper for the vertex name.  As is, it is mostly an unnecessary compli-
    # cation, as all it does is wrap a string name; however, if we need to add other fields like
    # ID numbers to these nodes, it would be a matter simply of making this class consistent 
    # with those demands. Also provides desired comparison overloads.
    class Node(object):
        def __init__(self, name):
            self.name = name
        def __eq__(self, other):
            if isinstance(other, type(self)):
                return self.name == other.name
            elif isinstance(other, str):
                return self.name == other
            else:
                return None

    ##########
    # Edge: an object wrapper for a single, quasi-directed edge.  Specifies a src and a dest as
    # well as the weight.  Is the class analog of the simple 3-tuple.  
    class Edge(object):
        def __init__(self, tup):
            self.src = str(tup[0])
            self.dest = str(tup[1])
            self.weight = float(tup[2])
        def __eq__(self, other):
            print self.src, self.dest, self.weight, ' -- ', other
            if isinstance(other, type(self)):
                return self.src == other.src and self.dest == other.dest \
                    and self.weight == other.weight
            elif isinstance(other, tuple):
                return self.src == other[0] and self.dest == other[1] and self.weight == other[2]
            else:
                return None

    ################################################################################
    # Clust's class functions. Have access to all Clust's fields, functions, classes.


    def quick_test(self, n1='Poland', n2='Brunei'):
        N1 = self.Node(n1)
        N2 = self.Node(n2)
        print N1 == N2, N1 == N1
        for N in self.graph.keys():
            sys.stdout.write( N.name + ', ')
        print '.\n'
        E1 = self.graph.getN(N1) # ******
        Eset = self.graph[N2]
        print E1 in Eset
        
   
    def read_dict_from_file(self, f):
    # takes a file and reads its contents as a dict of Nodes to a list of Edges 
        f.read(1)
        graph = {}
        while True:
            line = f.readline()
            if not line: break
            line.strip("{}[],'")
            k, v = line.split(': ')
            k = k.strip("'")
            v = v.strip('[]},\n').split('), (')
            n = self.Node(k)
            graph[n] = []
            for t in v:
                t = t.strip(")'](\n, ").split("', '")
                graph[n].append(self.Edge(tuple(t[:3])))
        return graph


