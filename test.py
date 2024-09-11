from queue import PriorityQueue

BEST_PATH = PriorityQueue()


BEST_PATH.put((10,1))
BEST_PATH.put((10,2))
BEST_PATH.put((12,3))
BEST_PATH.put((1,4))

while not BEST_PATH.empty():
    distance, num = BEST_PATH.get()
    print(f'{distance = }, {num = }')