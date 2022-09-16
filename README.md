# PyObfuscator

Make your code difficult to understand and read. Minimize exposure to attacks.

This is an educational project to learn more about the Abstract-Syntax-Tree library of python and to explore the possibilities you have with python obfuscation.

The project is still in a very early stage of development. It currently only works on very simple scripts, so use it at your own risk!

## Examples
Disclaimer: the third translation is not included yet, but it is as simple as renaming `MEMORY` to `m` and `OPCODES` to `o` etc.

Example 1: 
```python
number1 = 1
number2 = 5
sum = number1 + number2

# Translates to ------------------------------------------
from vm import *

MEMORY[0] = 1
MEMORY[1] = 5

MEMORY[2] = OPCODES[0](MEMORY[0], MEMORY[1])

# Translates to ------------------------------------------
from vm import *

m[0] = 1
m[1] = 5
m[2] = o[0](m[0], m[1])
```

Example 2:
```python
def print_sum(number1, number2):
    print(number1 + number2)

number1 = 1
number2 = 5
print_sum(number1, number2)

# Translates to ------------------------------------------
from vm import *

def function1(arg1, arg2):
    print(OPCODES[0](arg1, arg2))

CUSTOM_FUNCTIONS[0] = function1
MEMORY[0] = 1
MEMORY[1] = 5

MEMORY[2] = OPCODES[4](0, 0, 1)


# Translates to ------------------------------------------
from vm import *

def function1(arg1, arg2):
    print(OPCODES[0](arg1, arg2))
f[0] = function1
m[0] = 1
m[1] = 5
m[2] = o[4](0, 0, 1)
```

## Quick Start
A section explaining how to use the obfuscator will come as soon as it is useable for more complex code. 

## Planned Features
- Support for more complex code (classes, more operations etc.)
- Anti debugging method
- One line obfuscation
- many more..
