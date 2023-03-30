# Coding Documentation for G(J)IFY

## Module Header

### Formatting Description

Begin module with a single "shebang" (`#!`) line specifying to python the
enterpereter. The line `#!/usr/bin/env` should be sufficient.

### Header Block

1. Module Name
2. Date of creation
3. Contributors to Function in oder of most Contributed
4. Functions in that module
5. Description of module
6. Imports

### Example

```python
#!/usr/bin/env

################################################################################
# Something.py
# Author: Top Contributor, Second Most, Third most
# Date of Creation: MM-DD-YYYY
#
# Multi-line description of what a module does.
#
# (Global, public) functions:
#   function1(param1 : int) -> bool
#
#   function2(param1='default' : str, param2 : bool) -> int
#
#   function3() -> None
#
#   function4() -> None
#
################################################################################
```

## Functions

### Comment Block

Use a line of `#` with a length of 80 chars to separate methods.
Public methods use standard camel case, and 

1. Have parameters and description at the top of the function
2. Function names in camel case
3. If functions have similar functionality within them create a general helper
function.
4. Utilize exception handling for code that can take bad input

### Example

```python
################################################################################
# functionName(arg1 : int, arg2='defaultVal' : str) -> bool
#
# DESCRIPTION:
#   A description of the function
#
# PARAMETERS:
#   arg1 : int
#     - an example integer parameter
#   arg2 : int, optional
#     - an example string parameter
#
# RETURNS:
#   bool
#     - a boolean return type
#
# RAISES:
#   Exception
#     - if arg1 is less than or equal to o
################################################################################
def functionName(arg1 : int, arg2='defaultVal' : str) -> bool:
    if arg1 > 0:
        raise Exception("arg1 must be greater than 0")
    else:
        return True
################################################################################
```

## Classes

### Comment Block

- The name of the class
- a description of what it does and what it is used for

### Example

```python
################################################################################
# class ClassName()
# Description:
#   A description of the class
#
# Arguments:
#   arg1 : float
#   arg2=3 : int, optional
#   arg3='default' : str, optional
#
# <public> Attributes:
#   attribute1 : float
#   attribute2 : int
#   attribute3 : str
#   attribute4 : int
#
# <public> Functions:
#   function1(param1=5 : int, param2 : bool) ->
#     - one-line description:
################################################################################
class ClassName():
    __init__(self, arg1, arg2=3, arg3='default'):

        self.attribute1 = arg1
        self.attribute2 = arg2
        self.attribute3 = arg3
        self.attribute4 = 25
    
    ############################################################################
    # function1(param1 : int, param2 : bool) -> bool
    #
    # Description:
    #   A brief description of the function
    #
    # Parameters:
    #
    # Returns:
    #
    # Raises:
    ############################################################################
    def function1(self, param1=5 : int, param2 : bool) -> bool:

        if param2:
            raise Exception("param2 is true")

        return (param1 * self.attribute2) >= 25

    ############################################################################
    # function1()
    # 
    # Description:
    #   A brief description of the function
    #
    # Parameters:
    #
    # Returns:
    #
    # Raises:
    ############################################################################
    def _privateFunction(self):
        """One-line description

        multi-line description (if applicable)
        """
        self.attribute4 = 0
```