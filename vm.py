
MEMORY = {}
CUSTOM_FUNCTIONS = {}

def execute_function(reference, *arguments):
    #new_arguments = ()
    #for arg in arguments:
    #    new_arguments += (MEMORY[arg],)

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

OPCODES = [
    opcode_1,
    opcode_2,
    opcode_3,
    opcode_4,
    execute_function
]