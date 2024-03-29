from random import randint
from tracemalloc import start
from BoardClasses import Move
from BoardClasses import Board
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
import math
# import time as t

# What is a leaf node? : https://ai.stackexchange.com/questions/25426/unclear-definition-of-a-leaf-and-diverging-utc-values-in-the-monte-carlo-tree
# Some struggles - what is a leaf node? How to define it in the context of MCTS
#                - Best parameters for C and ITERATIONS
#                - Should I implement a heuristic?
#                - How to improve runtime efficiency?

C = math.sqrt(2)
ITERATIONS = 500

class Node():
    def __init__(self, board_history, color, parent, unexplored_children, move=None):
        self.board_history = board_history
        self.move = move
        self.color = color
        self.parent = parent
        self.unexplored_children = unexplored_children
        self.unexplored_children_length = len(unexplored_children)

        self.s_i = 0
        self.w_i = 0 
        self.children = []

    def update_history(self, move):
        self.board_history.append(move)



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

        self.board.saved_move = []
        get_all_possible_moves = [move for move_list in self.board.get_all_possible_moves(self.color) for move in move_list]
        self.root = Node([], self.color, None, get_all_possible_moves, None)
            
        i = 0
        while (i < ITERATIONS):
            to_expand = self.selection(self.root)
            child = self.expand(to_expand)
            winner_color = self.simulation(child)
            self.backpropogate(child, winner_color)            
            i += 1
        
        curr_max_val = float('-inf') 
        best_move = None
        for node in self.root.children:
            if node.s_i > curr_max_val:
                curr_max_val = node.s_i
                best_move = node.move
        self.board.make_move(best_move, self.color)

        return best_move

    def update_board(self, root):
        color = self.color # Since starting from self.root.
        for move in root.board_history: # Update board w/ root_history
            self.board.make_move(move, color)
            color = self.opponent[color]
    
    def undo_board(self):
        while self.board.saved_move != []:
            self.board.undo()
            
    def selection(self, root):
        if root.children == [] or root.unexplored_children_length != 0:
            return root
        else:
            best_score = float('-inf')
            for child in root.children:
                score = self.uct_score(child)
                if score > best_score:
                    best_score = score
                    node = child
            return self.selection(node)

    def expand(self, root):
        if root.unexplored_children_length == 0:
            # This is a terminal node.
            return root

        self.update_board(root)

        index = randint(0, root.unexplored_children_length-1)
        move = root.unexplored_children.pop(index)
        root.unexplored_children_length -= 1

        new_history = list(root.board_history)
        new_history.append(move)

        self.board.make_move(move, root.color)
        new_color = self.opponent[root.color]

        get_all_possible_moves = [move for move_list in self.board.get_all_possible_moves(new_color) for move in move_list]
        node = Node(new_history, new_color, root, get_all_possible_moves, move)

        root.children.append(node)

        return node
        
    def simulation(self, root):
        board = self.board

        turn_table = {1: "W", 2: "B"}
        player = root.color

        while True:

            winner = board.is_win(turn_table[player])
            if winner != 0:
                break

            moves = board.get_all_possible_moves(player)
            winner = board.is_win(turn_table[player])
            print(winner, player, moves)
            index = randint(0, len(moves)-1)
            inner_index = randint(0, len(moves[index])-1)
            move = moves[index][inner_index]
            board.make_move(move, player)


            player = self.opponent[player]

        self.undo_board()
        return winner
    
    def backpropogate(self, root, winner):
        while root != None:
            root.s_i += 1 # Always increment
            if root.color != winner:
                root.w_i += 1
            
            root = root.parent
