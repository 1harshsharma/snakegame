# ---
# Title: Python Snake Game
# Author: Harsh Sharma
# ---

import tkinter  # graphical user interface library
import random  # for random generation

rows = 25
cols = 25

tile_size = 25
wind_width = tile_size * rows
wind_length = tile_size * cols

class Tile:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

# Game Window
window = tkinter.Tk()

window.title("SNAKE")
window.resizable(False, False)  # Won't allow user to resize the window


canvas = tkinter.Canvas(window, bg = "black", width=wind_width, height=wind_length, borderwidth=0, highlightthickness=0)
canvas.pack()
canvas.update()

# Center the window when it open
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Initialise the game
snake = Tile(tile_size * 5, tile_size * 5)  # single tile, snake's head
food = Tile(tile_size * 10, tile_size * 10)
snake_body = []  # Multiple tile objects
velocityX = 0  # speed/direction
velocityY = 0  # speed/direction
game_over = False  # By default
score = 0

def change_direction(e):
    global velocityX, velocityY, game_over

    if game_over:
        return

    if e.keysym == "Up" and velocityY != 1:
        velocityX = 0
        velocityY = -1
    elif e.keysym == "Down" and velocityY != -1:
        velocityX = 0
        velocityY = 1
    elif e.keysym == "Left" and velocityX != 1:
        velocityX = -1
        velocityY = 0

    elif e.keysym == "Right" and velocityX != -1:
        velocityX = 1
        velocityY = 0
def generate_food():
    global food, snake, snake_body

    # Generate new food coordinates until it's not overlapping with the snake
    while True:
        new_food_x = random.randint(0, cols - 1) * tile_size
        new_food_y = random.randint(0, rows - 1) * tile_size
        food_collision = False

        # Check if the new food coordinates overlap with the snake's head or body
        if new_food_x == snake.x and new_food_y == snake.y:
            food_collision = True
        for tile in snake_body:
            if new_food_x == tile.x and new_food_y == tile.y:
                food_collision = True
                break

        # If no collision found, set the new food coordinates and break the loop
        if not food_collision:
            food.x = new_food_x
            food.y = new_food_y
            break

def move():
    global snake, food, snake_body, game_over, score

    if game_over:
        return
    
    if snake.x < 0 or snake.x >= wind_width or snake.y < 0 or snake.y >= wind_length:
        game_over = True
        return

    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return

    # Collision detection
    if snake.x == food.x and snake.y == food.y:  # Eats the food
        snake_body.append(Tile(food.x, food.y))
        generate_food()
        score += 1

    # Update snake body - catch up to the tile infront
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if i == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * tile_size
    snake.y += velocityY * tile_size

def draw():
    global snake, food, snake_body, game_over, score  # Reference the snake variable outside the function

    move()

    canvas.delete("all")  # Everytime we draw a new frame we clear the previous frame

    canvas.create_rectangle(food.x, food.y, food.x+tile_size, food.y+tile_size, fill="red")  # Draw food - if collide we will see the snake over the food

    # Draw snake body
    canvas.create_rectangle(snake.x, snake.y, snake.x+tile_size, snake.y+tile_size, fill="lime green") 
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x+tile_size, tile.y+tile_size, fill = "lime green")
    
    if game_over:
        canvas.create_text(wind_width//2, wind_length//2, font="arial 20",text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(25, 15, font="arial 12", text=f"score: {score}", fill="white")
    
    window.after(100, draw)  # After 100 millisecond call the draw function -> 10 frames/second

draw ()

window.bind("<KeyRelease>", change_direction) #when you press on any key and then let go

# Open the window?
window.mainloop()  # Will keep the window on 