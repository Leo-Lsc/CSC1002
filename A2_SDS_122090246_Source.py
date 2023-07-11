# Boardgame(Connect 4)
import turtle

def initialization():
    # initialize the game board
    global window, total_column, column1, column2, column3, column4, column5, column6, column7, column8
    window = turtle.Screen()
    window.setup(800, 600)
    column1 = [0] * 8
    column2 = [0] * 8
    column3 = [0] * 8
    column4 = [0] * 8
    column5 = [0] * 8
    column6 = [0] * 8
    column7 = [0] * 8
    column8 = [0] * 8
    total_column = [column1, column2, column3, column4, column5, column6, column7, column8]


def column_trackers():
    # Show the column positions of the game board
    x = -380
    y = -250
    time = 0
    lsc.color('black')
    while time < 8:
        lsc.begin_fill()
        lsc.penup()
        lsc.goto(x + time*100, y)
        lsc.pendown()            
        lsc.forward(60)
        lsc.right(90)
        lsc.forward(20)
        lsc.right(90)
        lsc.forward(60)
        lsc.right(90)
        lsc.forward(20)
        lsc.right(90)
        lsc.end_fill()
        time += 1


def mouse_tracking():
    # track the mouse position
   canvas = turtle.getcanvas()
   def get_mouse_position(event):
       global mouse_position
       mouse_position = (event.x, event.y)   
   canvas.bind('<Motion>', get_mouse_position)


def check_mouse_x():
    # check the mouse position of x
    global times
    mouse_tracking()
    x = mouse_position[0]
    if 22 <= x <= 82:
        times = 0
    elif 122 <= x <= 182:
        times = 1
    elif 222 <= x <= 282:
        times = 2
    elif 322 <= x <= 382:
        times = 3
    elif 422 <= x <= 482:
        times = 4
    elif 522 <= x <= 582:
        times = 5
    elif 622 <= x <= 682:
        times = 6
    elif 722 <= x <= 782:
        times = 7
    else:
        times = -1
    column_outline()
    turtle.ontimer(check_mouse_x, 10)


def column_outline():
    # outline the column based on the mouse position
    window.tracer(0)
    if times != -1:
        if turn % 2 == 0:
            outline.pencolor("yellow")
        else:
            outline.pencolor("pink")
        outline.penup()
        outline.goto(-380 + times*100, -250)
        outline.pendown()
        outline.forward(60)
        outline.right(90)
        outline.forward(20)
        outline.right(90)
        outline.forward(60)
        outline.right(90)
        outline.forward(20)
        outline.right(90)
    else:    
        outline.clear()
    window.tracer(1)


def change_color():
    # change the color of the token by turn
    global turn
    turn = turn + 1


def drop_token(cursor_x, cursor_y):
    # drop the token if there is a click
    x = cursor_x
    a = -1
    if -380 <= x <= -320:
        a = 0
    elif -280 <= x <= -220:
        a = 1
    elif -180 <= x <= -120:
        a = 2
    elif -80 <= x <= -20:
        a = 3
    elif 20 <= x <= 80:
        a = 4
    elif 120 <= x <= 180:
        a = 5
    elif 220 <= x <= 280:
        a = 6
    elif 320 <= x <= 380:
        a = 7
    else:
        return None
    if click[a] > 7:
        return None
    window.onclick(None)
    collect_clicks(a)
    window.tracer(0)
    lsc = turtle.Turtle("circle")
    lsc.shapesize(3)
    lsc.up()
    lsc.speed(0)
    lsc.goto(-350 + 100*a, 350)
    if turn % 2 == 0:
        lsc.color("blue")
    else:
        lsc.color("red")
    lsc.speed(6)
    window.update()
    window.tracer(1)
    lsc.showturtle()
    lsc.goto(-350 + 100*a, height[click[a] - 1])
    window.onclick(drop_token)
    token_position(a)
    if turn >= 8:
        check_horizontalwin()
        check_verticalwin()
    if turn >= 11:
        check_posidiagonalwin()
        check_negadiagonalwin()
    if turn == 65:
        # if the game is tied  
        window.title("Game Tied!")
        exit()
    change_color()


def collect_clicks(a):
    # collect the clicks of each column
    global height, click
    click[a] += 1


def token_position(a):
    # record the position of two different tokens
    if turn % 2 == 0:
        total_column[a][click[a] - 1] = 1
    else:
        total_column[a][click[a] - 1] = 2


