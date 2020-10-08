import tkinter
from tkinter import messagebox
import random


SNAKE_SPEED = 100
GRID_CELL = 20
SNAKE_DIRECTIONS = {'Up': [(0, -GRID_CELL), 'Down'], 
                'Down': [(0, GRID_CELL), 'Up'],
                'Left': [(-GRID_CELL, 0), 'Right'],
                'Right': [(GRID_CELL, 0), 'Left']
                }
GAME_FIELD_WIDTH = 500
GAME_FIELD_HEIGHT = 500
SNAKE_ALIVE = True
aviable_coords = set((x,y) for x in range(0,GAME_FIELD_WIDTH, GRID_CELL) for y in range(0, GAME_FIELD_HEIGHT, GRID_CELL))

class SnakePart(object):
    
    def __init__(self, x, y):
        self.obj = game_field.create_rectangle(x, y, x + GRID_CELL, y + GRID_CELL, fill='black')
        if (x,y) in aviable_coords:
            aviable_coords.remove((x,y))


class Snake(object):
    """ Змейка """
    
    def __init__(self, parts):
        self.parts = parts
        self.direction = SNAKE_DIRECTIONS['Right']

    def move(self, apple):
        """ Сдвигает змейку на один блок """ 
        snake_head_coords = game_field.coords(self.parts[-1].obj)
        new_snake_head_coords = list(map(lambda a,b: a + b, game_field.coords(self.parts[-1].obj), self.direction[0]*2))
        if new_snake_head_coords[0] not in range(0, GAME_FIELD_WIDTH) or new_snake_head_coords[1] not in range(0, GAME_FIELD_HEIGHT):
            return False
        aviable_coords.add(tuple(game_field.coords(self.parts[0].obj)[:2]))
        for i in range(len(self.parts) - 1):
            new_part_coord = game_field.coords(self.parts[i + 1].obj)
            if new_part_coord != new_snake_head_coords:
                game_field.coords(self.parts[i].obj, new_part_coord)
            else:
                return False
        game_field.coords(self.parts[-1].obj, new_snake_head_coords)
        distance_to_apple = game_field.bbox(self.parts[-1].obj, apple.obj)
        if abs(distance_to_apple[0] - distance_to_apple[2]) == 22 and abs(distance_to_apple[1] - distance_to_apple[3]) == 22:
            self.add_part()
            apple.chanage_coords()
            return True
        aviable_coords.remove(tuple(new_snake_head_coords[0:2]))
        return True

        
    def add_part(self):
        """ Увеличивает змейку """
        self.parts.insert(0, SnakePart(*game_field.coords(self.parts[0].obj)[:2]))
        

    def change_direction(self, event):
        """изменяет направление движения змеи"""
        game_field.bind('<KeyPress>', lambda event: None)

        if event.keysym in SNAKE_DIRECTIONS and event.keysym != self.direction[1]:
            self.direction = SNAKE_DIRECTIONS.get(event.keysym)


class Apple(object):
    """ Яблоко """

    def __init__(self):
        x, y = aviable_coords.pop()
        self.obj = game_field.create_rectangle(x, y, x + GRID_CELL, y + GRID_CELL, fill='red')
    
    def chanage_coords(self):
        new_x, new_y = aviable_coords.pop()
        new_coords = game_field.coords(self.obj, new_x, new_y, new_x + GRID_CELL, new_y + GRID_CELL)


class Game(object):

    def __init__(self):
        self.status = True
        self.snake_default_position = [(GRID_CELL, GRID_CELL), (2 * GRID_CELL, GRID_CELL), (3 * GRID_CELL, GRID_CELL)]
        self.snake = Snake([SnakePart(*self.snake_default_position[0]), 
                            SnakePart(*self.snake_default_position[1]), 
                            SnakePart(*self.snake_default_position[2])])
        self.apple = Apple()


    def start(self):
        if self.status:
            self.status = self.snake.move(self.apple)
            game_field.bind('<KeyPress>', self.snake.change_direction)
            root.after(SNAKE_SPEED, self.start)
        else:
            self.restart()
    
    def restart(self):
        global aviable_coords
        ans = messagebox.askyesno('GAME OVER', 'Начать новую игру?')
        if ans == True:
            game_field.delete('all')
            self.snake = Snake([SnakePart(*self.snake_default_position[0]), 
                            SnakePart(*self.snake_default_position[1]), 
                            SnakePart(*self.snake_default_position[2])])
            self.apple = Apple()
            self.status = True
            aviable_coords = set((x,y) for x in range(0,GAME_FIELD_WIDTH, GRID_CELL) for y in range(0, GAME_FIELD_HEIGHT, GRID_CELL))
            self.start()
        else:
            root.quit()
    

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("snake.py")
    root.resizable(width=False, height=False)
    game_field = tkinter.Canvas(root, width=GAME_FIELD_WIDTH, height=GAME_FIELD_HEIGHT, bg='white')
    game_field.focus_set()
    game_field.grid()
    Game().start()
    root.mainloop()