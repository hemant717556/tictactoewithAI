import itertools as it
import numpy as np
import game 
import mcts as mcts


def initial_state(size):
    
    board = np.empty((size,size), dtype=int)
    board[:] = 0
    return game.TicTacToe(board,size)

if __name__ == "__main__":
    play_count=20
    board_size=[3]
    player_1_win=0
    AI_1_or_player_2_win=0
    AI_2_or_player_3_win=0
    draw=0
    for size in board_size:
        for count in range(play_count):
            print("Current game :",count)
            print("\n")
            # count_games.append(count)
            state = initial_state(size)
            winner = 0
            while winner == 0:
                players = game.helper()
                for player in players:

                    #user's turn
                    if(player==1 or player==2):
                        # print("\n")
                        print(f"USER{player}'s turn")
                        a, node = mcts.baseline(state, player)

                        state = node.children(player)[a].state
                        print(state.board)
                        #print(input())
                        
                    else:
                        #AI's turn
                        print(f"AI {player}'s turn")
                        count=0
                        a, node = mcts.decide_action(state, player,None, num_rollouts=500, max_depth = 500, verbose=False)
                        print("count",count)
                        state = node.children(player)[a].state
                        print(state.board)
                        #print(input())
                        
                    #checks for a winner
                    winner = state.evaluate()
                    if winner > 0:
                            print(f"Player {winner} wins!!!!!!!!---------------")
                            if(winner==1):
                                player_1_win+=1
                            elif(winner==2):
                                AI_1_or_player_2_win+=1
                            else:
                                AI_2_or_player_3_win+=1
                            break
                    elif winner == -1:
                            print("------------It's a draw!")
                            draw+=1
                            break
                    


                   
    print("Total games played:",play_count)
    print("user won ",player_1_win,"times" )
    print("AI 2 won ",AI_1_or_player_2_win,"times" )
    print("AI 3 won ",AI_2_or_player_3_win,"times" )
    print("Game Drawn",draw,"times" )
    # print(count_nodes)
    

    # import matplotlib.pyplot as pt
    # pt.plot(count_nodes,'r-')
    # #pt.plot(count_pl,'r-')
    # # pt.legend(["Nodes","Test"])
    # pt.xlabel("Games")
    # pt.ylabel("Average visit")
    # pt.show()
