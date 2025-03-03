#include <iostream>
#include <string>
#include <vector>
#include <utility>
#include "do_for_each_template.h"

void Capitalize(std::string & str) {
    for (char& ch : str) {
        // converts a lowercase character to its uppercase
	    ch = std::toupper(ch);
    }
}

int main() {
	int a1 = 1, a2 = 2, a3 = 3, a4 = 4;
    do_for_each([](int& x) { x += 2; });
	do_for_each([](int& x) { x += 2; }, a1, a2, a3,a4);
	print(a1, a2, a3, a4);
	std::string str1 = "hello";
	std::string str2 = "world";
	do_for_each(Capitalize, str1, str2);
	print(str1, str2);
    return 0;
}
