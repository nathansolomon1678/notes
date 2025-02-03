COMPILER = g++
CFLAGS = -std=c++17
LINKER = $(COMPILER) -lm
EXEC = HW2
OBJ = HW2.o hashtable.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp hashtable.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
test:
	./$(EXEC)
.PHONY: all clean test
