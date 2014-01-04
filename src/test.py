from tspgraph import TSPGraph
from search import Search
from timer import Timer

import sys

graph = TSPGraph()

with Timer() as v:
    res = Search.search(graph, str(sys.argv[1]), float(sys.argv[2]))

print(str(sys.argv[1]) + "!" + str(sys.argv[2]) + "!" + str(res.cost) + "!" + str([graph.idlookup[x] for x in res.cycle]))
