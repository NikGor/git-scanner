import os
from pathlib import Path

class ProjectTree:
    def __init__(self, directory: Path):
        self.root = str(directory)
        self.modules = []

    def build_tree(self) -> dict:
        """Build a tree structure of the project directory."""
        self.modules = []
        tree = {"root": self.root, "modules": []}

        for root, _, files in os.walk(self.root):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    module_path = Path(root) / file
                    self.modules.append(module_path)
                    tree["modules"].append(module_path)

        return tree


def display_tree(tree: dict, report: dict) -> None:
    """Display the directory tree with module details."""
    print(f"Project Root: {tree['root']}")
    print("Modules:")
    for module in tree["modules"]:
        module_path = str(module)
        print(f"  - {module_path}")
        if module_path in report:
            module_info = report[module_path]
            print("    Imports:")
            for imp in module_info.get('imports', []):
                print(f"      - {imp}")
            print("    Classes:")
            for cls in module_info.get("classes", []):
                print(f"      - {cls['name']} (Methods:)")
                for method in cls["methods"]:
                    params = ", ".join(
                        f"{param['name']}: {param['type']}" for param in method["params"]
                    )
                    return_type = method["return_type"]
                    print(f"          {method['name']}({params}) -> {return_type}")
            print("    Functions:")
            for func in module_info.get("functions", []):
                params = ", ".join(
                    f"{param['name']}: {param['type']}" for param in func["params"]
                )
                return_type = func["return_type"]
                print(f"      - {func['name']}({params}) -> {return_type}")

