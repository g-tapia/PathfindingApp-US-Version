import heapq
import networkx as nx

from graph import Graph
from state import BFS, DFS, BESTFS, ASTAR, BEAM, DIJKSTRA, State

def animate(frame_number, frame, graph):
    """Matplotlib function used for animation"""

    global number_of_frames
    number_of_frames = frame_number

    actions = {
        "current": set_current_color,
        "visited": set_visited_color,
        "analyzing": set_analyzing_color,
        "add to open list": set_open_color,
        "pruning": set_pruned_edges,
        "simulate sort": simulate_sort,
        "gcost open": set_gcost_open_path_color,
        "gcost neighbor": set_gcost_neighbor_path_color,
        "changing parent": set_changing_parent_color,
        "changing parent to": set_changing_parent_to_color,
        "reset colors": set_to_original_colors,
        "no path found": no_path_found,
        "goal found": set_goal_color,
        "path": set_path_color,
    }

    revert_edges_to_original_color(graph)

    identifier = list(frame[frame_number].keys())[0]

    actions[identifier](frame[frame_number], graph)

    if identifier != "goal found" and identifier != "path":
        show_current_label(graph)

    return [graph.ax]
  

def show_current_label(graph):
    if graph.current_state is None:
        current_state = ""
    else:
        current_state = graph.current_state.name

    openlist = list(map(lambda n: n.name, graph.openlist))

    textstr = "\n".join((f"$Openlist={openlist}$", f"$CurrentState={current_state}$"))

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5, pad=0.3)

    if graph.legend is not None:
        graph.legend.remove()

    graph.legend = graph.ax.text(-0.90, 0.08, textstr, fontsize=graph.node_font_size, bbox=props)

def show_final_label(goal, graph):
    current = goal
    path = []
    while current:
        path.append(current.name)
        current = current.parent

    path = list(reversed(path))
    path_cost = str(goal.gcost) + "mi"
    textstr = "\n".join(
        (
            f"$number\\ of\\ states\\ on\\ path={len(path)}$",
            f"$path={path}$",
            f"$initial\\ state={path[0]}$",
            f"$goal\\ state={goal.name}$",
            f"$path\\ cost={path_cost}$",
        )
    )

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5, pad=0.3)

    if graph.legend is not None:
        graph.legend.remove()

    graph.ax.text(-0.90, 0.08, textstr, fontsize=graph.node_font_size, bbox=props)

def clear_previous_neighbors_textboxes(graph):
    for neighbor in graph.current_neighbors:
        neighbor.textbox.set_visible(False)

    graph.current_neighbors = []

def revert_edges_to_original_color(graph):
    for edge in graph.decolor_edges:
        edge.set_linestyle("solid")
        edge.set_color("black")

    graph.decolor_edges = []

def set_current_color(frame, graph):
    state = frame["current"]

    graph.node_artist_object[state.name].set_edgecolor("gold")
    graph.node_artist_object[state.name].set_linewidth(3)

    if State.algorithm in (BESTFS, ASTAR, BEAM):
        clear_previous_neighbors_textboxes(graph)

    if len(graph.openlist) > 0:
        if State.algorithm == DFS:
            graph.openlist.pop()
        else:
            heapq.heappop(graph.openlist)

    graph.current_state = state

