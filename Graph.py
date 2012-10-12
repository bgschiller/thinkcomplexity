"""
Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""
import collections
import string

class Vertex(object):
    """A Vertex is a node in a graph."""

    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        """Returns a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Edge(tuple):
    """An Edge is a list of two vertices."""

    def __new__(cls, *vs):
        """The Edge constructor takes two vertices."""
        if len(vs) != 2:
            raise ValueError, 'Edges must connect exactly two vertices.'
        return tuple.__new__(cls, vs)

    def __repr__(self):
        """Return a string representation of this object that can
        be evaluated as a Python expression."""
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
    """The str and repr forms of this object are the same."""


class Graph(dict):
    """A Graph is a dictionary of dictionaries.  The outer
    dictionary maps from a vertex to an inner dictionary.
    The inner dictionary maps from other vertices to edges.
    
    For vertices a and b, graph[a][b] maps
    to the edge that connects a->b, if it exists."""

    def __init__(self, vs=[], es=[]):
        """Creates a new graph.  
        vs: list of vertices;
        es: list of edges.
        """
        for v in vs:
            self.add_vertex(v)
            
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        self[v] = {}

    def add_edge(self, e):
        """Adds and edge to the graph by adding an entry in both directions.

        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, v, w):
        """retrieves the edge between v and w if one exists, and None otherwise"""
        try:
            return self[v][w]
        except KeyError:
            return None

    def remove_edge(self, e):
        """given an edge e, remove all references to it"""
        v, w = e
        del self[v][w]
        del self[w][v]

    def vertices(self):
        return self.keys()

    def edges(self):
        retval = set([])
        for v in self.vertices():
            for w in self.vertices():
                e = self.get_edge(v,w)
                if e is not None:
                    retval.add(e)
        return retval

    def out_vertices(self, v):
        return self[v].keys()

    def out_edges(self, v):
        return map(lambda w: self[v][w], self.out_vertices(v))
       
    def _all_vert_pairs(self):
        pairs = []
        verts = self.keys()
        for ix, v in enumerate(verts):
            for w in verts[ix+1:]: #verts[ix+1:] is every vert past v in the list
                pairs.append((v,w))
        return pairs

    def add_all_edges(self):
        for pair in self._all_vert_pairs():
            (v,w) = pair
            self[v][w] = Edge(v,w)
            self[w][v] = self[v][w]

    def add_regular_edges(self, kay):
        assert kay * len(self.vertices()) % 2 == 0 # k*n is even
        assert kay < len(self.vertices()) # k < n
        assert kay >= 0 and int(kay) == kay # kay is a non-negative integer
        for edge in self.edges():
            self.remove_edge(edge)
        num_neighbors = kay / 2
        verts = self.vertices()
        
        def neighbors(verts, ix):
            retval = []
            nn = num_neighbors
            offset = 1
            while nn > 0:
                if ix + offset >= len(verts):
                    offset -= len(verts)
                retval.append(verts[ix + offset])
                nn -= 1
            return retval

        for ix, v in enumerate(verts):
            for neighbor in neighbors(verts, ix):
                self.add_edge(Edge(v,neighbor))
            if num_neighbors *2 != kay: # i.e. kay is odd and we can't cut it in half.
                self.add_edge(Edge(v,verts[ix-len(verts)/2]))

        for v in verts:
            assert len(self.out_vertices(v)) == kay

    def is_connected(self):
        verts = self.vertices()
        if len(verts) == 0:
            return True
        q = collections.deque()
        visited = dict.fromkeys(self.vertices(), False)
        q.append(verts[0])
        visited[verts[0]] = True
        while len(q) > 0:
            v = q.popleft()
            for w in self.out_vertices(v):
                if not visited[w]:
                    visited[w] = True
                    q.append(w)
        return all(visited.values())

def labels(n):
    elements = string.ascii_lowercase + string.ascii_uppercase
    for c, i in zip(elements, xrange(n)):
        yield c
    for a, b, i in zip(labels(n - len(elements)),labels(n - len(elements)), xrange(n - len(elements))):
        yield a + b

def main(script, *args):
    v = Vertex('v')
    print v
    w = Vertex('w')
    print w
    e = Edge(v, w)
    print e
    g = Graph([v,w], [e])
    print g
    new = Vertex("new'un")
    g.add_vertex(new)
    print 'added vertex {}'.format(new)
    g.add_all_edges()
    print 'should include all edges: {}'.format(g)
    g.remove_edge(e)
    print 'should be missing edge {} : {}'.format(e,g)
    print 'the vertices are {}'.format(g.vertices())
    print 'the edges are {}'.format(g.edges())
    print 'out edges of {} are {}'.format(v, g.out_edges(v))

    print '\ntesting regular graph...'
    k = input('enter the degree')
    g.add_regular_edges(k)
    print 'added regular edges: {}'.format(g)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
