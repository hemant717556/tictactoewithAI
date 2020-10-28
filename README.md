# tictactoewithAI

This application implements the board game TicTacToe with modifications to the classic 3x3 board with just 2 players.
This app provides the users with the flexibility of deciding the size of the board and selects the player turns randomly instead of going in a particular order.

## How to run:
Ensure that you have Python 3.0 or higher installed on your device(necessary for using matplotlib).
Use cd <file directory> to change the directory to where your file is stored. 

## Libraries Used:
>Numpy Library 

## Installing Libraries(Use Python v3 or higher):
sudo apt install python3
pip install numpy


## Build and run the app:
python tictactoe.py

## Demo:
C:\Users\jaysh>cd C:\Users\jaysh\OneDrive\Desktop\Syracuse\AI\Project  'Enter the file directory after cd'

-------------------------------
      
Do you want to play a game? (y/n) y    #Enter your input here
y
Enter a board size(Greater than 3):4    #Enter your preferred board size here 
Here is the board.
[[0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]
 [0. 0. 0. 0.]]

To place your position, indicate the row number and the column number with spaces.


You are player 2    #Player selected at random
What position do you want to place? 22    #Enter your preferred position here(Ranging from [0][0] to [size][size])

-------------------------------
## Conclusion:
Once the game is finished i.e. reached its result state, the user will be asked if they would like to play again or exit.
