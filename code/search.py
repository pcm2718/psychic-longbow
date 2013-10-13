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

    def __init__(self, graph, visit_list=None, prevcosts=[]):
        self.graph = graph
        self.prevcosts = prevcosts

        self.visit_list=[]
        if visit_list == None:
            for x in graph.nodelist:
                self.visit_list.append(x[0])
            random.shuffle(self.visit_list)
        else:
            self.visit_list = visit_list[:]

        self.cost = 0
        for i in range(0, len(self.visit_list)-1):
            self.cost += graph.adjmatrix.get_adjvalue(self.visit_list[i], self.visit_list[i+1])
        self.cost += graph.adjmatrix.get_adjvalue(self.visit_list[-1], self.visit_list[0])



    def apply_op(self, op):
        return State(self.graph, op(self.visit_list), self.prevcosts + [self.cost])



class SolutionSearch:

    def __init__(self, graphfile="tsp225.txt"):
        self.graphfile = graphfile



    # This function for diagnostic purposes only.
    def search(self, func, graph, ops, maxittr):
        for i in range(0, maxittr+1):
            print ""
            s = func(graph, ops, pow(2, i))
            print func.__name__ + ":"
            print "Index: " + str(i)
            print "Iterations: " + str(pow(2, i))
            print "Checksum: " + str(sum(s.visit_list))
            print "Visit List: " + str(s.visit_list)
            print "Final Cost: " + str(s.cost)
            #print "Previous Costs: " + str(s.prevcosts)
            print ""
            print ""



    def generate_prob_1(self, func, ops, maxittr, outfile_name):
        infolist = []

        for k in range(5, 225, 5):
            graph = TSPGraph(self.graphfile, k)

            timelist = []
            for i in range(0, 5):
                with Timer() as t:
                    s = func(graph, ops, pow(2, maxittr))

                print ""
                s = func(graph, ops, pow(2, maxittr))
                print func.__name__ + ":"
                print "Index: " + str(k)
                print "Iterations: " + str(pow(2, maxittr))
                print "Checksum: " + str(sum(s.visit_list))
                print "Time: " + str(t.msecs)
                print "Visit List: " + str(s.visit_list)
                print "Final Cost: " + str(s.cost)

                timelist.append(t.msecs/5.0)

            infolist.append([str(k), str(sum(timelist))])

        outfile = open(outfile_name, 'w')
        for x in infolist:
            outfile.write(infolist[0] + ' ' + infolist[1] + '\n')
        outfile.close()



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



    def rand_subset(self, visit_list):
        cpy = visit_list[:]

        length = random.randint(2, min(20, len(visit_list)))
        if len(visit_list) == length:
            start = 0
        else:
            start = random.randint(0, len(visit_list)-length)

        tmp = cpy[start:start+length]
        random.shuffle(tmp)
        cpy[start:start+length] = tmp

        return cpy



    def reverse_subset(self, visit_list):
        cpy = visit_list[:]

        length = random.randint(2, min(20, len(visit_list)))
        if len(visit_list) == length:
            start = 0
        else:
            start = random.randint(0, len(visit_list)-length)

        tmp = cpy[start:start+length]
        tmp.reverse()
        cpy[start:start+length] = tmp

        return cpy



    def shift_subset():
        pass



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

#s.search(s.first_choice_search, graph, [s.swap_nodes, s.rand_subset, s.reverse_subset], 20)
#s.search(s.simulated_annealing_search, graph, [s.swap_nodes, s.rand_subset, s.reverse_subset], 20)
s.generate_prob_1(s.first_choice_search, [s.swap_nodes, s.rand_subset, s.reverse_subset], 15, "fctimedata.dat")
s.generate_prob_1(s.simulated_annealing_search, [s.swap_nodes, s.rand_subset, s.reverse_subset], 15, "satimedata.dat")
