from random import randint
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
import math
import copy

C = 2

class Node():
    def __init__(self, board, s_p):
        self.board = copy.deepcopy(board)
        self.s_i = 0
        self.w_i = 0 
        self.s_p = s_p
        self.children = []
    
class StudentAI():
    @staticmethod
    def uct_score(w_i, s_i, s_p):
        return (w_i/s_i) + C*(math.sqrt(math.log(s_p)/s_i))

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2

        self.root = Node(self.board, 0)

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)


        self.board.make_move(move,self.color)
        return move

    def selection(self):
        root = self.root

        while root.children != []:
            best_uct_value = float('-inf')
            best_uct_node = None
            for child in root.children:
                uct_value = StudentAI.uct_score(child.w_i, child.s_i, child.s_p)
                if uct_value > best_uct_value:
                    best_uct_value = uct_value
                    best_uct_node = child

            if best_uct_node is not None:
                root = best_uct_node
            else:
                self.expand(root)
                # 1. Run simulation
                # 2. Update root values
                break

        return # Move 
    
    def expand(self, root):
        moves = root.board.get_all_possible_moves(self.color)
        

    def simulation(self):
        pass
                
        

if __name__ == "__main__":
    pass
