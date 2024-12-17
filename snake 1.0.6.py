# Snake Game

from tkinter import *
import random
import winsound

# Settings
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 70
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_HEAD = "#FFFF00"          # Gelb
SNAKE_COLOR = "#FF00FF"
FOOD_COLOR = "#FF0000"           # Rot
BACKGROUND_COLOR = "#000000"     # Schwarz

# Snake-Klassifizierung
class Snake:    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_HEAD, tag="snake")
            self.squares.append(square)

# Food-Klassifizierung
class Food:    
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE)-1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Gameflow-Funktion
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
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        winsound.PlaySound("Snake\Sounds\snake_score.wav", winsound.SND_ASYNC)
        score += 1
        label.config(text="Score:{}\nHighscore:{}".format(score, highscore), font=('consolas', 15))
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

# Movement-Funktion
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

# Collision-Funktion
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

# GameOver-Funktion
def game_over():
    global score, highscore, save_highscore
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.2, font=('consolas',10000), text="|", fill="#990000", tag="gameover")
    if score > highscore:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.2, font=('consolas',10000), text="|", fill="#228B22", tag="gameover")
        save_highscore = open("Snake\data\highscore.txt", "w")
        save_highscore.write(str(score))
        save_highscore.close
        winsound.PlaySound("Snake\Sounds\highscore.wav", winsound.SND_ASYNC)
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/5, font=('consolas',40), text="NEW HIGHSCORE".format(score), fill="yellow", tag="gameover")
    else:
        winsound.PlaySound("Snake\Sounds\GameOver.wav", winsound.SND_ASYNC)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.8, font=('consolas',40), text="Dein Score:{}".format(score), fill="white", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2.2, font=('consolas',70), text="GAME OVER", fill="black", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.8, font=('consolas',40), text="Press SPACE to restart", fill="white", tag="newgame")
    if score <= 5:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="You're shit, duh", fill="black", tag="gameover")
    elif score >= 5 and score <= 10:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="You're okay", fill="black", tag="gameover")
    elif score >= 10 and score <= 15:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="Not bad", fill="black", tag="gameover")
    elif score >= 15 and score <= 20:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="Nice nice", fill="black", tag="gameover")
    elif score >= 20 and score <= 25:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="Good job", fill="black", tag="gameover")
    elif score >= 25 and score <= 68:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="Very nice", fill="black", tag="gameover")
    elif score == 69:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="I see what you did there", fill="black", tag="gameover")
    elif score >= 70:
        canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.06, font=('consolas',20), text="Very nice", fill="black", tag="gameover")
    window.bind('<space>', restart_game)

# Neustart-Funktion
def restart_game(event=None):
    global snake, food, score, direction, highscore, bg, random_bg
    canvas.delete(ALL)  # Clears the canvas
    random_bg = random.randint(1, 3)
    bg = PhotoImage(file = "Snake\data\pic" + str(random_bg) + ".png")
    canvas.pack(fill = "both", expand = True)
    canvas.create_image( 0, 0, image = bg, anchor = "nw")
    canvas.create_text(40, 690, font=('consolas',15), text="v.1.0.6", fill="#474747", tag="Version")
    window.unbind('<space>')
    if score >= highscore:
        highscore = score
    score = 0 
    direction = 's'    # Resets the direction
    label.config(text="Score:{}\nHighscore:{}".format(score, highscore), font=('consolas', 15))
    snake = Snake()       # Creates a new snake
    food = Food()         # Creates a new food
    next_turn(snake, food)  # Starts the game loop again

# Lable Window
window = Tk()
window.title("Sneaky Snake")
window.resizable(False, False)

# Scoreboard + Highscore
score = 0
load_highscore = open("Snake\data\highscore.txt", "r")
highscore = int(load_highscore.read())
load_highscore.close()
direction = 's'

label = Label(window, text="Score:{}\nHighscore:{}".format(score, highscore), font=('consolas', 15))
label.pack()

# Playground
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
random_bg = random.randint(1, 3)
bg = PhotoImage(file = "Snake\data\pic" + str(random_bg) + ".png")
canvas.pack(fill = "both", expand = True)
canvas.create_image( 0, 0, image = bg, anchor = "nw")
canvas.create_text(40, 690, font=('consolas',15), text="v.1.0.6", fill="#474747", tag="Version")
canvas.pack()

# Create Window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Controls
window.bind('<a>', lambda event: change_direction('a'))
window.bind('<d>', lambda event: change_direction('d'))
window.bind('<w>', lambda event: change_direction('w'))
window.bind('<s>', lambda event: change_direction('s'))

snake = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()