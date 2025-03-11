COMPILER = g++
CFLAGS = -std=c++20 -O3
LINKER = $(COMPILER) -lm
EXEC = HW7
OBJ = HW7.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp SimpleSet.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
.PHONY: all clean
