# Snake 贪吃蛇游戏
import turtle
import random
import time
from functools import partial

g_monster = None
g_keypressed = None
g_snake_sz = 0
flag = 0
before_pause = None

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"
HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"

def set_turtle(a, x, y):
    a.speed(0)
    a.up()
    a.setpos(x, y)

def setup_screen():
    # Set up screen and draw border
    global total_area, pen
    total_area = turtle.Screen()
    total_area.setup(580, 700)
    total_area.title("Snake by Leo")
    total_area.tracer(0)
    draw_area = turtle.Turtle()
    draw_area.hideturtle()
    set_turtle(draw_area, -250, 310)
    draw_area.pensize(5)
    draw_area.down()
    draw_area.goto(250, 310)
    draw_area.goto(250, -310)
    draw_area.goto(-250, -310)
    draw_area.goto(-250, 310)
    draw_area.up()
    draw_area.goto(-250, 210)
    draw_area.down()
    draw_area.goto(250, 210)
    draw_area.up()
    draw_area.goto(-240, 210)
    draw_area.write("Contact:                Time:                Motion:   ", font=("Arial", 16, "bold"))
    pen = turtle.Turtle()
    pen.hideturtle()
    set_turtle(pen, -100, 0)
    pen.write("Snake By Leo\n\n", font=("Arial", 16, "bold"))
    pen.write("Click anywhere to start, have fun!", font=("Arial", 16, "bold"))
    total_area.update()
    total_area.tracer(1)

def update_time():
    # update time status
    global start_time, time_status
    elapsed_time = int(time.time() - start_time)
    time_status.clear()
    time_status.write("{:d}".format(elapsed_time), font=("Arial", 16, "bold"))
    if not check_win_lose():
        turtle.ontimer(update_time, 1000)

def update_contact():
    # update contact status
    global contact, contact_status
    contact_status.clear()
    contact_status.write("{:d}".format(contact), font=("Arial", 16, "bold"))

def update_motion(key):
    # update motion status
    global motion, motion_status
    motion_status.clear()
    motion_status.write("{:s}".format(key), font=("Arial", 16, "bold"))

def start_game(x, y):
    # implement the status bar after click
    global contact, start_time, motion, time_status, contact_status, motion_status
    pen.clear()
    contact = 0
    start_time = time.time()
    motion = "Paused"

    # Contact status
    contact_status = turtle.Turtle()
    contact_status.hideturtle()
    set_turtle(contact_status, -150, 210)
    update_contact()

    # display the food , snake and monster
    set_food()
    set_snake()
    make_monster()
    
    # Time status
    time_status = turtle.Turtle()
    time_status.hideturtle()
    set_turtle(time_status, 20, 210)
    if not check_win_lose():
        update_time()
    
    # Motion status
    motion_status = turtle.Turtle()
    motion_status.hideturtle()
    set_turtle(motion_status, 170, 210)
    motion_status.write("{:s}".format(motion), font=("Arial", 16, "bold"))
    total_area.onclick(None)
    
    total_area.tracer(1)

    # Game start
    total_area.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    total_area.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    total_area.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    total_area.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)
    total_area.onkey(partial(onArrowKeyPressed,KEY_SPACE), KEY_SPACE)
    onTimerSnake()
    chase()

food_status = {i:1 for i in range(1, 6)}

def set_food():
    # Set up food
    global food
    food = []
    
    for i in range(5):
        food_turtle = turtle.Turtle()
        food.append(food_turtle)
        food[i].hideturtle()
        set_turtle(food[i], 20 * random.randint(-11, 11), 20 * random.randint(-14, 9) - 8)
        food[i].write(i+1, align="center", font=("Arial", 10, "bold"))

def hide_or_unhide_food():
    # choose number of food to hide or unhide
    choice = [i for i in range(1, 6)]
    number = random.randint(1, 5)
    
    for i in range(number):
        shuffle = random.choice(choice)
        choice.remove(shuffle)
        if food_status[shuffle] == 1:
            food_status[shuffle] = 0
            food[shuffle-1].clear()
        else:
            food_status[shuffle] = 1
            food[shuffle-1].write(shuffle, align="center", font=("Arial", 10, "bold"))
    
    if not check_win_lose():
        total_area.ontimer(hide_or_unhide_food, 5000)

