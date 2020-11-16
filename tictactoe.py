import numpy as np
import random
import math

history={}
class Node(object):
    def __init__(self, state):
        self.state = state
        self.visit_count = 0
        self.score_total_1 = 0
        self.score_total_2 = 0
        self.score_total_3 = 0
        self.score_estimate_1 = 0
        self.score_estimate_2 = 0
        self.score_estimate_3 = 0
        self.child_list = None # lazy child generation
    def children(self,current_player):#will perform action according to current player in all the child states
        if self.child_list is None:
            actions = self.state.valid_actions()
            self.child_list = []
            for action in actions:
                child = self.state.perform(action,current_player)
                self.child_list.append(Node(child))
        return self.child_list        
    def choose_child(self,current_player):
        children=self.children(current_player)
        a = np.argmax([
        uct(self,child)
        for child in children
        ])
        return children[a]
        


def uct(node,child):
    uct=child.score_estimate_2+(math.log(node.visit_count+0.1)/(child.visit_count+0.1))**0.5
    return uct

def rollout(node,current_player):
    if node.state.is_leaf(): result = node.state.get_score()
    else: result = rollout(node.choose_child(current_player),current_player)
    node.visit_count += 1
    node.score_total_1 += result[0]
    node.score_total_2 += result[1]
    node.score_total_3 += result[2]
    node.score_estimate_1 = node.score_total_1 / node.visit_count
    node.score_estimate_2 = node.score_total_2 / node.visit_count
    node.score_estimate_3 = node.score_total_3 / node.visit_count
    return result

'''def rollout(node,current_player):
    all_actions=node.children(current_player)#will give all actions as children//list of child states
    #print("in roll out",node.state.board)
    result=[]
    for action in all_actions:
        result.append(get_three_random_state(action))
    desired_child=get_max_child(result,current_player-1)
    node.visit_count += 1
    node.score_total_1 += result[desired_child][0]
    node.score_total_2 += result[desired_child][1]
    node.score_total_3 += result[desired_child][2]
    node.score_estimate_1 = node.score_total_1 / node.visit_count
    node.score_estimate_2 = node.score_total_2 / node.visit_count
    node.score_estimate_3 = node.score_total_3 / node.visit_count
    print(result[desired_child])
    return result[desired_child]'''


def get_max_child(result,index):
    #result ias a list of list
    best=0
    maximum=-math.inf 
    for i in range(len(result)-1):
        if(result[i][index]>maximum):
            best=i
            maximum=result[i][index]
    return best

def get_three_random_state(node):
    #will give a list of 3 random states according to the 3 random players
    #print("in get random function",node.state.board)
    if node.state.is_leaf():
        print("NOPE----------------------------------")
        return node.state.get_score()
    else:  
        roll1=rollout(node,1)
        roll2=rollout(node,2)
        roll3=rollout(node,3)
        result=[]
        result.append((roll1[0]+roll2[0]+roll3[0])/3)
        result.append((roll1[1]+roll2[1]+roll3[1])/3)
        result.append((roll1[2]+roll2[2]+roll3[2])/3)
        return [1,1,1]#result

 
   
def mcts_2(node):
    for _ in range(500): rollout(node,2)
    a = np.argmax([
        child.score_estimate_2
        for child in node.children(2)
        ])
    
    return node.children(2)[a]

def mcts_3(node):
    for _ in range(500): rollout(node,3)
    a = np.argmax([
        child.score_estimate_3
        for child in node.children(3)
        ])
    
    return node.children(3)[a]
