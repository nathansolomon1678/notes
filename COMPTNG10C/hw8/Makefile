COMPILER = g++
CFLAGS = -std=c++20 -O3
LINKER = $(COMPILER) -lm
EXEC = HW8
OBJ = HW8.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp ls_set.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
.PHONY: all clean test
