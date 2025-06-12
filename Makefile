SRC = main.py
EDITOR = editor.py

all: run

run:
	Python $(SRC)

editor:
	Python $(EDITOR)

debug:
	python -m pdb $(SRC)