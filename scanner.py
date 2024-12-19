from pathlib import Path
from datetime import datetime
from utils.parser import PythonModuleParser
from utils.tree import ProjectTree

class ProjectScanner:
    def __init__(self, directory: str):
        self.project_path = Path(directory)
        if not self.project_path.is_dir():
            raise ValueError(f"The path '{directory}' is not a valid directory.")
        self.tree = ProjectTree(self.project_path)
        self.report = {}

    def scan(self):
        """Scan the project directory and generate a report."""
        self.report = self.tree.build_tree()
        self.parse_modules()
        self.generate_report()

    def parse_modules(self):
        """Parse each module to extract detailed information."""
        for module in self.tree.modules:
            parser = PythonModuleParser(module)
            module_info = parser.parse()
            self.report[str(module)] = module_info

    def generate_report(self):
        """Generate a report of the scanned project."""
        report_dir = Path("reports")
        report_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"report_{timestamp}.txt"

        with report_file.open("w", encoding="utf-8") as f:
            f.write("You are very helpful AI-Assistant in the field of Python development. This is the basic structure of the project:\n\n")
            f.write(f"Project Root: {self.tree.root}\n")
            f.write("Modules:\n")
            for module in self.tree.modules:
                module_path = str(module)
                f.write(f"  - {module_path}\n")
                module_info = self.report.get(module_path)
                if module_info:
                    self.write_module_info(f, module_info)

            # Добавление окончательной информации
            f.write("\nБазируясь на этой структуре проекта:\n")
            f.write("Самый главный управляющий модуль проекта, его движок и сердце: <название_главного_модуля>\n")
            f.write("Модуль из которого запускается проект: <название_модуля_запуска>\n")
            f.write("Основные зависящие от него модули: <названия_зависящих_модулей>\n")
            f.write("Что проект делает: <описание_функциональности_проекта>\n")
            f.write("Какая его структура: <описание_структуры>\n")
            f.write("Сглаженное упрощенное дерево проекта с #комментариями: <упрощенное_дерево_проекта>\n")
            f.write("Часто используемые классы проекта: <названия_часто_используемых_классов>\n")
            f.write("Основные принципы: <основные_принципы>\n") 
            f.write("Что мне полезно знать для разработки внутри этого проекта: <полезная_информация>\n")
            f.write("Оценка SOLID принципов и MVC архитектуры от 1 до 10: <оценка_SOLID>\n")
            f.write("Кто разрабатывал этот проект - один или несколько разработчиков и какой их уровень от junior до senior: <уровень_разработчиков>\n")

        print(f"Report saved to {report_file}")

    def write_module_info(self, f, module_info):
        """Write module information to the report."""
        f.write("    Imports:\n")
        for imp in module_info.get('imports', []):
            f.write(f"      - {imp}\n")
        
        f.write("    Classes:\n")
        for cls in module_info.get("classes", []):
            f.write(f"      - {cls['name']} (Methods: {', '.join(method['name'] for method in cls['methods'] if method['name'] != '__init__')})\n")
            for method in cls['methods']:
                if method['name'] == '__init__':
                    continue  # Пропустить метод __init__
                return_type = method.get("return_type", "None")
                params = ", ".join(param['name'] for param in method['params'])
                description = method.get('description', 'Нет описания')
                f.write(f"        - {method['name']} (Return Type: {return_type})\n")
                f.write(f"          Params: {params}\n")
                f.write(f"          Description: {description}\n")
        
        f.write("    Functions:\n")
        for func in module_info.get("functions", []):
            return_type = func.get("return_type", "None")
            params = ", ".join(param['name'] for param in func['params'])
            description = func.get('description', 'Нет описания')
            f.write(f"      - {func['name']} (Return Type: {return_type})\n")
            f.write(f"        Params: {params}\n")
            f.write(f"        Description: {description}\n")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scan a Python project directory.")
    parser.add_argument("directory", type=str, help="Path to the project directory to scan.")
    args = parser.parse_args()

    scanner = ProjectScanner(args.directory)
    scanner.scan()
