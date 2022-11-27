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
        # self.time_table = {
        #     "selection": 0,
        #     "expand": 0,
        #     "simulation": 0,
        #     "backpropagate": 0,
        #     "check": 0,
        #     "choose": 0,
        # }

        # Debug

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
            print(i)
            # start = t.time()
            to_expand = self.selection(self.root)
            # end = t.time()
            # self.time_table["selection"] += (end-start)

            # start = t.time()
            child = self.expand(to_expand)
            # end = t.time()
            # self.time_table["expand"] += (end-start)

            # start = t.time()
            winner_color = self.simulation(child)
            # end = t.time()
            # self.time_table["simulation"] += (end-start)

            # start = t.time()
            self.backpropogate(child, winner_color)
            # end = t.time()
            # self.time_table["backpropagate"] += (end-start)
            
            i += 1
        
        curr_max_val = float('-inf') 
        best_move = None
        for node in self.root.children:
            if node.s_i > curr_max_val:
                curr_max_val = node.s_i
                best_move = node.move
        self.board.make_move(best_move, self.color)
        
        # for name, time in self.time_table.items():
        #     print(f"{name}: {time} seconds.")

        # self.time_table = {
        #     "selection": 0,
        #     "expand": 0,
        #     "simulation": 0,
        #     "backpropagate": 0,
        #     "check": 0,
        #     "choose": 0,
        # }
        return best_move

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

    def update_board(self, root):
        color = self.color # Since starting from self.root
        # print("start")
        for move in root.board_history: # Update board w/ root_history
            # print(color, move)
            self.board.make_move(move, color)
            color = self.opponent[color]
    
    def undo_board(self):
        while self.board.saved_move != []:
            self.board.undo()
            
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

        # self.undo_board() # Undo changes to original board
        root.children.append(node)

        return node
        
    def simulation(self, root):
        # self.update_board(root)
        board = self.board
        # print("Simulated Start Board: ")
        # self.board.show_board()

        turn_table = {1: "W", 2: "B"}
        player = root.color

        # time_table = {
        #     "check": 0,
        #     "choose": 0,
        # }

        while True:
            # s = t.time()
            winner = board.is_win(turn_table[player])
            # time_table["check"] += (t.time()-s)
            if winner != 0:
                break

            # moves = board.get_all_possible_moves(player)
            # s = t.time()
            moves = board.get_all_possible_moves(player)
            index = randint(0, len(moves)-1)
            inner_index = randint(0, len(moves[index])-1)
            move = moves[index][inner_index]
            board.make_move(move, player)
            # time_table["choose"] += (t.time()-s)


            player = self.opponent[player]

        # for name, time in time_table.items():
        #     self.time_table[name] += time

        self.undo_board()
        return winner
    
    def backpropogate(self, root, winner):
        while root != None:
            root.s_i += 1 # Always increment
            if root.color != winner:
                root.w_i += 1
            
            root = root.parent
