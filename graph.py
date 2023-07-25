# coding: utf-8

import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

from state import State

NODE_POSITIONS = {
    "CA": (0, 4),
    "WA": (2, 6),
    "OR": (2, 5),
    "NV": (2, 4),
    "ID": (4, 5),
    "UT": (4, 4),
    "AZ": (4, 3),
    "NM": (6, 3),
    "CO": (6, 4),
    "WY": (6, 5),
    "MT": (6, 6),
    "TX": (8, 2),
    "OK": (8, 3),
    "KS": (8, 4),
    "NE": (8, 5),
    "SD": (8, 6),
    "ND": (8, 7),
    "LA": (10, 2),
    "AR": (10, 3),
    "MO": (10, 4),
    "IA": (10, 5),
    "MN": (10, 6),
    "MS": (12, 2),
    "IL": (12, 5),
    "WI": (12, 6),
    "AL": (14, 2),
    "TN": (14, 3),
    "KY": (14, 4),
    "IN": (14, 5),
    "MI": (14, 6),
    "FL": (16, 1),
    "GA": (16, 2),
    "VA": (16, 3),
    "WV": (16, 4),
    "OH": (16, 5),
    "SC": (18, 1),
    "NC": (18, 2),
    "DC": (18, 3),
    "MD": (18, 4),
    "PA": (18, 5),
    "DE": (20, 4),
    "NJ": (20, 5),
    "NY": (20, 6),
    "VT": (20, 7),
    "CT": (22, 5),
    "MA": (22, 6),
    "NH": (22, 7),
    "RI": (24, 5),
    "ME": (24, 7),
}


class Graph:
    """represents a combination of networkx and matplotlib functionalities"""

    xlim = (-1, 25)
    ylim = (0, 8)

    def __init__(self):
        self.fig, self.ax, self.nx_graph = self.draw_plot()

        self.node_font_size = 10
        self.node_size = 950
        self.edge_width = 2
        self.edge_font_size = 7
        self.textbox_size = 6
        self.node_positions = NODE_POSITIONS
        self.node_artist_object = self.draw_nodes_on_plot()
        self.draw_node_labels_on_plot()
        self.edge_artist_object = self.draw_edges_on_plot()
        self.textboxes_cleared = False
        self.current_textbox = None

        self.reset_variables()

    @staticmethod
    def set_image(ax):
        x, x1 = ax.get_xlim()
        y, y1 = ax.get_ylim()

        with Image.open("logo.jpg") as img:
            ax.imshow(img, extent=[x, x1, y, y1], aspect="auto")

        plt.tight_layout(pad=1)

    def draw_plot(self):
        """
        Generation of graph via networkx library
        defining nodes and edges, setting the weight of edges as well
        BFS is used to make sure all possible edges are considered
        """

        states = list(NODE_POSITIONS.keys())
        graph = nx.Graph()
        initial = State(states[0])
        visited = []
        open_list = [initial]
        while open_list:
            current = open_list.pop()
            visited.append(current)
            for neighbor in current.find_neighbors():
                if neighbor not in visited:
                    open_list.append(neighbor)
                    graph.add_nodes_from([current.name])
                    graph.add_edges_from([(current.name, neighbor.name, {"distance": current.distance_to(neighbor)})])

        # using the matplotlib subplot function which returns a figure, and axesSubplot
        # fig is short for figure, this is the frame that holds our plot
        # (we cannot draw on fig, but we can resize it, and reshape it)
        # subplot is synonymous with axes(ax), it is the canvas we draw on
        fig, ax = plt.subplots(figsize=(25, 16))
        ax.set(xlim=self.xlim, ylim=self.ylim)
        self.set_image(ax)
        plt.close()

        return fig, ax, graph

    def draw_nodes_on_plot(self):
        """
        function responsible for drawing the nodes on the plot
        each state (node artist object that we can adjust its colors) is stored in a dictionary for future use
        """

        node_artist_object = {}
        for state in self.nx_graph.nodes:
            node_artist_object[state] = nx.draw_networkx_nodes(
                self.nx_graph,
                pos={state: self.node_positions[state]},
                node_color="tab:cyan",
                edgecolors="black",
                linewidths=1,
                node_size=self.node_size,
                ax=self.ax,
                nodelist=[state],
            )
        return node_artist_object

    def draw_node_labels_on_plot(self):
        """responsible for drawing the names of each node"""

        nx.draw_networkx_labels(
            self.nx_graph,
            pos=self.node_positions,
            font_color="black",
            font_size=self.node_font_size,
            font_family="Times New Roman",
            ax=self.ax,
        )

    def draw_edges_on_plot(self):
        """
        storing the edges and considering their inverse relationship for reference handling
        useful for pruning or altering colors
        """

        edge_artist_object = {}
        for tup in self.nx_graph.edges:
            edge = tup[0] + "-" + tup[1]
            inverse_edge = tup[1] + "-" + tup[0]

            edge_artist_object[edge] = nx.draw_networkx_edges(
                self.nx_graph,
                self.node_positions,
                edgelist={tup},
                edge_color="black",
                width=self.edge_width,
                ax=self.ax,
            )
            edge_artist_object[inverse_edge] = edge_artist_object[edge]

        return edge_artist_object

    # when redrawing the graph, we clear the ax (if True) to remove previous colourings
    # when False, we don't clear the current ax (ax represents the plot)
    def redraw_graph(self, clear=True):
        if clear:
            self.ax.clear()

        self.ax.set(xlim=self.xlim, ylim=self.ylim)
        self.set_image(self.ax)
        self.node_artist_object = self.draw_nodes_on_plot()
        self.draw_node_labels_on_plot()
        self.edge_artist_object = self.draw_edges_on_plot()
        self.reset_variables()

    def reset_variables(self):
        self.edge_labels = {}
        self.legend = None
        self.gcost_labels = []
        self.gcost_state_colors = []
        self.current_state = None
        self.current_neighbors = []
        self.openlist = []
        self.visited = []
        self.decolor_edges = []
        self.openlist_state = None
        self.pruned_edges = []
