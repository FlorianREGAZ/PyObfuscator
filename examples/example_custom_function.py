from vm import *

def print_sum(number1, number2):
    print(number1 + number2)


number1 = 1
number2 = 5
print_sum(number1, number2)

# Translates to --------------------------------------------------------------------------------------------------------
def function1(arg1, arg2):
    print(arg1 + arg2)

CUSTOM_FUNCTIONS[0] = function1
MEMORY[0] = 1
MEMORY[1] = 5

MEMORY[2] = execute_function(0, 0, 1)

# Translates to --------------------------------------------------------------------------------------------------------
def function1(arg1, arg2):
    print(OPCODES[0](arg1, arg2))

CUSTOM_FUNCTIONS[0] = function1
MEMORY[0] = 1
MEMORY[1] = 5

MEMORY[2] = OPCODES[4](0, 0, 1)


# Translates to --------------------------------------------------------------------------------------------------------

#f[0] = print_sum
#m[0] = 1
#m[1] = 5
#
#m[2] = o[4](0, 0, 1)
