
from queue import PriorityQueue


# Class that represents the Gameboard with entities and rules.
class GameBoard:
    X_MAX = 9
    Y_MAX = 9

    def __init__(self, k_x, k_y):
        """
        Initializes a new game board with the given 'K' position.
        Args:
            k_x (int): The x-coordinate of the 'K' position.
            k_y (int): The y-coordinate of the 'K' position.
        """
        self.K = (k_x, k_y)
        self.B = (float('inf'), float('inf'))
        self.danger_zones = {}

    def is_danger(self, move):
        """
        Checks if the given cell is a danger zone.
        Args:
            move (tuple[int][int]): The next move to make.
        Returns:
            bool: True if the cell is a danger zone, False otherwise.
        """
        x, y = move
        if (x, y) in self.danger_zones:
            return True
        return False

    def is_available(self, pos):
        """
        Checks if the given cell is available (not a danger zone and within bounds).
        Args:
            pos (tuple): The position of the cell as a tuple (x, y).
        Returns:
            bool: True if the cell is available, False otherwise.
        """
        x, y = pos
        if 0 <= x < 9 and 0 <= y < 9:
            if not self.is_danger(pos):
                return True
        return False


class BacktrackingEntity:
    def __init__(self, zone_size, k_x, k_y):
        """
            Initializes a new BacktrackingEntity with the given goal position and zone size.
        Args:
            zone_size (int): The size of the game board.
            k_x (int): The x-coordinate of the goal position.
            k_y (int): The y-coordinate of the goal position.
        """
        self.goal = (k_x, k_y)
        self.pos = (0, 0)
        self.zone_size = zone_size
        self.neighbours_priority = PriorityQueue()
        self.neighbours_priority.put(((self.heuristic(self.pos, self.goal), -self.heuristic(self.pos, (0, 0))), self.pos))
        self.path = []
        self.closed_set = set()
        self.parents = {(0, 0): 'init'}
        self.board = GameBoard(k_x, k_y)

    @staticmethod
    def heuristic(now, then):
        """
        Calculates the Manhattan distance heuristic between two positions.
        Args:
            now (tuple): The current position.
            then (tuple): The target position.
        Returns:
            int: The Manhattan distance between the two positions.
        """
        return abs(now[0] - then[0]) + abs(now[1] - then[1])

    @staticmethod
    def get_neighbors(pos):
        """
        Returns a list of neighboring positions to the given position.
        Args:
            pos (tuple): The position to get neighbors for.
        Returns:
            list: A list of neighboring positions.
        """
        x, y = pos
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def get_next_move(self):
        """
        Get the next neighbour move from the priority queue.
        Returns:
            list: The command and position.
        """
        self.backup()
        return self.neighbours_priority.get()

    def make_next_move(self, move):
        """
        Make the next move.
        Args:
            move (tuple): The next move to make.
        """
        current = move
        goal = self.goal
        if current not in self.closed_set:
            self.closed_set.add(current)
        neighbors = self.get_neighbors(current)

        self.neighbours_priority = PriorityQueue()
        for zone in neighbors:
            h = self.heuristic(zone, goal)
            if zone not in self.closed_set:
                if self.board.is_available(zone):
                    self.neighbours_priority.put(((h, -self.heuristic(zone, (0, 0))), zone))
                    self.parents[zone] = current

        self.pos = move

    def run(self, command):
        """
        Run the BacktrackingEntity with the given command.
        Args:
            command (list): The command to execute.
        Returns:
            list: The result of the command.
        """
        move = command[1]
        if move == self.goal:
            moves = self.reconstruct_the_path()
            return [['m', move], ['e', len(moves)]]

        else:
            return ['m', move]

    def backup(self):
        """
        Backing up to the position where we have possible moves or to the init.
        """
        while self.neighbours_priority.empty() and self.pos != 'init':
            move = self.parents[self.pos]
            if move == 'init':
                print('e', -1)
                exit(0)

            print('m', " ".join(map(str, [x for x in move])))

            for i in range(int(input())):
                unit = input()

            self.make_next_move(self.parents[self.pos])

    def reconstruct_the_path(self):
        """
        Reconstruct the path from the current position to the goal.
        Returns:
            list: The path from the current position to the goal.
        """
        path = []
        while self.pos != 'init':
            path.append(self.pos)
            self.pos = self.parents[self.pos]

        return path


# main
def main():
    n_zone_size = int(input())
    k_x, k_y = map(int, input().split())
    Neo = BacktrackingEntity(n_zone_size, k_x, k_y)
    move = Neo.get_next_move()

    # We are trying to reach the goal while we have possible moves
    while move != 'init':
        command = Neo.run(move)

        if command[1][0] == 'e':
            m = command[0]
            e = command[1]
            print(m[0], " ".join(map(str, [x for x in m[1]])))

            for i in range(int(input())):
                unit = input().split()
                zone = (int(unit[0]), int(unit[1]))
                if unit[2] in 'ASP':
                    if zone not in Neo.board.danger_zones:
                        Neo.board.danger_zones[zone] = unit[2]
                elif unit[2] == 'B':
                    Neo.board.B = zone
                else:
                    continue

            print(e[0], e[1])
            exit(0)

        else:
            print(command[0], " ".join(map(str, [x for x in command[1]])))

            for i in range(int(input())):
                unit = input().split()
                zone = (int(unit[0]), int(unit[1]))
                if unit[2] in 'ASP':
                    if zone not in Neo.board.danger_zones:
                        Neo.board.danger_zones[zone] = unit[2]
                elif unit[2] == 'B':
                    Neo.board.B = zone
                else:
                    continue

        Neo.make_next_move(move[1])
        move = Neo.get_next_move()
        if move == 'init':
            break

    print('e', '-1')


if __name__ == '__main__':
    main()