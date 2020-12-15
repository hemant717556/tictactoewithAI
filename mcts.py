import numpy as np
import math

def puct(node,cp):
    
    c = np.argmax(puct_probs(node,cp))
    return node.children(cp)[c]
def puct_probs(node,cp):
    uct=[]
    sp=1
    
    if(node.child_list==None):
        node.make_child_list(cp)
    Q = node.get_score_estimates()
    for i, j in enumerate(node.children(cp)):
        
        u_c=(sp*Q[i][cp-1]) + ( math.log(node.visit_count+0.1) / (j.visit_count+1) )**0.5
        uct.append(u_c)
    
    return np.array(uct)
    

class Node(object):
    def __init__(self, state, depth = 0, choose_method=puct):
        
        self.depth = depth
        self.state = state
        self.visit_count = 0

        self.score_total = np.zeros((3,), dtype=int)
        
        self.score_estimate= np.zeros((3,), dtype=float)
        
        self.child_list = None 
        self.choose_method = choose_method

        #for selecting chance node
        self.count1=0
        self.count2=0
        self.count3=0

    def make_child_list(self,cp):
        self.child_list = []
        for i in self.state.valid_actions():
            child_state = self.state.perform(i,cp)
            self.child_list.append(Node(child_state, self.depth+1, self.choose_method))  
        
    def children(self,cp):
        if self.child_list is None: self.make_child_list(cp)
        return self.child_list

    def get_score_estimates(self):

        Q = np.array([[0,0,0]],dtype=np.ndarray)
        
        for child in self.child_list:
            #print("for child",child.state.board)
            
            a=np.array(child.score_total/(child.visit_count+0.1))
            # print("A:\n",a)
            np.seterr(divide='ignore', invalid='ignore')
            # print("Q\n:",Q)
            Q=np.append(Q,[a],axis=0)
        # print("Final Q\n",Q[1:len(Q)])
        return Q[1:len(Q)]


    def get_visit_counts(self):
        return np.vectorize(lambda x: x.visit_count)(self.child_list)
        
    def choose_child(self,cp):
        return self.choose_method(self,cp)

#this function will select a chance node player by exploration
def chance_node_selection(cnode):
    return np.argmin([cnode.count1,cnode.count2,cnode.count2])+1


def uct_score_update(cnode,chance_node_number,uct,max_depth):    
    if cnode.depth == max_depth or cnode.state.is_leaf():
        result=cnode.state.get_score()
        
    else:
        result=rollout(cnode,chance_node_number,max_depth)
    
    uct.score_total += result
    uct.visit_count += 1
    
    return uct.score_total

def rollout(node,current_player, max_depth=None):
    
    if node.depth == max_depth or node.state.is_leaf():
        
        result = node.state.get_score()    
        #count_node.append(node.visit_count)
    else:
        #selcts a children based on the uct value
        uct_node=node.choose_child(current_player)
        if uct_node.depth == max_depth or uct_node.state.is_leaf():
            return uct_node.state.get_score()
        
        #select a chance node according to exploration
        chance_node_number=chance_node_selection(uct_node)
        
        #to update the uct score and recursion will continue from this function
        result = uct_score_update(uct_node.choose_child(chance_node_number),chance_node_number,uct_node,max_depth)


    node.visit_count += 1  
    node.score_total +=result
    return node.score_total

#baseline ai    
def baseline(state,current_player):
    node = Node(state)
    chil_list=node.children(current_player)
    c = np.random.choice(len(chil_list))
    return c,node

def decide_action(state,current_player,choose_method, num_rollouts, max_depth=50, verbose=False):
    
    if choose_method==None:
        choose_method=puct
    node = Node(state)
    
    for n in range(num_rollouts):
        if verbose and n % 10 == 0: print("Rollout %d of %d..." % (n+1, num_rollouts))
        rollout(node,current_player, max_depth=max_depth)
    score=node.get_score_estimates()

    if(current_player==2):
        return np.argmax(score,axis=0)[1], node 
    return np.argmax(score,axis=0)[2], node 









        

 
    
