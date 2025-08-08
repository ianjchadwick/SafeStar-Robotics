import sys
import time
import numpy as np
import collections
from queue import PriorityQueue

""" 
Create a node object with fields: 
node_id = integer
coords = list with x-y coordinates [x,y]
d_exit = manhattan distance to nearest exit. initialized at maxsize
safety = distance from a hazard location
neighbors = list of neighbors by node_id
cost = g(x) movement cost from "moves so far"
"""
class Node:
    def __init__(self, node_id: int, coords: list[int]):
        self.node_id = node_id
        self.coords = coords
        self.d_exit = sys.maxsize
        self.safety = sys.maxsize
        self.neighbors = []
        self.cost = float
        self.backpointer = int


"""
Implement a Queue for wavefront algorithm
"""
class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def enque(self, x: int):
        self.elements.append(x)

    def is_member(self, x) -> bool:
        return self.elements.count(x) != 0

    def pop(self) -> int:
        return self.elements.popleft()


class Graph:
    def __init__(self, size: int, obstacles: list, exits: list):
        self.grid = grid_construct(size, obstacles)
        self.nodes = []
        self.exits = exits

    """
    Output: The modified grid and a graph represented as a list of nodes which in turn represent the free spaces

    Initializes the graph from a grid where 1s are free space and 0s are blocked spaces. Adds each node to "nodes" list
    for each free space where the node_id-1 corresponds to the list's index for that node and to replace each "1" in the 
    grid with the number of the node_id that represents that space.
    """
    def graph_initialize(self):
        size = len(self.grid)
        # start numbering nodes at 1 because 0s are used for obstacles.
        nodeNum = 1

        for x in range(0, size):
            for y in range(0, size):
                if self.grid[x][y] == 1:
                    self.grid[x][y] = nodeNum
                    node = Node(nodeNum, [x, y])
                    self.nodes.append(node)
                    nodeNum = nodeNum + 1

    """
    Output: updates neighbors attribute for each node in the graph representing the edge list for that node

    Uses updated grid that has node numbers corresponding to their location in each open cell and the graph to populate 
    each node's neighbors attribute with a list of neighbors by node_id starting CW -> N, E, S, W. These represent the 
    undirected edges between each node
    """
    def node_get_neighbors(self):

        gridSize = len(self.grid) - 1
        for node in self.nodes:
            nodeX = node.coords[0]
            nodeY = node.coords[1]

            # Add neighbor's node_id from grid if non-zero
            # check N
            if nodeX != 0 and self.grid[nodeX - 1][nodeY] != 0:
                node.neighbors.append(self.grid[nodeX - 1][nodeY])
            # check E
            if nodeY != gridSize and self.grid[nodeX][nodeY + 1] != 0:
                node.neighbors.append(self.grid[nodeX][nodeY + 1])
            # check S
            if nodeX != gridSize and self.grid[nodeX + 1][nodeY] != 0:
                node.neighbors.append(self.grid[nodeX + 1][nodeY])
            # check W
            if nodeY != 0 and self.grid[nodeX][nodeY - 1] != 0:
                node.neighbors.append(self.grid[nodeX][nodeY - 1])

    """
    Output: Updated d_exit values for nodes in the graph

    Find the distance to the closest exit (d_exit) from a list of [x,y] coordinate pairs corresponding to exits in exitList
    and update the node's d_exit with that value
    """
    def node_set_d_exit(self):
        for node in self.nodes:
            for element in self.exits:
                d_exit = distance_manhattan(node.coords, element)
                if d_exit < node.d_exit:
                    node.d_exit = d_exit

    """
    Inputs: A list of hazard[x,y] coordinates
    Output: the graph with updated safety attribute for each node
    """
    def hazard_wavefront(self, hazard_coordinates: list[list[int]]):

        # Get the corresponding nod_id from the hazard coordinates
        hazard_locations = []
        for coordinate in hazard_coordinates:
            for node in self.nodes:
                if node.coords == coordinate:
                    hazard_locations.append(node.node_id)
                    break

        for hazard in hazard_locations:
            Q = Queue()
            self.nodes[hazard - 1].safety = 0
            Q.enque(hazard)
            closed = []
            while not Q.empty():
                n = Q.pop()
                closed.append(n)
                current = self.nodes[n-1]
                wavefront = current.safety + 1

                for neighbor_id in current.neighbors:
                    if neighbor_id not in closed:
                        if self.nodes[neighbor_id - 1].safety > wavefront:
                            self.nodes[neighbor_id - 1].safety = wavefront
                        if not Q.is_member(neighbor_id):
                            Q.enque(neighbor_id)

    def next_cost(self, currentNode, nextNode):

        cost = 2.0
        curr_d_exit = self.nodes[currentNode - 1].d_exit
        curr_safety = self.nodes[currentNode - 1].safety
        next_d_exit = self.nodes[nextNode - 1].d_exit
        next_safety = self.nodes[nextNode - 1].safety

        if curr_safety < next_safety and curr_d_exit > next_d_exit:
            cost = 0
        if curr_safety <= next_safety and curr_d_exit <= next_d_exit:
            cost = 1
        if curr_safety > next_safety and curr_d_exit >= next_d_exit:
            cost = 1.5
        if curr_safety > next_safety and curr_d_exit < next_d_exit:
            cost = 2
        return cost

    def safest_escape_path(self, start):
        pqueue = PriorityQueue()
        closed = []
        start_id = int()
        exit_id = int()
        path = []
        # find node_id for matching start node
        for node in self.nodes:
            if node.coords == start:
                start_id = node.node_id
                break
        self.nodes[start_id - 1].cost = 0
        pqueue.put((0, start_id))

        while not pqueue.empty():
            # Get node_id of the next best node in the queue
            nbest_id = pqueue.get()[1]
            closed.append(nbest_id)
            nbest = self.nodes[nbest_id - 1]

            # Check to see if at an exit
            if nbest.d_exit == 0:
                exit_id = nbest.node_id
                break

            for neighbor_id in nbest.neighbors:
                new_cost = nbest.cost + self.next_cost(nbest.node_id, neighbor_id)
                neighbor = self.nodes[neighbor_id - 1]
                if neighbor_id not in closed or new_cost < neighbor.cost:
                    neighbor.cost = new_cost
                    heuristic = neighbor.d_exit - neighbor.safety
                    neighbor_priority = new_cost + heuristic
                    neighbor.backpointer = nbest.node_id
                    if not any(neighbor_id in item for item in pqueue.queue):
                        pqueue.put((neighbor_priority, neighbor_id))

        path_id = exit_id
        while path_id != start_id:
            path.append(path_id)
            path_id = self.nodes[path_id - 1].backpointer

        path.append(start_id)
        path.reverse()
        return path

    def regular_a_star(self, start):
        pqueue = PriorityQueue()
        closed = []
        start_id = int()
        exit_id = int()
        path = []
        # find node_id for matching start node
        for node in self.nodes:
            if node.coords == start:
                start_id = node.node_id
                break
        self.nodes[start_id - 1].cost = 0
        pqueue.put((0, start_id))

        while not pqueue.empty():
            # Get node_id of the next best node in the queue
            nbest_id = pqueue.get()[1]
            nbest = self.nodes[nbest_id - 1]
            closed.append(nbest.node_id)

            # Check to see if at an exit
            if nbest.d_exit == 0:
                exit_id = nbest.node_id
                break

            for neighbor_id in nbest.neighbors:
                new_cost = nbest.cost + 1
                neighbor = self.nodes[neighbor_id - 1]

                if neighbor_id not in closed or new_cost < neighbor.cost:
                    neighbor.cost = new_cost
                    neighbor_priority = neighbor.d_exit + new_cost
                    neighbor.backpointer = nbest.node_id
                    if not any(neighbor_id in item for item in pqueue.queue):
                        pqueue.put((neighbor_priority, neighbor_id))

        path_id = exit_id
        while path_id != start_id:
            path.append(path_id)
            path_id = self.nodes[path_id - 1].backpointer

        path.append(start_id)
        path.reverse()
        return path


