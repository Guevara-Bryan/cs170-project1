import heapq
import csv 
import math
import time
import os


class Board:
    def __init__(self, sequence):
        self.tiles = list(sequence)

    def move_tile_up(self, tile):
        i = tile

        if i <= 2: return False # Tile is on the top-most row
        
        if self.tiles[i - 3] == "*":
            self.tiles[i], self.tiles[i - 3] = self.tiles[i - 3], self.tiles[i]
            return True
        return False # Tile is not empty

    def move_tile_down(self, tile):
        i = tile

        if i >= 6: return False # Tile is on the bottom-most row

        if self.tiles[i + 3] == "*": 
            self.tiles[i], self.tiles[i + 3] = self.tiles[i + 3], self.tiles[i]
            return True
        return False

    def move_tile_left(self, tile):
        i = tile

        if i in [0, 3, 6]: return False # Tile is on the left-most column

        if self.tiles[i - 1] == "*":
            self.tiles[i], self.tiles[i - 1] = self.tiles[i - 1], self.tiles[i]
            return True
        return False

    def move_tile_right(self, tile):
        i = tile

        if i in [2, 5, 8]: return False # Tile is on the right-most column

        if self.tiles[i + 1] == "*":
            self.tiles[i], self.tiles[i + 1] = self.tiles[i + 1], self.tiles[i]
            return True
        return False

    def get_sequence(self):
        return "".join(self.tiles)

    def get_possible_moves(self):
        i = self.tiles.index("*")

        if i == 0:
            moves = []
            self.move_tile_up(3)
            moves.append(self.get_sequence())
            self.move_tile_down(0)

            self.move_tile_left(1)
            moves.append(self.get_sequence())
            self.move_tile_right(0)

            return moves

        elif i == 1:
            moves = []
            self.move_tile_right(0)
            moves.append(self.get_sequence())
            self.move_tile_left(1)

            self.move_tile_left(2)
            moves.append(self.get_sequence())
            self.move_tile_right(1)

            self.move_tile_up(4)
            moves.append(self.get_sequence())
            self.move_tile_down(1)

            return moves

        elif i == 2:
            moves = [] 
            self.move_tile_right(1)
            moves.append(self.get_sequence())
            self.move_tile_left(2)

            self.move_tile_up(5)
            moves.append(self.get_sequence())
            self.move_tile_down(2)

            return moves
        elif i == 3:
            moves = []
            self.move_tile_down(0)
            moves.append(self.get_sequence())
            self.move_tile_up(3)

            self.move_tile_left(4)
            moves.append(self.get_sequence())
            self.move_tile_right(3)

            self.move_tile_up(6)
            moves.append(self.get_sequence())
            self.move_tile_down(3)

            return moves

        elif i == 4:
            moves = []
            self.move_tile_down(1)
            moves.append(self.get_sequence())
            self.move_tile_up(4)

            self.move_tile_left(5)
            moves.append(self.get_sequence())
            self.move_tile_right(4)

            self.move_tile_right(3)
            moves.append(self.get_sequence())
            self.move_tile_left(4)

            self.move_tile_up(7)
            moves.append(self.get_sequence())
            self.move_tile_down(4)

            return moves

        elif i == 5:
            moves = []
            self.move_tile_down(2)
            moves.append(self.get_sequence())
            self.move_tile_up(5)

            self.move_tile_right(4)
            moves.append(self.get_sequence())
            self.move_tile_left(5)

            self.move_tile_up(8)
            moves.append(self.get_sequence())
            self.move_tile_down(5)

            return moves

        elif i == 6:
            moves = []
            self.move_tile_down(3)
            moves.append(self.get_sequence())
            self.move_tile_up(6)

            self.move_tile_left(7)
            moves.append(self.get_sequence())
            self.move_tile_right(6)

            return moves

        elif i == 7:
            moves = []
            self.move_tile_down(4)
            moves.append(self.get_sequence())
            self.move_tile_up(7)

            self.move_tile_left(8)
            moves.append(self.get_sequence())
            self.move_tile_right(7)

            self.move_tile_right(6)
            moves.append(self.get_sequence())
            self.move_tile_left(7)

            return moves

        elif i == 8:
            moves = []
            self.move_tile_down(5)
            moves.append(self.get_sequence())
            self.move_tile_up(8)

            self.move_tile_right(7)
            moves.append(self.get_sequence())
            self.move_tile_left(8)

            return moves


    def __str__(self):
        s = "+-----------+\n"
        s += "| " + " | ".join(self.tiles[0:3]) + " |\n";
        s += "+---+---+---+\n"
        s += "| " + " | ".join(self.tiles[3:6]) + " |\n";
        s += "+---+---+---+\n"
        s += "| " + " | ".join(self.tiles[6:9]) + " |\n";
        s += "+-----------+\n"
        return s;

            