def set_analyzing_color(frame, graph):
    tup = list(frame.keys())[1]

    edge_label = {tup: str(frame[tup]) + " mi"}
    state1, state2 = tup

    current_position = {state1: graph.node_positions[state1], state2: graph.node_positions[state2]}

    state = frame["analyzing"]
    graph.node_artist_object[state.name].set_color("white")
    graph.node_artist_object[state.name].set_edgecolor("red")

    edge = state1 + "-" + state2

    graph.edge_artist_object[edge].set_linestyle("--")
    graph.edge_artist_object[edge].set_color("red")
    graph.edge_labels[edge] = nx.draw_networkx_edge_labels(
        graph.nx_graph,
        current_position,
        edge_labels=edge_label,
        font_color="black",
        font_size=graph.edge_font_size,
        ax=graph.ax,
    )

    if State.algorithm == DIJKSTRA:
        state.textbox.set_text(f"g(n)={state.gcost}mi")
        state.textbox.set_color("blue")

    elif State.algorithm == ASTAR:
        state.set_textbox(graph)
        state.textbox.set_text(f"f(n)={state.fcost}mi")

    elif State.algorithm == BESTFS:
        state.set_textbox(graph)
        state.textbox.set_text(f"h(n)={state.heuristics}mi")

    elif State.algorithm == BEAM:
        state.set_textbox(graph)
        state.textbox.set_text(f"g(n)={state.gcost}mi")

    graph.decolor_edges.append(graph.edge_artist_object[edge])
    graph.current_neighbors.append(state)

def simulate_sort(frame, graph):
    current, neighbor, counter = frame["simulate sort"]
    edge = current.name + "-" + neighbor.name

    if counter == 1:
        current.set_textbox(graph)
        current.textbox.set_text("sorting states")
        current.textbox.set_color("blue")
        graph.current_neighbors.append(current)

    graph.edge_artist_object[edge].set_linestyle("--")
    graph.edge_artist_object[edge].set_color("blue")

    neighbor.textbox.set_text("placement: " + str(counter))
    neighbor.textbox.set_color("blue")

    graph.decolor_edges.append(graph.edge_artist_object[edge])

def set_visited_color(frame, graph):
    state = frame["visited"]

    graph.visited.append(state)
    graph.node_artist_object[state.name].set_color("red")

def set_open_color(frame, graph):
    state = frame["add to open list"]

    if State.algorithm == BEAM:
        graph.textboxes_cleared = False
        graph.current_textbox.set_visible(False)

    if state not in graph.openlist:
        if State.algorithm == DFS:
            graph.openlist.append(state)
        else:
            heapq.heappush(graph.openlist, state)

    graph.node_artist_object[state.name].set_color("green")

def set_gcost_neighbor_path_color(frame, graph):
    state, edge, gcost = frame["gcost neighbor"]

    graph.node_artist_object[state.name].set_color("fuchsia")

    if edge is not None:
        graph.edge_artist_object[edge].set_color("fuchsia")
        graph.edge_artist_object[edge].set_linestyle("--")
        edge = graph.edge_artist_object[edge]

    if gcost is not None:
        x, y = graph.node_positions[state.name]
        textbox = set_gcost_textbox(state, graph, gcost, "neighbor")
        graph.gcost_labels.append(textbox)

    graph.gcost_state_colors.append([graph.node_artist_object[state.name], edge])

def set_gcost_open_path_color(frame, graph):
    state, edge, gcost = frame["gcost open"]

    if State.algorithm in (BESTFS, ASTAR, BEAM):
        clear_previous_neighbors_textboxes(graph)

    graph.node_artist_object[state.name].set_color("blue")
    if edge is not None:
        graph.edge_artist_object[edge].set_color("blue")
        graph.edge_artist_object[edge].set_linestyle("--")
        edge = graph.edge_artist_object[edge]

    if gcost is not None:
        if State.algorithm != DIJKSTRA:
            state.textbox.set_visible(False)
        textbox = set_gcost_textbox(state, graph, gcost, "open")
        graph.gcost_labels.append(textbox)

    graph.gcost_state_colors.append([graph.node_artist_object[state.name], edge])

def set_gcost_textbox(state, graph, gcost, path_type):
    x, y = graph.node_positions[state.name]
    y = y - 0.35 if path_type == "open" else y - 0.20

    color = "blue" if path_type == "open" else "fuchsia"

    props = dict(boxstyle="round", facecolor="wheat")

    textbox = graph.ax.text(
        x,
        y,
        "gcost =" + str(gcost) + " mi",
        size=graph.textbox_size,
        ha="center",
        va="center",
        color=color,
        bbox=props,
        fontweight="demibold",
        backgroundcolor="wheat",
        )

    return textbox

