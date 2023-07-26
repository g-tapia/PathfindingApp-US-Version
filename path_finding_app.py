#!/usr/bin/env python
# coding: utf-8

import heapq
import customtkinter
import networkx as nx

from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from graph import Graph
from state import BFS, DFS, BESTFS, ASTAR, BEAM, DIJKSTRA, State


from animation_functions import *

SHORT, LONG = 80, 220


class UserInterface:
    class Buttons:
        def __init__(self):
            self.start = None
            self.resume = None
            self.pause = None

    class Arguments:
        def __init__(self):
            self.initial_state = None
            self.goal_state = None
            self.interval = None
            self.node_size = None
            self.node_font_size = None
            self.edge_width = None
            self.edge_font = None
            self.textbox_size = None
            self.beam_size = None
            self.beam_size_entry = None
            self.dropdown_option = None

    class Frames:
        def __init__(self, ui):
            self.side_column = ui.create_side_column()
            self.top = ui.create_top_frame(self.side_column)
            self.middle = ui.create_middle_frame(self.side_column, self.top)
            self.bottom = ui.create_bottom_frame(self.side_column)

    class BeamElements:
        def __init__(self):
            self.elements = []

    def __init__(self):
        self.graph_redrawn = False
        self.resume_button_on = False
        self.start_button_pressed = False

        self.anim = None
        self.graph = Graph()
        self.graph_adjusters = []
        self.canvas = None
        self.number_of_frames = 0
        self.max_frame_number = 0

        self.window = self.create_window()
        self.buttons = self.Buttons()
        self.arguments = self.Arguments()
        self.frames = self.Frames(self)
        self.beam = self.BeamElements()

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def create_window(self):
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        window = customtkinter.CTk()
        window.title("Graph Traversal Animation")

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.geometry(f"{screen_width}x{screen_height}")
        window.maxsize(screen_width, screen_height)

        self.canvas = FigureCanvasTkAgg(self.graph.fig, master=window)
        self.canvas.draw()
        window.rowconfigure(0, weight=1)  # Allow the graph to expand vertically
        window.columnconfigure(1, weight=1)  # Allow the graph to expand horizontally

        self.canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")

        return window

    def create_side_column(self):
        side_column = customtkinter.CTkFrame(self.window, width=LONG)
        side_column.grid(row=0, column=0, rowspan=6, sticky="nsew")
        side_column.rowconfigure(6, weight=1)

        return side_column

    def create_top_frame(self, side_column):
        top_frame = customtkinter.CTkFrame(side_column, width=LONG)
        top_frame.grid(row=0, column=0)

        self.buttons.start = customtkinter.CTkButton(
            top_frame, text="Start Animation", command=lambda: self.start_animation()
        )

        start_state_header = customtkinter.CTkLabel(top_frame, text="Initial State:")
        self.arguments.initial_state = customtkinter.StringVar(top_frame)
        argument_initial_state_entry = customtkinter.CTkEntry(
            top_frame, textvariable=self.arguments.initial_state, width=SHORT
        )

        goal_state_header = customtkinter.CTkLabel(top_frame, text="Goal State:")
        self.arguments.goal_state = customtkinter.StringVar(top_frame)
        argument_goal_state_entry = customtkinter.CTkEntry(
            top_frame, textvariable=self.arguments.goal_state, width=SHORT
        )

        # creating the input fields
        interval_header = customtkinter.CTkLabel(top_frame, text="Interval Input[10] (Optional)")
        self.arguments.interval = customtkinter.StringVar(top_frame)
        argument_interval_entry = customtkinter.CTkEntry(top_frame, textvariable=self.arguments.interval)

        self.buttons.pause = customtkinter.CTkButton(
            top_frame, text="Pause Animation", command=lambda: self.stop_animation(), fg_color="dark red"
        )

        self.buttons.resume = customtkinter.CTkButton(
            top_frame, text="Resume Animation", command=lambda: self.resume_animation(), fg_color="dark green"
        )

        # Placements of buttons on the left side
        self.buttons.start.grid(row=2, column=0, padx=50, pady=20)
        self.buttons.pause.grid(row=3, column=0, padx=20, pady=10)

        start_state_header.grid(row=0, column=0, padx=(10, 0), pady=20, sticky="w")
        argument_initial_state_entry.grid(row=0, column=0, padx=(100, 10), pady=20, sticky="w")

        goal_state_header.grid(row=1, column=0, padx=(10, 0), pady=20, sticky="w")
        argument_goal_state_entry.grid(row=1, column=0, padx=(99, 10), pady=20, sticky="w")

        interval_header.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        argument_interval_entry.grid(row=5, column=0, padx=20, sticky="ew")

        return top_frame

    def create_middle_frame(self, side_column, top_frame):
        middle_frame = customtkinter.CTkFrame(side_column, width=LONG)
        middle_frame.grid(row=6, column=0, sticky="ew")

        redraw_button = customtkinter.CTkButton(
            middle_frame, text="Redraw Graph", command=lambda: self.redraw_current_graph()
        )

        node_size_header = customtkinter.CTkLabel(middle_frame, text="Node Size[950]:")
        self.arguments.node_size = customtkinter.StringVar(middle_frame)
        argument_node_size_entry = customtkinter.CTkEntry(
            middle_frame, textvariable=self.arguments.node_size, width=SHORT
        )

        node_font_size_header = customtkinter.CTkLabel(middle_frame, text="Node Font Size[10]:")
        self.arguments.node_font_size = customtkinter.StringVar(middle_frame)
        argument_node_font_size_entry = customtkinter.CTkEntry(
            middle_frame, textvariable=self.arguments.node_font_size, width=SHORT
        )

        edge_width_header = customtkinter.CTkLabel(middle_frame, text="Edge Width[2]:")
        self.arguments.edge_width = customtkinter.StringVar(middle_frame)
        argument_edge_width_entry = customtkinter.CTkEntry(
            middle_frame, textvariable=self.arguments.edge_width, width=SHORT
        )

        edge_font_header = customtkinter.CTkLabel(middle_frame, text="Edge Font[7]:")
        self.arguments.edge_font = customtkinter.StringVar(middle_frame)
        argument_edge_font_entry = customtkinter.CTkEntry(
            middle_frame, textvariable=self.arguments.edge_font, width=SHORT
        )

        text_boxes_size_header = customtkinter.CTkLabel(middle_frame, text="Text Box Size[6]:")
        self.arguments.textbox_size = customtkinter.StringVar(middle_frame)
        argument_textbox_size_entry = customtkinter.CTkEntry(
            middle_frame, textvariable=self.arguments.textbox_size, width=SHORT
        )

        self.arguments.dropdown_option = customtkinter.StringVar(top_frame)
        dropdown_menu = customtkinter.CTkComboBox(
            master=middle_frame,
            width=LONG,
            values=[BFS, DFS, BESTFS, ASTAR, BEAM, DIJKSTRA],
            variable=self.arguments.dropdown_option,
            command=self.algorithm_choice,
        )

        dropdown_menu.set("Algorithms Available")

        # placing widgets on the left side of the frame
        redraw_button.grid(row=2, column=0, padx=20, pady=20)

        node_size_header.grid(row=3, column=0, padx=5, pady=10, sticky="w")
        argument_node_size_entry.grid(row=3, column=0, padx=0, sticky="e")

        node_font_size_header.grid(row=4, column=0, padx=5, pady=10, sticky="w")
        argument_node_font_size_entry.grid(row=4, column=0, padx=0, sticky="e")

        edge_width_header.grid(row=5, column=0, padx=5, pady=10, sticky="w")
        argument_edge_width_entry.grid(row=5, column=0, padx=0, sticky="e")

        edge_font_header.grid(row=6, column=0, padx=5, pady=10, sticky="w")
        argument_edge_font_entry.grid(row=6, column=0, padx=0, sticky="e")

        text_boxes_size_header.grid(row=7, column=0, padx=5, pady=10, sticky="w")
        argument_textbox_size_entry.grid(row=7, column=0, padx=0, sticky="e")

        dropdown_menu.grid(row=0, column=0, padx=10, pady=20, sticky="ew")

        self.graph_adjusters = [
            redraw_button,
            node_size_header,
            argument_node_size_entry,
            node_font_size_header,
            argument_node_font_size_entry,
            edge_width_header,
            argument_edge_width_entry,
            edge_font_header,
            argument_edge_font_entry,
            text_boxes_size_header,
            argument_textbox_size_entry,
        ]

        return middle_frame

    def create_bottom_frame(self, side_column):
        bottom_frame = customtkinter.CTkFrame(side_column, width=LONG)
        bottom_frame.grid(row=7, column=0)

        appearance_mode_header = customtkinter.CTkLabel(bottom_frame, text="Appearance Mode:")
        appearance_mode_option_menu = customtkinter.CTkOptionMenu(
            bottom_frame, values=["Dark", "Light"], command=self.change_appearance_mode_event
        )

        appearance_mode_header.grid(row=5, column=0)
        appearance_mode_option_menu.grid(row=6, column=0, padx=50)

        return bottom_frame

    def algorithm_choice(self, algorithm_selected):
        if algorithm_selected == "beam search":
            self.beam_header = customtkinter.CTkLabel(self.frames.middle, text="Set Beam:")
            self.arguments.beam_size = customtkinter.StringVar(self.frames.middle)
            self.arguments.beam_size_entry = customtkinter.CTkEntry(
                self.frames.middle, textvariable=self.arguments.beam_size, width=SHORT
            )
            self.beam_header.grid(row=1, column=0, padx=(20, 40), pady=20, sticky="w")
            self.arguments.beam_size_entry.grid(row=1, column=0, padx=(10, 40), sticky="e")

            self.beam.elements = [self.beam_header, self.arguments.beam_size_entry]
        else:
            for value in self.beam.elements:
                value.grid_forget()

    def start_animation(self):
        if self.graph_redrawn:
            self.graph.redraw_graph(True)

        if self.resume_button_on:
            self.buttons.pause.grid(row=3, column=0, padx=20, pady=10)
            self.buttons.resume.grid_forget()

        if self.number_of_frames > 1 and self.number_of_frames + 1 != self.max_frame_number:
            self.anim.event_source.stop()
            self.graph.redraw_graph()

        elif self.number_of_frames > 0 and self.number_of_frames + 1 == self.max_frame_number:
            self.graph.redraw_graph()

        else:
            if self.start_button_pressed:
                self.graph.redraw_graph()

        arg_one = self.arguments.initial_state.get().upper()
        arg_two = self.arguments.goal_state.get().upper()

        initial = State(arg_one)
        goal = State(arg_two)
        algorithm = self.arguments.dropdown_option.get()

        if algorithm == BFS:
            frame = initial.breadth_first_search(initial, goal)

        elif algorithm == DFS:
            frame = initial.depth_first_search(initial, goal)

        elif algorithm == BESTFS:
            frame = initial.best_first_search(initial, goal)

        elif algorithm == ASTAR:
            frame = initial.a_star_search(initial, goal)

        elif algorithm == BEAM:
            arg = self.arguments.beam_size.get()
            beam_width = int(arg) if arg.isdigit() else 12
            frame = initial.beam_search(initial, goal, beam_width)

        elif algorithm == DIJKSTRA:
            frame = initial.dijkstras_search(initial, goal, self.graph)

        else:
            print(f"Invalid algorithm {algorithm} selected")
            return

        self.remove_graph_adjusters()
        self.start_button_pressed = True
        self.max_frame_number = len(frame)
        interval = self.arguments.interval.get()
        interval = 10 if interval == "" else int(interval)

        # made anim global since the funcAnimation function calls itself recursively to animate the frames.
        # Keeps returning the updated ax (plot) to draw, we pass the function the frame dictionary to know what to colour

        self.anim = animation.FuncAnimation(
            self.graph.fig,
            animate,
            fargs=(frame, self.graph, self),
            interval=interval,
            frames=self.max_frame_number,
            repeat=False,
            blit=True,
        )

    def stop_animation(self):
        self.anim.event_source.stop()
        self.resume_button_on = True
        self.buttons.pause.grid_forget()
        self.buttons.resume.grid(row=3, column=0, padx=20, pady=10)

    def resume_animation(self):
        self.anim.event_source.start()
        self.resume_button_on = False
        self.buttons.pause.grid(row=3, column=0, padx=20, pady=10)
        self.buttons.resume.grid_forget()

    def redraw_current_graph(self):
        if self.graph_redrawn:
            self.graph.ax.clear()

        edge_label = {("ND", "MN"): str(234) + " mi"}
        state1, state2 = ["ND", "MN"]
        state = State("ND")

        current_position = {state1: self.graph.node_positions[state1], state2: self.graph.node_positions[state2]}

        arg1 = self.arguments.node_font_size.get()
        arg2 = self.arguments.edge_width.get()
        arg3 = self.arguments.node_size.get()
        arg4 = self.arguments.textbox_size.get()
        arg5 = self.arguments.edge_font.get()

        self.graph.node_font_size = int(arg1) if arg1.isdigit() else self.graph.node_font_size
        self.graph.edge_width = int(arg2) if arg2.isdigit() else self.graph.edge_width
        self.graph.node_size = int(arg3) if arg3.isdigit() else self.graph.node_size
        self.graph.textbox_size = int(arg4) if arg4.isdigit() else self.graph.textbox_size
        self.graph.edge_font_size = int(arg5) if arg5.isdigit() else self.graph.edge_font_size

        self.graph.redraw_graph(True)
        state.set_textbox(self.graph)
        state.textbox.set_text("h(n) preview")
        set_gcost_textbox(State("MN"), self.graph, 200, "open")
        set_gcost_textbox(State("MN"), self.graph, 200, "neighbor")
        nx.draw_networkx_edge_labels(
            self.graph.nx_graph,
            current_position,
            edge_labels=edge_label,
            font_color="black",
            font_size=self.graph.edge_font_size,
            ax=self.graph.ax,
        )

        self.canvas.draw()
        self.graph_redrawn = True
        state.textbox.remove()

    def remove_graph_adjusters(self):
        for element in self.graph_adjusters:
            element.grid_forget()


def main():
    app = UserInterface()
    app.window.after(60, lambda: app.window.state("zoomed"))
    app.window.mainloop()


if __name__ == "__main__":
    main()
