from pynput import keyboard
from pynput.keyboard import Key
import os
import threading
import time
import random
# best run in console
# 286769 gud sht toradora doujin


def update_grid():
    global grid, r, c, food, snake, popped_tail
    grid[popped_tail[0]][popped_tail[1]] = 0
    for x in snake:
        grid[x[0]][x[1]] = 1
    grid[food[0]][food[1]] = 2


def game():
    global score, popped_tail, eaten_food, grid, food
    while True:
        tail = snake[-1][:]
        if direction == "quit":
            break
        elif direction == "up":
            tail[0] -= 1
        elif direction == "left":
            tail[1] -= 1
        elif direction == "right":
            tail[1] += 1
        elif direction == "down":
            tail[0] += 1
        snake.append(tail)
        if is_collided_with_body():
            grid = [[0 for x in range(c)] for y in range(r)]
        if is_food_eaten():
            eaten_food = food
            spawn_food()
            score += 25
        else:  # the previous if statement elongates the snake to the current direction, if food isn't eaten, then the tail gets removed, but if eaten then tail stays
            popped_tail = snake.pop(0)
            pass
        update_grid()  # draw the snake
        os.system("cls")
        print_grid()
        print('Score:', score)
        #print(direction)
        #print(snake)
        #for x in grid:
        #    print(x)
        # for x in grid:
        #     for y in x:
        #         print(y, end=" ")
        #     print()
        time.sleep(0.05)  # game speed


def is_collided_with_body():
    global snake
    snake_without_head = snake[:len(snake)-1]
    if snake[-1] in snake_without_head:
        snake = snake[snake.index(snake[-1]):len(snake)-1]
        return True
    return False


def is_food_eaten():
    global food
    if snake[-1] == food:
        return True
    return False


def spawn_food():
    global food, grid
    grid[food[0]][food[1]] = 0
    food = [random.randint(0, r-1), random.randint(0, c-1)]
    grid[food[0]][food[1]] = 2


def print_grid():
    print("# "*(len(grid[0])+2))
    for x in grid:
        print('# ', end='')
        for y in x:
            if y == 0:  # empty space
                print('  ', end='')
            elif y == 1:  # snake
                print('O ', end='')
            elif y == 2:  # food
                print('X ', end='')
        print('#')
    print("# "*(len(grid[0])+2))


def on_press(key):
    # handle pressed keys
    global direction
    keys = [Key.up, Key.left, Key.right, Key.down, Key.esc]
    if key not in keys:
        return

    if key == keys[0]:
        direction = "up"
    elif key == keys[1]:
        direction = "left"
    elif key == keys[2]:
        direction = "right"
    elif key == keys[3]:
        direction = "down"
    elif key == Key.esc:
        direction = "quit"
        return False

    if not game_thread.is_alive():
        game_thread.start()


def on_release(key):
    # handle released keys
    pass


r, c = list(map(int, input("Board size (r c): ").split()))
grid = [[0 for x in range(c)] for y in range(r)]
grid[0][0] = 1
snake = [[0, 0]]
food = [random.randint(0, r-1), random.randint(0, c-1)]
popped_tail = []
grid[food[0]][food[1]] = 2
score = 0
print_grid()
print("Press arrow keys to start...")
game_thread = threading.Thread(target=game)
direction = ""

with keyboard.Listener(on_press=on_press,on_release=on_release) as listener:
    listener.join()