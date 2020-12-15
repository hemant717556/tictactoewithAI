import numpy as np
import random
import torch as tr
import play_baseline_ai_and_mcts as bg
import mcts as mcts
import tictactoe_data_encoding as td
import tictactoe_net as tn
import play_tictactoe_net as net
import game 
import os



def initial_state(size):
    
    board = np.empty((size,size), dtype=int)
    board[:] = 0
    return game.TicTacToe(board,size)
def get_input_and_play():

    board_size=int(input("Enter a board size between [4,5,6,7,8] "))
    while(board_size<4 or board_size>8):
        board_size=int(input("Enter a valid board size between [4,5,6,7,8] "))

    print("\nWhat the player1, player2 and player3 should be??")
    print("\nOptions:")
    print("\n1.Human \t 2.Baseline AI \t 3.TreeBased AI \t 4.Treebased+NN AI")
    
    
    player_type=input("Enter your choice of otions having a space in between(e.g. 1 2 3)")
    

    a_list = player_type.split()
    map_object = map(int, a_list)
    player_type = list(map_object)

    for i in range(3):
        if (player_type[i] < 1 or player_type[i] > 4):
            player_type=input("Enter a valid choice of otions having a space in between(e.g. 1 2 3)")
            a_list = player_type.split()
            map_object = map(int, a_list)
            player_type = list(map_object)

    if(player_type[1]>3 or player_type[0]>3):
        print("Note:Please select 4 just for player 3.Our code is trained for player 3")
        player_type=input("Enter a valid choice of otions having a space in between(e.g. 1 2 3)")
        
        a_list = player_type.split()
        map_object = map(int, a_list)
        player_type = list(map_object)

    play_game(board_size,player_type)

def play_game(board_size,player_type):
            
    state = initial_state(board_size)

    winner = 0
    while winner==0:
        players = game.helper()
        data_file="data1%d.pkl"%board_size
        net_file="model%d.pth"%board_size

        for player in players:
    
            #user's turn
            if(player_type[player-1]==1):#user
                
                print(f"USER's turn")
                
                position = input("What position do you want to place?(please enter valid position with a space in between) ")
                print(state.board)
                print("You want to place at {} position.".format(position))

                a_list = position.split()
                map_object = map(int, a_list)
                position = list(map_object)
                state.place(player,position)    
                print(state.board)
                print(input("Press Enter to continue"))
            
            elif(player_type[player-1]==3):#TREEBASED AI
                
                print(f"Tree based AI's turn")
                a, node = mcts.decide_action(state, player,None, num_rollouts=500, max_depth = 500, verbose=True)
                state = node.children(player)[a].state
                print(state.board)
                print(input("Press Enter to continue"))
                
            elif(player_type[player-1]==2):#BASELINE AI
                
                print(f"BASEline AI's turn")
                a, node = mcts.baseline(state, player)
                state = node.children(player)[a].state
                print(state.board)


            else:
                print(f"Treebased AI+ NN's turn")
                a, node = mcts.decide_action(state,player,
                    choose_method=net.nn_puct(state,player,board_size),
                    num_rollouts=500, max_depth = 500, verbose=True)
                state = node.children(player)[a].state
                print(state.board)
                print(input("Press Enter to continue"))
                
            #checks for a winner
            winner = state.evaluate()
            if winner > 0:
                print(f"Player {winner} wins!!!!!!!!---------------")
                break
            elif winner == -1:
                print("------------It's a draw!------------")
                break
                

    
if __name__ == "__main__":
    
    print("---------------------------")
    print("---------Tic Tac Toe-------")
    print("---------------------------")
    start = input("Do you want to play a game? (y/n) ")
    if start.lower() in ["y", "yes"]:
        repeat = True
        get_input_and_play()
        while repeat:
            loop = input("Do you want to play again? (y/n) ")
            if loop.lower() in ["y", "yes"]:
                repeat = True
                get_input_and_play()
            else:
                repeat = False
                
    print("Goodbye!")

    
    


    


    

    
    
