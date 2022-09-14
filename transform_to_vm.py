import ast

class GeneralTransformer(ast.NodeTransformer):

    def visit_Module(self, node: ast.Module):
        """Add import statement, to import required variables for the VM"""
        node.body.insert(0, ast.ImportFrom(
            module='vm',
            names=[
                ast.alias(name='MEMORY'),
                ast.alias(name='OPCODES')
            ],
            level=0)
        )
        return node

class AssignTransformer(ast.NodeTransformer):

    def __init__(self, storage):
        self.storage = storage

    def visit_Assign(self, node: ast.Assign):
        """remove variables and use memory instead"""
        new_function_names = [value["new_name"] for value in self.storage["function_memory"].values()]
        if type(node.value) == ast.Name and node.value.id in new_function_names:
            return node

        new_target = []
        for target in node.targets:
            new_target.append(ast.Subscript(
                value=ast.Name(id='MEMORY', ctx=ast.Load()),
                slice=ast.Constant(value=self.storage["variable_memory_increment"]),
                ctx=ast.Store()
            ))
            self.storage["variable_memory"][target.id] = self.storage["variable_memory_increment"]
            self.storage["variable_memory_increment"] += 1

        return ast.Assign(
            targets=new_target,
            value=node.value,
            type_comment=None,
        )

class CallTransformer(ast.NodeTransformer):

    def __init__(self, storage):
        self.storage = storage

    def visit_Call(self, node: ast.Call):
        """call functions from function memory"""
        if node.func.id in self.storage["function_memory"]:
            function_index = self.storage["function_memory"][node.func.id]["index"]
            new_arguments = [ast.Constant(value=function_index)]
            for arg in node.args:
                new_arguments.append(arg.slice)
            return ast.Expr(
                value=ast.Call(
                    func=ast.Subscript(
                        value=ast.Name(id='OPCODES', ctx=ast.Load()),
                        slice=ast.Constant(value=4),
                        ctx=ast.Load()),
                    args=new_arguments,
                    keywords=[]
                )
            )

        return node

class FunctionTransformer(ast.NodeTransformer):

    def __init__(self, storage):
        self.storage = storage

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """rename all functions and their arguments"""

        # rename function
        new_function_name = f"function{self.storage['function_memory_increment']}"
        self.storage['function_memory'][node.name] = {
            "new_name": new_function_name,
            "index": self.storage['function_memory_increment']
        }
        node.name = new_function_name

        # rename function arguments
        argument_increment = 0
        argument_memory = {}
        for child_node in ast.walk(node):
            if type(child_node) == ast.arg:
                argument_memory[child_node.arg] = f"arg{argument_increment}"
                child_node.arg = f"arg{argument_increment}"
                argument_increment += 1
            elif type(child_node) == ast.Name and child_node.id in argument_memory:
                child_node.id = argument_memory[child_node.id]

        # save function to CUSTOM_FUNCTIONS memory
        index = node.parent.body.index(node)
        node.parent.body.insert(index + 1, ast.Assign(
            targets=[
                ast.Subscript(
                    value=ast.Name(id='CUSTOM_FUNCTIONS', ctx=ast.Load()),
                    slice=ast.Constant(value=self.storage['function_memory_increment']),
                    ctx=ast.Store())
            ],
            value=ast.Name(id=new_function_name, ctx=ast.Load()))
        )

        self.storage['function_memory_increment'] += 1
        return node

class NameTransformer(ast.NodeTransformer):

    def __init__(self, storage):
        # ignore VM imports & python in house functions (for now)
        self.storage = storage

    def visit_Name(self, node: ast.Name):
        """replace all variables with their memory position"""
        if node.id in self.storage["ignore_list"]:
            return node

        if node.id not in self.storage["variable_memory"]:
            return node
        else:
            return ast.Subscript(
                value=ast.Name(id='MEMORY', ctx=ast.Load()),
                slice=ast.Constant(value=self.storage["variable_memory"][node.id]),
                ctx=ast.Store()
            )

class OperatorTransformer(ast.NodeTransformer):

    def __init__(self):
        self.opcodes = {
            ast.Add: 0,
            ast.Sub: 1,
            ast.Mult: 2,
            ast.Div: 3,
        }

    def visit_BinOp(self, node: ast.BinOp):
        if type(node.op) not in self.opcodes:
            raise Exception("Binary Operation not supported")

        return ast.Call(
            func=ast.Subscript(
                value=ast.Name(id='OPCODES', ctx=ast.Load()),
                slice=ast.Constant(value=self.opcodes[type(node.op)]),
                ctx=ast.Load()),
            args=[
                node.left,
                node.right
            ],
            keywords=[]
        )


def main():
    with open("main.py", "r") as f:
        code = f.read()

    storage = {
        "ignore_list": ["MEMORY", "OPCODES", "print"],
        "variable_memory_increment": 0,
        "variable_memory": {},
        "function_memory_increment": 0,
        "function_memory": {},
    }

    tree = ast.parse(code)
    # set parent nodes
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    tree = ast.fix_missing_locations(GeneralTransformer().visit(tree))
    tree = ast.fix_missing_locations(FunctionTransformer(storage).visit(tree))
    tree = ast.fix_missing_locations(AssignTransformer(storage).visit(tree))
    tree = ast.fix_missing_locations(NameTransformer(storage).visit(tree))
    tree = ast.fix_missing_locations(CallTransformer(storage).visit(tree))
    final_tree = ast.fix_missing_locations(OperatorTransformer().visit(tree))

    print("----------------------------------------------------------------------")
    print("---AST Tree-----------------------------------------------------------")
    print(ast.dump(final_tree, indent=4))
    print("----------------------------------------------------------------------")
    print("---Code --------------------------------------------------------------")
    print(ast.unparse(final_tree))

if __name__ == '__main__':
    main()