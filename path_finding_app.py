#!/usr/bin/env python
# coding: utf-8

import heapq
import customtkinter
import networkx as nx

from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import Graph
from state import BFS, DFS, BESTFS, ASTAR, BEAM, DIJKSTRA, State

from animation_functions import *


def main():
    global number_of_frames 
    plt.rcParams["animation.embed_limit"] = 2**128
    
    def change_appearance_mode_event(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    short = 80
    long = 220

    # Create figure
    anim, result = None, None
    graph = Graph()

    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    # Create main window
    window = customtkinter.CTk()
    window.title("Graph Traversal Animation")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    window.maxsize(screen_width, screen_height)

    canvas = FigureCanvasTkAgg(graph.fig, master=window)
    canvas.draw()

    # Set grid layout for main window
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

    # create frames
    side_frame = customtkinter.CTkFrame(window, width=long)
    side_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
    side_frame.rowconfigure(6, weight=1)

    top_frame = customtkinter.CTkFrame(side_frame, width=long)
    top_frame.grid(row=0, column=0)

    middle_frame = customtkinter.CTkFrame(side_frame, width=long)
    middle_frame.grid(row=6, column=0, sticky="ew")

    bottom_frame = customtkinter.CTkFrame(side_frame, width=long)
    bottom_frame.grid(row=7, column=0)

    start_button = customtkinter.CTkButton(top_frame, text="Start Animation", command=lambda: start_animation())

    start_state_input = customtkinter.CTkLabel(top_frame, text="Initial State:")
    argument_initial_state = customtkinter.StringVar(top_frame)
    argument_initial_state_entry = customtkinter.CTkEntry(top_frame, textvariable=argument_initial_state, width=short)

    goal_state_input = customtkinter.CTkLabel(top_frame, text="Goal State:")
    argument_goal_state = customtkinter.StringVar(top_frame)
    argument_goal_state_entry = customtkinter.CTkEntry(top_frame, textvariable=argument_goal_state, width=short)

    # creating the input fields
    interval_input = customtkinter.CTkLabel(top_frame, text="Interval Input[10] (Optional)")
    argument_interval = customtkinter.StringVar(top_frame)
    argument_interval_entry = customtkinter.CTkEntry(top_frame, textvariable=argument_interval)

    pause_button = customtkinter.CTkButton(
        top_frame, text="Pause Animation", command=lambda: stop_animation(), fg_color="dark red"
    )

    resume_button = customtkinter.CTkButton(
        top_frame, text="Resume Animation", command=lambda: resume_animation(), fg_color="dark green"
    )
    resume_button_on = False

    redraw_button = customtkinter.CTkButton(middle_frame, text="Redraw Graph", command=lambda: redraw_current_graph())

    node_size_input = customtkinter.CTkLabel(middle_frame, text="Node Size[1200]:")
    argument_node_size = customtkinter.StringVar(middle_frame)
    argument_node_size_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_node_size, width=short)

    node_font_size_input = customtkinter.CTkLabel(middle_frame, text="Node Font Size[12]:")
    argument_node_font_size = customtkinter.StringVar(middle_frame)
    argument_node_font_size_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_node_font_size,
                                                           width=short)

    edge_width_input = customtkinter.CTkLabel(middle_frame, text="Edge Width[2]:")
    argument_edge_width = customtkinter.StringVar(middle_frame)
    argument_edge_width_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_edge_width, width=short)

    edge_font_input = customtkinter.CTkLabel(middle_frame, text="Edge Font[7]:")
    argument_edge_font = customtkinter.StringVar(middle_frame)
    argument_edge_font_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_edge_font, width=short)

    text_boxes_size_input = customtkinter.CTkLabel(middle_frame, text="Text Box Size[7]:")
    argument_textbox_size = customtkinter.StringVar(middle_frame)
    argument_textbox_size_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_textbox_size, width=short)

    inputs = []
    argument_beam_size = None

    def algorithm_choice(algorithm_selected):
        nonlocal top_frame, inputs, argument_beam_size

        if algorithm_selected == "beam search":

            beam_input = customtkinter.CTkLabel(middle_frame, text="Set Beam:")
            argument_beam_size = customtkinter.StringVar(middle_frame)
            argument_beam_size_entry = customtkinter.CTkEntry(middle_frame, textvariable=argument_beam_size,
                                                              width=short)
            beam_input.grid(row=1, column=0, padx=(20, 40), pady=20, sticky="w")
            argument_beam_size_entry.grid(row=1, column=0, padx=(10, 40), sticky="e")

            inputs = [beam_input, argument_beam_size_entry]
        else:
            for value in inputs:
                value.grid_forget()

    dropdown_option = customtkinter.StringVar(top_frame)
    dropdown_menu = customtkinter.CTkComboBox(
        master=middle_frame,
        width=long,
        values=[BFS, DFS, BESTFS, ASTAR, BEAM, DIJKSTRA],
        variable=dropdown_option,
        command=algorithm_choice,
    )

    dropdown_menu.set("Algorithms Available")

    appearance_mode_label = customtkinter.CTkLabel(bottom_frame, text="Appearance Mode:")
    appearance_mode_option_menu = customtkinter.CTkOptionMenu(
        bottom_frame, values=["Dark", "Light"], command=change_appearance_mode_event
    )

    # # Placements of buttons on the left side
    # start_button.grid(row=2, column=0, padx=50, pady=20)
    # pause_button.grid(row=3, column=0, padx=20, pady=10)

    # start_state_input.grid(row=0, column=0, padx=(10, 0), pady=20, sticky="w")
    # argument_initial_state_entry.grid(row=0, column=0, padx=(100, 10), pady=20, sticky="w")

    # goal_state_input.grid(row=1, column=0, padx=(10, 0), pady=20, sticky="w")
    # argument_goal_state_entry.grid(row=1, column=0, padx=(99, 10), pady=20, sticky="w")

    # interval_input.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
    # argument_interval_entry.grid(row=5, column=0, padx=20, sticky="ew")

    redraw_button.grid(row=2, column=0, padx=20, pady=20)

    node_size_input.grid(row=3, column=0, padx=5, pady=10, sticky="w")
    argument_node_size_entry.grid(row=3, column=0, padx=0, sticky="e")

    node_font_size_input.grid(row=4, column=0, padx=5, pady=10, sticky="w")
    argument_node_font_size_entry.grid(row=4, column=0, padx=0, sticky="e")

    edge_width_input.grid(row=5, column=0, padx=5, pady=10, sticky="w")
    argument_edge_width_entry.grid(row=5, column=0, padx=0, sticky="e")

    edge_font_input.grid(row=6, column=0, padx=5, pady=10, sticky="w")
    argument_edge_font_entry.grid(row=6, column=0, padx=0, sticky="e")

    text_boxes_size_input.grid(row=7, column=0, padx=5, pady=10, sticky="w")
    argument_textbox_size_entry.grid(row=7, column=0, padx=0, sticky="e")

    dropdown_menu.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

    appearance_mode_label.grid(row=5, column=0)
    appearance_mode_option_menu.grid(row=6, column=0, padx=50)

    max_frame_number = 0
    number_of_frames = 0
    start_button_pressed = False


    def start_animation():
        nonlocal anim, max_frame_number, resume_button, resume_button_on, bit, start_button_pressed
        nonlocal argument_beam_size
        global number_of_frames

        if bit:
            graph.redraw_graph(True)

        if resume_button_on:
            pause_button.grid(row=3, column=0, padx=20, pady=10)
            resume_button.grid_forget()

        if number_of_frames > 1 and number_of_frames + 1 != max_frame_number:
            anim.event_source.stop()
            graph.redraw_graph()

        elif number_of_frames > 0 and number_of_frames + 1 == max_frame_number:
            graph.redraw_graph()

        else:
            if start_button_pressed:
                graph.redraw_graph()

        arg_one = argument_initial_state.get().upper()
        arg_two = argument_goal_state.get().upper()

        initial = State(arg_one)
        goal = State(arg_two)
        algorithm = dropdown_option.get()

        if algorithm == BFS:
            frame = initial.breadth_first_search(initial, goal)

        elif algorithm == DFS:
            frame = initial.depth_first_search(initial, goal)

        elif algorithm == BESTFS:
            frame = initial.best_first_search(initial, goal)

        elif algorithm == ASTAR:
            frame = initial.a_star_search(initial, goal)

        elif algorithm == BEAM:
            arg = argument_beam_size.get()
            beam_width = int(arg) if arg.isdigit() else 12
            frame = initial.beam_search(initial, goal, beam_width)

        elif algorithm == DIJKSTRA:
            frame = initial.dijkstras_search(initial, goal, graph)

        else:
            print(f"Invalid algorithm {algorithm} selected")
            return

        remove_graph_adjusters()
        start_button_pressed = True
        max_frame_number = len(frame)
        interval = argument_interval.get()
        interval = 10 if interval == "" else int(interval)

        # made anim global since the funcAnimation function calls itself recursively to animate the frames.
        # Keeps returning the updated ax (plot) to draw, we pass the function the frame dictionary to know what to colour

        anim = animation.FuncAnimation(
            graph.fig, animate, fargs=(frame, graph), interval=interval, frames=max_frame_number, repeat=False,
            blit=True
        )

    def stop_animation():
        nonlocal max_frame_number, anim, resume_button, resume_button_on
        global number_of_frames

        if number_of_frames > 0 and number_of_frames + 1 != max_frame_number:
            anim.event_source.stop()
            resume_button_on = True
            pause_button.grid_forget()
            resume_button.grid(row=3, column=0, padx=20, pady=10)

    def resume_animation():
        nonlocal anim, resume_button, resume_button_on, pause_button

        anim.event_source.start()
        resume_button_on = False
        pause_button.grid(row=3, column=0, padx=20, pady=10)
        resume_button.grid_forget()

    bit = False

    def redraw_current_graph():
        nonlocal bit
        if bit:
            graph.ax.clear()

        edge_label = {("ND", "MN"): str(234) + " mi"}
        state1, state2 = ["ND", "MN"]
        state = State("ND")

        current_position = {state1: graph.node_positions[state1], state2: graph.node_positions[state2]}

        arg1 = argument_node_font_size.get()
        arg2 = argument_edge_width.get()
        arg3 = argument_node_size.get()
        arg4 = argument_textbox_size.get()
        arg5 = argument_edge_font.get()

        graph.node_font_size = int(arg1) if arg1.isdigit() else graph.node_font_size
        graph.edge_width = int(arg2) if arg2.isdigit() else graph.edge_width
        graph.node_size = int(arg3) if arg3.isdigit() else graph.node_size
        graph.textbox_size = int(arg4) if arg4.isdigit() else graph.textbox_size
        graph.edge_font_size = int(arg5) if arg5.isdigit() else graph.edge_font_size

        graph.redraw_graph(True)
        state.set_textbox(graph)
        state.textbox.set_text("h(n) preview")
        set_gcost_textbox(State("MN"), graph, 200, "open")
        set_gcost_textbox(State("MN"), graph, 200, "neighbor")
        nx.draw_networkx_edge_labels(
            graph.nx_graph,
            current_position,
            edge_labels=edge_label,
            font_color="black",
            font_size=graph.edge_font_size,
            ax=graph.ax,
        )

        canvas.draw()
        bit = True
        state.textbox.remove()

    def remove_graph_adjusters():
        redraw_button.grid_forget()

        node_size_input.grid_forget()
        argument_node_size_entry.grid_forget()

        node_font_size_input.grid_forget()
        argument_node_font_size_entry.grid_forget()

        edge_width_input.grid_forget()
        argument_edge_width_entry.grid_forget()

        edge_font_input.grid_forget()
        argument_edge_font_entry.grid_forget()

        text_boxes_size_input.grid_forget()
        argument_textbox_size_entry.grid_forget()

    window.after(0, lambda:window.state('zoomed'))
    window.mainloop()


if __name__ == "__main__":
    main()