def setSnakeHeading(key):
    if key in HEADING_BY_KEY.keys():
        snake.setheading( HEADING_BY_KEY[key] )

def onArrowKeyPressed(key):
    # control the motion of the snake
    global g_keypressed, motion, flag, before_pause
    
    # Exert the hide or unhide food function after the game starts
    flag = flag + 1
    if flag == 1:
        hide_or_unhide_food()

    g_keypressed = key
    total_area.tracer(0)

    # Check if the snake is at the border and allow it to change direction under certain conditions
    if snake.xcor() <= -240 and key != KEY_LEFT:
        setSnakeHeading(key)
        motion = g_keypressed
    elif snake.xcor() >= 240 and key != KEY_RIGHT:
        setSnakeHeading(key)
        motion = g_keypressed
    elif snake.ycor() <= -300 and key != KEY_DOWN:
        setSnakeHeading(key)
        motion = g_keypressed
    elif snake.ycor() >= 200 and key != KEY_UP:
        setSnakeHeading(key)
        motion = g_keypressed

    # Pause or unpause the snake
    if g_keypressed == KEY_SPACE and motion != "Paused":
        for key, value in HEADING_BY_KEY.items():
            if value == snake.heading():
                before_pause = key
        motion = "Paused"
        update_motion(motion)

    elif g_keypressed == KEY_SPACE and motion == "Paused" and not check_collision_with_body() :
        motion = before_pause
        update_motion(motion)

    elif g_keypressed == KEY_SPACE and motion == "Paused" and check_collision_with_body():
        motion = "Paused"
        update_motion(motion)
    
    else:
        motion = g_keypressed
        setSnakeHeading(key)
        update_motion(key)
        

    total_area.tracer(1)

def set_snake():
    # Set up snake
    global snake
    snake = turtle.Turtle()
    snake.shape("square")
    snake.color("red")
    snake.up()

body = [] # list of tuples (x,y) of body segments

def check_collision_with_body():
    global body, snake

    for segment in body:
        if g_keypressed == KEY_UP and abs(snake.xcor() - segment[0]) < 15 and abs(snake.ycor() + 20 - segment[1]) < 15:
            return True
        elif g_keypressed == KEY_DOWN and abs(snake.xcor() - segment[0]) < 15 and abs(snake.ycor() - 20 - segment[1]) < 15:
            return True
        elif g_keypressed == KEY_LEFT and abs(snake.xcor() - 20 - segment[0]) < 15 and abs(snake.ycor() - segment[1]) < 15:
            return True
        elif g_keypressed == KEY_RIGHT and abs(snake.xcor() + 20 - segment[0]) < 15 and abs(snake.ycor() - segment[1]) < 15:  
            return True
        elif g_keypressed == KEY_SPACE:
            if before_pause == KEY_UP and abs(snake.xcor() - segment[0]) < 20 and abs(snake.ycor() + 20 - segment[1]) < 10:
                return True
            elif before_pause == KEY_DOWN and abs(snake.xcor() - segment[0]) < 20 and abs(snake.ycor() - 20 - segment[1]) < 10:
                return True
            elif before_pause == KEY_LEFT and abs(snake.xcor() - 20 - segment[0]) < 10 and abs(snake.ycor() - segment[1]) < 20:
                return True
            elif before_pause == KEY_RIGHT and abs(snake.xcor() + 20 - segment[0]) < 10 and abs(snake.ycor() - segment[1]) < 20:  
                return True
    return False