class TicTacToe(object):
    def __init__(self, board,size):
        self.board = board.copy()
        self.size=size

    #checks if a state is leaf node
    def is_leaf(self):
        if self.evaluate() != 0: return True
        return False
    def score_for_max_player(self,current_player):
        #max player is AI(2,3)
        score=-1
        winner=self.evaluate()
        if winner==current_player:
            score=1
        if winner== -1:
            score=0
        return score #score is 1 if current AI wins the round,-1 if it loses and 0 if it draws

    def is_max_players_turn(self):
        return (self.board == 1).sum() == (self.board == 2).sum()

    def is_min_players_turn(self):
        return not self.is_max_players_turn()

    def valid_actions(self):
        return list(zip(*np.nonzero(self.board == 0)))

    def place(self, player, position):
        if self.board[position[0], position[1]] == 0:
            self.board[position[0], position[1]] = player
            return True
        else:
            print("Cannot place in that position.")
            return False
    def perform(self, action,current_player):
        row, col = action
        new_state = TicTacToe(self.board,self.size)
        new_state.board[row, col] = current_player
        return new_state
    #checks Row win
    def row_win(self, player):
        return np.any((np.all(self.board == player, axis=1)))

    #checks Column win
    def col_win(self, player):
        return np.any((np.all(self.board==player, axis=0)))

    #checks diagonal win
    def diag_win(self, player):
        diag1 = self.board.diagonal()  #array([board[0,0], board[1,1], board[2,2]])
        diag2 = np.fliplr(self.board).diagonal()#np.array([board[0,2], board[1,1], board[2,0]])
        return np.all(diag1 == player) or np.all(diag2 == player)
    #returns a list of scores fro three players
    def get_score(self):
        score=self.evaluate()
        if(score==1):
            player1_score=1
            player2_score=-1
            player3_score=-1
        elif(score==2):
            player1_score=-1
            player2_score=1
            player3_score=-1
        elif(score==3):
            player1_score=-1
            player2_score=-1
            player3_score=1
        else:
            player1_score=0
            player2_score=0
            player3_score=0
        return [player1_score,player2_score,player3_score]
        
    #checks for a winner
    def evaluate(self):
        winner = 0
        players=[1,2,3]
        for player in players:
            if self.row_win(player) or self.col_win(player) or self.diag_win(player) :
                winner = player
        if np.all(self.board != 0) and winner == 0:#draw
            winner = -1
        return winner # -1 for draw [1,2,3] according to winner

    def play_game(self):
        print("To place your position, indicate the row number and the column number with a space.(like 2 3)")
        winner = 0
        while winner == 0:
            players = helper()
            for player in players:
                if(player==1):
                    print("\n")
                    print(f"You are player {player}")
                    
                    position = input("What position do you want to place? ")
                    print("You want to place at {} position.".format(position))

                    a_list = position.split()
                    map_object = map(int, a_list)
                    position = list(map_object)
                    self.place(player,position)    
                    print(self.board)
                    winner = self.evaluate()
                    if winner > 0:
                        print(f"Player {winner} wins!!!!!!!!")
                        break
                    elif winner == -1:
                        print("It's a draw!")
                        break
                    print()
                else:
                    print(f"AI {player}'s turn")
                    if(player==2):
                        child = mcts_2(Node(self))
                        self=child.state
                    else:
                        child = mcts_3(Node(self))
                        self=child.state
                    print(self.board)
                    winner = self.evaluate()
                    if winner > 0:
                        print(f"Player {winner} wins!!!!!!!!")
                        break
                    elif winner == -1:
                        print("It's a draw!")
                        break
                    print()
        return winner
    

def print_header():
    print("---------------------------------------------------------------------")
    print("         TIC TAC TOE WITH RANDOMIZED PLAYER SELECTION")
    print("---------------------------------------------------------------------\n")



def helper():
    b=[]
    while(True):
        player=random.randint(1,3)
        if(player not in b):
            b.append(player)
        if(len(b)==3):
            return b
    
def initial_state():
    size = int(input("Enter a board size(Greater than 2):"))
    '''while (size < 3):
        size = int(input("Enter valid board size(Greater than 2):"))'''
    board = np.empty((size,size), dtype=int)
    board[:] = 0
    return TicTacToe(board,size)
        
if __name__ == "__main__":
    print_header()
    start = input("Do you want to play a game? (y/n) ")
    if start.lower() in ["y", "yes"]:
        repeat = True
        while repeat:
            state = initial_state()
            state.play_game()
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
        
 
    
