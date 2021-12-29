XX := g++
CXXFLAGS := -O3 -Wall -Wconversion -Wextra -Wpedantic -std=c++11 -ljpeg

TARGET := main
OBJS := main.o hw6.o image.o -ljpeg
INCS := hw6.hpp image.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
