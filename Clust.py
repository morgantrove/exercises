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

class Clust(object):
    graph = {}

    def __init__(self, filename='graph_file.txt'):
        if filename:
            f = open(filename, 'r')
            self.graph = self.read_dict_from_file(f)
            f.close()


    class Cluster(object):
        pass
    class Node(object):
        def __init__(self, name):
            self.name = name
    class Edge(object):
        def __init__(self, tup):
            self.src = tup[0]
            self.dest = tup[1]
            self.weight = float(tup[2])


   
    def read_dict_from_file(self, f):
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

    def match_parenthesis(text):
    # Returns the index of the matching parenthesis. Returns -1 if unmatched.
        begun = False
        counter = 0
        for c in range(0, len(text)):
            if counter < 0: return -1
            if text[c] == ('[' or '{' or '('):
                counter += 1
                if not begun: begun = True
            if text[c] == (']' or '}' or ')'):
                counter -= 1
            if counter == 0 and begun: return c
        return -1
     
   
    
