#ifndef STUDENTAI_H
#define STUDENTAI_H
#include "AI.h"
#include "Board.h"
#include <vector>
#pragma once

//The following part should be completed by students.
//Students can modify anything except the class name and exisiting functions and varibles.
#include <random>

class Node
{
public:
    Node(vector<Move> boardHist, int color, Node* parent, vector<Move> unexploredChildren, Move* move);
	~Node();
    void deallocate(Node* node);
    void addHistory(Move move);
    void printChildren();

    vector<Move> boardHist;
    vector<Move> unexploredChildren;
    vector<Node*> children;
    Move* move;
    Node* parent;
    int color;
    int unexploredChildrenLen;

    double s_i;
    double w_i;
};

class StudentAI :public AI
{
public:
    Board board;
	Node* root;
	StudentAI(int col, int row, int p);
	virtual Move GetMove(Move board);

	void updateBoard(Node* node);
	void undoBoard();
	double uctScore(Node* node);

	Node* selection(Node* node);
	Node* expand(Node* node);
	int simulation(Node* node);
	void backpropagate(Node* node, int winner);

};



#endif //STUDENTAI_H

