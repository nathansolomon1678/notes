#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include "SimpleSet.h"


int main() {
    simple_set<float> floats;
    floats.insert(2.2f);
    floats.insert(4.4f);
    floats.insert(4.4f);
    floats.insert(0.98333f);
    floats.insert(-0.98333f);
    std::cout << std::boolalpha;
    std::cout << "floats:\n";
    std::cout << floats.find(4.4f) << '\n';
    std::cout << floats.find(19.f) << '\n';
    std::cout << floats.size() << '\n';
    
    simple_set<int*> ints;
    int i1 = 1, i2 = 2, i3 = 3, i4=6, i5=1;
    ints.insert(&i1);
    ints.insert(&i2);
    ints.insert(&i3);
    ints.insert(&i4);
    ints.insert(&i5);
    ints.erase(3);
    std::cout << "ints:\n";
    std::cout << ints.find(1) << '\n';
    std::cout << ints.find(3) << '\n';
    std::cout << ints.size() << '\n';
    
    simple_set<bool> bools;
    bools.insert(true);
    bools.insert(true);
    bools.insert(false);
    std::cout << "bools:\n";
    std::cout << bools.find(true) << '\n';
    std::cout << bools.find(false) << '\n';
    bools.erase(false);
    std::cout << bools.size() << '\n';
    return 0;
}
