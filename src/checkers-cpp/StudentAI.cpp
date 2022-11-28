#include "StudentAI.h"
#include <random>
#include <limits>

//The following part should be completed by students.
//The students can modify anything except the class name and exisiting functions and varibles.
double C = sqrt(2);
int ITER = 500;

Node::Node(vector<Move> boardHist, int color, Node* parent, vector<Move> unexploredChildren, Move* move)
    :boardHist{boardHist}, color{color}, parent{parent}, unexploredChildren{unexploredChildren}, move{move}
{
    children;
    unexploredChildrenLen = unexploredChildren.size();

    s_i = 0;
    w_i = 0;
}

Node::~Node()
{
    for (int i = 0; i < this->children.size(); ++i)
    {
        delete this->children[i]->move;
        delete this->children[i];
    }
}

void Node::deallocate(Node* node)
{
    // for (int i = 0; i < node->children.size(); ++i)
    // {
    //     delete node->children[i]->move;
    //     delete node->children[i];
    // }
}

void Node::printChildren()
{
    cout << "  Children" << endl;
    for (int i = 0; i < children.size(); ++i)
    {
        cout << "    " << children[i] << endl;
    }
}

void Node::addHistory(Move move)
{
    boardHist.push_back(move);
}

StudentAI::StudentAI(int col,int row,int p)
	:AI(col, row, p)
{
    board = Board(col,row,p);
    board.initializeGame();
    player = 2;
    root = NULL;
}

vector<Move> flattenVect(vector<vector<Move>> moves)
{
    vector<Move> flattenedVec;
    for (int i = 0; i < moves.size(); ++i)
    {
        for (int j = 0; j < moves[i].size(); ++j)
        {
            flattenedVec.push_back(moves[i][j]);
        }
    }
    return flattenedVec;
}

Move StudentAI::GetMove(Move move)
{
    if (move.seq.empty())
    {
        player = 1;
    } else{
        board.makeMove(move,player == 1?2:1);
    }
    
    board.saved_move_list.clear();
    vector<vector<Move>> getAllMoves = board.getAllPossibleMoves(player);

    vector<Move> emptyVector;

    Node* parent;
    root = new Node(emptyVector, player, NULL, flattenVect(getAllMoves), NULL); 
    
    int i = 0;
    Node* toExpand;
    Node* child;
    int winner;

    while (i < ITER)
    {
        // cout << "Loop: " << i << endl;
        toExpand = selection(root);
        // cout << "1" << endl;
        child = expand(toExpand);
        // cout << "2" << endl;
        winner = simulation(child);
        // cout << "3" << endl;
        backpropagate(child, winner);
        // cout << "4" << endl;
        ++i;
    }

    // cout << "loop finished" << endl;
    double currMax  = -INFINITY;
    Node* bestMove = NULL;
    root->children.size();
    for (int i = 0; i < root->children.size(); ++i)
    {
        // cout << i << endl;
        if ((root->children[i])->s_i > currMax)
        {
            currMax = root->s_i;
            bestMove = root->children[i];
        }
    }
    // cout << "loop finished" << endl;
    // cout << bestMove->move->toString() << endl;
    Move bestMv = *(bestMove->move);
    board.makeMove(bestMv, player);
    // board.showBoard();
    delete root;
    return bestMv;
}

void StudentAI::updateBoard(Node* node)
{
    int p = player;
    // board.showBoard();
    for (int i = 0; i < node->boardHist.size(); ++i)
    {
        // cout << p << " & " << node->boardHist[i].toString() << endl;
        board.makeMove(node->boardHist[i], p);
        p = (p == 1?2:1);
    }
}
void StudentAI::undoBoard()
{
    while (board.saved_move_list.size() != 0)
    {
        board.Undo();
    }
}
double StudentAI::uctScore(Node* node)
{
    // return (node.w_i/node.s_i) + C*(math.sqrt(math.log(node.parment.s_i)/node.s_i))
    return (node->w_i / node->s_i) + C*(sqrt(log(node->parent->s_i/node->s_i)));
}

Node* StudentAI::selection(Node* node)
{
    if (node->children.size() == 0 || node->unexploredChildrenLen != 0)
    {
        return node;
    }
    else
    {
        Node* best_node = NULL;
        double best_score = -INFINITY;
        double score;
        for (int i = 0; i < node->children.size(); ++i)
        {
            score = uctScore(node->children[i]);
            // cout << i << ": " << node->children[i] << " " << node->s_i << " " <<  node->w_i << endl;
            
            if (score > best_score)
            {
                best_score = score;
                best_node = node->children[i];
            }
        }
        // cout << "Best: " << best_node << endl;
        // cout << best_node->children.size() << endl;
        // cout << best_node->unexploredChildrenLen << endl;
        return selection(best_node);

    }
}

Node* StudentAI::expand(Node* node)
{
    if (node->unexploredChildrenLen == 0)
    {
        return node;
    }

    updateBoard(node);

    int index = rand() % (node->unexploredChildrenLen);
    Move move = (node->unexploredChildren)[index];
    node->unexploredChildren.erase(node->unexploredChildren.begin()+index);
    node->unexploredChildrenLen--;

    vector<Move> newHistory; // Check if this copy is correct
    for (int i = 0; i < node->boardHist.size(); ++i)
    {
        newHistory.push_back(node->boardHist[i]);
    }
    newHistory.push_back(move);

    board.makeMove(move, node->color);
    int newPlayer = (node->color==1?2:1);
    Move* saveMove = new Move(move);

    Node* newNode = new Node(newHistory, newPlayer, node, flattenVect(board.getAllPossibleMoves(newPlayer)), saveMove);

    node->children.push_back(newNode);
    return newNode;
}

int StudentAI::simulation(Node* node)
{
    int player = root->color;
    int winner;
    string p;
    vector<vector<Move>> moves;
    int outer_index;
    int inner_index;
    Move move;

    while (true)
    {
        if (player == 1)
        {
            p = "W";
        }
        else
        {
            p = "B";
        }
        winner = board.isWin(p);

        if (winner != 0)
        {
            break;
        }

        moves = board.getAllPossibleMoves(player);
        outer_index = rand() % moves.size();
        inner_index = rand() % moves[outer_index].size();
        move = moves[outer_index][inner_index];

        board.makeMove(move, player);
        player = (player == 1?2:1);

    }
    undoBoard();
    return winner;

}

void StudentAI::backpropagate(Node* node, int winner)
{
    while (node != NULL)
    {
        node->s_i++;
        if (node->color != winner)
        {
            root->w_i++;
        }
        node = node->parent;
    }
}

