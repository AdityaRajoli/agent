import ast
import os

def parse_code_constraints(file_paths):
    constraints = {}
    for filepath in file_paths:
        if not os.path.exists(filepath):
            continue

        if filepath.endswith('.py'):
            with open(filepath, 'r') as f:
                code = f.read()
            tree    = ast.parse(code)
            funcs   = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            branches= len([node for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While))])
            constraints[filepath] = {
                "functions": funcs,
                "branches" : branches,
                "lang"     : "python"
            }

        elif filepath.endswith('.c'):
            constraints[filepath] = {
                "lang" : "c",
                "note" : "C static constraints"
            }

    return constraints
