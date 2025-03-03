#include <iostream>
#include<iomanip> 
#include "binary_search_tree.h"

BinarySearchTree::BinarySearchTree() {
    root = nullptr;
}

void BinarySearchTree::insert(std::string element) {
    Node* new_node = new Node;
    new_node->data = element;
    new_node->left = nullptr;
    new_node->right = nullptr;
    if (root == nullptr) {
        root = new_node;
    } else {
        add_node(root, new_node);
    }
}

int BinarySearchTree::count(std::string element) const {
    Node* current = root;
    while (current != nullptr) {
        if (element < current->data) {
            current = current->left;
        } else if (element > current->data) {
            current = current->right;
        } else {
            return 1;
        }
    }
    return 0;
}

void BinarySearchTree::erase(std::string element) {
    Node* to_be_removed = root;
    Node* parent = nullptr;
    bool found = false;
    while (!found && to_be_removed != nullptr) {
        if (element == to_be_removed->data) {
            found = true;
        } else {
            parent = to_be_removed;
            if (element < to_be_removed->data) {
                to_be_removed = to_be_removed->left;
            } else {
                to_be_removed = to_be_removed->right;
            }
        }
    }
    if (!found) {
        return;
    }
    // to_be_removed contains element
    // If one of the children is empty, use the other

    if (to_be_removed->left == nullptr || to_be_removed->right == nullptr) {
        Node* new_child;
        if (to_be_removed->left == nullptr) {
            new_child = to_be_removed->right;
        } else {
            new_child = to_be_removed->left;
        }
        if (parent == nullptr) // Found in root {
            root = new_child;
        } else if (parent->left == to_be_removed) {
            parent->left = new_child;
        } else {
            parent->right = new_child;
        }
        return;
    }
    // Neither subtree is empty
    // Find smallest element of the right subtree
    Node* smallest_parent = to_be_removed;
    Node* smallest = to_be_removed->right;
    while (smallest->left != nullptr) {
        smallest_parent = smallest;
        smallest = smallest->left;
    }

    // smallest contains smallest child in right subtree
    // Move contents, unlink child
    to_be_removed->data = smallest->data;
    if (smallest_parent == to_be_removed) {
        smallest_parent->right = smallest->right;
    } else {
        smallest_parent->left = smallest->right;
    }
}

void BinarySearchTree::print() const {
    print(root, 0, ' ');
    std::cout << std::endl;
}

void BinarySearchTree::print(Node* parent, int indent, char symbol) const {
    if (parent == nullptr) {
        return;
    }
    print(parent->right, indent + 4, '/');
    // Print right subtree with increased indentation
    std::cout << std::setw(indent) << symbol << parent->data << std::endl;
    // Print current node with indentation
    print(parent->left, indent + 4, '\\'); 
    // Print left subtree with increased indentation
}

void BinarySearchTree::add_node(Node* parent, Node* new_node) const {
    if (new_node->data < parent->data) {
        if (parent->left == nullptr) {
            parent->left = new_node;
        } else {
            add_node(parent->left, new_node);
        }
    } else if (new_node->data > parent->data) {
        if (parent->right == nullptr) {
            parent->right = new_node;
        } else {
            add_node(parent->right, new_node);
        }
    }
}


Iterator BinarySearchTree::begin() const {
    Iterator iter;
    Node* current = root;
    while (current != nullptr) {
        iter.nodeStack.push(current);
        current = current->left;
    }
    iter.container = this;
    return iter;
}

Iterator BinarySearchTree::end() const {
    Iterator iter;
    iter.container = this;
    return iter;
}


std::string Iterator::get() const {
    if (!nodeStack.empty()) {
        return nodeStack.top()->data;
    } else {
        return "";
    }
}

bool Iterator::equals(const Iterator& other) const {
    if (nodeStack.size() != other.nodeStack.size()) {
        return false;
    }
    // Create temporary stacks to preserve the original stacks
    auto tempStack1 = nodeStack;
    auto tempStack2 = other.nodeStack;
    // Compare each element in the stacks
    while (!tempStack1.empty()) {
        if (tempStack1.top() != tempStack2.top()) {
            return false;  // Elements are different
        }
        tempStack1.pop();
        tempStack2.pop();
    }
    // Stacks are equal
    return true;  
}

bool Iterator::isend() const {
    return nodeStack.empty();
}

void Iterator::next() {
    if (!nodeStack.empty()) {
        Node* current = nodeStack.top();
        nodeStack.pop();
        // Move to the right subtree
        Node* rightChild = current->right;
        while (rightChild != nullptr) {
            nodeStack.push(rightChild);
            rightChild = rightChild->left;
        }
    }
}

BreadthFirstIterator BinarySearchTree::Bbegin() const {
    return BreadthFirstIterator(root);
}

BreadthFirstIterator BinarySearchTree::Bend() const {
    return BreadthFirstIterator(nullptr);
}

BreadthFirstIterator::BreadthFirstIterator(Node* root) {
    if (root != nullptr) {
        q.push(root);
    }
}

std::string BreadthFirstIterator::get() const {
    return q.front()->data;
}

void BreadthFirstIterator::next() {
    Node* n = q.front();
    q.pop();
    if (n->left != nullptr) {
        q.push(n->left);
    }
    if (n->right != nullptr) {
        q.push(n->right);
    }
}

bool BreadthFirstIterator::equals(const BreadthFirstIterator& other) const {
    return q.size() == 0 && other.q.size() == 0
        || q.size() > 0 && other.q.size() > 0
        && q.front() == other.q.front();
}

bool BreadthFirstIterator::isend() const {
    return q.empty();
}
