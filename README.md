# SpellingBee by G-J-IFY

## Description
Welcome to SpellingBee by G-J-IFY. 

This is an homage to the New York Times word puzzle, Spelling Bee. Users are
prompted to build words using only the seven letters in their puzzle, and each
word must include the center letter. Letters can be repeated within a word. 

Can you guess all the words and become the Queen Bee you're meant to be?


## Dependencies

This application runs on the following operating systems
  - Windows 10, 11
  - macOS
  - Linux

Before running the program, you must have Python installed 
  (3.11.2 at the time).<br>
Installation instructions can be found on the [official python site.](https://www.python.org/downloads/)

**These dependencies will be automatically isntalled:**
- pytest 7.2.2
- pyqt6 6.4.2
- prompt_toolkit 3.0.38
- pytest-cov 4.0.0
- coverage 7.2.2
- pycryptodome 3.17

## Installation

First, clone repository with:

```
git clone "https://github.com/mucsci-students/2023sp-420-G-J-IFY.git"
```

Then, navigate to `./GitHub/2023sp-420-G-J-IFY/

If you would like to install in a virtual environment, run:

Windows:
```
python -m venv venv
```
MacOS/Linux
```
python3 -m venv venv
```

then activate the environment:

Windows:
```
source venv/bin/activate
```
MacOS/Linux:
```
source venv/bin/activate
```

To install the requirements

Windows:
```
pip install -r requirements.txt
```
MacOS/Linux
```
pip3 install -r requirements.txt
```

## Executing program

### Running the GUI

Windows:
```
python spellingbee
```

MacOS/Linux:
```
python3 spellingbee
```

### Running the CLI

Windows:
```
python spellingbee --cli
```

macOS/Linux:
```
python3 spellingbee --cli
```

### Running the tests

To run the tests, enter the following command
```
pytest
```

### Running the tests with code coverage

To run the tests and check code coverage of the model, enter
the following command
```
pytest --cov=spellingbee/model
```

To generate a coverage report of the model, after running the above command,
enter the following
```
coverage report -m
```

## Creational Design Patterns

### MVC

Organized out into applicable folders, our project has all of our backend 
business logic stored in `2023sp-420-g-j-ify/SpellingBee/model`

For the visual representation of the game's underlying logic, we have two 
classes, `2023sp-420-g-j-ify/cview/cli.py` and 
`2023sp-420-g-j-ify/gview/MainWindow.py`.

Finally, to bridge the gap between the model and the two views, we have a 
combination of `2023sp-420-g-j-ify/controller/GUIAdapter.py`, 
`2023sp-420-g-j-ify/controller/CLIAdapter.py`, and 
`2023sp-420-g-j-ify/controller/cmd.py` that act as the controller.

### Singleton

The output object is used to store information to be displayed to the user 
playing either the CLI or GUI version of the game. Since this object needs to 
be accessed in any file and only one copy should exist, we implemented 
singleton to prevent another to be created. Stored in 
`2023sp-420-g-j-ify/SpellingBee/model/output.py`.

The object is created in `spellingbee/controller/cController/__main__.py` for
the CLI and in `spellingbee/controller/GUIAdapter.py` for the GUI.


## Behavioral Patterns

### Strategy

The game requires a mix of saving options, which led to a confusing mix of 
fucntion calls that largely did the same thing. We implemented a strategy to
reduce the complexity of function calls. Strategy class is stored in 
`spellingbee/model/StateStorage.py`

### Command 

To implement a command pattern, we created 
`2023sp-420-g-j-ify/controller/cmd.py` that contains a collection of classes 
that are used to execute commonly used commands. Many of those classes are 
directly accessed in the CLI through "!" commands, and those same commands are 
accessed by the GUI through its buttons.

### Decorator

In order to improve our code reusability, we needed to employ two decorators, 
`2023sp-420-g-j-ify/controller/GUIAdapter.py` and 
`2023sp-420-g-j-ify/controller/CLIAdapter.py`, to allow both views to use the 
commands added in `cmd.py`. These decorators allow the entire model to be 
completely independent of the view.

### Iterator

We have lots of lists in our program, and need to be able to work through them
quickly and simply. An iterator pattern was implemented for just that purpose.
An example can be found in `spellingbee/controller/cController/CLIAdapter.py`
in the removeColumn funciton.


## Authors

**Isaak Weidman**
- @IRWeidman
- irweidma@millersville.edu

**Gaige Zakroski**
- @gmzakros
- gmzakros@millersville.edu

**Yah'hymbey Baruti Ali-Bey**
- @ybaruti
- yabaruti@millersville.edu

**Jacob M Lovegren**
- @JMLovegren
- jmlovegr@millersville.edu

**Francesco Spagnolo**
- @Frannyspag24
- fnspagno@millersville.edu

## Version History
- 1.0.0
  - Initial CLI release

- 2.0.0
  - Initial GUI release

- 3.0.0
  - Launch of hints feature

- 4.0.0
  - Launch of local high score
  - Launch of encrypted saves
  - updates to GUI and CLI

## License

This project is licensed under the `MIT` License - see the `LICENSE.md` 
file for details.
