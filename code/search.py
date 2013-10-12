# Parker Michaleson
# A01248939
# parker.michaelson@gmail.com
# Assignment #3



import sys
import math
import time
import random
from timer import Timer
from tspgraph import TSPGraph



class State:

    def __init__(self, graph, visit_list=[], prevcosts=[]):
        self.graph = graph
        self.prevcosts = prevcosts

        if visit_list == []:
            for x in graph.nodelist:
                visit_list.append(x[0])
            random.shuffle(visit_list)
        self.visit_list = visit_list[:]

        self.cost = 0
        for i in range(0, len(self.visit_list)-1):
            self.cost += graph.adjmatrix.get_adjvalue(visit_list[i], visit_list[i+1])
        self.cost += graph.adjmatrix.get_adjvalue(visit_list[-1], visit_list[0])



    def apply_op(self, op):
        visit_list = op(self.visit_list)
        return State(self.graph, visit_list, self.prevcosts + [self.cost])



class SolutionSearch:

    def __init__(self, graphfile="tsp225.txt"):
        self.graphfile = graphfile



    # This function for diagnostic purposes only.
    def search(self, func, graph, ops, maxittr):
        for i in range(0, maxittr+1):
            print ""
            s = func(graph, ops, pow(2, i))
            print "Iterations: " + str(pow(2, i))
            print ""
            print func.__name__ + ":"
            print s.visit_list
            print "Final Cost: " + str(s.cost)
            #print "Previous Costs: " + str(s.prevcosts)
            print ""
            print ""



    def generate_prob_1(self, func, ops, maxittr, outfile_name):
        for k in range(5, 225, 5):
            graph = TSPGraph(self.graphfile, k)

            #outfile = open(outfile_name, 'w')

            #timelist = []
            with Timer() as t:
                s = func(graph, ops, pow(2, maxittr))

            #infolist.append([i, s.visited_list])

            print ""
            print func.__name__ + ":"
            print "Nodes: " + str(len(graph.nodelist))
            print "Iterations: " + str(pow(2, maxittr))
            print "Visit Order: " + str(s.visit_list)
            print "Final Cost: " + str(s.cost)
            print "Time: " + str(t.secs)
            print ""

        #for s in statelist:
            #s = map(lambda x : str(graph.nodelist[x][1]) + ' ' + str(graph.nodelist[x][2]) + '\n', s)

            #for t in s:
                #outfile.write(t)
            #outfile.write('\n\n')



    def generate_linedata(self, outfile_name):
        funclist = [self.search_a, self.search_b, self.search_c, self.search_d]
        graph = TSPGraph(self.graphfile, 225)

        outfile = open(outfile_name, 'w')

        statelist = []
        linelist = []
        for func in funclist:
            with Timer() as t:
                s = func(graph, t)

            statelist.append(s.visited_list)

            print ""
            print "# " + str(len(graph.nodelist)) + " nodes, " + func.__name__
            print "# " + str([node for node in s.visited_list])
            print "# " + str([graph.idlookup[node] for node in s.visited_list])
            print "# " + str(s.current_cost)
            print str(len(graph.nodelist)) + " " + str(t.secs)
            print ""

        for s in statelist:
            s = map(lambda x : str(graph.nodelist[x][1]) + ' ' + str(graph.nodelist[x][2]) + '\n', s)

            for t in s:
                outfile.write(t)
            outfile.write('\n\n')



    def swap_nodes(self, visit_list):
        cpy = visit_list[:]

        i = random.randint(0, len(cpy)-1)
        j = random.randint(0, len(cpy)-1)

        temp = cpy[i]
        cpy[i] = cpy[j]
        cpy[j] = temp

        return cpy



    def twoopt(self, visit_list):
        cpy = visit_list[:]

        i = random.randint(0, len(cpy)-1)
        j = random.randint(0, len(cpy)-1)

        i_0 = cpy[i]
        i_1 = cpy[i+1]
        j_0 = cpy[j]
        j_1 = cpy[j+1]

        cpy[i+1] = j_1
        cpy[j+1] = i_1

        return cpy

 

    def five_cycle(self, visit_list):
        cpy = visit_list[:]

        nodelist = []
        for i in range(0, 5):
            nodelist.append(random.randint(0, len(cpy)-1))

        for i in nodelist:
            temp = cpy[i]
            cpy.remove(temp)
            cpy.append(temp)

        return cpy



    def first_choice_search(self, graph, oplist, maxittr):
        state = State(graph)

        for i in range(0, maxittr):
            nextop = random.choice(oplist)
            nextstate = state.apply_op(nextop)

            deltae = state.cost - nextstate.cost 

            if deltae > 0:
                del(state)
                state = nextstate

        return state



    def schedule(self, ittr, maxittr):
        return float(maxittr - ittr)/float(maxittr)

    def simulated_annealing_search(self, graph, oplist, maxittr):
        state = State(graph)
        best = state

        for i in range(0, maxittr):
            temp = self.schedule(i, maxittr)

            if temp <= 0:
                break

            nextop = random.choice(oplist)
            nextstate = state.apply_op(nextop)

            deltae =  state.cost - nextstate.cost

            if deltae > 0:
                state = nextstate
            else:
                if math.exp(float(deltae)/float(temp)) > random.uniform(0,1):
                    state = nextstate

            if state.cost < best.cost:
                best = state

        return best





s = SolutionSearch()
graph = TSPGraph("tsp225.txt", 225)

#s.search(s.first_choice_search, graph, [s.swap_nodes], 20)
#s.search(s.simulated_annealing_search, graph, [s.swap_nodes], 20)
s.generate_prob_1(s.first_choice_search, [s.swap_nodes], 15, "timedata.dat")
