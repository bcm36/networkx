"""
*******
GraphSON
*******
Read and write graphs in GraphSON format.

This implementation does not support mixed graphs (directed and unidirected
edges together), hyperedges, nested graphs, or ports.

"GraphSON is a JSON-based format for individual graph elements
(i.e. vertices and edges). How these elements are organized and
utilized when written as a complete graph can also be considered
GraphSON format.

In other words, the schema for GraphSON is very flexible and therefore,
any JSON document or fragment that is produced by or can be consumed by
the Blueprints IO packages can be considered valid GraphSON."

https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library

Format
------
GraphSON is a JSON-based format for individual graph elements
(i.e. vertices and edges).  It is used in the Blueprints interface.

For more information and examples, see
https://github.com/tinkerpop/blueprints/wiki/GraphSON-Reader-and-Writer-Library
"""
__author__ = """\n""".join(['Salim Fadhley',
                            'Aric Hagberg (hagberg@lanl.gov)'
                            ])

__all__ = ['parse_graphson', 'read_graphson', 'write_graphson', 'GraphSONReader', 'GraphSONWriter']

import networkx as nx
from networkx.utils import open_file, make_str
import warnings
import json
import collections

@open_file(1,mode='wb')
def write_graphson(G, path, encoding='utf-8',prettyprint=True):
    """Write G in GraphML XML format to path

    Parameters
    ----------
    G : graph
       A networkx graph
    path : file or string
       File or filename to write.
       Filenames ending in .gz or .bz2 will be compressed.
    encoding : string (optional)
       Encoding for text data.
    prettyprint : bool (optional)
       If True use line breaks and indenting in output XML.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> nx.write_graphml(G, "test.graphml")

    Notes
    -----
    This implementation does not support mixed graphs (directed and unidirected
    edges together) hyperedges, nested graphs, or ports.
    """
    writer = GraphSONWriter(encoding=encoding,prettyprint=prettyprint)
    writer.set_graph(G)
    writer.dump(path)

@open_file(0,mode='rb')
def read_graphson(path,node_type=str):
    """Read graph in GraphSON format from path.

    Parameters
    ----------
    path : file or string
       File or filename to write.
       Filenames ending in .gz or .bz2 will be compressed.

    node_type: Python type (default: str)
       Convert node ids to this type

    Returns
    -------
    graph: NetworkX graph
        If no parallel edges are found a Graph or DiGraph is returned.
        Otherwise a MultiGraph or MultiDiGraph is returned.

    Notes
    -----
    This implementation does not support mixed graphs (directed and unidirected
    edges together), hypergraphs, nested graphs, or ports.

    """
    reader = GraphSONReader(node_type=node_type)
    # need to check for multiple graphs

    return reader(path=path)

def parse_graphson(graphson_string, node_type=str):
    """Read graph in GraphSON format from string.

    Parameters
    ----------
    graphson_string : string
       String containing graphml information
       (e.g., contents of a graphml file).

    node_type: Python type (default: str)
       Convert node ids to this type

    Returns
    -------
    graph: NetworkX graph
        If no parallel edges are found a Graph or DiGraph is returned.
        Otherwise a MultiGraph or MultiDiGraph is returned.

    Examples
    --------
    >>> G=nx.path_graph(4)
    >>> linefeed=chr(10) # linefeed=\n
    >>> s=linefeed.join(nx.generate_graphson(G))
    >>> H=nx.parse_graphson(s)

    Notes
    -----
    This implementation does not support mixed graphs (directed and unidirected
    edges together), hypergraphs, nested graphs, or ports.

    """
    reader = GraphSONReader(node_type=node_type)

    # need to check for multiple graphs
    glist=reader(data_dict=json.loads(graphson_string))

    return glist

class GraphSONWriter(object):
    def __init__(self, graph=None, encoding="utf-8",prettyprint=True):

        self.prettyprint=prettyprint
        self.encoding = encoding
        self.keys={}

        self.data = {}

        if graph is not None:
            self.set_graph(graph)


    def __str__(self):
        if self.prettyprint:
            pass #@todo pprint json
            #self.indent(self.xml)

        return json.dump(self.data)

    def set_graph(self, G):
        """
        Replaces any data with graph G
        """
        #retain order (vertices must come first)
        self.data = collections.OrderedDict()
        self.data['vertices'] = []
        self.data['edges'] = []

        for node,data in G.nodes_iter(data=True):
            d = {'_id':node, '_type':'vertex'}
            d.update(data)

            self.data['vertices'].append(d)


        if G.is_multigraph():
            for src,dest,key,data in G.edges_iter(data=True, keys=True):
                d = {'_id':key, '_outV':src, '_inV':dest, '_type':'edge'}
                self.data['edges'].append(d)
        else:
            for src,dest,data in G.edges_iter(data=True):
                d = {'_outV':src, '_inV':dest, '_type':'edge'}
                edge_id = data.get('id',None)
                if edge_id:
                    d['_id'] = edge_id

                self.data['edges'].append(d)

    def dump(self, stream):
        if self.prettyprint:
            #self.indent(self.xml)
            pass

        s = json.dump(self.data, stream)

    def indent(self, elem, level=0):
        # in-place prettyprint formatter
        i = "\n" + level*"  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i


class GraphSONReader(object):
    """Read a GraphSON document.  Produces NetworkX graph objects.
    """
    def __init__(self, node_type=str):
        self.node_type=node_type
        self.multigraph=False # assume multigraph and test for parallel edges

    def __call__(self, path=None, data_dict=None):
        if path is not None:
            return self.make_graph(json.loads(path.read()))
        elif data_dict is not None:
            return self.make_graph(data_dict)
        else:
            raise ValueError("Must specify either 'path' or 'data_dict' as kwarg.")

    def make_graph(self, graph_dict):
        try:
            #access dict with vertices & edges
            graph_dict = graph_dict['graph']
        except KeyError:
            pass

        self.mode = graph_dict.get("mode", "NORMAL")

        # set default graph type (MultiDiGraph)
        G=nx.MultiDiGraph()

        # add nodes
        if self.mode == "NORMAL":
            for node_dict in graph_dict['vertices']:
                self.add_node(G, node_dict)

            # add edges
            for edge_dict in graph_dict['edges']:
                self.add_edge(G, edge_dict)

            # add graph data
            G.graph.update(graph_dict)

        else:
            raise nx.NetworkXError("Unrecognized GraphSON 'mode'")

        # switch to Graph or DiGraph if no parallel edges were found.
        if not self.multigraph:
            if G.is_directed():
                return nx.DiGraph(G)
            else:
                return nx.Graph(G)
        else:
            return G

    def add_node(self, G, node_dict):
        """Add a node to the graph.
        """
        # find the node by id and cast it to the appropriate type
        node_id = self.node_type(node_dict.get("_id"))

        G.add_node(node_id, node_dict)

    def add_edge(self, G, edge_dict):
        """Add an edge to the graph.
        """
        source = self.node_type(edge_dict.get("_outV"))
        target = self.node_type(edge_dict.get("_inV"))

        edge_id = edge_dict.get("_id", None)
        data = {}
        if edge_id:
            data["id"] = edge_id

        if G.has_edge(source,target):
            # mark this as a multigraph
            self.multigraph=True

        G.add_edge(source, target, key=edge_id, **data)

