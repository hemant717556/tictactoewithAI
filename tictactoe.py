import numpy as np
import random
import matplotlib.pyplot as plt

def print_header():
    print("---------------------------------------------------------------------")
    print("         TIC TAC TOE WITH RANDOMIZED PLAYER SELECTION")
    print("---------------------------------------------------------------------\n")

#create the board
def create_board(size):
    return np.zeros((size,size))

#checks row win
def row_win(board, player):
    return np.any((np.all(board == player, axis=1)))

#checks Column win
def col_win(board, player):
    return np.any((np.all(board==player, axis=0)))

#checks diagonal win
def diag_win(board, player):
    
    diag1 = board.diagonal()  #array([board[0,0], board[1,1], board[2,2]])
    diag2 = np.fliplr(board).diagonal()#np.array([board[0,2], board[1,1], board[2,0]])
    return np.all(diag1 == player) or np.all(diag2 == player)

#checks for a winner
def evaluate(board, players=[1,2,3]):
    winner = 0
    for player in players:
        if row_win(board, player):
            winner = player
        elif col_win(board, player):
            winner = player
        elif diag_win(board, player):
            winner = player
    if np.all(board != 0) and winner == 0:
        winner = -1
    return winner

#helper function to randomly select a player
def helper():
    b=[]
    while(True):
        player=random.randint(1,3)
        if(player not in b):
            b.append(player)
        if(len(b)==3):
            return b
        
#function to update the board
def place(board, player, position):
    if board[position[0], position[1]] == 0:
        board[position[0], position[1]] = player
        return True
    else:
        print("Cannot place in that position.")
        return False
    #return board


def game_loop():

    start = input("Do you want to play a game? (y/n) ")
    #print(start)
    if start.lower() in ["y", "yes"]:
        repeat = True
        while repeat == True:
            play_game()
            loop = input("Do you want to play again? (y/n) ")
            if loop.lower() in ["y", "yes"]:
                repeat = True
            else:
                repeat = False
                print("Goodbye!")
    elif start.lower() in ["n", "no"]:
        repeat = False
        print("Goodbye!")
    else:
        print("I'm sorry, I didn't understand.")
        game_loop()
        
        
def play_game():
    """
    Game proper.
    """
    board_size=int(input("Enter a board size(Greater than 2):"))
    while(board_size<3):
        board_size=int(input("Enter valid board size(Greater than 2):"))
    board = create_board(board_size)
    print("Here is the board.")
    a = np.arange(6).reshape(2,3)
    print("   "+"  ".join([str(i) for i in range(board_size)]))
    for count, row in enumerate(board):
        print(count, row)
    print("To place your position, indicate the row number and the column number with a space.(like 2 3)")
    winner = 0
    while winner == 0:
        players = helper()
        for player in players:
            print("\n")
            print(f"You are player {player}")
            position = input("What position do you want to place? ")
            print("You want to place at {} position.".format(position))

            a_list = position.split()
            map_object = map(int, a_list)
            position = list(map_object)
            while position[0] > board_size-1 or position[1] > board_size-1 or position[0]<0 or position[1]<0 or (place(board, player, position)==False):
                print(board)
                position = input("Enter valid position place? ")
                print("You want to place at {} position.".format(position))
                a_list = position.split()
                map_object = map(int, a_list)
                position = list(map_object)
                
                
            print(board)
            winner = evaluate(board, players)
            if winner > 0:
                print(f"Player {winner} wins!!!!!!!!")
                break
            elif winner == -1:
                print("It's a draw!")
                break
            print()
    return winner

def main():
    print_header()
    game_loop()

if __name__ == '__main__':
    main()

