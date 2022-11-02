from random import randint
from tracemalloc import start
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
import math
import copy

C = 2
ITERATIONS = 3

class Node():
    def __init__(self, board, color, previous, move=None):
        self.board = copy.deepcopy(board)
        self.move = move
        self.color = color
        self.previous = previous

        self.s_i = 0
        self.w_i = 0 
        self.children = []
    
    def recalculate(self):
        w_i = 0
        s_i = 0
        for child in self.children:
            w_i += child.s_i - child.w_i
            s_i += child.s_i
        self.w_i = w_i
        self.s_i = s_i
    
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
        return (node.w_i/node.s_i) + C*(math.sqrt(math.log(node.previous.s_i)/node.s_i))

    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        self.root = Node(self.board, self.color, None)

        i = 0
        while (i < ITERATIONS):
            self.selection(self.root)
            i += 1
        
        curr_max_val = float('-inf') 
        best_move = None
        for node in self.root.children:
            if node.s_i > curr_max_val:
                curr_max_val = node.s_i
                best_move = node.move
        print(self.board.is_valid_move(best_move))

        self.board.make_move(best_move, self.color)
        return move

    def selection(self, root):
        if root.children == []:
            self.expand(root)
            root.recalculate()
        else:
            best_uct_value = float('-inf')
            best_uct_node = None
            for child in root.children:
                uct_value = self.uct_score(child)
                if uct_value > best_uct_value:
                    best_uct_node = child
            self.selection(best_uct_node)
            # Recalulate root's variables
            root.recalculate()
            
    def expand(self, root):
        color = 2 if root.color==1 else 1 # FIX ME
        moves = root.board.get_all_possible_moves(root.color)

        for move1 in moves:
            for move in move1:
                # Create New Nodes
                board = copy.deepcopy(self.board)
                board.make_move(move, root.color)
                node = Node(board, color, root, move)
                root.children.append(node)

                # Simulate
                winner = self.simulation(root.board, color)
                if winner != color:
                    node.w_i += 1
                node.s_i += 1
        
    def simulation(self, board, player):
        board = copy.deepcopy(board)

        while winner:=(board.is_win(player)):
            
            moves = board.get_all_possible_moves(player)
            index = randint(0, len(moves)-1)
            inner_index = randint(0, len(moves[index])-1)
            move = moves[index][inner_index]
            board.make_move(move, player)

            player = (2 if player == 1 else 1) # FIX ME

        return winner

if __name__ == "__main__":
    pass