"""
Inputs: integer for size of grid, list describing obstacle location and dimension (see * below)
Output: An array representation of a 2D grid where 1s represent free space and 0s are spaces blocked by obstacles

Create a 'size' x 'size' square ndarray with ones to represent free space and zeros for the spaces blocked by obstacles.
The x-axis is the vertical (row) axis and the y-axis is the horizontal (column) axis.

*Obstacles are represented as a list where each 'obstacle' list is composed of the top left starting coordinate and the 
length in the x and y directions [ [x,y], xLength, yLength].
"""
def grid_construct(size, obstacles):
    grid = np.ones([size, size], dtype=int)

    for obstacle in obstacles:
        xStart = obstacle[0][0]
        yStart = obstacle[0][1]
        xLength = obstacle[1]
        yLength = obstacle[2]

        for x in range(xStart, xStart+xLength):
            for y in range(yStart, yStart+yLength):
                grid[x][y] = 0
    return grid


# Determines that manhattan distance between two points on a grid where the points are a list of [x,y] coordinates
def distance_manhattan(point1, point2):
    distance = abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])
    return distance


if __name__ == "__main__":

    """
    9x9 test 1
    * = Obstacles
    HZ = hazard [0,6]
    ES = Escapee [1,4]
    EX = Exit [3, 8], [8, 0]
    [ 1  2  3  4  5  6 HZ  8  9]
    [10  ******* ES  * 12  ****]
    [13  * 14 15 16  * 17 18 19]
    [20  * 21  0 22  * 23 24 EX]
    [26  * 27  0 28  * 29  ****]
    [30 31 32 33 34 35 36 37 38]
    [************** 39  *******]
    [40 41 42 43  * 44 45 46 47]
    [EX 49 50 51 52 53  0 54 55]
     
    Safest Shortest Path:14
    [11, 16, 22, 28, 34, 35, 39, 44, 53, 52, 51, 50, 49, 48]
     
    A* Shortest Path:9
    [11, 5, 6, 7, 12, 17, 23, 24, 25]
    """

    obstacles = [[[1, 1], 1, 3],
                 [[1, 1], 4, 1],
                 [[3, 3], 2, 1],
                 [[1, 5], 4, 1],
                 [[1, 7], 1, 2],
                 [[4, 7], 1, 2],
                 [[6, 0], 1, 5],
                 [[6, 4], 2, 1],
                 [[6, 6], 1, 3],
                 [[8, 6], 1, 1]]
    exits = [[3, 8], [8, 0]]
    hazards = [[0, 6]]
    size = 9
    start = [1, 4]

    graph = Graph(size, obstacles, exits)
    graph.graph_initialize()
    graph.node_get_neighbors()
    graph.node_set_d_exit()

    safetygrid = np.zeros([size, size], dtype=int)
    d_exitgrid = np.zeros([size, size], dtype=int)

    wave_tic = time.perf_counter()
    graph.hazard_wavefront(hazards)
    wave_toc = time.perf_counter()
    print(graph.grid)

    node_count = len(graph.nodes)
    print("Number of Nodes: " + str(node_count))

    print("Wavefront Timer: ")
    print(wave_toc - wave_tic)
    safe_tic = time.perf_counter()
    safest_shortest_path = graph.safest_escape_path(start)
    safe_toc = time.perf_counter()
    print("Safest Path A* Timer: ")
    print(safe_toc - safe_tic)
    safest_PL = len(safest_shortest_path)
    print("Safest Shortest Path:" + str(safest_PL))
    print(safest_shortest_path)
    star_tic = time.perf_counter()
    a_star_shortest_path = graph.regular_a_star(start)
    star_toc = time.perf_counter()
    print("Regular A* Timer: ")
    print(star_toc - star_tic)
    a_star_PL = len(a_star_shortest_path)
    print("A* Shortest Path:" + str(a_star_PL))
    print(a_star_shortest_path)

    """
    9x13 test 2
    * = Obstacles
    HZ = hazard [0,11] (Node 12)
    ES = Escapee [1,9] (Node 17)
    EX = Exit [8, 0], [5, 12]
    [ 1  2  3  4  5  6  7  8  9 10 11 HZ 13]
    [14 ** 15  ********** 16 ** ES ***** 18]
    [19 ** 20 21 22 23 ** 24 ** 25 26 ** 27]
    [28 ** 29 30 31 32 ** 33 34 35 36 ** 37]
    [38 39 40  ********** 41  ********** 42]
    [43 44 45 46 47 48 49 50 51 52 53 54 EX]
    [******** 56 ** 57 ** 58 *********** 59]
    [60 61 62 63 ** 64 ** 65 66 67 68 ** 69]
    [EX 71 72 73 ** 74 ** 75 76 77 78 ** 79]
    
    Safest Shortest Path:19
    [17, 25, 26, 36, 35, 34, 33, 41, 50, 49, 48, 47, 46, 56, 63, 62, 61, 60, 70]
    
    A* Shortest Path:10
    [17, 10, 11, 12, 13, 18, 27, 37, 42, 55]
    """

    obstacles2 = [[[1, 1], 3, 1],
                 [[1, 3], 1, 3],
                 [[1, 6], 4, 1],
                 [[1, 8], 2, 1],
                 [[1, 10], 1, 2],
                 [[1, 11], 4, 1],
                 [[4, 3], 1, 4],
                 [[4, 8], 1, 4],
                 [[6, 0], 1, 3],
                 [[6, 4], 3, 1],
                 [[6, 6], 3, 1],
                 [[6, 8], 1, 4],
                 [[6, 11], 3, 1],
                 [[9, 0], 4, 13]]
    exits2 = [[5, 12], [8, 0]]
    hazards2 = [[0, 11]]
    size2 = 13
    start2 = [1, 9]

    graphtest2 = Graph(size2, obstacles2, exits2)
    graphtest2.graph_initialize()
    graphtest2.node_get_neighbors()
    graphtest2.node_set_d_exit()

    safetygrid2 = np.zeros([size2, size2], dtype=int)
    d_exitgrid2 = np.zeros([size2, size2], dtype=int)

    wave_tic = time.perf_counter()
    graphtest2.hazard_wavefront(hazards2)
    wave_toc = time.perf_counter()
    print(graphtest2.grid)

    node_count = len(graphtest2.nodes)
    print("Number of Nodes: " + str(node_count))

    print("Wavefront Timer: ")
    print(wave_toc - wave_tic)
    safe_tic = time.perf_counter()
    safest_shortest_path = graphtest2.safest_escape_path(start2)
    safe_toc = time.perf_counter()
    print("Safest Path A* Timer: ")
    print(safe_toc - safe_tic)
    safest_PL = len(safest_shortest_path)
    print("Safest Shortest Path:" + str(safest_PL))
    print(safest_shortest_path)
    star_tic = time.perf_counter()
    a_star_shortest_path = graphtest2.regular_a_star(start2)
    star_toc = time.perf_counter()
    print("Regular A* Timer: ")
    print(star_toc - star_tic)
    a_star_PL = len(a_star_shortest_path)
    print("A* Shortest Path:" + str(a_star_PL))
    print(a_star_shortest_path)
