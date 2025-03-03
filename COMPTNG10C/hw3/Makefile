COMPILER = g++
CFLAGS = -std=c++17
LINKER = $(COMPILER) -lm
EXEC = HW3
OBJ = HW3.o BinarySearchTree.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp BinarySearchTree.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
.PHONY: all clean test
