#include <iostream>
#include <filesystem>
#include <fstream>
#include "compare.h"

int main(int argc, const char* argv[]) {
if (argc <  3) {
	std::cerr << "Usage: " << argv[0] << "<string1>,<string2>" << std::endl;
	std::ofstream fout("errorOutput.txt");
	if (fout.is_open()) {
		fout << "Usage: " << argv[0] << "<string1>,<string2>" << std::endl;
		fout.close();
	}
	else {
	// Handle the case when the file could not be opened
	std::cerr << "Error opening the file for writing\n";
	}

	return 1; // Return non=zero to indicate an error
	}


	std::filesystem::path p1 = std::string(argv[1]);
	std::filesystem::path p2 = std::string(argv[2]);
	CompareFiles com(p1,p2);
	com.show_stats();
        return 0;
}
