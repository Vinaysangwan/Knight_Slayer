SRC = main.py

all: run

run:
	Python $(SRC)

debug:
	python -m pdb $(SRC)