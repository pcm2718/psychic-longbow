# Parker Michaleson
# A01248939
# parker.michaelson@gmail.com
# Assignment #3



import random
import math
from timer import Timer
from tspgraph import TSPGraph
from state import State



class Search:

    def search(graph, search, budget):
        searchhash = {
                'fc' : Search.fc_search ,
                'sa' : Search.sa_search
                }

        with Timer() as t:
            return searchhash[search](graph, budget, t)



    def fc_search(graph, budget, timer):
        # Might be able to simplify this.
        cycle = list(range(0, len(graph.nodelist)))
        #random.shuffle(cycle)
        state = State(graph, cycle, [])

        while timer.get_secs() < budget:
            # Apply operation.
            nextstate = state.get_cpy()
            nextstate.swap_nodes()
            deltae = state.cost - nextstate.cost 

            if deltae > 0:
                state = nextstate

        return state



    def schedule(time, budget):
        return float(budget - time)/float(budget)

    def sa_search(graph, budget, timer):
        # Might be able to simplify this.
        cycle = list(range(0, len(graph.nodelist)))
        #random.shuffle(cycle)
        state = State(graph, cycle, [])
        best = state.get_cpy()

        while timer.get_secs() < budget:
            temp = Search.schedule(timer.get_secs(), budget)

            if temp <= 0:
                break

            #nextop = random.choice(oplist)
            nextstate = state.get_cpy()
            nextstate.swap_nodes()
            deltae =  state.cost - nextstate.cost

            if deltae > 0:
                state = nextstate
            else:
                if math.exp(float(deltae)/float(temp)) > random.uniform(0,1):
                    state = nextstate

            if state.cost < best.cost:
                best = state.get_cpy()

        return best
