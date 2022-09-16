
# saves variables
MEMORY = {}
# saves functions
CUSTOM_FUNCTIONS = {}

def execute_function(reference, *arguments):
    """
    This functions is able to call functions saved inside `CUSTOM_FUNCTIONS`
    """
    new_arguments = (MEMORY[arg] for arg in arguments)
    return CUSTOM_FUNCTIONS[reference](*new_arguments)

def opcode_1(arg1, arg2):
    return arg1 + arg2

def opcode_2(arg1, arg2):
    return arg1 - arg2

def opcode_3(arg1, arg2):
    return arg1 * arg2

def opcode_4(arg1, arg2):
    return arg1 / arg2

# will save all in house functions of python from +, -, *, / to sum, list, dict etc. etc.
OPCODES = [
    opcode_1,
    opcode_2,
    opcode_3,
    opcode_4,
    execute_function
]