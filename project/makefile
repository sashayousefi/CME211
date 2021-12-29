CXX := g++
CXXFLAGS := -O3 -Wall -Wconversion -Wextra -Wpedantic -std=c++11 

TARGET := main
OBJS := main.o COO2CSR.o matvecops.o CGSolver.o sparse.o heat.o 
INCS := COO2CSR.hpp matvecops.hpp CGSolver.hpp sparse.hpp heat.cpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
