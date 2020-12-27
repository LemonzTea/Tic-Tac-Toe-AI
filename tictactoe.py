"""
Tic Tac Toe Player
"""

import math
import copy
from util import Node

# Possible moves of the board
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.

    1. Check if there is a winner
        a. Check if there is any remaining spaces

    2. Since X start first
        a. if X == O, means it is X's turn
        b. if X > O, means its O's turn
    """

    # No more possible moves to be made if there is a winner
    if winner(board) is not None:
        return None

    # If there is a no winner
    xCount = 0
    oCount = 0

    for row in board:
        for col in row:
            if col == X:
                xCount += 1
            elif col == O:
                oCount += 1
    
    # Check if there is any remaining spaces
    if xCount + oCount == 9:
        return None
    elif xCount == oCount:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    
    1. The actions function should return a set of all of the possible actions that can be taken on a given board.
        1. Each action should be represented as a tuple (i, j) where i corresponds to the row of the move (0, 1, or 2)
           and j corresponds to which cell in the row corresponds to the move (also 0, 1, or 2).
        2. Possible moves are any cells on the board that do not already have an X or an O in them.
        3. Any return value is acceptable if a terminal board is provided as input.
    """

    possibleActions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                possibleActions.add((row, col))

    if len(possibleActions) != 0:
        return possibleActions
    else:
        return None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    1. The result function takes a board and an action as input, and should return a new board state, without modifying the original board.
        1. If action is not a valid action for the board, your program should raise an exception.
        2. The returned board state should be the board that would result from taking the original input board, 
           and letting the player whose turn it is make their move at the cell indicated by the input action.
        3. Importantly, the original board should be left unmodified: since Minimax will ultimately require 
           considering many different board states during its computation. This means that simply updating a
           cell in board itself is not a correct implementation of the result function. You’ll likely want to
           make a deep copy of the board first before making any changes.
    """

    # Raise an exception if action is invalid
    if action is None:
        raise Exception("Invalid Action Made")

    # Deep Copy of the board
    resultBoard = copy.deepcopy(board)
    
    # Get current Player
    currentPlayer = player(board)

    # Update the resultBoard with the action
    resultBoard[action[0]][action[1]] = currentPlayer

    return resultBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check if player has won vertically
    def checkVerical(player):
        for col in range(len(board)):
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                return True
        return False

    # Check if player has won horizontally
    def checkHorizontal(player):
        for row in range(len(board[0])):
            if board[row][0] == player and board[row][1] == player and board[row][2] == player:
                return True
        return False

    # Check if player has won diagonally
    def checkDiagonally(player):
        diagonal_fromTopLeft = True
        diagonal_fromBottomLeft = True
        
        # Check Top Left to Bottom Right
        for i in range(len(board)):
            # print(f"{i},{i}, topleft")
            if board[i][i] != player:
                diagonal_fromTopLeft = False
                

        # Check Bottom Left to Top Right
        for col in reversed(range(len(board))):
            row = (len(board) - 1) - col
            # print(f"{row},{col} bottomLeft")
            if board[row][col] != player:
                diagonal_fromBottomLeft = False

        
        # If any return true, player has won
        if diagonal_fromBottomLeft or diagonal_fromTopLeft:
            return True
        else:
            return False

    # Check if player has won in any way possible
    def checkPlayer(player):
        if checkHorizontal(player) or checkVerical(player) or checkDiagonally(player):
            return True
        else:
            return False
        
    if checkPlayer(X):
        return X
    elif checkPlayer(O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there is a winner
    if winner(board) is not None:
        return True;
    
    # If there is a no winner
    xCount = 0
    oCount = 0

    for row in board:
        for col in row:
            if col == X:
                xCount += 1
            elif col == O:
                oCount += 1
    
    # Check if there is any remaining spaces
    if xCount + oCount == 9:
        return True
    else:
        return False



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winningPlayer = winner(board)

    if winningPlayer == X:
        return 1
    elif winningPlayer == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # ALPHA - best already explored option along path to the root for maximizer
    # BETA - best already explored option along path to the root for minimizer

    def MAX_VALUE(board, alpha, beta):
        if terminal(board):
            return utility(board)

        score = -999
        for action in actions(board):
            score = max(score, MIN_VALUE(result(board, action), alpha, beta))
            alpha = max(alpha, score)

            # if the best option for maximizer is > best option for beta
            # no need to look at other actions
            if alpha > beta:
                break;
        
        return score

    # If AI is O, the Ai will want to generate the lowest maximum score
    def MIN_VALUE(board, alpha, beta):
        if terminal(board):
            return utility(board)

        score = 999 
        for action in actions(board):
            score = min(score, MAX_VALUE(result(board, action), alpha, beta))
            beta = min (beta, score)

            # if the best option for minimizer is < best option for alpha
            # no need to look at other actions
            if beta < alpha:
                break
        
        return score
    
    currentPlayer = player(board)
    nodeList = []
    if currentPlayer == X:
        for action in actions(board):
            nodeList.append(Node(board, action, MIN_VALUE(result(board, action), -999, 999)))

        bestNode = nodeList[0]
        for node in nodeList:
            if node.score > bestNode.score:
                bestNode = node
        return bestNode.action   
    else:
        for action in actions(board):
            nodeList.append(Node(board, action, MAX_VALUE(result(board, action), -999, 999)))
        
        bestNode = nodeList[0]
        for node in nodeList:
            if node.score < bestNode.score:
                bestNode = node
        return bestNode.action