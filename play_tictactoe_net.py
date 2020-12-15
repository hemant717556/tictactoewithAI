import itertools as it
import numpy as np
import random
import torch as tr
import play_baseline_ai_and_mcts as bg
import mcts as mcts
import tictactoe_data_encoding as bd
import tictactoe_net as bn
board_size=4

def update_size(size):
    global board_size
    board_size=size

def helper():
    return np.random.permutation([1,2,3])

net = bn.TicTacToeNet1(board_size)
net.load_state_dict(tr.load("model%d.pth" % board_size))

def nn_puct(state,player,board_size):
    node=mcts.Node(state)
    with tr.no_grad():
        x = tr.stack(tuple(map(bd.encode, [child.state for child in node.children(player)])))
        y = net(x)
        probs = tr.softmax(y.flatten(), dim=0)
        a = np.random.choice(len(probs), p=probs.detach().numpy())
    return node.children(player)[a]

def play_net(size):
    update_size(size)
    state = bg.initial_state(board_size)
    print("Game No:",count)
    print("\n")
    winner = 0
    while winner == 0:
        print("Start\n",state.board)
        players=helper()
        
        for player in players:
            valid_actions = state.valid_actions()
            if state.is_leaf():

                winner = state.evaluate()
                continue
            if len(valid_actions) == 1:
                #print(valid_actions)
                state = state.perform(valid_actions[0],player)
                winner = state.evaluate()
                break
            if player==3:
                a, node = mcts.decide_action(state,player,
                    choose_method=nn_puct(state,player,board_size),
                    num_rollouts=500, max_depth = 500, verbose=False)
                state = node.children(player)[a].state
            else :
                a, node = mcts.decide_action(state, player,None, num_rollouts=500, max_depth = 500, verbose=False)
                state = node.children(player)[a].state
            print(state.board)
        winner=state.evaluate()
        if winner > 0:
            print(f"Player {winner} wins!!!!!!!!---------------")
        else:
                print("------------It's a draw!")
                break
    print("Winner is ",winner)



    




