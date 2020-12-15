import numpy as np
import random

def helper():
    return np.random.permutation([1,2,3])

class TicTacToe(object):
    def __init__(self, board,size):
        self.board = board.copy()
        self.size=size

    #checks if a state is leaf node
    def is_leaf(self):
        if self.evaluate() != 0: return True
        return False

    #returns the score of AI
    '''def score(self,current_player):
        #max player is AI(2,3)
        score=-1
        winner=self.evaluate()
        if winner==current_player:
            score=1
        if winner== -1:
            score=0
        return score #score is 1 if current AI wins the round,-1 if it loses and 0 if it draws'''

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
    # def row_win(self, player):
    #     return np.any((np.all(self.board == player, axis=1)))

    # #checks Column win
    # def col_win(self, player):
    #     return np.any((np.all(self.board==player, axis=0)))

    # #checks diagonal win
    # def diag_win(self, player):
    #     diag1 = self.board.diagonal()  #array([board[0,0], board[1,1], board[2,2]])
    #     diag2 = np.fliplr(self.board).diagonal()#np.array([board[0,2], board[1,1], board[2,0]])
    #     return np.all(diag1 == player) or np.all(diag2 == player)

    #checks Row win
    def row_win(self, player):
        len = self.size - 2
        for row in range(len):
            for col in range(len):
                board1 = self.board[row:row+3,col:col+3]
                if np.any((np.all(board1==player,axis=1))):# and self.board[row,col+1]==player and self.board[row,col+2]==player:
                    return True
        return False
        #return np.any((np.all(self.board == player, axis=1)))
    #checks Column win
    def col_win(self, player):
        # for col in self.board:
        #     for row in col-3:
        #         if self.board[row,col]==player and self.board[row+1,col]==player and self.board[row+2,col]==player:
        #             return True
        # return False
        len = self.size - 2
        for col in range(len):
            for row in range(len):
                board1 = self.board[row:row+3,col:col+3]
                if np.any((np.all(board1==player,axis=0))):# and self.board[row,col+1]==player and self.board[row,col+2]==player:
                    return True#
        return False
        # return np.any((np.all(self.board==player, axis=0)))

    #checks diagonal win
    def diag_win(self, player):
        len = self.size - 2
        for row in range(len):
            for col in range(len):
                board1 = self.board[row:row+3,col:col+3]
                diag1 = board1.diagonal()  #array([board[0,0], board[1,1], board[2,2]])
                diag2 = np.fliplr(board1).diagonal()#np.array([board[0,2], board[1,1], board[2,0]])
                if np.all(diag1 == player) or np.all(diag2 == player):
                    # print("---------------------------")
                    return True
        return False
        # diag1 = self.board.diagonal()  #array([board[0,0], board[1,1], board[2,2]])
        # diag2 = np.fliplr(self.board).diagonal()#np.array([board[0,2], board[1,1], board[2,0]])
        # return np.all(diag1 == player) or np.all(diag2 == player)
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

    
    