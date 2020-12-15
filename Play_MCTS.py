import itertools as it
import numpy as np
import game 
import mcts as mcts


def initial_state():
    size = int(input("Enter a board size(Greater than 2):"))
    while (size < 3):
        size = int(input("Enter valid board size(Greater than 2):"))
    board = np.empty((size,size), dtype=int)
    board[:] = 0
    return game.TicTacToe(board,size)




if __name__ == "__main__":
    #print_header()
    start = input("Do you want to play a game? (y/n) ")
    if start.lower() in ["y", "yes"]:
        repeat = True
        while repeat:
            state = initial_state()
            
            print("To place your position, indicate the row number and the column number with a space.(like 2 3)")
            winner = 0
            while winner == 0:
                players = game.helper()
                for player in players:

                    #user's turn
                    if(player==1):
                        print("\n")
                        print(f"You are player {player}")
                        
                        position = input("What position do you want to place? ")
                        print("You want to place at {} position.".format(position))

                        a_list = position.split()
                        map_object = map(int, a_list)
                        position = list(map_object)
                        state.place(player,position)    
                        print(state.board)
                        
                    else:
                        #AI's turn
                        print(f"AI {player}'s turn")
                        a, node = mcts.decide_action(state, player, num_rollouts=500, max_depth = 500, verbose=True)

                        state = node.children(player)[a].state
                        print(state.board)
                        
                    #checks for a winner
                    winner = state.evaluate()
                    if winner > 0:
                            print(f"Player {winner} wins!!!!!!!!")
                            break
                    elif winner == -1:
                            print("It's a draw!")
                            break
                    print()
            
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
        