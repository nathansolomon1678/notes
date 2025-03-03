COMPILER = g++
CFLAGS = -std=c++17
LINKER = $(COMPILER) -lm
EXEC = HW1
OBJ = HW1.o compare.o
all: $(EXEC)
$(EXEC): $(OBJ)
	$(LINKER) -o $@ $^
%.o: %.cpp compare.h
	$(COMPILER) $(CFLAGS) -c $< -o $@
clean:
	rm -f $(OBJ) $(EXEC)
