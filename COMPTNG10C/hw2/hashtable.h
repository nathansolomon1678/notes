#pragma once
#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <string>
#include <vector>


size_t hash_code(const std::string& str);

class HashTable;
class Iterator;
class Node;

// Node of a linked list for chaining buckets of hash table
class Node {
private:
    std::string data;
    Node* next;
    friend class HashTable;
    friend class Iterator;
};

class Iterator {
public:
    std::string get() const;
    void next();
    bool equals(const Iterator& other) const;
    bool operator==(const Iterator& other) const;
    void operator++();
    std::string operator*() const;
private:
    const HashTable* container;
    int bucket_index;
    Node* current;
    friend class HashTable;
};

class HashTable {
public:
    HashTable(size_t nbuckets);
    size_t count(const std::string& x);  // Return 0 if x is in the set, otherwise 0
    void insert(const std::string& x);
    void erase(const std::string& x);
    Iterator begin() const;
    Iterator end() const;
    size_t size() const;  // Return number of elements in set
    size_t buckets_size() const;  // Return number of buckets
private:
    std::vector<Node*> buckets;
    size_t current_size;
    float load_factor;
    void grow_if_necessary();
    friend class Iterator;
};

#endif
