CC = "g++"
PROJECT = conduccionAutomatica
SRC = conduccionAutomatica.cpp

LIBS = `pkg-config opencv4 --cflags --libs`

$(PROJECT) :$(SRC)
	$(CC) $(SRC) -o $(PROJECT) $(LIBS)

run:
	./$(PROJECT)