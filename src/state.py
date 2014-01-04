import random



class State:

    def __init__(self, graph, cycle, prevcosts):
        self.graph = graph
        self.cycle = cycle[:]
        self.prevcosts = prevcosts[:]
        self.compute_cost()



    def compute_cost(self):
        # This might be a place for a generator.
        self.cost = sum([self.graph.adjmatrix.get_adjvalue(self.cycle[i], self.cycle[i+1]) for i in range(-1, len(self.cycle)-1)])
        return self.cost



    def get_cpy(self):
        return State(self.graph, self.cycle[:], self.prevcosts[:])



    def swap_nodes(self):
        i = random.randint(0, len(self.cycle)-1)
        j = random.randint(0, len(self.cycle)-1)
        self.cycle[i], self.cycle[j] = self.cycle[j], self.cycle[i]

        # Special fast cost adjustment here?
        self.compute_cost()



    # Don't know if I need to implement this.
    def shift_subset(self):
        pass



    def rand_subset(self):
        length = random.randint(2, min(20, len(cycle)))
        if len(cycle) == length:
            start = 0
        else:
            start = random.randint(0, len(cycle)-length)

        tmp = self.cycle[start:start+length]
        random.shuffle(tmp)
        self.cycle[start:start+length] = tmp

        # Special fast cost adjustment here?
        self.compute_cost()



    def reverse_subset(self):
        length = random.randint(2, min(20, len(cycle)))
        if len(cycle) == length:
            start = 0
        else:
            start = random.randint(0, len(cycle)-length)

        self.cycle[start:start+length] = self.cycle[start:start+length].reverse()
        
        # Special fast cost adjustment here?
        self.compute_cost()