class node:
    def __init__(self, cost, sequence, parent, depth):
        self.sequence = sequence
        self.parent = parent
        self.cost = cost
        self.depth = depth

    # To make it compatible with the priority queue
    def __lt__(self, other):
        return self.cost < other.cost



class Problem:
    def __init__(self, initial_state, final_state, heuristic, print_trace):
        self.initial_state = initial_state
        self.final_state = final_state
        self.heuristic = heuristic
        self.print_trace = print_trace

    def backtrace(self, node):
        current = node
        moves = []
        while(current.parent != None):
            moves.append(current.sequence)
            current = current.parent

        moves.append(current.sequence)
        moves.reverse()
        return moves


    def graph_search(self):
        root_node_cost = 0 + self.heuristic(self.initial_state, self.final_state)
        initial_depth = 0
        frontier = [node(root_node_cost, self.initial_state, None, initial_depth)]
        heapq.heapify(frontier)
        max_size_of_queue = 0
        total_nodes_expanded = 0
        explored = set()

        while(len(frontier) > 0):
            leaf_node = heapq.heappop(frontier)
            leaf = Board(leaf_node.sequence)
            h = self.heuristic(leaf_node.sequence, self.final_state)

            if len(frontier) > max_size_of_queue:
                max_size_of_queue = len(frontier)
            total_nodes_expanded += 1

            if self.print_trace:
                print(f"The best node to expand with g(n) = {leaf_node.cost - h} and h(n) = {h} is:\n{leaf}")
                print("Expanding this node...")

            if leaf.get_sequence() == self.final_state:
                if self.print_trace:
                    print("========== SOLUTION FOUND ==========")
                print(f"max size of qeueue: .......... {max_size_of_queue}\ntotal nodes expanded: .......... {total_nodes_expanded}\ndepth of solution node: .......... {leaf_node.depth}")
                return self.backtrace(leaf_node)
            
            for i in leaf.get_possible_moves():
                if i not in explored:
                    heapq.heappush(frontier, node(leaf_node.cost + 1 + h, i, leaf_node, leaf_node.depth + 1))
                    explored.add(i)
        return False
    

# gets the distance between two indexes in the board
def get_distance(a, b):
    return math.floor(math.sqrt((math.floor(b / 3) - math.floor(a / 3))**2 + ((b % 3) - (a % 3))**2))


# Euclidean distance Heuristic
def euclidean_distance_heuristic(sequence, final_state):
    num = 0

    for i in range(len(final_state)):
        if sequence[i] != final_state[i]:
            correct = final_state.index(sequence[i])
            num += get_distance(i, correct)


    return num

def misplaced_tiles_heuristic(sequence, final_state):
    num = 0

    for i in range(len(final_state)):
        if sequence[i] != final_state[i]:
            num += 1

    return num

def uniform_cost_heuristic(sequence, final_state):
    return 0

