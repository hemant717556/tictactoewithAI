import numpy as np
import torch as tr
import random
import play_baseline_ai_and_mcts as play
import math
import mcts as mcts
board_size=4
def update_size(size):
    global board_size
    board_size=size

def helper():
    b=[]
    while(True):
        player=random.randint(1,3)
        if(player not in b):
            b.append(player)
        if(len(b)==3):
            return b

def generate(num_examples, depth, board_size):
    data = []
    utility=[]
    for n in range(num_examples):
        state = play.initial_state(board_size)
        winner = 0
        while winner == 0:
            players=helper()
            for player in players:
                valid_actions = state.valid_actions()
                # print(valid_actions)
                if len(valid_actions) == 1:
                    
                    state = state.perform(valid_actions[0],player)
                    winner = state.evaluate()
                    utility=state.get_score()
                    break
                if state.is_leaf(): 
                    winner = state.evaluate()
                    utility=state.get_score()
                    continue
                a, node = mcts.decide_action(state, player,None,10)
                state = node.children(player)[a].state
                Q = node.get_score_estimates()
                winner = state.evaluate()
                for c,child in enumerate(node.children(player)):
                    utility=Q[c]
                    state=child.state
                #data.append((child.state, Q[c]))
        data.append((state, utility))
    return data

def encode(state):
    # returns encoding of state
    # encoding[0,:,:] == 1 where there are blanks, 0 elsewhere
    # encoding[1,:,:] == 1 where there are "O"s, 0 elsewhere
    # encoding[2,:,:] == 1 where there are "X"s, 0 elsewhere
    # encoding[3,:,:] == 1 where there are "X"s, 0 elsewhere
    s = tr.zeros(4,board_size,board_size)
    for row in range(board_size):
        for col in range(board_size):
            if state.board[row,col] == 0:
                s[0,row,col] = 1#tr.tensor([1,0,0,0])
            if state.board[row,col] == 1:
                s[1,row,col] = 1#tr.tensor([0,1,0,0])
            if state.board[row,col] == 2:
                s[2,row,col] = 1#tr.tensor([0,0,1,0])
            if state.board[row,col] == 3:
                s[3,row,col] = 1#tr.tensor([0,0,0,1])
    return s



def helper_data(board_size):
    input_list = []
    output_list = []
    update_size(board_size)
    examples = generate(num_examples=100, depth=100, board_size=board_size)
    for n, (state, utility) in enumerate(examples):
        print("example %d:" % n)
        print(state.board)
        input_list.append(encode(state))
        output_list.append(utility)


    print("Encoding of last example state:")
    encoding = encode(state)
    print(encoding)

    # # quick test for encode
    encoding = encode(play.initial_state(board_size))
    assert(type(encoding) == tr.Tensor)
    expected = tr.zeros((4,board_size,board_size))
    expected[0,:,:] = 1
    
    
    outputs = tr.tensor(output_list,dtype=tr.float)
    
    
    player_3=[]
    for output in outputs:
        player_3.append(output[2])
    outputs = tr.tensor(player_3,dtype=tr.float) 
    outputs = tr.reshape(outputs,(len(examples),1))
    print(outputs)
    inputs = tr.tensor(tr.stack(input_list,0),dtype=tr.float)
    tr.reshape(inputs,(len(examples),4,board_size,board_size))

    import pickle as pk
    with open("data1%d.pkl" % board_size, "wb") as f: pk.dump((inputs, outputs), f)




    


   
