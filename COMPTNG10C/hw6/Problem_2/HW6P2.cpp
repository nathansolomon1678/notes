#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include "selection_sort_template.h"

bool compareSquares(int x, int y) {
    return x * x < y * y;
};
auto bySize = [](const std::string& x, const std::string& y) -> bool { return x.size() < y.size(); };

int main() {
	std::vector<int> container1 = {3, 1, 4, -5, 6, 9};
	auto begin1 = std::begin(container1);
	auto end1 = std::end(container1);
	selection_sort(begin1, end1);
	for (auto it = begin1; it != end1; ++it) {
		std::cout << *it << " ";
    }
	std::cout << std::endl;
	double container2[6] = {3, 1, 4, -5, 6, 9};
	auto begin2 = std::begin(container2);
	auto end2 = std::end(container2);
	selection_sort(begin2, end2,&compareSquares);
	for (auto it = begin2; it != end2; ++it) {
		std::cout << *it << " ";
    }
	std::cout << std::endl;
	std::vector<std::string> container3 {"apple", "Kiwi", "orange"};
	auto begin3 = std::begin(container3);
	auto end3 = std::end(container3);
	selection_sort(begin3, end3, bySize);
	for (auto it = begin3; it != end3; ++it) {
		std::cout << *it << " ";
    }
	std::cout << std::endl;
    return 0;
}
