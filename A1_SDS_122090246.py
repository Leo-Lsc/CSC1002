#数字华容道 Sliding-Puzzle
import random
import copy


def introduction():
    # Introduction of the game
    print("""
        Welcome to Leo’s puzzle game. Here is a brief introduction.
        At the start of the game, you will see a puzzle with numbers in random postition.
        You need to rearrange the number in the puzzle by sliding them around the empty space
        until the elements are arranged in a specific order. Now let's start. Good luck!
        """)

def setup():
    # set up the letters of movement
    while True:
        direction = input("Enter the four letters used for left, right, up and down move > ").lower().replace(' ', '')

        # Check if the user input contains exactly 4 letters
        if len(direction) != 4:
            print("Invalid input. Please enter exactly four letters.")
            continue

        # Check if the user input contains only lowercase letters a-z
        if not all('a' <= enter <= 'z' for enter in direction):
            print("Invalid input. Please enter only letters a-z.")
            continue

        # Check if the user input contains any repeated letters
        if len(set(direction)) != 4:
            print("Invalid input. Please do not repeat any letter.")
            continue

        return list(direction)

def choose_puzzle():
    # choose the kind of puzzle and teach the users how to end the game

    while True:
        choose = input("Enter 1 for 8-puzzle, 2 for 15-puzzle or done to end the game > ")
        if choose == str(1):
            return eval(choose)

        elif choose == str(2):
            return eval(choose)

        elif choose == "done":
            exit()

        else:
            print("invalid input, please enter 1, 2 or done")

def solvable_3x3(puzzle):

    inversions = 0
    for i in range(len(puzzle)):
        if puzzle[i] != 0:
            for j in range(i):
                if puzzle[j] > puzzle[i]:
                    inversions += 1


    return inversions % 2 == 0

def get_0index(puzzle):
    return puzzle.index(0)

def find_0_row(puzzle):
    """Return the row of '0' in the puzzle"""
    width = int(len(puzzle) ** 0.5)
    return get_0index(puzzle) // width

def solvable_4x4(puzzle):
    zero_row = find_0_row(puzzle)
    inversions = 0
    for i in range(len(puzzle)):
        if puzzle[i] != 0:
            for j in range(i):
                if puzzle[j] > puzzle[i]:
                    inversions += 1
    if zero_row % 2 == 0:
        return inversions % 2 == 1
    else:
        return inversions % 2 == 0


def get_puzzle(choose):
    #define a puzzle based on user's choice
    n = 8 if choose == 1 else 15
    puzzle = [i for i in range(1, n + 1)]
    puzzle.append(0)
    while True:
        random.shuffle(puzzle)
        if choose == 1:
            if solvable_3x3(puzzle):
                return puzzle
        elif choose == 2:
            if solvable_4x4(puzzle):
                return puzzle

def printstate(puzzle):
   #print the state of the puzzle
   length = len(puzzle)
   width = int(length ** 0.5)
   for i in range(0, length, width):
       row = puzzle[i:i+width]
       for number in row:
           if number == 0:
               print("    ", end = "")
           else:
               print("%4d" % number, end="")
       print()



def choice_move(index, direction, puzzle):
    #tell the users w
    # hich motion can be activated
    lsc = copy.copy(direction)
    movement = ["left", "right", "up", "down"]
    if len(puzzle) == 9:
        if index in [2, 5, 8]:
            # cannot go left
            lsc[0] = None
            movement[0] = None
        if index in [0, 3, 6]:
            # cannot go right
            lsc[1] = None
            movement[1] = None
        if index in [6, 7, 8]:
            # cannot go up
            lsc[2] = None
            movement[2] = None
        if index in [0, 1, 2]:
            # cannot go down
            lsc[3] = None
            movement[3] = None
    else:
        if index in [3, 7, 11, 15]:
            # cannot go left
            lsc[0] = None
            movement[0] = None
        if index in [0, 4, 8, 12]:
            # cannot go right
            lsc[1] = None
            movement[1] = None
        if index in [12, 13, 14, 15]:
            # cannot go up
            lsc[2] = None
            movement[2] = None
        if index in [0, 1, 2, 3]:
            # cannot go down
            lsc[3] = None
            movement[3] = None
    while True:
        i = 0
        available = "Enter your move "
        for j in lsc:
            if j == None:
                i = i + 1
                continue
            available = available + movement[i] + "-%s > " % (j)
            i = i + 1
        print(available, end="")
        choice = input()
        if choice in lsc:
            return choice
        else:
            print("invalid input, please enter again")


def _move(index, choice, puzzle, direction):
    #move the puzzle

    l = direction[0]
    r = direction[1]
    u = direction[2]
    d = direction[3]
    size = len(puzzle)
    width = int(size ** 0.5)
    if choice == l:
        # go left
        puzzle[index], puzzle[index + 1] = puzzle[index + 1], puzzle[index]
    elif choice == r:
        # go right
        puzzle[index], puzzle[index-1] = puzzle[index-1], puzzle[index]
    elif choice == u:
        # go up
        puzzle[index], puzzle[index+width] = puzzle[index+width], puzzle[index]
    elif choice == d:
        # go down
        puzzle[index], puzzle[index-width] = puzzle[index-width], puzzle[index]
    return puzzle

def wincondition(puzzle):
    #test the player whether win the game
    if puzzle == [1,2,3,4,5,6,7,8,0] or puzzle == [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]:
        print(''' Congratulations! You have won the game! They say one who can pass 
        through Leo's test has the same intelligence with Albert Einstein. You have all reason to 
        be proud of this, because Einstein is the closest man to god and me on Earth.''')
        return 1
    return 0


if __name__ == '__main__':
    #test the code
    introduction()
    direction = setup()
    while True:
        choose = choose_puzzle()
        puzzle = get_puzzle(choose)
        printstate(puzzle)
        count = 0
        while True:
            count = count + 1
            index = get_0index(puzzle)
            choice = choice_move(index, direction, puzzle)
            puzzle = _move(index, choice, puzzle, direction)
            printstate(puzzle)
            if wincondition(puzzle):
                print("Used %d steps, good job!"% (count))
                break
            