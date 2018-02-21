## miniChessDriver.py
## version 0.1
## November 30, 2017

## Here's the crude, unpolished first version of a user
## interface for your miniChess function

## It doesn't really know much about who wins the game
## or when...although it does know that if it can't make
## a move, the human player wins.

## It does not validate the coordinates for the move
## that is entered by the user.  You can move any pawn
## on either side to any square.  So be careful.

## We have supplied "dummy" move_maker and
## move_chooser functions so that this
## program will run without causing an
## error.  But the program will not play
## the game correctly until you replace
## our two functions with your functions.

## Put your definitions for move_maker and
## move_chooser up here in this space.
##
## Replace the two function definitions below
## with your functions.
##
## DO NOT LEAVE OUR FUNCTIONS HERE

import copy
import prog67

def move_piece(board, color, row, col, new_r, new_c):
    """Given the board, piece color, position, and new position, returns a new board that
    represents the move without altering the original board.
    """
    #Deep copying the board so that the original is not altered
    new_board = copy.deepcopy(board)

    #Changing the new position of the piece to the appropriate color
    new_board[new_r][new_c] = color

    #Changing the previous position of the piece to be empty
    new_board[row][col] = 0

    return new_board

def piece_moves(board, row, col, color):
    """Given a board, color, and piece position, generates and returns a list of possible
    moves for that piece to make by returning a list of boards (two dimensional lists) that
    are equivalent to the outcome of a move.
    """

    ##Initializing starting variables for later use, including direction of movement along the
    ##rows, list of possible moves for the piece, and color of the enemy pieces
    move_dir = 0
    piece_move_list = []
    enemy_color = 0

    ##Based on the color that is input, assigns the direction of the friendly color's movement
    ##and the enemy's color
    if color == 1:
        move_dir = 1
        enemy_color = 2
    elif color == 2:
        move_dir = -1
        enemy_color = 1
    else:
        print("Color Error")
        return
    
    #Assigning the next row for the piece, according to the movement direction
    new_row = row + move_dir
    #Checking to make sure the piece isn't already at the end of the board
    if new_row > len(board)-1 or new_row < 0:
        return
    
    #If the space directly in front is empty, adding that movement to the movement list
    if board[new_row][col] == 0:
        piece_move_list.append(move_piece(board, color, row, col, new_row, col))

    ##If the spaces diagonal to the piece are in bounds and have enemy pieces, adding that
    ##movement to the movement list
    if col-1 >= 0 and board[new_row][col-1] == enemy_color:
        piece_move_list.append(move_piece(board, color, row, col, new_row, col-1))
    if col+1 <= len(board)-1 and board[new_row][col+1] == enemy_color:
        piece_move_list.append(move_piece(board, color, row, col, new_row, col+1))
        
    return piece_move_list

def move_maker(board, color):
    """Given a board and player color, generates every possible move for the player and returns
    those moves as a list of boards (two dimensional lists) that represent the boards after
    making the possible moves.
    """
    return prog67.move_maker(board, color)
##    #Initializing the list to hold the possible moves
##    moves = []
##
##    ##Checks every space on the board for a friendly piece, then utilizes piece_moves() to
##    ##find the possible movements for each friendly piece, adding those movements to the
##    ##list of all possible moves
##    for row in range(0,len(board)):
##        for col in range(0,len(board[row])):
##            if board[row][col] == color:
##                added_boards = piece_moves(board,row,col,color)
##                #Checking to make sure that the list of moves for a piece isn't empty
##                if added_boards != None and len(added_boards) > 0:
##                    moves += added_boards
##
##    return moves

