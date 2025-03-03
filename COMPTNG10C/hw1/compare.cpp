#include "compare.h"

CompareFiles::CompareFiles(const std::string& p1, const std::string& p2) : p1(fs::path(p1)), p2(fs::path(p2)) {
    std::string line;

    std::string file_1_contents = "";
    std::ifstream ifs_1(this->p1.string());
    while (std::getline(ifs_1, line)) {
        for (char c : line) {
            if (!std::isspace(c)) {
                file_1_contents += c;
            }
        }
    }
    ifs_1.close();

    std::string file_2_contents = "";
    std::ifstream ifs_2(this->p2.string());
    while (std::getline(ifs_2, line)) {
        for (char c : line) {
            if (!std::isspace(c)) {
                file_2_contents += c;
            }
        }
    }
    ifs_2.close();

    common = longestCommonSubsequence(file_1_contents, file_2_contents);
}

CompareFiles::CompareFiles(const fs::path& p1, const fs::path& p2) : p1(p1), p2(p2) {
    std::string line;

    std::string file_1_contents = "";
    std::ifstream ifs_1(p1.string());
    while (std::getline(ifs_1, line)) {
        for (char c : line) {
            if (!std::isspace(c)) {
                file_1_contents += c;
            }
        }
    }
    ifs_1.close();

    std::string file_2_contents = "";
    std::ifstream ifs_2(p2.string());
    while (std::getline(ifs_2, line)) {
        for (char c : line) {
            if (!std::isspace(c)) {
                file_2_contents += c;
            }
        }
    }
    ifs_2.close();

    common = longestCommonSubsequence(file_1_contents, file_2_contents);
}

void CompareFiles::show_stats() const {
    std::cout << "Pair: " << p1.string() << ", " << p2.string() << std::endl;
    std::cout << "Common subsequence length: " << common.size() << std::endl;
    std::cout << "Overlap: " << common << std::endl;
}

std::string CompareFiles::longestCommonSubsequence(std::string X, std::string Y) {
    int m = X.size();
    int n = Y.size();
    int dp[m][n];
    for (int i = 0; i <= m; ++i) {
        for (int j = 0; j <= n; ++j) {
            if (i == 0 || j == 0) {
                dp[i][j] = 0;
            } else if (X[i-1] == Y[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
            } else {
                dp[i][j] = std::max(dp[i-1][j], dp[i][j-1]);
            }
        }
    }
    std::string lcs = "";
    int i = m;
    int j = n;
    while (i > 0 && j > 0) {
        if (X[i-1] == Y[j-1]) {
            lcs = X[i-1] + lcs;
            --i;
            --j;
        } else if (dp[i-1][j] > dp[i][j-1]) {
            --i;
        } else {
            --j;
        }
    }
    return lcs;
}
