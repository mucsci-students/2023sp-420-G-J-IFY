ifeq ($(OS), Windows_NT)
all: setup


setup:
	pip install pytest
	pip install PyQt6
	pip install -e .
	

activate:
	. .venv/Scripts/activate

venv:
	py -m venv .venv

run: setup
	py SpellingBee

tests: setup
	py tests

deactivate:
	deactivate

cleanVenv: 
	rmdir .venv/Scripts
	rmdir .venv/Include
	rmdir .venv/Lib
	del .venv/pyvenv.cfg
	cls

cleanTests:
	del ./src/data/saves/TESTFILE1.json
	del ./src/data/saves/TESTFILE2.json
	del ./src/data/saves/TESTFILE3.json
	del ./src/data/saves/TESTFILE4.json
	del ./src/data/saves/TESTFILE5.json

else

all: setup


setup:
	pip install pytest
	pip install PyQt6
	pip install -e .
	

activate:
	. .venv/bin/activate

venv:
	python3 -m venv .venv

run: setup
	python3 SpellingBee
	

tests: setup
	python3 tests
	clear

deactivate: cleanVenv
	deactivate

cleanVenv: 
	rm -r ./.venv/include
	rm -r .venv/lib
	rm -r .venv/bin
	rm .venv/pyvenv.cfg
	clear
cleanTests: tests
	rm -r ./src/data/saves/TESTFILE1.json
	rm -r ./src/data/saves/TESTFILE2.json
	rm -r ./src/data/saves/TESTFILE3.json
	rm -r ./src/data/saves/TESTFILE4.json
	rm -r ./src/data/saves/TESTFILE5.json
	clear

endif