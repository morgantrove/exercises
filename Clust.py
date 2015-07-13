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

##########################################################################################
##############################     Cluster
# Cluster has two purposes: 1) be a collection of Nodes and provide functions on/for
# them and 2) simplify the process of determining what edges are and are not within 
# the cluster itself (ie, all e for which both e.src and e.dest are in cluster.V)
class Cluster(object):
    pass

################################################################################
##############################     Graph
# Graph: a glorified, 'robust-ified' dictionary of verticies (as Nodes) to lists of 
# each such vertex's outgoing Edges.  The class usage is much better over the simple dict
# usage due mainly to the trouble you'd have to go through iterating through Node objs, etc.
class Graph(object):
    graph = {}
    n_names = {} # use wrapper function NodeNames() to get names. Maps to indices.

    def __init__(self, in_graph):
        self.graph = in_graph  # maps named Nodes to list of Edges 
            

    # *~*~* This function is recommended as a user function *~*~*
    # Returns the str name of the node specified by n if it exists; else, returns None.
    # Takes entries as either node objects or strings.
    def getS(self, n): 
        if isinstance(n, str):
            if self.__existNamedNode(n): return n
            else: return None
        elif isinstance(n, type(self.graph.keys()[0])): # ie, isinstance(n, 'Node')
            if self.__existNamedNode(n.name): return n.name
            else: return None
        else:
            return None

    # *~*~* This function is recommended as a user function *~*~*
    # Returns a node specified by n; else, returns None.
    # Takes entries as either node objects or strings.
    def getN(self, n): 
        if isinstance(n, str):
            if self.__existNamedNode(n): return Node(n)
            else: return None
        elif isinstance(n, type(self.graph.keys()[0])): # ie, isinstance(n, 'Node')
            if self.__existNamedNode(n.name): return n
            else: return None
        else:
            return None


    # returns T/F : if sname is the name of a node in the dict
    def __existNamedNode(self, sname):
        if sname in self.NodeNames(): return True; return False

    # returns a list of the names of each node in the graph.
    def NodeNames(self):
        if len(self.n_names) == 0:
            index = 0
            for k in self.graph.keys():
                self.n_names[k.name] = index
                index += 1
        return self.n_names.keys()

    # Returns the list of edges for a query node.  Careful: if such a node doesn't 
    # exist, then it will return an _empty_ list!
    def edges(self, qnode):
        return self.getEdgesFromStrNm(self.getS(qnode))

    def getEdgesFromStrNm(self, str_nm):
        return self.graph.values()[self.n_names[str_nm]] # note: due to Node object's inability
        # to be indexed easily, this method uses a slight workaround, with the marginal
        # disadvantage of requiring the already-in-place memory taken by dict n_names. 



# Generically, Node | str --> Node. Else --> None.
def getNd(n):
    if isinstance(n, str):  return Node(n);
    elif isinstance(n, type(self.graph.keys()[0])):  return n;
    else: return None;



################################################################################
##############################      Node
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
    


################################################################################
##############################      Edge
# Edge: an object wrapper for a single, quasi-directed edge.  Specifies src and dest Nodes
# as well as the float weight.  Is the class analog of the simple 3-tuple.  
class Edge(object):
    def __init__(self, tup):
        self.src = getNd(tup[0])
        self.dest = getNd(tup[1])
        self.weight = float(tup[2])
    def __eq__(self, other):
        print "&&", self.src, self.dest, self.weight, ' -- ', other
        if isinstance(other, type(self)):
            return self.src == other.src and self.dest == other.dest \
                and self.weight == other.weight
        elif isinstance(other, tuple):
            return self.src == other[0] and self.dest == other[1] and self.weight == other[2]
        else:
            return None




################################################################################
##############################      Clust
# Clust: An overarching class to 1) hold Graph, Node, Edge, and Cluster objects and
#  2) to provide most of the utility functions as needed by the clustering process.
class Clust(object):
    G = None
    def __init__(self, filename='graph_file.txt'):
        if filename:
            f = open(filename, 'r')
            self.G = self.Graph(self.read_dict_from_file(f))
            f.close()

    # Clust's class functions. Have access to all Clust's fields, functions, classes.

    def quick_test(self, n1='Poland', n2='Brunei'):
        N1 = self.Node(n1)
        N2 = self.Node(n2)
        print N1 == N2, N1 == N1
        for nname in self.G.NodeNames():
            sys.stdout.write( nname + ', ')
        print '.\n'
        print self.G.n_names.keys()[1], self.G.n_names.values()[1]
        for x in self.G.graph.values()[self.G.n_names.values()[1]]:
            print x.src.name, x.dest.name, x.weight
        E1 = self.Edge((self.G.getN(N1), self.G.getN(N2), 0))
        Eset = self.G.edges(N1)
        print " * ", E1, Eset, ">>"
        
   
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


