ifeq ($(OS), Windows_NT)
all:run


setup:
	pip install pytest
	pip install -e .

activate:
	. .venv/Scripts/activate

venv:
	py -m venv .venv

run: tests
	py SpellingBee

tests: setup
	py tests

deactivate:
	deactivate

clean:
	rmdir .venv/Scripts
	rmdir .venv/Include
	rmdir .venv/Lib
	del .venv/pyvenv.cfg
	del *.json

else

all:run


setup:
	pip install pytest
	pip install -e .

activate:
	source .venv/Scripts/activate

venv:
	python3 -m venv .venv

run: tests
	python3 SpellingBee

tests: setup
	python3 tests

deactivate:
	deactivate

clean:
	rm .venv/Scripts
	rm .venv/Include
	rm .venv/Lib
	rm .venv/pyvenv.cfg
	rm *.json

endif