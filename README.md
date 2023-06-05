# PathfindingApp (US-Version) Demonstration

Note: This project was difficult to put together, it was done before the GPT era. It was challenging, but rewarding.

Video quality looks better not recorded (max 1080p recorded). Speed adjustments vary by performance of your computer.

Additionally, there were some complex issues that I came across, had to think outside the box to overcome them. Especiallly, since I had no projects to reference from.

I took various library functions and created something complex, completely off my own imagination. Roughly, 1000 lines of code.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
    - [Speed Adjustment](#speed-adjustment)
    - [Resizing Feature](#resizing-feature)
    - [Pause/Resume Animation](#pause-resume-animation)
3. [Algorithms](#algorithms)
4. [Animations](#Animations)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Introduction

Welcome to the Pathfinding App documentation. The Pathfinding App is an interactive tool that enables users to visualize and understand various pathfinding algorithms in a user-friendly interface. It features adjustable speed settings, resizable nodes and edges, and a pause/resume animation feature to control visualization. 

## Features

### Speed Adjustment

The Speed Adjustment feature provides an intuitive input control, allowing users to control the speed of the algorithm execution in real-time. This is helpful for both learning purposes, by slowing down to understand each step, and for time efficiency, by speeding up the algorithm once the concept is understood.

### Resizing Feature

The Resizing feature allows users to manipulate the size of nodes and edges in the graph.This allows users with the ability to adjust the size of nodes and edges in the graph. You can modify the size of these elements, making the graph larger, smaller, or adjust it to your preferred size to fit your screen. This functionality allows for a more personalized viewing experience.



https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/fcd8edb0-7df4-4d91-8681-d64950fe795d



### Pause/Resume Animation

The Pause/Resume Animation feature enables users to control the visualization flow of the algorithm. This function allows users to pause the algorithm at any time to study the current state, and then resume when ready. 

## Algorithms

The Pathfinding App supports a wide array of pathfinding algorithms, including but not limited to:

1. Breadth-First Search (BFS)
2. Depth-First Search (DFS)
3. Dijkstra's Algorithm
4. Best First Search
5. A* Search Algorithm
6. Beam Search

Each algorithm comes with a brief description, use case scenarios, and pros and cons to provide a better understanding of its working principles and applications.

## Animations (Search is done alphabetically)

## Color Meaning
1. **Color red (in visited list)**

2. **Color green (in open list)**

3. **Color yellow around state (current state)**

### 1. Breadth-First Search (BFS)


https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/4a3182fa-26a5-4340-9ee7-6b9bb7c93653

Breadth-First Search (BFS) leverages a queue, a First-In-First-Out (FIFO) data structure, to systematically explore every vertex of a graph or, in this case, each state in our analogy. The algorithm starts by adding the starting state (North Dakota) to the queue and marking it as visited. Then, it enters its main loop.

In each iteration, BFS removes the state at the front of the queue (dequeues) and examines it (marks as visited). It then identifies all the neighboring states that have not been visited yet. These states are then added (enqueued) to the back of the queue. This process ensures that we first visit all of the neighbors of the current state before moving on to the neighbors' neighbors.

The queue's FIFO nature ensures that BFS proceeds level by level, visiting all states one 'edge' away, then all states two 'edges' away, and so on. This process continues until all reachable states have been visited or the specific goal state has been reached. The use of a queue, therefore, is instrumental for the algorithm to systematically and effectively traverse all states.

While Breadth-First Search (BFS) can be useful for certain tasks, there are some potential downsides when applying it to a large graph like a map of the United States:

1. **Space Complexity**: BFS stores all vertices of the current level before visiting the vertices at the next level. If you're exploring a large graph like a map of the United States, you could end up storing many states in memory at once, leading to high space complexity. This could potentially strain resources if memory is limited.

2. **Lack of Path Optimality**: BFS will find a solution (if one exists) but it may not be the most efficient or shortest one. If you're trying to find the shortest route between two states, BFS may not give you the optimal result. For instance, if you're trying to find the shortest path from Florida to Washington, BFS might visit states like Texas or Illinois, even though these are not along the shortest path.

3. **Uniformed Search**: BFS treats all edges as equal. It doesn't take into account the actual distances between states or any other edge costs. Two neighboring states in the Midwest may be much further apart than two neighboring states in the Northeast, but BFS treats them as equivalent.

4. **Inefficient for Large Distances**: If the goal node (state) is far from the source node, BFS could be quite inefficient as it exhaustively explores all states level by level. In the context of US states, if we are searching for a state far from the starting state (like starting from California (CA) and looking for Maine (ME)), BFS will still go through every single state on the way.

5. **Cyclic Graphs**: BFS could potentially get stuck in an infinite loop if there are cycles in the graph and if it doesn't keep track of the nodes it has already visited. In a real-world map, states often have more than two neighboring states, potentially creating cycles, so care must be taken to avoid revisiting states.


---

### 2. Depth-First Search (DFS)



https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/b1510b16-5a86-4591-929a-db2ca7fa0c8a



Depth-First Search (DFS) utilizes a stack, a Last-In-First-Out (LIFO) data structure, to systematically traverse every vertex of a graph. The algorithm starts by pushing the initial state (for instance, Texas) onto the stack and marking it as visited. Then, DFS proceeds into its main loop.

In each iteration, DFS removes the state at the top (right-side) of the stack (pops) and examines it. It then identifies all the neighboring states that have not yet been visited. These states are subsequently added (pushed) to the top of the stack. This process ensures that we first explore one path as deeply as possible, visiting all of the states along that path before retracting to the last state where there were unvisited neighbors and continuing the search along the next path.

The stack's LIFO nature ensures that DFS probes deeply into the graph, visiting all states along a single path before retracing steps to explore the next available path. This pattern continues until all accessible states have been visited, or the specific goal state has been found.

DFS differs from BFS by its use of a stack, which results in different traversal order. The LIFO nature of the stack means that DFS follows a path as far as it can go, and then retreats back to the last branching point where there were unvisited nodes.

Now, let's talk about potential downsides of DFS in the context of a map of the US:

1. **Path Optimality**: DFS does not guarantee the shortest path. Given its nature, DFS might end up visiting states far from the target state Michigan while there might be other unvisited states much closer to Michigan.

2. **Space Complexity**: DFS could potentially require a lot of space. If the search path becomes very long, the stack could also become exceedingly large, possibly leading to high space complexity.

3. **Time Complexity**: DFS can be slow for large graphs. It fully explores one path to the end before backtracking, which could take a significant amount of time if the graph is large and the end of the path is far from the root.

4. **Cyclic Graphs**: Like BFS, DFS needs to keep track of visited nodes to avoid cycles and infinite loops. Without this, the algorithm could potentially get stuck going back and forth between two states.

5. **Lack of Search Control**: As DFS is eager and dives deep into nodes, without additional control measures, it can potentially explore very deep and irrelevant parts of the graph. This could make DFS very inefficient if the target node is located high up in the search tree.

---

### 3. Dijkstra's Algorithm



https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/72528777-662d-4262-9183-efaf2510f48b


Dijkstra's algorithm is an optimal, graph traversal algorithm that uses a priority queue data structure to systematically explore all vertices in a graph. The algorithm starts by initializing the starting state (let's say Maine 'ME') with a cost of 0, representing g(n), the cost to reach the starting state. This cost is also referred to as the "path cost". The algorithm assigns every other state a cost of infinity, signifying that we don't yet know the shortest path to those states. With this setup complete, Dijkstra's algorithm enters its main loop.

The main loop operates by repeatedly selecting the state with the lowest known g(n) cost. At each iteration, Dijkstra's algorithm removes the state with the lowest cost (the state with the smallest g(n)) that has not yet been visited (marked red) from the priority queue and "visits" it. It then identifies all neighboring states. For each neighbor, the algorithm calculates the cost, g(n), of the path through the neighbouring state to the starting state. 

To help better understand this path idea, notice when the colors change all pink this represents one path, another is represented by blue. As we find the neighbouring states, we mark the parent of the neighbor as the one who found it. For example, ME finds three neighbors, so we mark the parent attribute of each neighbor as ME, indicating that we have three seperate paths at first, but they keep growing as more neighbors are found. Now with this in mind, if another state finds a state that has already been added to the open list (meaning that we assigned it a parent already), but not explored yet, then we can compare the g(n) cost of the current state that found it to its already assigned parent. If the current state minimizes the g(n) cost, then we switch the parent attribute of the openlist state to this current state since it is more effecient. Notice that there is a orange link that moves, indicating that we changed the parent since we compared the two path costs and decided that this parent makes the path more effecient.

Through this process, Dijkstra's algorithm ensures it explores the state with the shortest known path from the start state. This operation continues until all reachable states have been visited, or the specific goal state (in our analogy, Colorado) is reached. 

In sum, Dijkstra's algorithm systematically and effectively traverses all states by continually selecting the state with the lowest g(n) cost for exploration. The priority queue, by always dequeuing the state with the smallest g(n), plays a crucial role in maintaining the algorithm's efficiency.

Although Dijkstra's algorithm is a powerful tool, there are potential downsides when applying it to a large graph like a map of the United States:

1. **Performance**: Dijkstra's algorithm can be computationally expensive for large maps, such as the map of the United States, because it performs a complete search and explores all states in the graph.

2. **Negative Edge Weights**: Dijkstra's algorithm does not handle negative weight edges. This isn't typically a problem when dealing with physical distances (since distances are always positive) but can limit the algorithm's applicability in other types of graphs where weights can potentially be negative.

3. **No Heuristic Guidance**: Unlike A*, Dijkstra's algorithm doesn't use a heuristic to direct its search towards the goal. This means it may spend significant time exploring states that are in the opposite direction of the goal.

4. **Space Complexity**: Like BFS, A*, and Best-First Search, Dijkstra's algorithm can lead to high space complexity because it might need to store many states in the queue, a problem if memory is limited.

---

### 4. Best First Search

https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/3d991a52-a2f3-4790-a748-cc41400a591e

Best-First Search (BFS) employs a priority queue, a data structure that always dequeues the highest priority element, to systematically explore every vertex of a graph or, in this case, each state in our analogy. This priority is typically determined by a heuristic (h(n)), a kind of estimate that predicts how close a state is to the goal. In this case, the heuristic might be the straight-line distance from the current state to New York. The algorithm starts by adding the starting state (Oregon) to the queue and marking it as visited. Then, it enters its main loop.

In each iteration, Best-First Search removes the state with the highest priority (the state estimated to be closest to the goal, NY) from the queue (dequeues) and examines it. It then identifies all the neighboring states that have not been visited yet. These states are then added (enqueued) to the queue with a priority based on the heuristic. This process ensures that we first visit the state that our heuristic estimates to be closest to New York.

The priority queue's nature ensures that Best-First Search proceeds by always exploring the most promising state, the state that the heuristic estimates to be closest to the goal. This process continues until the specific goal state, NY, has been reached. The use of a priority queue, therefore, is instrumental for the algorithm to systematically and effectively traverse all states.

While Best-First Search can be effective for certain tasks, there are potential downsides when applying it to a large graph like a map of the United States:

1. **Heuristic Dependence**: The efficiency of Best-First Search heavily depends on the quality of the heuristic. A poorly chosen heuristic can lead to inefficient paths or even make the algorithm fail to find a path.

2. **Lack of Optimality**: Best First Search does not guarantee the most efficient path. In this case, it only considered the distance to the goal, this did not ensure that we had the most optimal path since we did not acknowledge the distance to each neighbor. We will run the same inputs for A* search below, so that you can see how Best First Search did not lead to the optimal path.

3. **Space Complexity**: Like BFS, Best-First Search may need to store a large number of states in the queue, leading to high space complexity. This could be problematic if memory is limited.

4. **Inefficiency for Uniform Cost Graphs**: For graphs where all edges have the same cost, Best-First Search degenerates into BFS as the heuristic does not provide any additional information, leading to similar inefficiencies as BFS in such scenarios.

---

### 5. A* Search Algorithm


https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/79830fe7-f14c-448f-a1c9-c83cf4a01eda

(Recommended to read dijkstra's description before reading A* search, to better understand it)

The A* search algorithm incorporates elements of both Dijkstra's algorithm and Best-First Search. It utilizes a priority queue, much like Best-First Search, to systematically explore every vertex of a graph. The algorithm begins by adding the starting state (Oregon) to the queue and marking it as visited. Then, it enters its main loop.

Unlike Best-First Search, which uses a heuristic to determine priority, A* uses a combination of the cost so far to reach the current state (known as g(n)) and the estimated cost from the current state to the goal (known as h(n)) to prioritize states. This total cost f(n) = g(n) + h(n) gives A* its characteristic blend of informed and exhaustive searching.

In each iteration, A* removes the state with the lowest total cost (the state with the smallest f(n)) from the queue and examines it. It then identifies all the neighboring states that have not been visited yet. These states are added to the queue with a priority based on their total cost. A* also keeps track of the parent of each state - the state from which it was discovered. 

If a neighboring state is already in the queue (known as the open list in A* terminology), A* compares the total cost of reaching the neighbor through the current state and the previously found path. If the new path is more efficient (lower total cost), A* updates the cost and parent of the neighbor state to reflect the more efficient path.

This process ensures that A* not only finds a path to the goal but aims to find the most efficient path based on its heuristic and real costs. The use of a priority queue and keeping track of the parent states is instrumental for A* to systematically, effectively, and efficiently traverse all states.

The A* algorithm has several advantages when applied to a large graph like a map of the United States:

1. **Optimality**: Unlike Best-First Search, A* guarantees to find the shortest path to the goal, as long as the heuristic is admissible (never overestimates the actual cost) and consistent (satisfies the triangle inequality).

2. **Efficiency**: A* is usually more efficient than Best-First Search as it uses the real cost to guide its search, which tends to result in fewer states visited and thus less memory used.

However, there are also potential downsides to A*:

3. **Heuristic Dependence**: The efficiency of A* is highly dependent on the quality of the heuristic. A poorly chosen heuristic can lead to inefficiencies or even make the algorithm perform as poorly as Dijkstra's (if the heuristic always returns 0) or Best-First Search (if the heuristic ignores the cost so far).

4. **Space Complexity**: Like other graph search algorithms, A* can suffer from high space complexity as it needs to store all visited states, which could be problematic if memory is limited. 

5. **Complexity of Implementation**: Keeping track of the parent of each node and updating these when a better path is found makes the implementation of A* more complex than that of some other search algorithms.

---

### 6. Beam Search

Beta = 3

https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/fabf6f66-fffb-4c92-8122-855a5d23b322

Beta = 1 (No solution)

https://github.com/g-tapia/PathfindingApp-US-Version--Demonstration/assets/78235399/632cd056-b1d6-49ef-a418-635675be8975


Beam Search is a heuristic search algorithm that operates by exploring the most promising nodes in a graph. In our context, it's like traversing a map of the United States, but rather than examining all states, Beam Search focuses on a select "beam" of states. This beam represents the set of most promising states, selected based on a heuristic or cost function.

In our new scenario, let's assume we're starting from Missouri (MO) with our goal state being Maine (ME). Beam Search initiates by expanding the starting state (MO) and examining its neighboring states. From these, it selects the 𝛽 most promising states to retain in the beam, where 𝛽 is a predefined parameter determining the width of the beam. These "most promising" states are those that, according to our heuristic, are estimated to be closest to ME. 

As the algorithm progresses, it extends these 𝛽 states, generating their neighbors. However, in line with the beam search strategy, only the 𝛽 most promising states from this expanded list are kept in the beam. 

This process of expansion and selection continues iteratively, with the beam advancing towards the goal state while maintaining a width of 𝛽 states. Beam Search continues until it reaches the goal state (ME) or exhausts all possible paths. 

By maintaining a constant beam width (𝛽), the algorithm retains a manageable number of states at each level, enhancing memory efficiency compared to other algorithms like Breadth-First Search or Depth-First Search. 

Despite these advantages, there are some potential drawbacks when applying Beam Search to a large graph, such as the map of the United States:

1. **Incomplete**: Since Beam Search only maintains the 𝛽 most promising states at each level, it might miss potential solutions. There's no guarantee it will find a solution even if one exists.

2. **Suboptimal Solutions**: The solutions Beam Search finds might not be optimal or the shortest path to the goal state. The quality of the solution is heavily dependent on the value of 𝛽, with a small 𝛽 possibly causing the search to overlook better paths.

3. **Heuristic Dependency**: The performance of Beam Search is heavily reliant on the heuristic function used to estimate the cost to the goal state. A poorly chosen heuristic may lead to less promising states being included in the beam, making the search less efficient.

4. **Limited Exploration**: Beam Search explores a relatively small subset of paths due to its strict beam width limitation. This strategy could lead to potentially viable paths being unexplored, causing the algorithm to be less comprehensive than others, like A* or Dijkstra's.

---



## Usage

Animated pathfinding applications can be a highly valuable tool for learning, particularly in subjects like computer science, mathematics, or logic. Here's why:

1. **Visualizing Abstract Concepts**: Algorithms, by their nature, are abstract. They involve a series of steps that can sometimes be challenging to envision. Animated pathfinding applications, however, make these concepts tangible by visually demonstrating how different algorithms work in real-time. This visualization can help students grasp these abstract concepts more easily and thoroughly.

2. **Engaging Learning Experience**: An animated application provides an engaging, interactive learning experience. It can make learning more fun and interactive, which can help maintain students' interest and improve their retention of the material.

3. **Comparison and Analysis**: By visualizing different pathfinding algorithms side by side, students can easily compare and analyze their performance. They can see how different algorithms handle the same problem, how they differ in terms of speed, efficiency, and path quality, and how they react to different constraints.

4. **Promotes Critical Thinking**: Using animated pathfinding applications encourages students to think critically. They can observe the algorithm's behavior, predict its next steps, and even debug it if it doesn't behave as expected. This engagement promotes a deeper understanding of the algorithm's inner workings.

5. **Versatility in Learning Scenarios**: These applications can be used in a variety of educational contexts. In a classroom, they can be used to demonstrate concepts during a lecture, or students can use them individually or in groups for assignments or projects. In textbooks or online resources, they can provide interactive content to supplement written material.

Incorporating animated pathfinding applications in learning environments can stimulate students' interest in algorithms and computational thinking, enhancing their learning experience and understanding of these key concepts.


## License

This section contains information about the licensing of the Pathfinding App. I have no license, but this section looks cool so I kept it (lol)

For any additional inquiries, please feel free to contact me. I hope that you find the Pathfinding App useful in your studies and work.
