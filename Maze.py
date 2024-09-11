import pygame as py
import random
from Cell import Cell, COLORS, Empty, Up, Down, Right, Left
from queue import PriorityQueue

TYPES_OF_MAZES = ['ORIGIN SIFT', 'DFS']

class Maze():
    def __init__(self, WIDTH: int, HEIGHT: int, WALL_SIZE: int, MARGIN: int, CELL_NUM_H: int, CELL_NUM_V: int, TYPE: str,
                 Path: bool, Manhattan: bool, Euclidean: bool):
        self.WALL_SIZE = WALL_SIZE
        self.MARGIN = MARGIN
        self.CELL_NUM_H = CELL_NUM_H
        self.CELL_NUM_V = CELL_NUM_V

        CellSizeH = (WIDTH - 2 * self.MARGIN) / CELL_NUM_H
        CellSizeV = (HEIGHT - 2 * self.MARGIN) / CELL_NUM_V

        self.CELL_SIZE = min(CellSizeH,CellSizeV)
        self.MARGIN_H = (WIDTH - (self.CELL_NUM_H * self.CELL_SIZE)) / 2
        self.MARGIN_V = (HEIGHT - (self.CELL_NUM_V * self.CELL_SIZE)) / 2

        '''CORNERS'''
        self.LeftUpCornerX = self.MARGIN_H
        self.LeftDownCornerX = self.MARGIN_H
        self.LeftUpCornerY = self.MARGIN_V
        self.LeftDownCornerY = HEIGHT - self.MARGIN_V

        self.RightUpCornerX = WIDTH - self.MARGIN_H
        self.RightDownCornerX = WIDTH - self.MARGIN_H
        self.RightUpCornerY = self.MARGIN_V
        self.RightDownCornerY = HEIGHT - self.MARGIN_V


        '''SOLVER'''
        self.PosibleJumps: list = []
        self.START_X = self.START_Y = 0
        self.EXPLORE_X = self.EXPLORE_Y = 0
        self.GOAL_X = (self.CELL_NUM_H - 1)
        self.GOAL_Y = (self.CELL_NUM_V - 1)
        self.CHANGE_MAZE_X = self.START_X;  self.CHANGE_MAZE_Y = self.START_X

        self.Path: bool = Path
        self.Manhattan: bool = Manhattan
        self.Euclidean: bool = Euclidean

        self.ExploredCells: int = 0
        self.SolutionLength: int = 0
        self.TimeSolving: float = 0

        '''CELL LIST AND PRIORITY QUEUE'''
        self.explored_cells: list[Cell] = []
        self.BEST_PATH = PriorityQueue()
        self.MAZE_EXPLORED: list[list[Cell]] = []
        self.reset_solve_maze()

        self.MAZE: list[list[int]] = []
        '''START PERFECT MAZE'''
        self.TYPE = TYPE
        if self.TYPE == 'ORIGIN SIFT':
            self.set_maze_origin_sift()
        elif self.TYPE == 'DFS':
            self.set_maze_dfs()

    def regenerate_maze(self):
        if self.TYPE == 'ORIGIN SIFT':
            self.set_maze_origin_sift()
        elif self.TYPE == 'DFS':
            self.set_maze_dfs()
    def set_empty_maze(self):
        self.MAZE = []
        for j in range(self.CELL_NUM_V):
            self.MAZE.append([])
            for i in range(self.CELL_NUM_H):
                self.MAZE[j].append(Empty)
    def set_maze_origin_sift(self):
        self.set_empty_maze()
        self.reset_solve_maze()
        print('Starting origin sift maze...')
        for i in range(len(self.MAZE)):
            for j in range(len(self.MAZE[0])):
                if j < self.CELL_NUM_H - 1:
                    self.MAZE[i][j] = Right
                elif i < self.CELL_NUM_H - 1:
                    self.MAZE[i][j] = Down
                else:
                    self.MAZE[i][j] = Empty
        for _ in range(50 * self.CELL_NUM_V * self.CELL_NUM_H):
            self.change_maze()

    def set_maze_dfs(self):
        self.set_empty_maze()
        self.reset_solve_maze()
        print('Starting dfs maze...')
        VISITED_MAZE: list[list[bool]] = []
        for j in range(self.CELL_NUM_V):
            VISITED_MAZE.append([])
            for i in range(self.CELL_NUM_H):
                VISITED_MAZE[j].append(False)

        notVisited: list = [(self.START_X, self.START_Y)]

        while len(notVisited) > 0:
            x, y = notVisited.pop(0)
            VISITED_MAZE[y][x] = True
            self.PosibleJumps = []
            if x - 1 >= 0 and self.MAZE[y][x - 1] != Right and not VISITED_MAZE[y][x - 1]:
                self.PosibleJumps.append(Left)
                aux: tuple = (x - 1,y)
                if aux not in notVisited:
                    notVisited.append(aux)
            if x + 1 < self.CELL_NUM_H and self.MAZE[y][x + 1] != Left and not VISITED_MAZE[y][x + 1]:
                self.PosibleJumps.append(Right)
                aux = (x + 1, y)
                if aux not in notVisited:
                    notVisited.append(aux)
            if y - 1 >= 0 and self.MAZE[y - 1][x] != Down and not VISITED_MAZE[y - 1][x]:
                self.PosibleJumps.append(Up)
                aux = (x, y - 1)
                if aux not in notVisited:
                    notVisited.append(aux)
            if y + 1 < self.CELL_NUM_V and self.MAZE[y + 1][x] != Up and not VISITED_MAZE[y + 1][x]:
                self.PosibleJumps.append(Down)
                aux = (x,y + 1)
                if aux not in notVisited:
                    notVisited.append(aux)

            NEXT_DIR: int = Empty
            if len(self.PosibleJumps) > 0:
                NEXT_DIR = random.choice(self.PosibleJumps)
            self.MAZE[y][x] = NEXT_DIR

        # for _ in range(self.CELL_NUM_V * self.CELL_NUM_H):
            # self.change_maze()
    def draw_maze(self, SCREEN):
        # Wall UP
        py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.LeftUpCornerX, self.LeftUpCornerY,
                                                      self.CELL_SIZE * self.CELL_NUM_H, self.WALL_SIZE))
        # Wall DOWN
        py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.LeftDownCornerX, self.LeftDownCornerY,
                                                      self.CELL_SIZE * self.CELL_NUM_H, self.WALL_SIZE))
        # Wall LEFT
        py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.LeftUpCornerX, self.LeftUpCornerY,
                                                      self.WALL_SIZE, self.CELL_SIZE * self.CELL_NUM_V))
        # Wall RIGHT
        py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.RightUpCornerX, self.RightUpCornerY,
                                                      self.WALL_SIZE, self.CELL_SIZE * self.CELL_NUM_V))

        for i in range(len(self.MAZE)):
            for j in range(len(self.MAZE[i])):
                if (j - 1 >= 0) and (self.MAZE[i][j - 1] != Right) and (self.MAZE[i][j] != Left):
                    py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.MARGIN_H + j * self.CELL_SIZE,
                                                                  self.MARGIN_V + i * self.CELL_SIZE,
                                                                  self.WALL_SIZE, self.CELL_SIZE
                                                                  ))
                if (i - 1 >= 0) and (self.MAZE[i - 1][j] != Down) and (self.MAZE[i][j] != Up):
                    py.draw.rect(SCREEN, COLORS['WHITE'], py.Rect(self.MARGIN_H + j * self.CELL_SIZE,
                                                                  self.MARGIN_V + i * self.CELL_SIZE,
                                                                  self.CELL_SIZE, self.WALL_SIZE
                                                                  ))

        '''SOLVER'''
        self.ExploredCells = len(self.explored_cells)
        for cell in self.explored_cells:
            cell.draw_cell(SCREEN)


        self.MAZE_EXPLORED[self.GOAL_Y][self.GOAL_X].draw_cell(SCREEN)
        self.MAZE_EXPLORED[self.START_Y][self.START_X].draw_cell(SCREEN)
        self.SolutionLength = 0
        if self.BEST_PATH.empty(): return

        distance, objective_cell = self.BEST_PATH.get()
        self.BEST_PATH.put((distance, objective_cell))

        while objective_cell.get_prev_direction != Empty:
            objective_cell.draw_cell(SCREEN, 'SOLVED')
            self.SolutionLength += 1

            direction: int = objective_cell.get_prev_direction()
            x, y = objective_cell.get_position()

            if direction == Up:
                objective_cell = self.MAZE_EXPLORED[y - 1][x]
            elif direction == Down:
                objective_cell = self.MAZE_EXPLORED[y + 1][x]
            elif direction == Left:
                objective_cell = self.MAZE_EXPLORED[y][x - 1]
            elif direction == Right:
                objective_cell = self.MAZE_EXPLORED[y][x + 1]
            else:
                break
        self.MAZE_EXPLORED[self.GOAL_Y][self.GOAL_X].draw_cell(SCREEN)
        self.MAZE_EXPLORED[self.START_Y][self.START_X].draw_cell(SCREEN)

    def change_maze(self):
        self.PosibleJumps = []

        if self.CHANGE_MAZE_X - 1 >= 0:
            self.PosibleJumps.append(Left)
        if self.CHANGE_MAZE_X + 1 < self.CELL_NUM_H:
            self.PosibleJumps.append(Right)
        if self.CHANGE_MAZE_Y - 1 >= 0:
            self.PosibleJumps.append(Up)
        if self.CHANGE_MAZE_Y + 1 < self.CELL_NUM_V:
            self.PosibleJumps.append(Down)

        if len(self.PosibleJumps) > 0:
            NEXT_DIR: int = random.choice(self.PosibleJumps)
        else: NEXT_DIR = Empty

        self.MAZE[self.CHANGE_MAZE_Y][self.CHANGE_MAZE_X] = NEXT_DIR
        if NEXT_DIR == Up:
            self.CHANGE_MAZE_Y -= 1
        if NEXT_DIR == Down:
            self.CHANGE_MAZE_Y += 1
        if NEXT_DIR == Left:
            self.CHANGE_MAZE_X -= 1
        if NEXT_DIR == Right:
            self.CHANGE_MAZE_X += 1
        self.MAZE[self.CHANGE_MAZE_Y][self.CHANGE_MAZE_X] = Empty

    def reset_solve_maze(self):
        self.reset_time_solving()
        self.EXPLORE_X = self.START_X
        self.EXPLORE_Y = self.START_Y
        self.BEST_PATH = PriorityQueue()
        self.explored_cells = []
        self.MAZE_EXPLORED: list[list[Cell]] = []
        for j in range(self.CELL_NUM_V):
            self.MAZE_EXPLORED.append([])
            for i in range(self.CELL_NUM_H):
                aux: Cell = Cell(self.CELL_SIZE, i, j,
                                 self.START_X, self.START_X,
                                 self.GOAL_X, self.GOAL_Y,
                                 self.MARGIN_H, self.MARGIN_V,
                                 self.WALL_SIZE, Path=self.Path,
                                 Manhattan=self.Manhattan, Euclidean=self.Euclidean
                                 )
                if j == 0 and i == 0: aux.set_g(0, Empty)
                self.MAZE_EXPLORED[j].append(aux)
    def set_to_solve_maze_a_star(self):
        self.reset_solve_maze()
        start_cell: Cell = Cell(self.CELL_SIZE,
                                self.EXPLORE_X, self.EXPLORE_Y,
                                self.START_X, self.START_X,
                                self.GOAL_X, self.GOAL_Y,
                                self.MARGIN_H, self.MARGIN_V, self.WALL_SIZE, 0)
        self.BEST_PATH.put((start_cell.distance, start_cell))

    def step_solve_maze_a_star(self):
        # To finish searching
        if self.BEST_PATH.empty():
            goalCell = self.MAZE_EXPLORED[self.GOAL_Y][self.GOAL_X]
            self.BEST_PATH.put((goalCell.distance,goalCell))
            return True
        distance, best_cell = self.BEST_PATH.get()
        if best_cell.is_goal():
            goalCell = self.MAZE_EXPLORED[self.GOAL_Y][self.GOAL_X]
            self.BEST_PATH.put((goalCell.distance, goalCell))
            return True
        cellX, cellY = best_cell.get_position()

        '''⬅️'''
        if cellX - 1 >= 0 and (self.MAZE[cellY][cellX - 1] == Right or self.MAZE[cellY][cellX] == Left):
            aux: Cell = self.MAZE_EXPLORED[cellY][cellX - 1]
            if aux.get_g() > best_cell.get_g():
                aux.set_g(best_cell.get_g() + 1, Right)
                self.BEST_PATH.put((aux.get_distance(),aux))
                self.explored_cells.append(aux)

        '''➡️'''
        if cellX + 1 < self.CELL_NUM_H and (self.MAZE[cellY][cellX + 1] == Left or self.MAZE[cellY][cellX] == Right):
            aux: Cell = self.MAZE_EXPLORED[cellY][cellX + 1]
            if aux.get_g() > best_cell.get_g():
                aux.set_g(best_cell.get_g() + 1, Left)
                self.BEST_PATH.put((aux.get_distance(), aux))
                self.explored_cells.append(aux)

        '''⬆️'''
        if cellY - 1 >= 0 and (self.MAZE[cellY - 1][cellX] == Down or self.MAZE[cellY][cellX] == Up):
            aux: Cell = self.MAZE_EXPLORED[cellY - 1][cellX]
            if aux.get_g() > best_cell.get_g():
                aux.set_g(best_cell.get_g() + 1, Down)
                self.BEST_PATH.put((aux.get_distance(), aux))
                self.explored_cells.append(aux)

        '''⬇️'''
        if cellY + 1 < self.CELL_NUM_V and (self.MAZE[cellY + 1][cellX] == Up or self.MAZE[cellY][cellX] == Down):
            aux: Cell = self.MAZE_EXPLORED[cellY + 1][cellX]
            if aux.get_g() > best_cell.get_g():
                aux.set_g(best_cell.get_g() + 1, Up)
                self.BEST_PATH.put((aux.get_distance(), aux))
                self.explored_cells.append(aux)

        # To keep searching
        return False

    def set_path(self, b: bool = None):
        self.Path = b if b is not None else not self.Path
        self.reset_solve_maze()

    def set_manhattan(self, b: bool = None):
        self.Manhattan = b if b is not None else not self.Manhattan
        self.reset_solve_maze()

    def set_euclidean(self, b: bool = None):
        self.Euclidean = b if b is not None else not self.Euclidean
        self.reset_solve_maze()
    def get_explored_cells(self):
        return self.ExploredCells
    def get_solution_length(self):
        return self.SolutionLength
    def get_time_solving(self):
        return self.TimeSolving
    def add_time_solving(self, deltaTime: float):
        self.TimeSolving += deltaTime
    def reset_time_solving(self):
        self.TimeSolving = 0
    def set_type_of_maze(self, type: str):
        self.TYPE = type