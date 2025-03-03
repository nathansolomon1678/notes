COMPILER = g++
CFLAGS = -std=c++20 -O3
LINKER = $(COMPILER) -lm
EXEC = HW6P2
OBJ = HW6P2.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp selection_sort_template.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
.PHONY: all clean test
