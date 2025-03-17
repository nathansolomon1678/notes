#include <iostream>
#include <string>
#include <vector>
#include <iomanip>
#include "ls_set.h"


int main() {
    ls_set<int***> ls;
    int i1 = 1, i2 = 2, i3 = 3;
    int j1 = 1;
    int *p1 = &i1, *p2 = &i2, *p3 = &i3;
    int *q1 = &j1, *q2 = &i2;
    int **pp1 = &p1, **pp2 = &p2, **pp3 = &p3;
    int **pq1 = &q1, **pq2 = &q2;
    ls.insert(&pp1); ls.insert(&pq1);
    ls.insert(&pp2); ls.insert(&pq2);
    ls.insert(&pp3);    ls.erase(1);
    std::cout << ls.find(1) << ' ' << ls.find(2) << ' ';
    std::cout << ls.size( ) << ' ';
    std::cout << std::endl;

    return 0;
}
