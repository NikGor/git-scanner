import ast
from pathlib import Path


class PythonModuleParser:
    def __init__(self, file_path: Path):
        self.file_path = file_path

    def parse(self) -> dict:
        """Parse a Python module and extract imports, classes, and methods."""
        with self.file_path.open("r", encoding="utf-8") as file:
            try:
                tree = ast.parse(file.read())
            except SyntaxError:
                return {"error": "Failed to parse due to syntax errors"}

        result = {
            "imports": [],
            "classes": [],
            "functions": []
        }

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.Import):
                result["imports"].extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                module = node.module or "unknown"
                result["imports"].extend([f"{module}.{alias.name}" for alias in node.names])
            elif isinstance(node, ast.ClassDef):
                methods = []
                for n in node.body:
                    if isinstance(n, ast.FunctionDef):
                        methods.append({
                            "name": n.name,
                            "params": [
                                {
                                    "name": arg.arg,
                                    "type": self.get_annotation(arg.annotation)
                                }
                                for arg in n.args.args
                            ],
                            "return_type": self.get_annotation(n.returns),
                            "description": ast.get_docstring(n) or "Нет описания"
                        })
                result["classes"].append({"name": node.name, "methods": methods})
            elif isinstance(node, ast.FunctionDef):
                result["functions"].append({
                    "name": node.name,
                    "params": [
                        {
                            "name": arg.arg,
                            "type": self.get_annotation(arg.annotation)
                        }
                        for arg in node.args.args
                    ],
                    "return_type": self.get_annotation(node.returns),
                    "description": ast.get_docstring(node) or "Нет описания"
                })

        return result

    def get_annotation(self, annotation):
        if isinstance(annotation, ast.Attribute):
            if hasattr(annotation.value, 'id'):
                return f"{annotation.value.id}.{annotation.attr}"
            return f"{annotation.attr}"
        elif isinstance(annotation, ast.Name):
            return annotation.id
        return "unknown"
