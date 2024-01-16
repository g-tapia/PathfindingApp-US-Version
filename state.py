# coding: utf-8

import heapq
import timeit
import pandas as pd



"""
This section contains the algorithms used for animation
- when an algorithm is used, it returns a dictionary "frame" that is used to pass to the animation function
- the dictionary generates the number of frames and the action of each frame
- example: frame number : visited so color x
"""

BFS = "breadth first search"
DFS = "depth first search"
BESTFS = "best first search"
ASTAR = "a star search"
BEAM = "beam search"
DIJKSTRA = "dijkstras search"

DRIVING_DISTANCES = pd.read_csv('neighbors.csv', index_col=0)
STRAIGHT_LINE_DISTANCES = pd.read_csv('straight_distances.csv', index_col=0)

class State:
    frame, frame_number, algorithm, priority, beginning_time = None, None, None, None, None

    def __init__(self, name):
        self.name = name
        self.parent = None
        self.heuristics = 0
        self.gcost = 0
        self.fcost = 0
        self.priority = 0
        self.textbox = None

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        if State.algorithm == BFS:
            return self.priority < other.priority

        if State.algorithm == BESTFS:
            return self.heuristics < other.heuristics

        if State.algorithm == ASTAR:
            return self.fcost < other.fcost

        if State.algorithm == BEAM:
            return self.gcost < other.gcost

        if State.algorithm == DIJKSTRA:
            return self.gcost < other.gcost

    def goal_distance(self, goal):
        target = goal.name

        return STRAIGHT_LINE_DISTANCES.loc[self.name, target]

    def distance_to(self, neighbor):
        target = neighbor.name

        return DRIVING_DISTANCES.loc[self.name, target]
      
    def find_neighbors(self):
        parent = self.name

        neighbors = DRIVING_DISTANCES.loc[parent]
        neighbors = neighbors[neighbors > 0].index.tolist()
        
        groupedNeighbors =[State(neighbor) for neighbor in neighbors]
        return groupedNeighbors
      
    def set_textbox(self, graph, y_increase=0):
        x, y = graph.node_positions[self.name]
        y += y_increase + 0.25
        props = dict(boxstyle="round", facecolor="wheat")
        self.textbox = graph.ax.text(
            x,
            y,
            "inf(+)",
            size=graph.textbox_size,
            ha="center",
            va="center",
            bbox=props,
            fontweight="demibold",
            backgroundcolor="wheat",
        )

    @staticmethod
    def initialize_static_variables():
        State.frame = {}
        State.frame_number = -1
        State.algorithm = None
        State.priority = 1

    @staticmethod
    def add_current_frame(value):
        State.frame_number += 1
        State.frame[State.frame_number] = value

    @staticmethod
    def add_gcost_frames(neighbor, openlist_neighbor):
        count = 0

        open_pointer = openlist_neighbor
        while open_pointer.parent:
            gcost = None
            if count == 0:
                gcost = open_pointer.gcost
                count += 1
            edge = open_pointer.name + "-" + open_pointer.parent.name
            State.add_current_frame({"gcost open": [open_pointer, edge, gcost]})
            open_pointer = open_pointer.parent

        State.add_current_frame({"gcost open": [open_pointer, None, None]})

        count = 0
        neighbor_pointer = neighbor
        while neighbor_pointer.parent:
            gcost = None
            if count == 0:
                gcost = neighbor_pointer.gcost
                count += 1
            edge = neighbor_pointer.name + "-" + neighbor_pointer.parent.name
            State.add_current_frame({"gcost neighbor": [neighbor_pointer, edge, gcost]})
            neighbor_pointer = neighbor_pointer.parent

        State.add_current_frame({"gcost neighbor": [neighbor_pointer, None, None]})
        State.add_current_frame({"changing parent": [neighbor, neighbor.name + "-" + openlist_neighbor.parent.name]})
        State.add_current_frame(
            {"changing parent to": [neighbor, neighbor.name + "-" + neighbor.parent.name, openlist_neighbor]}
        )
        State.add_current_frame({"reset colors": []})

    @staticmethod
    def print_results(initial, goal):
        visited = []
        child = goal

        while child:
            visited.append(child.name)
            State.add_current_frame({"path": child})
            child = child.parent

        end = timeit.default_timer()
        print(
            "\nThe goal state was found...\n"
            + "("
            + State.algorithm
            + " algorithm)\n===================================="
        )
        print("Name: George Tapia (A20450857)")
        print(
            "Number of states on path:",
            len(visited),
            "\nVisited States:",
            visited[::-1],
            "\nInitial State:",
            initial.name,
            "\nGoal State:",
            goal.name,
        )
        print("Path cost:", goal.gcost)
        print("Execution time:", end - State.beginning_time, "\n\n\n")

    @staticmethod
    def goal_found(state):
        State.add_current_frame({"goal found": state})
        return State.frame

    @staticmethod
    def breadth_first_search(initial, goal):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = BFS
        if initial == goal:
            return State.goal_found(initial)

        openlist = []
        visitedlist = []

        State.add_current_frame({"add to open list": initial})
        heapq.heappush(openlist, initial)
        while openlist:
            current = heapq.heappop(openlist)
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor not in openlist:
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        neighbor.parent = current
                        State.priority += 1
                        neighbor.priority = State.priority
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )

                        if neighbor == goal:
                            State.add_current_frame({"goal found": neighbor})
                            State.print_results(initial, neighbor)
                            return State.frame

                        heapq.heappush(openlist, neighbor)
                        State.add_current_frame({"add to open list": neighbor})
            State.add_current_frame({"visited": current})

        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame

    @staticmethod
    def depth_first_search(initial, goal):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = DFS
        if initial == goal:
            return State.goal_found(initial)

        openlist = []
        visitedlist = []

        State.add_current_frame({"add to open list": initial})
        openlist.append(initial)
        while openlist:
            current = openlist.pop()
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor not in openlist:
                        neighbor.parent = current
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )

                        if neighbor == goal:
                            State.add_current_frame({"goal found": neighbor})
                            State.print_results(initial, neighbor)
                            return State.frame

                        openlist.append(neighbor)
                        State.add_current_frame({"add to open list": neighbor})
            State.add_current_frame({"visited": current})
        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame

    @staticmethod
    def best_first_search(initial, goal):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = BESTFS
        if initial == goal:
            return State.goal_found(initial)

        openlist = []
        visitedlist = []

        State.add_current_frame({"add to open list": initial})
        heapq.heappush(openlist, initial)
        while openlist:
            current = heapq.heappop(openlist)
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor not in openlist:
                        neighbor.parent = current
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        neighbor.heuristics = neighbor.goal_distance(goal)
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )

                        if neighbor == goal:
                            State.add_current_frame({"goal found": neighbor})
                            State.print_results(initial, neighbor)
                            return State.frame

                        heapq.heappush(openlist, neighbor)
                        State.add_current_frame({"add to open list": neighbor})
            State.add_current_frame({"visited": current})

        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame

    @staticmethod
    def a_star_search(initial, goal):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = ASTAR

        openlist = []
        visitedlist = []

        State.add_current_frame({"add to open list": initial})
        heapq.heappush(openlist, initial)
        while openlist:
            current = heapq.heappop(openlist)
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            if current == goal:
                State.add_current_frame({"goal found": current})
                State.print_results(initial, current)
                return State.frame

            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor in openlist:
                        idx = openlist.index(neighbor)
                        openlist_neighbor = openlist[idx]  # we grab CO with parent UT
                        tentative = current.gcost + current.distance_to(neighbor)  # take the distance from WY to CO
                        if tentative < openlist_neighbor.gcost:
                            neighbor.parent = current
                            neighbor.gcost = tentative
                            State.add_current_frame(
                                {
                                    "analyzing": openlist_neighbor,
                                    (current.name, neighbor.name): current.distance_to(neighbor),
                                }
                            )
                            State.add_gcost_frames(neighbor, openlist_neighbor)

                            openlist_neighbor.parent = current
                            openlist_neighbor.gcost = tentative
                            openlist_neighbor.fcost = tentative + openlist_neighbor.heuristics
                    else:
                        neighbor.parent = current
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        neighbor.heuristics = neighbor.goal_distance(goal)
                        neighbor.fcost = neighbor.gcost + neighbor.heuristics
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )
                        heapq.heappush(openlist, neighbor)
                        State.add_current_frame({"add to open list": neighbor})

            State.add_current_frame({"visited": current})

        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame

    @staticmethod
    def beam_search(initial, goal, beam_width=15):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = BEAM

        openlist = []
        visitedlist = []

        heapq.heappush(openlist, initial)
        while openlist:
            current = heapq.heappop(openlist)
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            if current == goal:
                State.add_current_frame({"goal found": current})
                State.print_results(initial, current)
                return State.frame

            group = []
            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor not in openlist:
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )

                        group.append(neighbor)

            sorted_group = sorted(group, key=lambda n: n.gcost)
            pruned_states, best_matches = sorted_group[beam_width:], sorted_group[:beam_width]
            for index, node in enumerate(sorted_group):
                State.add_current_frame({"simulate sort": (current, node, index+1)})

            for n in pruned_states:
                State.add_current_frame({"pruning": [current, n]})

            for n in best_matches:
                n.parent = current
                heapq.heappush(openlist, n)
                State.add_current_frame({"add to open list": n})

            State.add_current_frame({"visited": current})
        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame

    @staticmethod
    def dijkstras_search(initial, goal, graph):
        State.beginning_time = timeit.default_timer()
        State.initialize_static_variables()
        State.algorithm = DIJKSTRA

        openlist = []
        visitedlist = []

        initial.set_textbox(graph)
        initial.textbox.set_text(str(0) + " mi")
        initial.textbox.set_color("blue")
        heapq.heappush(openlist, initial)
        while openlist:
            current = heapq.heappop(openlist)
            visitedlist.append(current)
            State.add_current_frame({"current": current})

            if current == goal:
                State.add_current_frame({"goal found": current})
                State.print_results(initial, current)
                return State.frame

            for neighbor in current.find_neighbors():
                if neighbor not in visitedlist:
                    if neighbor in openlist:
                        idx = openlist.index(neighbor)
                        openlist_neighbor = openlist[idx]
                        tentative = current.gcost + current.distance_to(neighbor)

                        if tentative < openlist_neighbor.gcost:
                            neighbor.parent = current
                            neighbor.gcost = tentative
                            State.add_current_frame(
                                {
                                    "analyzing": openlist_neighbor,
                                    (current.name, neighbor.name): current.distance_to(neighbor),
                                }
                            )
                            State.add_gcost_frames(neighbor, openlist_neighbor)
                            openlist_neighbor.parent = current
                            openlist_neighbor.gcost = tentative
                            openlist_neighbor.fcost = tentative + openlist_neighbor.heuristics
                    else:
                        neighbor.set_textbox(graph)
                        neighbor.parent = current
                        neighbor.gcost = current.distance_to(neighbor) + current.gcost
                        State.add_current_frame(
                            {"analyzing": neighbor, (current.name, neighbor.name): current.distance_to(neighbor)}
                        )
                        heapq.heappush(openlist, neighbor)
                        State.add_current_frame({"add to open list": neighbor})

            State.add_current_frame({"visited": current})
        else:
            State.add_current_frame({"no path found": (initial, goal)})
            return State.frame
