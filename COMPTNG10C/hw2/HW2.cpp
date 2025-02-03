#include <iostream>
#include <string>
#include <vector>

#include "hashtable.h"

int main() {
    HashTable myHashTable(2);

    myHashTable.insert("One");
    myHashTable.insert("Two");
    myHashTable.insert("Three");
    myHashTable.insert("Four");
    myHashTable.insert("Five");
    myHashTable.insert("Six");

    myHashTable.erase("Four");
    myHashTable.erase("Nine");
    for (auto it = myHashTable.begin(); !it.equals(myHashTable.end()); it.next()) {
        std::cout << it.get() << std::endl;
    }
    std::cout << myHashTable.count("Six") << std::endl;
    std::cout << myHashTable.size() << " " << myHashTable.buckets_size() << std::endl;
    for (int i = 0; i < 100; i++) {
        myHashTable.insert(std::to_string(i));
    }
    std::cout << myHashTable.size() << " " << myHashTable.buckets_size() << std::endl;
    for (int i = 0; i < 100; i++) {
        myHashTable.erase(std::to_string(i));
    }
    std::cout << myHashTable.size() << " " << myHashTable.buckets_size() << std::endl;

    return 0;
}
