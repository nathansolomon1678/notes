#ifndef BINARY_SEARCH_TREE_H
#define BINARY_SEARCH_TREE_H

#include <string>
#include <stack>
#include <queue>

class BinarySearchTree;
class Iterator;
class Node;


class Node {
public:
    static long int ncall;
    //equals the total number of constructor calls
    Node(){
        left=nullptr;
        right = nullptr;
        ncall++;
    };
private:
    std::string data;
    Node* left;
    Node* right;
    friend class BinarySearchTree;
    friend class BreadthFirstIterator;
    friend class Iterator;
};
long int Node::ncall = 0;


class Iterator {
public:
    /**
       Looks up the value at a position.
       @return the value of the node to which the iterator points
    */
    std::string get() const;
    /**
       Advances the iterator to the next node.
       Inorder Traversal
    */
    void next();
    /**
       Compares two iterators.
       @param other the iterator to compare with this iterator
       @return true if this iterator and other are equal
    */
    bool equals(const Iterator& other) const;
    bool isend() const;
private:
    const BinarySearchTree* container;
    std::stack<Node*> nodeStack;
    //Stack: Typically used for in - order, pre - order, or post - order traversal.
    //Queue : Used for level - order traversal(BFS).
    friend class BinarySearchTree;
};



/*
   This class implements a binary search tree whose
   nodes hold strings.
*/
class BinarySearchTree {
public:
    /**
       Constructs an empty tree.
    */
    BinarySearchTree();
    /**
       Inserts a new node into the tree.
       @param element the element to insert
    */
    void insert(std::string element);
    /**
       Tries to find an element in the tree.
       @param element the element to find
       @return 1 if the element is contained in the tree
    */
    int count(std::string element) const;
    /**
       Tries to remove an element from the tree. Does nothing
       if the element is not contained in the tree.
       @param element the element to remove
    */
    void erase(std::string element);
    /**
       Prints the contents of the tree in sorted order.
    */
    void print() const;
    /**
   Returns an iterator to the beginning of this BinarySearchTree.
   @return a BinarySearchTree iterator to the beginning
*/
    Iterator begin() const;
    /**
       Returns an iterator past the end of this BinarySearchTree.
       @return a BinarySearchTree iterator past the end
    */
    Iterator end() const;
    /**
Returns an BreadthFirstIterator to the beginning of this BinarySearchTree.
@return a BinarySearchTree iterator to the beginning
*/
    BreadthFirstIterator Bbegin() const;
    /**
       Returns an BreadthFirstIterator past the end of this BinarySearchTree.
       @return a BinarySearchTree iterator past the end
    */
    BreadthFirstIterator Bend() const;
private:
    /**
       Prints a node and all of its descendants in sorted order.
       @param parent the root of the subtree to print
    */
    void print(Node* parent, int indent, char symbol) const;
    /**
       Inserts a new node as a descendant of a given node.
       @param parent the root node
       @param new_node the node to insert
    */
    void add_node(Node* parent, Node* new_node) const;
    Node* root;
    friend class Iterator;
    friend class BreadthFirstIterator;
};


/**
   This iterator visits the nodes of a tree in
   breadth-first order.
*/
class BreadthFirstIterator {
public:
    /**
       Constructs an iterator for a given tree.
       @param root the root of the tree
    */
    BreadthFirstIterator(Node* root);
    /**
       Gets the element to which this iterator points.
       @return the element
    */
    std::string get() const;
    /**
       Advances this iterator to the next position.
    */
    void next();
    bool equals(const BreadthFirstIterator& other) const;
    bool isend() const;
private:
    std::queue<Node*> q;
};


#endif
