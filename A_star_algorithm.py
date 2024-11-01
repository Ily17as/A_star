
from queue import PriorityQueue


# Class that represents the Gameboard with entities and rules.
class GameBoard:
    # The maximum x/y-coordinate of the game board.
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

    def is_danger(self, x, y):
        """
        Checks if the given cell is a danger zone.
        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        Returns:
            bool: True if the cell is a danger zone, False otherwise.
        """
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
            if not self.is_danger(x, y):
                return True
        return False


# Class that represents the A* algorithm entity (Neo).
class AStarEntity:
    def __init__(self, zone_size, k_x, k_y):
        """
        Initializes a new AStarEntity with the given goal position and zone size.
        Args:
            zone_size (int): The size of the game board.
            k_x (int): The x-coordinate of the keymaker position.
            k_y (int): The y-coordinate of the keymaker position.
        """
        self.goal = (k_x, k_y)
        self.pos = (0, 0)
        self.zone_size = zone_size
        self.poss_queue = PriorityQueue()
        self.poss_queue.put(((0, self.heuristic(self.pos, self.goal)), self.pos))
        self.closed_set = set()
        self.parents = {(0, 0): 'init'}
        self.g_score = {(0, 0): 0}
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
        Returns the next move in the priority queue.
        Returns:
            list: The next move as a list [cost, position (tuple)].
        """
        return self.poss_queue.get()

    def make_next_move(self, move):
        """
        Makes the next move and updates the entity's state.
        Args:
            move (tuple[int][int]): The next move to make.
        """
        # Storing the info about the move
        current = move
        goal = self.goal
        self.closed_set.add(current)
        neighbors = self.get_neighbors(current)

        # Adding its neighbours to the priority queue
        for zone in neighbors:
            h = self.heuristic(zone, goal)
            if zone not in self.closed_set:
                if self.board.is_available(zone):
                    if zone in self.g_score:
                        self.g_score[zone] = min(self.g_score[current] + 1, self.g_score[zone])
                    else:
                        self.g_score[zone] = self.g_score[current] + 1
                    g = self.g_score[zone]
                    self.poss_queue.put(((g + h, h), zone))

                    self.parents[zone] = current

        # Updating the entity's position
        self.pos = move

    def run(self, command):
        """
        Executes a command and returns the result.
        Args:
            command (list): A list containing the command and its arguments.
        Returns:
            list: A list containing the result of the command and its cost.
        """
        move = command[1]
        if move == self.goal:
            return [['m', move], ['e', self.g_score[self.goal]]]

        else:
            return ['m', move]

    def get_to_next_move(self, move):
        """
        Reconstructs the path from the start position to the goal position.
        Returns:
            list: A list containing the path from the start position to the goal position.
        """
        # Stepping back before we reach the right cell
        while self.heuristic(self.pos, move) > 1:
            self.pos = self.parents[self.pos]

            # If we reach the init position, we need to go out of the loop and go other direction
            if self.pos == 'init':
                break
            print('m', " ".join(map(str, [x for x in self.pos])))

            for i in range(int(input())):
                unit = input()

        # Going in other direction
        if self.pos == 'init':
            self.pos = (0, 0)
            path = []
            # Reconstructing the path
            while self.pos != move:
                move = self.parents[move]
                path.append(move)

            path.pop()
            path.reverse()

            # Moving to the right cell
            for m in path:
                print('m', " ".join(map(str, [x for x in m])))

                for i in range(int(input())):
                    unit = input()


def main():
    """
    Runs the A* algorithm on a game board and prints the result.
    Args:
        None
    """
    n_zone_size = int(input())
    k_x, k_y = map(int, input().split())
    Neo = AStarEntity(n_zone_size, k_x, k_y)

    # We are searching while we have moves to do
    while Neo.poss_queue.empty() is False:
        move = Neo.get_next_move()
        Neo.get_to_next_move(move[1])

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

    print('e', '-1')


if __name__ == '__main__':
    main()