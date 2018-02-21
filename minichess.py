##minichess.py
##Daniel Ritchie
##30 November 2017

import prog67

def print_board(board):
    result = ""
    for row in board:
        for char in row:
            if char == 1:
                result += "w"
            elif char == 2:
                result += "b"
            else:
                result += "-"
        result += "\n"
    print result

def gen_board():
    size = int(input("Enter the side length of the board: "))
    result = []
    first_row = []
    last_row = []
    for i in range(0,size):
        first_row.append(1)
        last_row.append(2)
    result += first_row
    for i in range(0,size-2):
        row = []
        for j in range(0,size):
            row.append(0)
        result += row
    return result



def prompt_player_move(board, color):
    print("Enter the row and column of the piece you would like to move")
    row = int(input("\tRow: "))
    col = int(input("\tColumn: "))
    
    print("Enter the row and column of where you would like to move")
    new_row = int(input("\tRow: "))
    new_col = int(input("\tColumn: "))

    return [row, col, new_row, new_col]
    
def playround(board, player_color):
    if player_color == 1:
        
    elif player_color == 2:
        

def init_player_color():
    player_color = input("Which color would like to play ('b' or 'w')?\n")
    if player_color == 'w':
        return 1
    elif player_color == 'b':
        return 2
    else:
        return init_player_color()

def play():
    print("Welcome to Mini Chess! You will play against the computer.")
    player_color = init_player_color()
    board = gen_board(board_size)
    
