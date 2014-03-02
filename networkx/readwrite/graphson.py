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

__all__ = ['write_graphson', 'read_graphson', 'generate_graphson',
           'parse_graphml', 'GraphMLWriter', 'GraphMLReader']

import networkx as nx
from networkx.utils import open_file, make_str
import warnings


