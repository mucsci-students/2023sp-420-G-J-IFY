# SpellingBee by G-J-IFY

## Description
---
Welcome to SpellingBee by G-J-IFY. 

This is an homage to the New York Times word puzzle, Spelling Bee. Users are
prompted to build words using only the seven letters in their puzzle, and each
word must include the center letter. Letters can be repeated within a word. 

Can you guess all the words and become the Queen Bee you're meant to be?

### Dependencies

This application runs on the following operating systems
  - Windows 10, 11
  - macOS
  - Linux

Before running the program, you must have Python installed 
  (3.11.2 at the time). (https://www.python.org/downloads/)

Also be sure to download Chocolatey if you are on windows.
  Run this command in Administrative PowerShell window to install Choclatey:
  Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))


### Installing

- First, clone repository with:

```
git clone "https://github.com/mucsci-students/2023sp-420-G-J-IFY.git"
```

- Then, navigate to `./GitHub/2023sp-420-G-J-IFY/` and run the following command:

```
make
```

### Executing program

- To run, the program, run:
Windows:
```
python src (To launch GUI)

python src -c (To launch CLI)
```
macOS/Linux:
```
python3 src (To launch GUI)

python src -c (To launch CLI)

```

- To run tests, run:
Windows:
```
make tests
```
macOS/Linux:
```
make tests
```
- After runing tests run:
```
make cleanTests
```
## Authors
---

Contributors' names and contact info

Isaak Weidman
- @IRWeidman
- irweidma@millersville.edu

Gaige Zakroski
- @gmzakros
- gmzakros@millersville.edu

Yah'hymbey Baruti Ali-Bey
- @ybaruti
- yabaruti@millersville.edu

Jacob M Lovegren
- @JMLovegren
- jmlovegr@millersville.edu

Francesco Spagnolo
- @Frannyspag24
- fnspagno@millersville.edu

## Version History
---
- 1.0.0
  - Initial CLI release

- 2.0.0
  - Initial GUI release

## License
---

This project is licensed under the `MIT` License - see the `LICENSE.md` file for details.
