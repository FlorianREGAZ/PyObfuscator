from vm import *

number1 = 1
number2 = 5
sum = number1 + number2

# Translates to --------------------------------------------------------------------------------------------------------

MEMORY[0] = 1
MEMORY[1] = 5

MEMORY[2] = OPCODES[0](MEMORY[0], MEMORY[1])

# Translates to --------------------------------------------------------------------------------------------------------

#m[2] = o[0](m[0], m[1])