def onTimerSnake():
    global motion, g_snake_sz, body, food

    if g_keypressed == None:
        total_area.ontimer(onTimerSnake, 200)
        return

    # Advance snake
    if motion != "Paused" and not check_win_lose():
        if snake.xcor() + 240 <= 15 and snake.heading() == 180:
            motion = "Paused"
        elif 240 - snake.xcor() <= 15 and snake.heading() == 0:
            motion = "Paused"
        elif snake.ycor() + 300 <= 15 and snake.heading() == 270:   
            motion = "Paused"
        elif 200 - snake.ycor() <= 15 and snake.heading() == 90:
            motion = "Paused"   
        else:
            # remove the food from the screen if the snake eats it
            for i in range(5):
                if (snake.xcor() - food[i].xcor())**2 + (snake.ycor() - food[i].ycor())**2 < 100 and food_status[i+1] == 1:
                    g_snake_sz = g_snake_sz + i + 1
                    food[i].clear()
                    food[i].goto(500, 500)

            if not check_collision_with_body() and g_snake_sz > 5:
                # snake moves
                body.append([snake.xcor(), snake.ycor()])
                if len(snake.stampItems) != g_snake_sz:
                    snake.color(*COLOR_BODY)
                    snake.stamp()
                    snake.color(COLOR_HEAD) 
                    snake.forward(20)
                else:
                    # Clear the tail
                    snake.color(*COLOR_BODY)
                    snake.stamp()
                    snake.color(COLOR_HEAD)
                    snake.forward(20)
                    snake.clearstamps(1) 
                    body.pop(0)
            
            elif not check_collision_with_body() and g_snake_sz <= 5:
                body.append([snake.xcor(), snake.ycor()])
                if len(snake.stampItems) != 5:
                    g_snake_sz = g_snake_sz + 1
                    snake.color(*COLOR_BODY)
                    snake.stamp()
                    snake.color(COLOR_HEAD) 
                    snake.forward(20)
                else:
                    snake.color(*COLOR_BODY)
                    snake.stamp()
                    snake.color(COLOR_HEAD)
                    snake.forward(20)
                    snake.clearstamps(1) 
                    body.pop(0)

    total_area.update()
    total_area.ontimer(onTimerSnake, 180 + 2 * g_snake_sz) # Lower the snake speed as the snake grows

def make_monster():
    # Make monster appear at a random location which has a fair distance from the snake
    global monster
    monster = turtle.Turtle()
    monster.shape("square")
    monster.color("purple")
    set_turtle(monster, random.randint(-240, 240), random.randint(-300, 200))
    
    while (monster.xcor())**2 + (monster.ycor())**2 < 30000:
        set_turtle(monster, random.randint(-240, 240), random.randint(-300, 200))

def chase():
    # Make monster chase snake
    global monster, snake, contact, body
     
    if not check_win_lose():
        xDistance = snake.xcor() - monster.xcor()
        yDistance = snake.ycor() - monster.ycor()
        for i in body:
            if abs(monster.xcor() - i[0]) < 20 and abs(monster.ycor() - i[1]) < 20:
                contact = contact + 1
                update_contact()
        if abs(xDistance) > abs(yDistance) and xDistance > 0:
            monster.goto(monster.xcor() + 20, monster.ycor())
        elif abs(xDistance) > abs(yDistance) and xDistance < 0:
            monster.goto(monster.xcor() - 20, monster.ycor())
        elif abs(yDistance) > abs(xDistance) and yDistance > 0:
            monster.goto(monster.xcor(), monster.ycor() + 20)
        elif abs(yDistance) > abs(xDistance) and yDistance < 0:
            monster.goto(monster.xcor(), monster.ycor() - 20)

    monster_speed = random.choice((280, 320, 360, 400, 440, 480)) # Randomize the speed of the monster
    total_area.ontimer(chase, monster_speed)

def check_win_lose():
    # Check if snake has eaten all the food or if it has been eaten by the monster
    if food[0].xcor() == 500 and food[1].xcor() == 500 and food[2].xcor() == 500 \
        and food[3].xcor() == 500 and food[4].xcor() == 500:
        if len(snake.stampItems) == 20:
            pen.goto(0, 260)
            pen.write("Winner!!", align="center", font=("Arial", 30, "normal"))
            return True
    
    elif abs(snake.xcor() - monster.xcor()) < 15 and abs(snake.ycor() - monster.ycor()) < 15:
        pen.goto(0, 260)
        pen.write("Game over!!", align="center", font=("Arial", 30, "normal"))
        return True
    
    else:
        return False

if __name__ == "__main__":
    setup_screen()
    total_area.tracer(0)
    total_area.onclick(start_game)
    total_area.listen()
    total_area.mainloop()