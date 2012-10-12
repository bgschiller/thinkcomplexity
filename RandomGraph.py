#! python
'''A RandomGraph using the Erdos-Renyi model. A special case of Graph'''

import Graph
import random

class RandomGraph(Graph.Graph):
    def add_random_edges(self, prob):
        '''Starting with an edgeless graph, for every pair of nodes, add an edge with probability prob'''
        for edge in self.edges():
            self.remove_edge(edge)
        
        for pair in self._all_vert_pairs():
            if random.random() < prob:
                self.add_edge(Graph.Edge(*pair))

def proportion_connected(num_nodes, prob, num_trials=10):
    labels = string.ascii_lowercase + string.ascii_uppercase
    for trial in xrange(num_trials):
        g = RandomGraph([Vertex(c) for c in labels[:num_nodes]])
        g.add_random_edges

if __name__ == '__main__':
    import GraphWorld
    g = RandomGraph()
    for person in ('Brian','Morgan','David','Teresa','Corbin','Miranda','Remy','Jordan','Heidi'):
        g.add_vertex(Graph.Vertex(person))
    prob = float(input('connect edges with what probability? [0.0,1.0]'))
    g.add_random_edges(prob)
    print 'g {} connected!'.format('is' if g.is_connected() else 'is not')
    layout = GraphWorld.CircleLayout(g)
    gw = GraphWorld.GraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()
