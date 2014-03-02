#!/usr/bin/env python
from nose.tools import *
from nose import SkipTest
import networkx as nx
import io
import tempfile
import os
import json

class TestGraph(object):

    def setUp(self):
        self.simple_directed_data="""{
          "graph": {
            "mode":"NORMAL",
            "vertices":[
              {
                "_id":"n0",
                "_type":"vertex"
              },
              {
                "_id":"n1",
                "_type":"vertex"
              },
              {
                "_id":"n2",
                "_type":"vertex"
              },
              {
                "_id":"n3",
                "_type":"vertex"
              },
              {
                "_id":"n4",
                "_type":"vertex"
              },
              {
                "_id":"n5",
                "_type":"vertex"
              },
              {
                "_id":"n6",
                "_type":"vertex"
              },
              {
                "_id":"n7",
                "_type":"vertex"
              },
              {
                "_id":"n8",
                "_type":"vertex"
              },
              {
                "_id":"n9",
                "_type":"vertex"
              },
              {
                "_id":"n10",
                "_type":"vertex"
              }
            ],
            "edges": [
              {
                "_id":"foo",
                "_type":"edge",
                "_outV":"n0",
                "_inV":"n2"
              },
              {
                "_type":"edge",
                "_outV":"n1",
                "_inV":"n2"
              },
              {
                "_type":"edge",
                "_outV":"n2",
                "_inV":"n3"
              },
              {
                "_type":"edge",
                "_outV":"n3",
                "_inV":"n4"
              },
              {
                "_type":"edge",
                "_outV":"n3",
                "_inV":"n5"
              },
              {
                "_type":"edge",
                "_outV":"n4",
                "_inV":"n6"
              },
              {
                "_type":"edge",
                "_outV":"n6",
                "_inV":"n5"
              },
              {
                "_type":"edge",
                "_outV":"n5",
                "_inV":"n7"
              },
              {
                "_type":"edge",
                "_outV":"n6",
                "_inV":"n8"
              },
              {
                "_type":"edge",
                "_outV":"n8",
                "_inV":"n7"
              },
              {
                "_type":"edge",
                "_outV":"n8",
                "_inV":"n9"
              }
            ]
          }
        }
        """

        self.simple_directed_graph=nx.DiGraph()
        self.simple_directed_graph.add_node('n10')
        self.simple_directed_graph.add_edge('n0','n2',id='foo')
        self.simple_directed_graph.add_edges_from([('n1','n2'),
                                                   ('n2','n3'),
                                                   ('n3','n5'),
                                                   ('n3','n4'),
                                                   ('n4','n6'),
                                                   ('n6','n5'),
                                                   ('n5','n7'),
                                                   ('n6','n8'),
                                                   ('n8','n7'),
                                                   ('n8','n9'),
                                                   ])

        self.simple_directed_fh = \
            io.BytesIO(self.simple_directed_data.encode('UTF-8'))


    def test_read_simple_directed_graphson(self):
        data = json.loads(self.simple_directed_data)

        G=self.simple_directed_graph
        H=nx.read_graphson(self.simple_directed_fh)
        assert_equal(sorted(G.nodes()),sorted(H.nodes()))
        assert_equal(sorted(G.edges()),sorted(H.edges()))
        assert_equal(sorted(G.edges(data=True)),
                     sorted(H.edges(data=True)))
        self.simple_directed_fh.seek(0)

        I=nx.parse_graphson(self.simple_directed_data)
        assert_equal(sorted(G.nodes()),sorted(I.nodes()))
        assert_equal(sorted(G.edges()),sorted(I.edges()))
        assert_equal(sorted(G.edges(data=True)),
                     sorted(I.edges(data=True)))