def outline_4token(c, r, tyc):
    # outline the 4 connected tokens if there is a win
    tt = turtle.Turtle()
    window.tracer(0)
    tt.hideturtle()
    tt.pensize(15)
    tt.pencolor("purple")
    if tyc == 1:
        for i in range(4):
            tt.penup()
            tt.goto(-350 + 100*c, -245 + 65*r)
            tt.pendown()
            tt.circle(30)
            c = c + 1
    elif tyc == 2:
        for i in range(4):
            tt.penup()
            tt.goto(-350 + 100*c, -245 + 65*r)
            tt.pendown()
            tt.circle(30)
            r = r + 1
    elif tyc == 3:
        for i in range(4):
            tt.penup()
            tt.goto(-350 + 100*c, -245 + 65*r)
            tt.pendown()
            tt.circle(30)
            c = c + 1
            r = r + 1
    elif tyc == 4:
        for i in range(4):
            tt.penup()
            tt.goto(-350 + 100*c, -245 + 65*(r + 3))
            tt.pendown()
            tt.circle(30)
            c = c + 1
            r = r - 1
    window.update()
    window.tracer(1)


def check_horizontalwin():
    # check if there is a horizontal win
    c = 0
    r = 0
    for i in range(8):
        for j in range(5):
            if (total_column[c])[r] != 0 and (total_column[c])[r] == (total_column[c + 1])[r] \
                == (total_column[c + 2])[r] == (total_column[c + 3])[r]:
                if (total_column[c])[r] == 1:
                    window.title("Winner ! Player 1!")
                    tyc = 1
                    outline_4token(c, r, tyc)
                    window.onclick(None)
                else:
                    window.title("Winner ! Player 2!")
                    tyc = 1
                    outline_4token(c, r, tyc)
                    window.onclick(None)
            c += 1
        c = 0
        r += 1


def check_verticalwin():
    # check if there is a vertical win
    c = 0
    r = 0
    for i in range(8):
        for j in range(5):
            if (total_column[c])[r] != 0 and (total_column[c])[r] == (total_column[c])[r + 1] \
                == (total_column[c])[r + 2] == (total_column[c])[r + 3]:
                if (total_column[c])[r] == 1:
                    window.title("Winner ! Player 1!")
                    tyc = 2
                    outline_4token(c, r, tyc)
                    window.onclick(None)
                else:
                    window.title("Winner ! Player 2!")
                    tyc = 2
                    outline_4token(c, r, tyc)
                    window.onclick(None)
            r += 1
        c += 1
        r = 0


def check_posidiagonalwin():
    # check if there is a positive diagonal win
    c = 0
    r = 0
    for i in range(5):
        for j in range(2):
            if (total_column[c])[r] != 0 and (total_column[c])[r] == (total_column[c + 1])[r + 1] \
                == (total_column[c + 2])[r + 2] == (total_column[c + 3])[r + 3]:
                if (total_column[c])[r] == 1:
                    window.title("Winner ! Player 1!")
                    tyc = 3
                    outline_4token(c, r, tyc)
                    window.onclick(None)
                else:
                    window.title("Winner ! Player 2!")
                    tyc = 3
                    outline_4token(c, r, tyc)
                    window.onclick(None)
            c += 1
        r += 1
        c = 0


def check_negadiagonalwin():
    # check if there is a negative diagonal win
    c = 0
    r = 0
    for j in range(5):
        for j in range(2):
            if (total_column[c])[r + 3] != 0 and (total_column[c])[r + 3] == (total_column[c + 1])[r + 2] \
                == (total_column[c + 2])[r + 1] == (total_column[c + 3])[r]:
                if (total_column[c])[r + 3] == 1:
                    window.title("Winner ! Player 1!")
                    tyc = 4
                    outline_4token(c, r, tyc)
                    window.onclick(None)
                else:
                    window.title("Winner ! Player 2!")
                    tyc = 4
                    outline_4token(c, r, tyc)
                    window.onclick(None)
            c += 1
        r -= 1
        c = 0


if __name__ == "__main__":
    turtle.title("Welcome to Leo's Boardgame(Connect 4)")
    mouse_position = (0, 0)
    height = [-215, -150, -85, -20, 45, 110, 175, 240]
    click = [0, 0, 0, 0, 0, 0, 0, 0]
    initialization()
    lsc = turtle.Turtle()
    lsc.hideturtle()
    lsc.speed(0)
    column_trackers()
    outline = turtle.Turtle()
    outline.hideturtle()
    outline.speed(0)
    outline.pensize(5)
    check_mouse_x()
    turn = 2
    window.onclick(drop_token)
    window.mainloop()