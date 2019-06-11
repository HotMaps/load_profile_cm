import copy

from igraph import Graph, plot
import numpy as np
from collections import Counter


class NetworkGraph:
    """
    Class wrapping igraph functionality for the planning and debugging of source sink flow models. It strictly differs
    between source and sink vertices which may be important for further analysis. It can handle coherent sources
    and sinks, which are already connected (internally).
    """

    def __init__(self, source_sink_edges, source_source_edges, sink_sink_edges,
                 source_correspondence, sink_correspondence):
        """
        Constructor to initial the NetworkGraph object

        :param source_sink_edges: adjacency list containing the connections of sources with sinks. Sinks and sources can
                                  have the same ID.
        :type source_sink_edges: list. [[sink1, sink2], [sink1, sink4], [], ...]
        :param source_source_edges: adjacency list containing the connections  between sources and other sources.
        :type source_source_edges: list. [[source1], [source2, source3], ...]
        :param sink_sink_edges: adjacency list containing the connections between sinks and other sinks.
        :type sink_sink_edges: list. [[sink1, sink2], [sink1, sink4], [], ...]
        :param source_correspondence: list containing the correspondence of sources. Sources with the same
                                      correspondence value are considered as one coherent set of sources which are
                                      connected internally. The capacity of the coherent set of sources is equal to the
                                      sum of the individual sources.
        :type source_correspondence: list. [correspondence of source 1, correspondence of source 2, ...]
        :param sink_correspondence: list containing the correspondence of sinks. Sinks with the same
                                      correspondence value are considered as one coherent set of sinks which are
                                      connected internally. The capacity of the coherent set of sinks is equal to the
                                      sum of the individual sinks.
        :type sink_correspondence: list. [correspondence of sink 1, correspondence of sink 2, ...]


        Attributes:
            number_of_sources: Number of source vertices. Int.
            number_of_sinks: Number of sink vertices. Int.
            vertex_to_source: Maps vertex ID to source ID. Dic.
            vertex_to_sink: Maps vertex ID to sink ID. Dic.
            source_to_vertex: Maps source ID to vertex ID. Dic.
            sink_to_vertex: Maps sink ID to vertex ID. Dic.
            graph: Graph containing all vertices and edges. igraph Graph.
            max_flow_graph: slightly altered graph for max_flow calculations. igraph Graph.
            infinite_source_vertex: Vertex ID of the infinte source vertex in the max_flow_graph. Int.
            infinite_sink_vertex: Vertex ID of the infinite sink vertex in the max_flow_graph. Int.
        """

        self.number_of_sources = len(source_source_edges)
        self.number_of_sinks = len(sink_sink_edges)

        # specified later by the build_graph() method
        self.vertex_to_source = {}
        self.vertex_to_sink = {}
        self.source_to_vertex = {}
        self.sink_to_vertex = {}
        self.graph = Graph()

        # specified later by  the build_correspondence_graph()
        self.correspondence_graph = Graph()
        self.source_correspondence = source_correspondence
        self.sink_correspondence = sink_correspondence
        # node ids of the nodes connecting correspondence nodes together
        self.connecting_node_of_source_correspondence = {}
        self.connecting_node_of_sink_correspondence = {}
        self.number_of_coherent_sources = 0
        self.number_of_coherent_sinks = 0

        # specified later by the build_max_flow_graph() method
        self.max_flow_graph = Graph()
        self.infinite_source_vertex = 0
        self.infinite_sink_vertex = 0

        # build self.graph with given inputs
        self.build_graph(source_sink_edges, source_source_edges, sink_sink_edges)
        # build self.correspondence_graph based on self.graph
        self.build_correspondence_graph()
        # build self.max_flow_graph based on self.graph
        self.build_max_flow_graph()

    def build_graph(self, source_sink_edges, source_source_edges, sink_sink_edges):
        """
        Method constructing the graph object

        :param source_sink_edges: adjacency list containing the connections of sources with sinks. Sinks and sources can
                                  have the same ID.
        :type source_sink_edges: list. [[sink1, sink2], [sink1, sink4], [], ...]
        :param source_source_edges: adjacency list containing the connections  between sources and other sources.
        :type source_source_edges: list. [[source1], [source2, source3], ...]
        :param sink_sink_edges: adjacency list containing the connections between sinks and other sinks.
        :type sink_sink_edges: list. [[sink1, sink2], [sink1, sink4], [], ...]

        :return:
        """

        # map vertex ID's to source ID's
        vertex_to_source = {}
        for source, _ in enumerate(source_source_edges):
            vertex_to_source[source] = source
        self.vertex_to_source = vertex_to_source

        # map vertex ID's to sink ID's
        vertex_to_sink = {}
        for sink, _ in enumerate(sink_sink_edges):
            vertex_to_sink[self.number_of_sources + sink] = sink
        self.vertex_to_sink = vertex_to_sink

        # map source ID's to vertex ID's by reversing injective vertex_to_source dic.
        source_to_vertex = {v: k for k, v in self.vertex_to_source.items()}
        self.source_to_vertex = source_to_vertex
        # map sink ID's to vertex ID's by reversing injective vertex_to_sink dic.
        sink_to_vertex = {v: k for k, v in self.vertex_to_sink.items()}
        self.sink_to_vertex = sink_to_vertex

        # build igraph Graph object
        g = Graph(directed=False)
        g.add_vertices(self.number_of_sources + self.number_of_sinks)

        # construct pairs of vertex ID's connected by the adjacency lists.
        for source, sinks in enumerate(source_sink_edges):
            for sink in sinks:
                g.add_edge(source_to_vertex[source], sink_to_vertex[sink])
        for source1, sources in enumerate(source_source_edges):
            for source2 in sources:
                g.add_edge(source_to_vertex[source1], source_to_vertex[source2])
        for sink1, sinks in enumerate(sink_sink_edges):
            for sink2 in sinks:
                g.add_edge(sink_to_vertex[sink1], sink_to_vertex[sink2])

        self.graph = g

        # assigning source vertices a red color and sink vertices a blue color attribute
        self.graph.vs["color"] = ["red"] * self.number_of_sources + ["blue"] * self.number_of_sinks

    def build_correspondence_graph(self):
        """
        Method constructing the correspondence graph needed to connect coherent sources or sinks without costs.

        :return:
        """
        g = copy.deepcopy(self.graph)

        # check for sources with same correspondence. If two or more sources have the same correspondence the
        # graph will need an additional node connecting them
        c = Counter(self.source_correspondence)
        coherent_sources_correspondence = [correspondence for correspondence in c if c[correspondence] > 1]
        self.number_of_coherent_sources = len(c)
        # check for sinks with same correspondence. If two or more sinks have the same correspondence the
        # graph will need an additional node connecting them
        c = Counter(self.sink_correspondence)
        coherent_sinks_correspondence = [correspondence for correspondence in c if c[correspondence] > 1]
        self.number_of_coherent_sinks = len(c)

        # reinitialize the dict containing the node ids of the nodes used to connect each correspondence
        self.connecting_node_of_source_correspondence = {}
        # only iterate over correspondences with at least two members
        for correspondence in coherent_sources_correspondence:
            for source, source_correspondence in zip(range(self.number_of_sources), self.source_correspondence):
                if source_correspondence == correspondence:
                    # check if a node for the correspondence already exists
                    if correspondence in self.connecting_node_of_source_correspondence:
                        # connect source with the correspondence node
                        g.add_edge(self.connecting_node_of_source_correspondence[correspondence],
                                   self.source_to_vertex[source])
                    else:
                        # if new correspondence encountered, adds new correspondence node
                        g.add_vertices(1)
                        self.connecting_node_of_source_correspondence[correspondence] = g.vcount() - 1
                        g.add_edge(self.source_to_vertex[source],
                                   self.connecting_node_of_source_correspondence[correspondence])

        self.connecting_node_of_sink_correspondence = {}
        for correspondence in coherent_sinks_correspondence:
            for sink, sink_correspondence in zip(range(self.number_of_sinks), self.sink_correspondence):
                if sink_correspondence == correspondence:
                    if correspondence in self.connecting_node_of_sink_correspondence:
                        g.add_edge(self.sink_to_vertex[sink],
                                   self.connecting_node_of_sink_correspondence[correspondence])
                    else:
                        g.add_vertices(1)
                        self.connecting_node_of_sink_correspondence[correspondence] = g.vcount() - 1
                        g.add_edge(self.sink_to_vertex[sink],
                                   self.connecting_node_of_sink_correspondence[correspondence])

        self.correspondence_graph = g

        self.correspondence_graph.vs["color"] = ["red"] * self.number_of_sources + ["blue"] * self.number_of_sinks +\
                                                ["red"] * len(self.connecting_node_of_source_correspondence) +\
                                                ["blue"] * len(self.connecting_node_of_sink_correspondence)

    def build_max_flow_graph(self):
        """
        Method constructing the max_flow_graph object required for max_flow computations

        :return:
        """

        g = copy.deepcopy(self.correspondence_graph)
        # add infinite source and sink vertex
        g.add_vertices(2)

        # assign the new vertices unique vertex ID's
        self.infinite_source_vertex = g.vcount() - 2
        self.infinite_sink_vertex = g.vcount() - 1

        # connect all sources with the infinite source and all sinks with the infinite sink by an edge
        for source, correspondence in zip(range(self.number_of_sources), self.source_correspondence):
            if correspondence not in self.connecting_node_of_source_correspondence:
                g.add_edge(self.infinite_source_vertex, self.source_to_vertex[source])
            else:
                if not g.are_connected(self.infinite_source_vertex, self.connecting_node_of_source_correspondence[correspondence]):
                    g.add_edge(self.infinite_source_vertex, self.connecting_node_of_source_correspondence[correspondence])

        for sink, correspondence in zip(range(self.number_of_sinks), self.sink_correspondence):
            if correspondence not in self.connecting_node_of_sink_correspondence:
                g.add_edge(self.infinite_sink_vertex, self.sink_to_vertex[sink])
            else:
                if not g.are_connected(self.infinite_sink_vertex, self.connecting_node_of_sink_correspondence[correspondence]):
                    g.add_edge(self.infinite_sink_vertex, self.connecting_node_of_sink_correspondence[correspondence])

        self.max_flow_graph = g

        self.max_flow_graph.vs["color"] = ["red"] * self.number_of_sources + ["blue"] * self.number_of_sinks + \
            ["red"] * len(self.connecting_node_of_source_correspondence) + \
            ["blue"] * len(self.connecting_node_of_sink_correspondence) + ["red"] + ["blue"]

    def return_adjacency_lists(self):
        """
        method returning the adjacency list in the same style as required by the constructor. Hence three separate lists
        containing the source_sink, source_source and sink_sink adjacencies.

        :return: three adjacency lists for the source_sink, source_source and sink_sink adjacencies.
        :rtype: tuple of lists. ([], [], []).
        """

        source_source_adjacencies = []
        source_sink_adjacencies = []
        sink_sink_adjacencies = []

        # iterate through adjacency list of graph
        for vertex1, vertices in enumerate(self.correspondence_graph.get_adjlist()):

            # determine if vertex1 is a source or sink
            if vertex1 < self.number_of_sources:
                source_source_adjacencies .append([])
                source_sink_adjacencies .append([])

                # iterate though sublist of adjacency list
                for vertex2 in set(vertices):
                    # determine if vertex2 is a source or sink
                    if vertex2 < self.number_of_sources:
                        if vertex1 < vertex2:
                            source_source_adjacencies[-1].append(self.vertex_to_source[vertex2])
                    elif self.number_of_sources + self.number_of_sinks > vertex2 >= self.number_of_sources:
                        source_sink_adjacencies[-1].append(self.vertex_to_sink[vertex2])

            elif self.number_of_sources + self.number_of_sinks > vertex1 >= self.number_of_sources:
                sink_sink_adjacencies.append([])

                # iterate though sublist of adjacency list
                for vertex2 in set(vertices):
                    # determine if vertex2 is a source or sink
                    if self.number_of_sources + self.number_of_sinks > vertex2 >= self.number_of_sources:
                        if vertex1 < vertex2:
                            sink_sink_adjacencies[-1].append(self.vertex_to_sink[vertex2])

        return source_sink_adjacencies, source_source_adjacencies, sink_sink_adjacencies

    def add_edge_attribute(self, name, source_sink_attributes, source_source_attributes, sink_sink_attributes):
        """
        Method adding an edge attribute.

        :param name: Name of the edge attribute.
        :type name: str.
        :param source_sink_attributes: Adjacency list but instead of indices it contains the value of the attribute. For
                                       this reason the list must have the exact same shape as the source_sink_adjacency
                                       list
        :param source_source_attributes: Adjacency list but instead of indices it contains the value of the attribute. For
                                         this reason the list must have the exact same shape as the source_source_adjacency
                                         list
        :param sink_sink_attributes: Adjacency list but instead of indices it contains the value of the attribute. For
                                     this reason the list must have the exact same shape as the sink_sink_adjacency
                                     list
        :return:
        """

        edge_attributes = []
        for attributes in source_sink_attributes:
            for attribute in attributes:
                edge_attributes.append(attribute)
        for attributes in source_source_attributes:
            for attribute in attributes:
                edge_attributes.append(attribute)
        for attributes in sink_sink_attributes:
            for attribute in attributes:
                edge_attributes.append(attribute)

        if self.graph.ecount() == len(edge_attributes):
            self.graph.es[name] = edge_attributes
            self.correspondence_graph.es[name] = edge_attributes + [0] * (self.correspondence_graph.ecount() -
                                                                          self.graph.ecount())
        else:
            raise TypeError("given attributes must have same shape as "
                            "source_sink_adjacencies, source_source_adjacencies, sink_sink_adjacencies")

    def get_edge_attribute(self, name):
        """
        Method returning an edge attribute. The edges can be identified with the return_edge_source_target_vertices()
        method.

        :param name: name of the attribute.
        :type name: str.
        :return: list containing the edge attribute.
        :rtype: list.
        """

        return self.graph.es[name]

    def reduce_to_minimum_spanning_tree(self, attribute_name):
        """
        Removes edges of graph to minimize the value of summed edge attribute but remains the same vertex connectivity.

        :param attribute_name: attribute after which the minimum spanning tree is constructed.
        :type attribute_name: str
        :return:
        """

        self.correspondence_graph = \
            self.correspondence_graph.spanning_tree(weights=self.correspondence_graph.es[attribute_name])

        # get attributes from correspondence graph to update self.graph
        attributes = []
        for attribute in self.graph.es.attribute_names():
            attributes.append((attribute, self.correspondence_graph.es[attribute]))

        # check which edges are relevant for self.graph
        non_correspondence_edges = []
        for edge in self.correspondence_graph.es:
            if (edge.source in self.vertex_to_source or edge.source in self.vertex_to_sink) and \
                    (edge.target in self.vertex_to_source or edge.target in self.vertex_to_sink):
                non_correspondence_edges.append((edge.source, edge.target))

        # reset self.graph and rebuild according to the MST
        self.graph = Graph()
        self.graph.add_vertices(self.number_of_sources + self.number_of_sinks)
        # assigning source vertices a red color and sink vertices a blue color attribute
        self.graph.vs["color"] = ["red"] * self.number_of_sources + ["blue"] * self.number_of_sinks
        self.graph.add_edges(non_correspondence_edges)
        for attribute_name, values in attributes:
            self.graph.es[attribute_name] = values[:len(non_correspondence_edges)]

        # update correspondence graph and max flow graph
        self.build_correspondence_graph()
        self.build_max_flow_graph()

    def maximum_flow(self, source_capacities, sink_capacities):
        """
        function computing the maximum flow of a given source sink network

        :param source_capacities: list containing the capacity of each source.
        :type source_capacities: list.
        :param sink_capacities: list containing the demand of each sink.
        :type sink_capacities: list.
        :return: returns a touple of three lists. The first one has the same length as source_capacities and contains
                 the actual flow of the sources. The second is indicating the flow of the sinks. The third one
                 indicates the flow though the edges of the graph.
        :rtype: tuple. ([], [], [])

        """
        r"""
        This function is computing the maximum flow of all sources to sinks. In order to do so a graph is build
        as following:
        sources "su" and
        sinks "si" 
        forming the vertices of the graph. All vertices are indicated by [].
        Additionally there is an [infinite source] and [infinite sink] vertex. 
        The [infinite source] has edges leading to each [su]. These are weighted with the capacity H_e of each source.
        The weights do represent the maximum flow through the specific edge.
        No edge is directed.
        Each [si] has an edge connecting it to the [infinite sink]. Each of those edges has the weight demand H_d.
        Once again these weights represent the maximum flow through the specific edge.
        All other edges (edges connecting [su] with [si] or [su], or [si] with [si]) do not have weights and therefore 
        unrestricted flow.
        For numerical reasons those edges are weighted with 1000 which does not introduce further 
        restrictions.
        Further the other weights are normalized with the factor 1/max(weights)(hence largest possible weight of 
        restricted edges is 1)
        for numerical reasons.
        
                                           [infinite source]
                                            /      |      \
                                       H_e1/   H_e2|   H_e3\
                                          /        |        \
                                       [su1]-----[su2]     [su3]
                                         |       / |         |
                                         |  -----  |         |
                                         | /       |         |
                                       [si1]     [si2]-----[si3]
                                          \        |        /
                                       H_d1\   H_d2|   H_d3/
                                            \      |      /
                                            [infinite sink]
        
        Now the Push-relabel maximum flow algorithm is applied to the graph.
        
        Notes: 
        Unlike in the example the number of [su] does not have to be equal to [si].
        Neither does every [su] need an edge to [si] or vice versa.                            
        """

        if len(source_capacities) == self.number_of_sources and len(sink_capacities) == self.number_of_sinks:

            effective_source_capacities = []
            position = {}
            for source_capacity, correspondence in zip(source_capacities, self.source_correspondence):
                if correspondence in position:
                    effective_source_capacities[position[correspondence]] += source_capacity
                else:
                    effective_source_capacities.append(source_capacity)
                    position[correspondence] = len(effective_source_capacities) - 1

            effective_sink_capacities = []
            position = {}
            for sink_capacity, correspondence in zip(sink_capacities, self.sink_correspondence):
                if correspondence in position:
                    effective_sink_capacities[position[correspondence]] += sink_capacity
                else:
                    effective_sink_capacities.append(sink_capacity)
                    position[correspondence] = len(effective_sink_capacities) - 1

            # find normalization so that the max capacity is 1

            normalization = 1 / np.max(np.append(effective_source_capacities, effective_sink_capacities))
            effective_source_capacities = np.array(effective_source_capacities) * normalization
            effective_sink_capacities = np.array(effective_sink_capacities) * normalization
            # give real edges unrestricted flow
            flow_capacities = np.append([1000] * self.correspondence_graph.ecount(),
                                        np.append(effective_source_capacities, effective_sink_capacities))

            self.max_flow_graph.es["flow_capacity"] = flow_capacities
            # NOTE igraph maxflow leaks memory including version 0.7.1.post6 (does not free some solution vector,
            # hence leaks around 8*(number_of_sources + number_of_sinks + number_of_edges) bytes of memory every call)
            solution = self.max_flow_graph.maxflow(self.infinite_source_vertex, self.infinite_sink_vertex, "flow_capacity")

            # rescale flow to original, after weight normalization
            solution = np.array(solution.flow) / normalization
            source_flow = - solution[-self.number_of_coherent_sinks - self.number_of_coherent_sources:-self.number_of_coherent_sinks]
            sink_flow = solution[-self.number_of_coherent_sinks:]
            connection_flow = solution[:-self.number_of_coherent_sources - self.number_of_coherent_sinks -
                                       (self.correspondence_graph.ecount() - self.graph.ecount())]

            return source_flow, sink_flow, connection_flow
        else:
            raise TypeError("Source capacites and sink capacities must have same length as the number of sources and "
                            "number of sinks in the graph")

    def plot(self, source_coordinates, sink_coordinates):
        """
        Plots graph. Sources are red dots and sinks blue.

        :param source_coordinates: tuple of coordinates of sources. Same order as implied by the adjacency list or the
                                   return_vertices method
        :param sink_coordinates: tuple of coordinates of sinks. Same order as implied by the adjacency list or the
                                 return_vertices method
        :return:
        """

        # TODO automate proper layout and scaling of plot
        plot(self.graph, layout=source_coordinates + sink_coordinates, bbox=(8000, 8000), vertex_size=5, edge_width=2)

    def plot_all_connections(self, source_coordinates, sink_coordinates):
        """
        Plots graph with connections of coherent nodes. Sources are red dots and sinks blue.

        :param source_coordinates: tuple of coordinates of sources. Same order as implied by the adjacency list or the
                                   return_vertices method
        :param sink_coordinates: tuple of coordinates of sinks. Same order as implied by the adjacency list or the
                                 return_vertices method
        :return:
        """
        source_correspondence_coordinates = {}
        for correspondence, coordinate in zip(self.source_correspondence, source_coordinates):
            if correspondence in self.connecting_node_of_source_correspondence:
                source_correspondence_coordinates[correspondence] = coordinate
        source_correspondence_coordinates = [source_correspondence_coordinates[k] for k in source_correspondence_coordinates]

        sink_correspondence_coordinates = {}
        for correspondence, coordinate in zip(self.sink_correspondence, sink_coordinates):
            if correspondence in self.connecting_node_of_sink_correspondence:
                sink_correspondence_coordinates[correspondence] = coordinate
        sink_correspondence_coordinates = [sink_correspondence_coordinates[k] for k in sink_correspondence_coordinates]

        plot(self.correspondence_graph, layout=source_coordinates + sink_coordinates +
             source_correspondence_coordinates + sink_correspondence_coordinates, bbox=(8000, 8000), vertex_size=5,
             edge_width=2)

    def plot_max_flow_graph(self, source_coordinates, sink_coordinates):
        """
        Plots graph with connections of coherent nodes and the infinte source and sink vertices.
        Sources are red dots and sinks blue.

        :param source_coordinates: tuple of coordinates of sources. Same order as implied by the adjacency list or the
                                   return_vertices method
        :param sink_coordinates: tuple of coordinates of sinks. Same order as implied by the adjacency list or the
                                 return_vertices method
        :return:
        """
        source_correspondence_coordinates = {}
        for correspondence, coordinate in zip(self.source_correspondence, source_coordinates):
            if correspondence in self.connecting_node_of_source_correspondence:
                source_correspondence_coordinates[correspondence] = coordinate
        source_correspondence_coordinates = [source_correspondence_coordinates[k] for k in source_correspondence_coordinates]

        sink_correspondence_coordinates = {}
        for correspondence, coordinate in zip(self.sink_correspondence, sink_coordinates):
            if correspondence in self.connecting_node_of_sink_correspondence:
                sink_correspondence_coordinates[correspondence] = coordinate
        sink_correspondence_coordinates = [sink_correspondence_coordinates[k] for k in sink_correspondence_coordinates]

        all_coordinates = source_coordinates + sink_coordinates

        y_min = min(all_coordinates, key=lambda x: x[0])[0]
        y_max = max(all_coordinates, key=lambda x: x[0])[0]
        x_min = min(all_coordinates, key=lambda x: x[1])[1]
        x_max = max(all_coordinates, key=lambda x: x[1])[1]

        delta_y = y_max - y_min
        mean_x = (x_max + x_min) / 2

        infinite_source_coordinate = [(mean_x, y_min - 0.2 * delta_y)]
        infinite_sink_coordinate = [(mean_x, y_max + 0.2*delta_y)]

        plot(self.max_flow_graph, layout=source_coordinates + sink_coordinates +
             source_correspondence_coordinates + sink_correspondence_coordinates + infinite_source_coordinate +
             infinite_sink_coordinate, bbox=(1000, 1000), vertex_size=5,
             edge_width=2)

    def return_edge_source_target_vertices(self):
        """
        Method returning every source and target vertex of every edge.

        :return: list containing tuples of source and target vertices of every edge.
        :rtype: list. [(), (), ()]
        """

        edge_source_target = []

        for edge in self.graph.es:
            # determine is source of edge is a source or sink
            if edge.source < self.number_of_sources:
                source = ("source", self.vertex_to_source[edge.source])
            else:
                source = ("sink", self.vertex_to_sink[edge.source])
            # determine if target of edge is a source or sink
            if edge.target < self.number_of_sources:
                target = ("source", self.vertex_to_source[edge.target])
            else:
                target = ("sink", self.vertex_to_sink[edge.target])

            edge_source_target.append((source, target))

        return edge_source_target

    def delete_edges(self, edges):
        """
        Method deleting edges of graph

        :param edges: list of tuples of source target vertices which edges will be deleted. Each source and target is a
                      separate tuple indicating if the index is a source or sink  index.
        :type edges: list. [(("source", 1), ("source", 2)), (("source", 1), ("sink", 0)), ...]
        :return:
        """

        edges_to_delete = []
        for source, target in edges:
            if source[0] == "source":
                index_source = self.source_to_vertex[source[1]]
            else:
                index_source = self.sink_to_vertex[source[1]]
            if target[0] == "source":
                index_target = self.source_to_vertex[target[1]]
            else:
                index_target = self.sink_to_vertex[target[1]]
            edges_to_delete.append((index_source, index_target))

        self.graph.delete_edges(edges_to_delete)
        # update correspondence graph
        self.build_correspondence_graph()
        # update max_flow graph
        self.build_max_flow_graph()

    def return_number_of_edges(self):
        """
        Method returning the total count of edges of the graph.

        :return: total number of edges.
        :rtype: int.
        """

        return self.graph.ecount()

    def return_number_of_vertices(self):
        """
        Method returning the total number of vertices of the graph.

        :return: number of vertices.
        :rtype: int.
        """

        return self.graph.vcount()

    def return_vertices(self):
        """
        Method returning vertices in the exact order stored in the graph.

        :return: list of tuples with vertex id and an indication if the vertex is a source or sink.
        :rtype: list. [(), (), ()]
        """

        vertices = []
        for vertex in self.graph.vs:
            if vertex.index < self.number_of_sources:
                vertices.append(("source", self.vertex_to_source[vertex.index]))
            else:
                vertices.append(("sink", self.vertex_to_sink[vertex.index]))

        return vertices
