from random import randint
from tracemalloc import start
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
import math
import copy

C = 2
ITERATIONS = 5

class Node():
    def __init__(self, board, color, parent, move=None):
        self.board = copy.deepcopy(board)
        self.move = move
        self.color = color
        self.parent = parent

        self.s_i = 0
        self.w_i = 0 
        self.children = []
    
class StudentAI():
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        
        # My code
        self.root = None

    def uct_score(self, node):
        return (node.w_i/node.s_i) + C*(math.sqrt(math.log(node.parent.s_i)/node.s_i))

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        self.root = Node(self.board, self.color, None)

        i = 0
        while (i < ITERATIONS):
            to_expand = self.selection(self.root)
            child = self.expand(to_expand)
            winner_color = self.simulation(child)
            self.backpropogate(child, winner_color)
            i += 1
        
        # curr_max_val = float('-inf') 
        # best_move = None
        # for node in self.root.children:
        #     if node.s_i > curr_max_val:
        #         curr_max_val = node.s_i
        #         best_move = node.move
        # self.board.make_move(best_move, self.color)
        # return best_move

    def selection(self, root):
        ...
            
    def expand(self, root):
        ...
        
    def simulation(self, root):
        ...
    
    def backpropogate(self, root, winner):
        ...

if __name__ == "__main__":
    # Branch Test
    pass
