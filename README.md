# tictactoewithAI

This application implements the board game TicTacToe for 3 players with modifications to the classic 3x3 board.
This application provides the users with the flexibility of deciding the size of the board and selects the player turns randomly instead of going in a particular order and the player's turn is randomized.

## Dependency
- Python3
- Numpy
- PyTorch
- Matplotlib



## How to Run

- First, Install the python modules which are specified above.
- Download the zipped folder
- Go to the directory
- Run python final.py
- It will ask you if you want to play(Yes or No)
- Then you will have to enter a board size.And size should be between 4 to 8.
- Then it will ask "What the player1, player2 and player3 should be??"

  Options:

  1.Human 	 2.Baseline AI 	 3.TreeBased AI 	 4.Treebased+ NN AI
  Enter your choice of options having a space in between(e.g. 1 2 3)
  
  1 2 3 means player1-Human player2-BaselineAi player3-TreeBased AI
  
- Enter 4 (i.e. Treebased + NN just for player 3).Our code is trained for player 3

- For user,You need to give indexes in "What position do you want to place?(please enter valid position with a space in between)" like 1 3

- For Baseline AI,a random place will be choosen.

- After Tree based AI and Tree based + NN,Please press Enter to go to next step

- After the game ends,It will again ask if you want to play again.



## My Solution

### Task 1
- Created a new type called ReportingStructure, that has two properties: employee and numberOfReports. 
- We need to find the number of employees those come under or report directly od indirectly to an employee.
- We can treat this problem as counting the nodes under a pecific root node.
- I am using DFS algorithm to count the number of reports under an employee.
- I have created a new GET endpoint,which accepts an employee id and returns the fully populated JSON file with employees who reports to the given employee.
- The values are computed on the fly and are not persisted.

### Task 2
- Created a new type, Compensation with fields: employee, salary, and effectiveDate.
- Created a GET endpoint to get the compensation details of an employee.It accepts an employeeId.
- Valid id check has been done.
- Also created a POST endpoint to create the compensation object of a specific employee.
- For POST,the request body only needs a valid employeeID,salary and effective date.
- Compensation can only be created for the existing employees. 