def has_won(board, color):
    """Given a board and color, checks if that color has won the game, returning True if
    they have won and False if they have not.
    """

    #Initializing variables for the end row of the color, enemy color, and number of enemies
    end_row = 0
    opp_color = 0
    opp_pieces = 0

    #Assigning correct values for the end row and opponent color based on the given friendly color
    if color == 1:
        end_row = len(board)-1
        opp_color = 2
    elif color == 2:
        opp_color = 1
    else:
        print("Color Error")
        return

    ##Checking every space on the board to see if a friendly piece has made it to the end row
    ##and tallying the enemy pieces otherwise.
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == end_row and board[row][col] == color:
                return True
            elif board[row][col] == opp_color:
                opp_pieces += 1

    #Utlizing the move_maker() function to generate the possible opponent moves for later use
    opp_enemy_moves = move_maker(board, opp_color)

    ##Checks for either of the remaining two win scenarios (eliminating all opposing pieces
    ##or not allowing any moves for the opponent) based on the information previously gathered
    if opp_pieces == 0:
        return True
    elif len(opp_enemy_moves) == 0:
        return True
    else:
        return False

def assign_points(board, color):
    """Given a current board and color, assigns points based on how close the color is to
    achieving one of the victory requirements.
    Point Criteria:
        +1 for every friendly piece (towards goal of taking every enemy piece)
        -1 for every enemy piece (towards goal of taking every enemy piece)
        +.25 for every space past the starting line a friendly piece has moved (working towards
            goal of reaching the end of the board)
        -.01 for every enemy move that can be made (towards goal of making the last move while
            the opponent cannot make another move: only intented to be a tiebreaker, as it is
            the least viable to predict)
    """

    ##Initializing starting variables for number of friendly pieces, enemy pieces, starting row,
    ##difference between friendly and enemy pieces, number of total forward spaces moved, total
    ##points, and point conversion factors for spaces moved and enemy moves possible.
    friends = 0
    start_row = 0
    enemies = 0
    piece_diff = 0
    forward_spaces = 0
    total = 0
    enemy_move_pt_factor = .01
    friendly_move_space_factor = .25

    #Assigning the enemy color and start row based on the given color
    if color == 1:
        enemy_color = 2
    elif color == 2:
        start_row = 2
        enemy_color = 1
    else:
        print("Color Error")
        return

    #Calculating the number of possible enemy moves and subtracting the appropriate points
    num_enemy_moves = len(move_maker(board, enemy_color))
    total -= enemy_move_pt_factor * num_enemy_moves

    ##Looping through the positions in the board and counting the number of forward spaces,
    ##friendly pieces, and enemy pieces, for use in calculating point totals.
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == color:
                friends += 1
                forward_spaces += abs(start_row - row)
            elif board[row][col] == enemy_color:
                enemies += 1

    #Calculating the total point values
    diff = friends-enemies
    total += friendly_move_space_factor * forward_spaces
    total += diff
    
    return total

def assign_pts_look_ahead(board, color, isEnemy, counter):
    """Given a board, color, boolean that describes whether that color is the computer's opponent,
    and counter to limit recursion, returns the total point value for this board. Only "looks ahead"
    three moves past the original move
    """

    ##Checking to see if the board is a win or loss, assigns 10 points for a win and 10 for
    ##a loss. Also ends the recursion if a win or loss is reached.
    if has_won(board, color):
        if isEnemy:
            return -10
        else:
            return 10
    ##If an endgame has not been reached, checking if the counter has exceeded 2, in which case
    ##points are assigned to the board as is, according to assign_points(), for the board position
    ##of the computer.    
    elif counter > 2:
        if isEnemy and color == 1:
            return assign_points(board, 2)
        elif isEnemy and color ==2:
            return assign_points(board, 1)
        else:
            return assign_points(board, color)

    #Creating and assigning the next function call's color
    if color == 1:
        next_color = 2
    else:
        next_color = 1

    #Initializing the total points that will be totalled using recursion of this function
    total = 0

    ##Generating every possible move for the enemy to make, and calling this function to assign
    ##points to each of those possibilities, totalling them and returning the total.
    future_moves = move_maker(board, next_color)
    for move in future_moves:
        total += assign_pts_look_ahead(move, next_color, not isEnemy, counter+1)
        
    return total

def move_chooser(board_list, color):
    """Given a list of possible moves and a color, returns the move (represented as a two
    dimensional list) that, according to the point assignment algorithm and "looking ahead",
    is the best available move. 
    """
    return prog67.move_chooser(board_list, color)
