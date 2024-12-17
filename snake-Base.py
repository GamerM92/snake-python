from tkinter import *
from tkinter import colorchooser
import random
import winsound

# Game settings
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 70
SPACE_SIZE = 20
BODY_PARTS = 3
FOOD_COLOR = "#FF0000"           # Food color
BACKGROUND_COLOR = "#000000"     # Background color

# Default color for the snake, updated from setup screen
snake_color = "#FFFF00"          

class Snake:    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake_color, tag="snake")
            self.squares.append(square)

    def update_snake_color(self):
        for square in self.squares:
            canvas.itemconfig(square, fill=snake_color)

class Food:    
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "w":
        y -= SPACE_SIZE
    elif direction == "s":
        y += SPACE_SIZE
    elif direction == "a":
        x -= SPACE_SIZE
    elif direction == "d":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=snake_color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction

    if new_direction == 'a':
        if direction != 'd':
            direction = new_direction
    elif new_direction == 'd':
        if direction != 'a':
            direction = new_direction
    elif new_direction == 'w':
        if direction != 's':
            direction = new_direction
    elif new_direction == 's':
        if direction != 'w':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

def start_game_window():
    global canvas, snake, food, window, label, score, direction
    window = Tk()
    window.title("Snake Game")

    direction = 's'
    score = 0

    label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
    canvas.pack()

    window.update()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    window.bind('<a>', lambda event: change_direction('a'))
    window.bind('<d>', lambda event: change_direction('d'))
    window.bind('<w>', lambda event: change_direction('w'))
    window.bind('<s>', lambda event: change_direction('s'))

    snake = Snake()
    food = Food()

    next_turn(snake, food)

    window.mainloop()

def open_setup_window():
    def choose_snake_color():
        global snake_color
        color = colorchooser.askcolor(title="Choose Snake Color")
        if color[1]:
            snake_color = color[1]
            color_display.config(bg=snake_color)  # Update the display to reflect the chosen color

    def start_game():
        setup_window.destroy()  # Close setup window
        start_game_window()     # Start the main game

    # Setup windddow
    setup_window = Tk()
    setup_window.title("Game Setup")

    # Instructions
    Label(setup_window, text="Choose a color for your snake:").pack(pady=10)

    # Color picker button and display
    color_display = Label(setup_window, width=20, height=2, bg=snake_color)
    color_display.pack(pady=5)
    Button(setup_window, text="Pick Color", command=choose_snake_color).pack(pady=5)

    # Start game button
    Button(setup_window, text="Start Game", command=start_game).pack(pady=10)

    setup_window.mainloop()

# Start the setup window
open_setup_window()