
import numpy as np
import torch as tr
from torch.nn import Sequential, Conv2d, Linear, Flatten, ReLU, Tanh, Sigmoid

def TicTacToeNet1(board_size):
    model = Sequential(Flatten(),Linear(4*board_size**2, 2, True),Tanh(),Linear(2,1))
    return model
   

def calculate_loss(net, x, y_targ):
    y = net(x)
    e = tr.sum((y-y_targ)**2)
    return (y, e)
    

def optimization_step(optimizer, net, x, y_targ):
    optimizer.zero_grad()
    y, e = calculate_loss(net, x, y_targ)
    # print("Y:\n",y)
    e.backward()
    optimizer.step()
    return (y,e)
    
def helper(board_size):
    net = TicTacToeNet1(board_size=board_size)
    print(net)

    import pickle as pk
    with open("data1%d.pkl" % board_size,"rb") as f: (x, y_targ) = pk.load(f)
    optimizer = tr.optim.Adam(net.parameters())
    print(optimizer)
    train_loss, test_loss = [], []
    shuffle = np.random.permutation(range(len(x)))
    split = 5
    train, test = shuffle[:-split], shuffle[-split:]
    
    for epoch in range(500):
        y_train, e_train = optimization_step(optimizer, net, x[train], y_targ[train])
        y_test, e_test = calculate_loss(net, x[test], y_targ[test])
        if epoch % 10 == 0: print("%d: %f (%f)" % (epoch, e_train.item(), e_test.item()))
        train_loss.append(e_train.item() / (len(shuffle)-split))
        np.seterr(divide='ignore', invalid='ignore')
        test_loss.append(e_test.item() / split)
    
    tr.save(net.state_dict(), "model%d.pth" % board_size)
    
    

    

