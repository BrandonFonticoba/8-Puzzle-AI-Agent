""" Brandon Fonticoba
    October 2019
    AI - Dr. Burns
    8 Puzzle
"""
from queue import PriorityQueue
import copy
import time


class Puzzle():
    """A sliding-block puzzle."""

    def __init__(self, grid):
        """Instances differ by their number configurations."""
        self.grid = copy.deepcopy(grid) # No aliasing!
        self.g = 0

    def __lt__(self, other):
        return other.h(other) < self.h(self)

    def display(self):
        """Print the puzzle."""
        for row in self.grid:
            for number in row:
                print(number, end='')
            print()
        print()

    def moves(self):
        """Return a list of possible moves given the current configuration."""

        move_list = []
        row = 0
        column = 0

        # Finding the empty spot in the current puzzle instance.
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    row = i
                    column = j
                    break
            else:
                continue
            break

        # Given empty spot, checks which moves are valid.
        if column - 1 >= 0:
            move_list.append('W')

        if column + 1 <= 2:
            move_list.append('E')

        if row - 1 >= 0:
            move_list.append('N')

        if row + 1 <= 2:
            move_list.append('S')

        return move_list

    def neighbor(self, move):
        """Return a Puzzle instance like this one but with one move made."""

        row = 0
        column = 0

        # Finding the empty spot in the current puzzle instance.
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == ' ':
                    row = i
                    column = j
                    break
            else:
                continue
            break

        temp = 0

        # Creating a new puzzle instance with the depth g value + 1 from the previous puzzle instance.
        new_puzzle = self.grid
        new_depth = self.g + 1
        return_puzzle = Puzzle(new_puzzle)
        return_puzzle.g = new_depth

        # Move position in puzzle once to the east. Swapping the value to the east with the empty spot.
        if move == 'E':
            temp = return_puzzle.grid[row][column + 1]
            return_puzzle.grid[row][column + 1] = ' '
            return_puzzle.grid[row][column] = temp
            return return_puzzle

        # Move position in puzzle once to the west. Swapping the value to the west with the empty spot.
        if move == 'W':
            temp = return_puzzle.grid[row][column - 1]
            return_puzzle.grid[row][column - 1] = ' '
            return_puzzle.grid[row][column] = temp
            return return_puzzle

        # Move position in puzzle once to the north. Swapping the value to the north with the empty spot.
        if move == 'N':
            temp = return_puzzle.grid[row - 1][column]
            return_puzzle.grid[row - 1][column] = ' '
            return_puzzle.grid[row][column] = temp
            return return_puzzle

        # Move position in puzzle once to the south. Swapping the value to the south with the empty spot.
        if move == 'S':
            temp = return_puzzle.grid[row + 1][column]
            return_puzzle.grid[row + 1][column] = ' '
            return_puzzle.grid[row][column] = temp
            return return_puzzle

    def h(self, goal):
        """Compute the distance heuristic from this instance to the goal."""
        distance = 0
        for i in range(3):
            for j in range(3):
                if goal.grid[i][j] != ' ':
                    value = goal.grid[i][j]
                    index = (i, j)
                    for k in range(3):
                        for l in range(3):
                            if self.grid[k][l] == value:
                                distance += abs(index[0] - k) + abs(index[1] - l)
                                break
                        else:
                            continue
                        break

        return distance + self.g

    """ This function assumes that the goal is always [[' ', 1, 2], [3, 4, 5], [6, 7, 8]]
    
    def h(self, current):
        # Compute the distance heuristic from this instance to the goal.
        
        distance = 0
        for i in range(3):
            for j in range(3):
                if current.grid[i][j] != ' ':
                    x, y = divmod(current.grid[i][j], 3)
                    distance += abs(x - i) + abs(y - j)
        return distance + current.g
        
        """


class Node():
    """Node Object that contains grid layout, the move made to get there, and the previous Node."""

    def __init__(self, position, prev_move, prev_node):
        """Instances differ by their current agent locations."""
        self.position = position
        self.prev_move = prev_move
        self.prev_node = prev_node

class Agent():
    """Knows how to solve a sliding-block puzzle with A* search."""

    def astar(self, puzzle, goal):
        """Return a list of moves to get the puzzle to match the goal."""

        # Node objects for each position visited in puzzle.
        nodes = {}

        # Instance of start position Node.
        start_node = Node(puzzle.grid, '', (puzzle.grid, ''))
        nodes.update({str(puzzle.grid): start_node})

        # List of visited grid layouts.
        searched = []

        # Return list of moves to get to the goal.
        path_list = []

        # Frontier to manage different puzzle instances.
        frontier = PriorityQueue()
        frontier.put((puzzle.h(goal), puzzle))
        searched.append(puzzle.grid)
        current_puzzle = None

        # Goal Node
        end = None

        # A* Loop.
        while not frontier.empty():
            current_puzzle = frontier.get()
            current = current_puzzle[1]
            if current.grid == goal.grid:
                break
            searched.append(current.grid)
            for move in current.moves():
                previous_move = move
                path_node = Node((), '', ())
                neighbor = current.neighbor(move)
                if neighbor.grid not in searched and is_in_q(neighbor.grid, frontier) is False:
                    path_node.position = neighbor.grid
                    path_node.prev_move = move
                    path_node.prev_node = (current.grid, previous_move)
                    if path_node.position == goal.grid:
                        end = path_node
                    nodes.update({str(neighbor.grid): path_node})
                    frontier.put((neighbor.h(goal), neighbor))

        # Tracing back from the goal Node to the start Node and getting the previous move each time.
        while end.prev_move != '':
            path_list.insert(0, end.prev_move)
            prev = str(end.prev_node[0])
            end = nodes[prev]

        return path_list


def is_in_q(x, q):
    """Checks if a certain element is present in a given queue."""

    q_list = q.queue
    for xs in q_list:
        if x == xs[1]:
            return True
    return False


def main():
    """Create a puzzle, solve it with A*, and console-animate."""

    puzzle = Puzzle([[8, ' ', 6], [5, 4, 7], [2, 3, 1]])
    puzzle.display()
    agent = Agent()
    goal = Puzzle([[' ', 1, 2], [3, 4, 5], [6, 7, 8]])
    path = agent.astar(puzzle, goal)

    while path:
        move = path.pop(0)
        puzzle = puzzle.neighbor(move)
        time.sleep(.2)
        puzzle.display()


if __name__ == '__main__':
    main()