def set_pruned_edges(frame, graph):
    current, neighbor = frame["pruning"]

    if State.algorithm in (BESTFS, ASTAR, BEAM) and not graph.textboxes_cleared:
        clear_previous_neighbors_textboxes(graph)
        graph.textboxes_cleared = True
        current.textbox.set_text("pruning edges")
        current.textbox.set_color("fuchsia")
        current.textbox.set_visible(True)
        graph.current_textbox = current.textbox

    edge = current.name + "-" + neighbor.name
    graph.edge_artist_object[edge].set_visible(False)

    graph.node_artist_object[neighbor.name].set_color("tab:cyan")
    graph.node_artist_object[neighbor.name].set_edgecolor("black")

    graph.edge_labels[edge][(current.name, neighbor.name)].remove()

def set_changing_parent_color(frame, graph):
    state, edge = frame["changing parent"]

    graph.node_artist_object[state.name].set_color("white")
    graph.node_artist_object[state.name].set_edgecolor("darkorange")

    graph.edge_artist_object[edge].set_color("darkorange")
    graph.edge_artist_object[edge].set_linestyle("solid")

    graph.openlist_state = [graph.node_artist_object[state.name], graph.edge_artist_object[edge]]

def set_changing_parent_to_color(frame, graph):
    state, edge, openlist_neighbor = frame["changing parent to"]

    graph.node_artist_object[state.name].set_color("white")
    graph.node_artist_object[state.name].set_edgecolor("darkorange")

    graph.edge_artist_object[edge].set_color("darkorange")
    graph.edge_artist_object[edge].set_linestyle("solid")

    openlist_neighbor.textbox.set_text(str(openlist_neighbor.gcost) + "mi")
    openlist_neighbor.textbox.set_color("fuchsia")

    old_state, old_edge = graph.openlist_state
    old_edge.set_color("black")
    old_edge.set_linestyle("solid")

    graph.gcost_state_colors.append([graph.node_artist_object[state.name], graph.edge_artist_object[edge]])

def set_to_original_colors(frame, graph):
    changed_already = set()
    for state, edge in graph.gcost_state_colors:
        if state in changed_already:
            continue

        if state is not None and edge is None:
            state.set_color("red")
            changed_already.add(state)

        else:
            state.set_color("red")
            edge.set_linestyle("solid")
            edge.set_color("black")
            changed_already.add(state)

    state.set_color("green")
    edge.set_linestyle("solid")
    edge.set_color("black")

    graph.gcost_state_colors = []

    for label in graph.gcost_labels:
        label.set_visible(False)

    graph.gcost_labels = []

def set_goal_color(frame, graph):
    state = frame["goal found"]

    if State.algorithm in (BESTFS, ASTAR, BEAM):
        clear_previous_neighbors_textboxes(graph)

    show_final_label(state, graph)

    graph.node_artist_object[state.name].set_color("gold")

def set_path_color(frame, graph):
    state = frame["path"]

    graph.node_artist_object[state.name].set_color("gold")

def no_path_found(frame, graph):
    initial, goal = frame["no path found"]

    if graph.legend is not None:
        graph.legend.remove()

    textstr = "\n".join(
        (
            f"$NO\\ PATH\\ FOUND\\ (Open\\ List\\ Exhausted)$",
            f"$number\\ of\\ states\\ on\\ path={0}$",
            f'$path={"NONE"}$',
            f"$initial\\ state={initial.name}$",
            f"$goal\\ state={goal.name}$",
            f"$path\\ cost={0}$",
        )
    )

    props = dict(boxstyle="round", facecolor="wheat", alpha=0.5, pad=0.3)

    graph.ax.text(-0.90, 0.08, textstr, fontsize=graph.node_font_size, bbox=props, color="red")