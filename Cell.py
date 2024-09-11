import pygame as py
COLORS: dict[str, tuple] = {
        'WHITE': (255, 255, 255),
        'BLUE': (27, 78, 207),
        'RED': (232, 57, 51),
        'GREEN': (60, 130, 63),
        'PURPLE': (202, 67, 230),
        'YELLOW': (130, 127, 60)
}
Empty, Up, Right, Down, Left = 0, 1, 2, 3, 4

class Cell():
    def __init__(self, CELL_SIZE: float, x: int, y: int, startX: int, startY: int, goalX: int, goalY: int,
                 margin_h: float, margin_v: float, wall_size:float, g: int = None, Path: bool = True,
                 Manhattan: bool = True, Euclidean: bool = False):
        self.CELL_SIZE = CELL_SIZE
        self.x, self.y = x, y
        self.goalX, self.goalY = goalX, goalY
        self.startX, self.startY = startX, startY
        self.g = float('inf') if g is None else g
        self.distance = abs(self.x-self.goalX) + abs(self.y-self.goalY) + self.g
        self.margin_h, self.margin_v = margin_h, margin_v
        self.wall_size = wall_size
        self.prevDirection = Empty

        self.Path = Path
        self.Manhattan = Manhattan
        self.Euclidean = Euclidean

    def get_position(self):
        return self.x, self.y
    def get_distance(self):
        return self.distance
    def calc_distance(self):
        res: float = 0
        if self.Path:
            res += self.g
        if self.Manhattan:
            res += abs(self.x-self.goalX) + abs(self.y-self.goalY)
        elif self.Euclidean:
            res += ((self.x-self.goalX)**2 + (self.y-self.goalY)**2)**0.5

        self.distance = res
    def set_g(self,g:int, direction: int):
        self.g = g
        self.prevDirection = direction
        self.calc_distance()
    def get_g(self):
        return self.g
    def get_prev_direction(self):
        return self.prevDirection
    def is_goal(self):
        return self.x == self.goalX and self.y == self.goalY
    def __lt__(self, other):
        return (self.x - other.x) < 0 or (self.y - other.y) < 0
    def draw_cell(self, SCREEN, cellType: str = 'EXPLORED'):
        color = COLORS['YELLOW']
        if self.x == self.goalX and self.y == self.goalY:
            color = COLORS['RED']
        if self.x == self.startX and self.y == self.startY:
            color = COLORS['BLUE']
        elif cellType == 'SOLVED':
            color = COLORS['GREEN']
        py.draw.rect(SCREEN, color, py.Rect(self.margin_h + self.wall_size + self.x * self.CELL_SIZE,
                                            self.margin_v + self.wall_size + self.y * self.CELL_SIZE,
                                            self.CELL_SIZE - self.wall_size*2, self.CELL_SIZE - self.wall_size*2
                                            ))

    def set_path(self, b: bool = None):
        self.Path = b if b is not None else not b
        self.calc_distance()

    def set_manhattan(self, b: bool = None):
        self.Manhattan = b if b is not None else not b
        self.calc_distance()

    def set_euclidean(self, b: bool = None):
        self.Euclidean = b if b is not None else not b
        self.calc_distance()
