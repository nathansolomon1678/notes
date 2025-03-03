COMPILER = g++
CFLAGS = -std=c++14 -O3
LINKER = $(COMPILER) -lm
EXEC = HW6P1
OBJ = HW6P1.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp do_for_each_template.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
.PHONY: all clean test