def run_single_board_heuristic(path, sequence, heuristic, final_state, print_trace=True):
    if not os.path.exists(path):
        os.makedirs(path)

    game = Problem(sequence, final_state, heuristic[1], print_trace)
    start = time.time()
    result = game.graph_search()
    duration = time.time() - start
    if result:
        with open(f"{path}/{heuristic[0]}_trace.txt", "w") as tfile:
            tfile.write("solution found\n")
            tfile.write("======================== BACK TRACE ========================\n")
            for i in range(len(result)):
                s = Board(result[i])
                tfile.write(f"Step #{i}\n{s}")
    else:
        print("NO SOLUTION FOUND")

    print(f"Time to compute: .......... {round(duration, 5)} seconds")
    print(f"Trace written to {path}/{heuristic[0]}_trace.txt")
    print("--------------------------------")



if __name__ == '__main__':
    parent_path = os.getcwd()
    default = "123*45678"
    final_state = "12345678*"
    while True:
        print("================================ 8 Puzzle Solver =====================================")
        sequence = input("Leave empty to continue with default\nPlease enter the starting sequence (use \"*\" for the empty cell): ")
        if len(sequence) == 0:
            print("Nothing entered. Continuing with default")
            sequence = default
        elif len(sequence) > 0 and (len(sequence) < 9 or len(sequence) > 9):
            print("INVALID SIZE OF SEQUENCE\nPlease enter a sequence of 9 characters")
            continue

        temp = Board(sequence)
        print(f"Starting Sequence Saved\n{temp}")


        print("Please select an option:\n1) Run the default demo\n2) Run the uniform cost search algorithm\n3) Run the Misplaced Tiles Heuristic\n4) Run the Euclidean Distance heuristic\n5) Quit")
        selection = input("Enter your option: ")

        if selection.isnumeric():
            selection = int(selection)
        else:
            print("PLEASE ENTER NUMBERS ONLY\n")
            continue


        if selection == 1:
            with open("test_cases.csv", newline='') as tfile:
                reader = csv.reader(tfile)
                for entry in reader:
                    print(f"=============================== Computing Soulution for Test Case: {entry[0].upper()} =================================")
                    temp = Board(entry[1])
                    print(temp)
                    print(f"\n----------- Comuting solution with UNIFORM COST SEARCH -----------------")
                    run_single_board_heuristic(f"{parent_path}/traces/uniform", entry[1], [entry[0], uniform_cost_heuristic], final_state, False)
                    print(f"\n----------- Comuting solution with MISPLACED TILES HEURISTIC -----------------")
                    run_single_board_heuristic(f"{parent_path}/traces/misplaced", entry[1], [entry[0], misplaced_tiles_heuristic], final_state, False)
                    print(f"\n----------- Comuting solution with EUCLIDEAN DISTANCE HEURISTIC -----------------")
                    run_single_board_heuristic(f"{parent_path}/traces/euclidean", entry[1], [entry[0], euclidean_distance_heuristic], final_state, False)

        elif selection == 2:
            print(f"\n============================= Computing solution using UNIFORM COST SEARCH ===================================")
            temp = Board(sequence)
            print(temp)
            run_single_board_heuristic(f"{parent_path}/traces/uniform", sequence, ["UNIFORM COST SEARCH", uniform_cost_heuristic], final_state)
        elif selection == 3:
            print(f"\n============================= Computing solution using MISPLACED TILES HEURISTIC ===================================")
            temp = Board(sequence)
            print(temp)
            run_single_board_heuristic(f"{parent_path}/traces/misplaced", sequence, ["MISPLACED TILES HEURISTIC", misplaced_tiles_heuristic], final_state)
        elif selection == 4:
            print(f"\n============================= Computing solution using EUCLIDEAN DISTANCE HEURISTIC ===================================")
            temp = Board(sequence)
            print(temp)
            run_single_board_heuristic(f"{parent_path}/traces/euclidean", sequence, ["EUCLIDEAN DISTANCE HEURISTIC", euclidean_distance_heuristic], final_state)
        elif selection == 5:
            print("Thanks for using the 8 Puzzle Solver")
            break
        else: 
            print("PLEASE ENTER A VALID OPTION\n")
            continue

    