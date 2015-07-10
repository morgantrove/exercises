# graphs.py

import my_helpers
import time, random, os, BestMatches, math, sys, os.path
from collections import defaultdict
from trove.curation.tools.chanifier.importer import ModelViewer
import pydot
import pyparsing


def BuildGraph_d_tup(d, directed = False):
    # format: dictionary of verts_1 to 2-tuples of (verts_2, weights), as created by BestMatches' analyze.
    rets = []
    """  These following lines are useful information if you want to know if there are
         nodes that are 'sinks' or 'sources'.  Useful if directed == True. """
    if directed:
        sinks = False # code is set to False iff verts_2 is a subset of d.keys()==verts_1.
        sources = False # code is set to False iff d.keys()==verts_1 is a subset of verts_2.
        found_targs = set()
        for d_k in d.keys():
            for d_k_neighbor in d[d_k]:
                found_targs = found_targs | set(d_k_neighbor[0])
                if d_k_neighbor[0] not in d.keys():
                    sinks = True
        for d_k in d.keys():
            if d_k not in found_targs:
                sources = True
        rets.append(sinks)
        rets.append(sources)

    V = d.keys()
    E = []
    for v1 in d.keys():
        E.append([(v1, v2, w[:-1]) for v2, w in d[v1]])

    rets.append(V); rets.append(E)
    return rets

def makeDotGraph(g, name="default_name"):
# g as in a 2-long array of node_names, lists of edges_w/_weights_per_node, as from BuildGraph above
    dot_obj = pydot.Dot(directed=False)
    for n in g[0]:
        dot_obj.add_node(pydot.Node(n))
    for ind in range(len(g[1])):
        for e in g[1][ind]:
            n1 = e[0]
            n2 = e[1]
            w = e[2]
            dot_obj.add_edge(pydot.Edge(n1, n2, weight=w))
    if os.path.isfile(name+'.png'):
        print "File",name,"already exists. Please enter a new name as a second makeDotGraph argument."
    else:
        open(name+".png", 'w').close()
        time.sleep(1)
        dot_obj.write_png(name+".png")

def forceDirect(g, time_to_run=0, delay=0):
    # Applies a force-directed transformation to a BestMatches.analyze(..) graph.  Returns it with
    # new edge weights. Ported from my own (MRB) CS106L assignment GraphViz.
    while time_to_run == 0:
        new_ttr = input("Please enter how many seconds to run the prog: ")
        if new_ttr.isdigit() and len(str(new_ttr)) > 0 and new_ttr > 0 and new_ttr <= 30:
            time_to_run = new_ttr
            print "Running for", time_to_run, "second:"

        
