CXX=g++
CXXFLAGS=-fPIC -O2 -march=native

all: libEDTSurf.so

libEDTSurf.so: ParsePDB.o ProteinSurface.o EDTSurf.o
	$(CXX) -shared -Wl,-soname,$@ $^ -o $@
	rm $^

ProteinSurface.o: ProteinSurface.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

ParsePDB.o: ParsePDB.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

EDTSurf.o: EDTSurf.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f ProteinSurface.o ParsePDB.o EDTSurf.o libEDTSurf.so