##    ##Initializing the list of points that correspond by index to the list of moves and the index
##    ##of the move with the highest point value
##    board_pts = []
##    best_move_index = 0
##
##    ##Looping through each board, checks if it has won (if so, immediately returns that board),
##    ##and otherwse adds the point score for that board to the point list
##    for board in board_list:
##        if has_won(board, color):
##            return board
##        board_pts.append(assign_pts_look_ahead(board, color, False, 0))
##    
##    ##Finding the index of the max value of the point list, and assigning the corresponding
##    ##movement to the return variable
##    for index in range(1,len(board_list)):
##        if board_pts[best_move_index] < board_pts[index]:
##            best_move_index = index
##    result = board_list[best_move_index]
##
##    return result

## keep everything below as is ======================================


## print a board
## 0 prints as '-', 1 prints as 'w', 2 prints as 'b'

def printBoard(board):
    print("   ", end = "")
    for i in range(0, len(board[0])):
        print(str(i)+" ", end = "")

    print("\n")
    row = 0
    for r in board:
        print(row, " ", end = "")
        for c in r:
            if c == 1:
                print("w ", end = "")
            elif c == 2:
                print("b ", end = "")
            else:
                print("- ", end = "")
        print()
        row = row + 1
    print()
            

## create an initial board, with dimension
## passed as the argument. 1s at the top,
## 2s at the bottom, 0s everywhere else
    
def makeInitBoard(dim):
    board = []
    for i in range(0,dim):
        row = []
        for j in range(0,dim):
            row.append(0)
        board.append(row)

    for i in range(0,dim):
        board[0][i] = 1
        board[dim - 1][i] = 2
        
    return board


## this is the user interface for the miniChess game.
## just run the program and type 'miniChess()' in the
## interaction window

def miniChess():
    from random import randint

    print("Welcome to miniChess")

    ## ask for board size and create initial board
    
    dim = int(input("What size board would you like? \n(enter an integer greater than 2): "))
    bheight = dim
    bwidth = dim
    b = makeInitBoard(dim)
    
    print("\nHere's the initial board...\n")
    
    printBoard(b)

    ## ask user to select color of pawns
    ## if user selects white, then the program's color is 2 (i.e., black)
    ## if user selects black, then the program's color is 1 (i.e., white)

    while True:
        answer = input("Choose the white pawns or black pawns (enter 'w' or 'b' or 'quit'): ")
        if answer == "w":
            mycolor = 2
            playercolor = 1
            break
        if answer == "b":
            mycolor = 1
            playercolor = 2
            break
        if answer == "quit":
            print("Ending the game")
            return

    ## if program has white pawns, generate program's first move

    if mycolor == 1:
        print("Here's my opening move...\n")
##        possiblemoves = move_maker(b, mycolor)  # don't change this function call
##        b = move_chooser(possiblemoves, mycolor) # don't change this function call
        column = randint(0, bwidth - 1)
        b[1][column] = b[0][column]
        b[0][column] = 0
        printBoard(b)

    ## game loop

    while True:
        
        ## ask for user's move
        ## coordinates are not validated at this time
        
        print("\nEnter the coordinates of the pawn you wish to move:")
        fromrow = int(input("   row: "))
        fromcol = int(input("   col: "))
        print("Enter the coordinates of the destination square: ")
        torow = int(input("   row: "))
        tocol = int(input("   col: ")) # oops
        b[torow][tocol] = b[fromrow][fromcol]
        b[fromrow][fromcol] = 0
        print("This is your move...\n")
        printBoard(b)

        if has_won(b,playercolor):
            print("Congratulations! You win!")
            return
        
        ## here is where the program uses the functions created by the student
        
        possiblemoves = move_maker(b, mycolor)  # don't change this function call
        if possiblemoves == []:
            print("I can't move\nCongratulations! You win!")
            return
        b = move_chooser(possiblemoves, mycolor) # don't change this function call


        print("Here's my response...\n")
        printBoard(b)

        if has_won(b,mycolor):
            print("Sorry, you have lost :(")
            return



