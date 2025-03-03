#ifndef compare_h
#define compare_h
#include <filesystem>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
namespace fs = std::filesystem;
class CompareFiles {
public:
    CompareFiles(const std::string&, const std::string&);
    CompareFiles(const fs::path&, const fs::path&);
    void show_stats() const;
private:
    fs::path p1;
    fs::path p2;
    std::string common;
    std::string longestCommonSubsequence(std::string X, std::string Y);
};
#endif /* compare_h */
