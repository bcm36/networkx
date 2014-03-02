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


        self.attribute_graph=nx.DiGraph(id='G')
        self.attribute_graph.graph['node_default']={'color':'yellow'}
        self.attribute_graph.add_node('n0',color='green')
        self.attribute_graph.add_node('n2',color='blue')
        self.attribute_graph.add_node('n3',color='red')
        self.attribute_graph.add_node('n4')
        self.attribute_graph.add_node('n5',color='turquoise')
        self.attribute_graph.add_edge('n0','n2',id='e0',weight=1.0)
        self.attribute_graph.add_edge('n0','n1',id='e1',weight=1.0)
        self.attribute_graph.add_edge('n1','n3',id='e2',weight=2.0)
        self.attribute_graph.add_edge('n3','n2',id='e3')
        self.attribute_graph.add_edge('n2','n4',id='e4')
        self.attribute_graph.add_edge('n3','n5',id='e5')
        self.attribute_graph.add_edge('n5','n4',id='e6',weight=1.1)

        self.attribute_data = """{
            "graph": {
                "vertices": [
                    {
                        "_id": "n0",
                        "color": "green"
                    },
                    {
                        "_id": "n1"
                    },
                    {
                        "_id": "n2",
                        "color": "blue"
                    },
                    {
                        "_id": "n3",
                        "color": "red"
                    },
                    {
                        "_id": "n4"
                    },
                    {
                        "_id": "n5",
                        "color": "turquoise"
                    }
                ],
                "edges": [
                    {
                        "_id": "e0",
                        "_outV": "n0",
                        "_inV": "n2",
                        "weight": 1
                    },
                    {
                        "_id": "e1",
                        "_outV": "n0",
                        "_inV": "n1",
                        "weight": 1
                    },
                    {
                        "_id": "e2",
                        "_outV": "n1",
                        "_inV": "n3",
                        "weight": 2
                    },
                    {
                        "_id": "e3",
                        "_outV": "n3",
                        "_inV": "n2"
                    },
                    {
                        "_id": "e4",
                        "_outV": "n2",
                        "_inV": "n4"
                    },
                    {
                        "_id": "e5",
                        "_outV": "n3",
                        "_inV": "n5"
                    },
                    {
                        "_id": "e6",
                        "_outV": "n5",
                        "_inV": "n4",
                        "weight": 1.1
                    }
                ]
            }
        }
        """
        self.attribute_fh = io.BytesIO(self.attribute_data.encode('UTF-8'))

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

    def test_write_read_simple_directed_graphson(self):
        G=self.simple_directed_graph
        fh=io.BytesIO()
        nx.write_graphson(G,fh)
        fh.seek(0)
        H=nx.read_graphson(fh)
        assert_equal(sorted(G.nodes()),sorted(H.nodes()))
        assert_equal(sorted(G.edges()),sorted(H.edges()))
        assert_equal(sorted(G.edges(data=True)),
                     sorted(H.edges(data=True)))
        self.simple_directed_fh.seek(0)

    def test_read_attribute_graphml(self):
        G=self.attribute_graph
        H=nx.read_graphson(self.attribute_fh)
        assert_equal(sorted(G.nodes(True)),sorted(H.nodes(data=True)))
        ge=sorted(G.edges(data=True))
        he=sorted(H.edges(data=True))
        for a,b in zip(ge,he):
            assert_equal(a,b)
        self.attribute_fh.seek(0)
        I=nx.parse_graphson(self.attribute_data)
        assert_equal(sorted(G.nodes(True)),sorted(I.nodes(data=True)))
        ge=sorted(G.edges(data=True))
        he=sorted(I.edges(data=True))
        for a,b in zip(ge,he):
            assert_equal(a,b)
if __name__ == "__main__":
    t = TestGraph()
    t.setUp()
    t.test_read_attribute_graphml()
