import pygame as py
from Maze import Maze, TYPES_OF_MAZES
from Text import Text


def main():
    py.init()
    # ========================= VARIABLES =========================
    screen_info = py.display.Info()
    WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
    MAZE_SIZE_H, MAZE_SIZE_V = 50, 25
    CHANGED_SIZE: bool = False
    TIME_SINCE_CHANGED_SIZE: float = 0

    REFERENCE_FPS = 1200
    text_size: int = 15
    text_offSet: int = 10

    Path, Manhattan, Euclidean = False, True, False
    INDEX_TYPE_OF_MAZE = 0
    # ========================= COMPONENTS =========================
    MAZE: Maze = Maze(WIDTH, HEIGHT, 1, 25, MAZE_SIZE_H, MAZE_SIZE_V, TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE],
                      Path, Manhattan, Euclidean)

    text_font = py.font.SysFont("Arial", text_size)
    def draw_text(textToRender: Text) -> None:
        img = text_font.render(str(textToRender), True, textToRender.text_col)
        SCREEN.blit(img, textToRender.pos)

    PathText = Text("Path (1)", True, 10, HEIGHT - text_size * 1 - text_offSet)
    ManhattanText = Text("Manhattan (2)", True, 10, HEIGHT - text_size * 2 - text_offSet)
    EuclideanText = Text("Euclidean (3)", False, 10, HEIGHT - text_size * 3 - text_offSet)

    ExploredCellsText = Text("Explored cells", 0, 10, text_size * 1 - text_offSet)
    SolutionLengthText = Text("Solution Length", 0, 10,text_size * 2 - text_offSet)
    TimeSolvingText = Text("Time to solve", 0, 10, text_size * 3 - text_offSet, sufix='s')

    SolveKeyText = Text("Solve (s)", None,
                        WIDTH - text_size * 12 - text_offSet , text_size * 1 - text_offSet)
    ResetKeyText = Text("Rest maze (r / t)", TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE],
                        WIDTH - text_size * 12 - text_offSet, text_size * 2 - text_offSet)
    ChangingMazeKeyText = Text("Change maze (q)", None,
                               WIDTH - text_size * 22 - text_offSet, text_size * 3 - text_offSet)
    StartChangingMazeKeyText = Text("Start changing maze (e)", None,
                                    WIDTH - text_size * 22 - text_offSet, text_size * 1 - text_offSet)
    StopChangingMazeKeyText = Text("Stop changing maze (w)", None,
                                   WIDTH - text_size * 22 - text_offSet, text_size * 2 - text_offSet)

    HorizontalSizeText = Text("Horizontal Size (← or →)", MAZE_SIZE_H,
                              WIDTH - text_size * 11 - text_offSet,
                              HEIGHT - text_size * 1 - text_offSet)
    VerticalSizeText = Text("Vertical Size (↓ or ↑)", TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE],
                            WIDTH - text_size * 9 - text_offSet,
                            HEIGHT - text_size * 2 - text_offSet)

    TEXTS = [PathText, ManhattanText, EuclideanText, ExploredCellsText, SolutionLengthText, TimeSolvingText,
             TimeSolvingText, SolveKeyText, ResetKeyText, ChangingMazeKeyText, StartChangingMazeKeyText,
             StopChangingMazeKeyText, HorizontalSizeText, VerticalSizeText]
    # ========================= BASIC =========================
    SCREEN = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption('Py Double pendulum simulation')
    CLOCK = py.time.Clock()
    # ========================= BASIC =========================
    SOLVING_MAZE: bool = False
    CHANGING_MAZE: bool = False
    RUNNING_GAME: bool = True
    while RUNNING_GAME:
        deltaTime = CLOCK.tick(REFERENCE_FPS) / 1000.0
        if deltaTime == 0:
            continue
        if SOLVING_MAZE: MAZE.add_time_solving(deltaTime)
        if CHANGED_SIZE: TIME_SINCE_CHANGED_SIZE += deltaTime

        # ========================= COMPONENTS AND TEXT=========================
        SCREEN.fill((0, 0, 0))
        MAZE.draw_maze(SCREEN)
        if SOLVING_MAZE: SOLVING_MAZE = not MAZE.step_solve_maze_a_star()
        if CHANGING_MAZE: MAZE.change_maze()

        PathText.set_value(Path)
        ManhattanText.set_value(Manhattan)
        EuclideanText.set_value(Euclidean)

        ExploredCellsText.set_value(MAZE.get_explored_cells())
        SolutionLengthText.set_value(MAZE.get_solution_length())
        TimeSolvingText.set_value(round(MAZE.get_time_solving(),3))

        ResetKeyText.set_value(TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE])

        HorizontalSizeText.set_value(MAZE_SIZE_H)
        VerticalSizeText.set_value(MAZE_SIZE_V)

        for text in TEXTS:
            draw_text(text)
        # ========================= EVENTS =========================
        events = py.event.get()
        for event in events:
            if event.type == py.QUIT:
                RUNNING_GAME = False
            elif event.type == py.KEYUP:
                # ONLY ONCE PER PRESS
                if event.key == py.K_ESCAPE:
                    RUNNING_GAME = False
                    break
                # Change
                elif event.key == py.K_r:
                    MAZE.regenerate_maze()
                    CHANGING_MAZE = False
                elif event.key == py.K_t:
                    INDEX_TYPE_OF_MAZE = (INDEX_TYPE_OF_MAZE + 1) % len(TYPES_OF_MAZES)
                    MAZE.set_type_of_maze(TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE])
                elif event.key == py.K_e:
                    MAZE.reset_solve_maze()
                    CHANGING_MAZE = True
                elif event.key == py.K_w:
                    CHANGING_MAZE = False
                # Solver
                elif event.key == py.K_s and not SOLVING_MAZE:
                    CHANGING_MAZE = False
                    SOLVING_MAZE = True
                    MAZE.set_to_solve_maze_a_star()
                elif event.key == py.K_1:
                    Path = not Path
                    MAZE.set_path()
                elif event.key == py.K_2:
                    Manhattan = not Manhattan
                    if Manhattan: Euclidean = False
                    MAZE.set_manhattan()
                    MAZE.set_euclidean(Euclidean)
                elif event.key == py.K_3:
                    Euclidean = not Euclidean
                    if Euclidean: Manhattan = False
                    MAZE.set_euclidean()
                    MAZE.set_manhattan(Manhattan)
                elif (event.key == py.K_UP or event.key == py.K_DOWN or
                      event.key == py.K_RIGHT or event.key == py.K_LEFT):
                    if event.key == py.K_UP:
                        if MAZE_SIZE_V < 200:
                            MAZE_SIZE_V += 1
                            CHANGED_SIZE = True
                            TIME_SINCE_CHANGED_SIZE = 0

                    elif event.key == py.K_DOWN:
                        if MAZE_SIZE_V > 1:
                            MAZE_SIZE_V -= 1
                            CHANGED_SIZE = True
                            TIME_SINCE_CHANGED_SIZE = 0

                    elif event.key == py.K_RIGHT:
                        if MAZE_SIZE_H < 200:
                            MAZE_SIZE_H += 1
                            CHANGED_SIZE = True
                            TIME_SINCE_CHANGED_SIZE = 0

                    elif event.key == py.K_LEFT:
                        if MAZE_SIZE_H > 1:
                            MAZE_SIZE_H -= 1
                            CHANGED_SIZE = True
                            TIME_SINCE_CHANGED_SIZE = 0

        # Resize maze
        if CHANGED_SIZE and TIME_SINCE_CHANGED_SIZE > 0.2:
            TIME_SINCE_CHANGED_SIZE = 0
            CHANGED_SIZE = False
            MAZE = Maze(WIDTH, HEIGHT, 1, 25, MAZE_SIZE_H, MAZE_SIZE_V,
                        TYPES_OF_MAZES[INDEX_TYPE_OF_MAZE],
                        Path, Manhattan, Euclidean)

        key = py.key.get_pressed()
        # WHILE PRESSED
        if key[py.K_q]:
            MAZE.reset_solve_maze()
            MAZE.change_maze()


        py.display.update()

    py.quit()


if __name__ == "__main__":
    main()