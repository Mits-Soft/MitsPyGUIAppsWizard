import re
import subprocess
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from jsondot import JsonDot, Dot
import json

TEMPLATES_PATH = Path(__file__).parent.parent / "templates"

class AppProject:
    def __init__(self, name: str, base_path: Path, framework_path: Path):
        self.name = self._validate_name(name)
        self.project_path = base_path / self.name
        self.framework_path = framework_path
        self.app_data_path = self.framework_path / "projects" / self.name
        self.template_env = Environment(loader=FileSystemLoader(str(TEMPLATES_PATH)))

    def _validate_name(self, name: str) -> str:
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", name):
            raise ValueError("❌ El nombre debe ser un identificador válido de Python.")
        return name

    def bootstrap(self):
        self._create_structure()
        self._create_virtualenv()
        self._install_dependencies()
        self._generate_files()
        self._save_metadata()

    def _create_structure(self):
        print("AppProject:_create_structure -> Creating project structure in: ")
        modules = ["logic", "view", "logging", "settings"]
        for module in modules:
            path = self.project_path / "core" / module
            path.mkdir(parents=True, exist_ok=True)
            print(str(path))
            (path / "__init__.py").touch()
        data_path = self.app_data_path
        data_path.mkdir(parents=True, exist_ok=True)
        print("AppProject:_create_structure -> Project structure created")

    def _create_virtualenv(self):
        subprocess.run(["python", "-m", "venv", str(self.project_path / "env")])

    def _install_dependencies(self):
        subprocess.run(["pip", "install", "PySide6", "JsonDot"])

    def _render_template(self, template_name: str, context: dict) -> str:
        template = self.template_env.get_template(template_name)
        return template.render(context)

    def _generate_files(self):
        context = {"app_name": self.name}
        files = {
            f"{self.name}.py": "app_template.py",
            "core/logic/logic_controller.py": "logic_controller_template.py",
            "core/view/view_controller.py": "view_controller_template.py",
            "core/logging/logging_controller.py": "logging_controller_template.py",
            "core/settings/settings_controller.py": "settings_controller_template.py"
        }
        for target_relpath, template_name in files.items():
            target_path = self.project_path / target_relpath
            content = self._render_template(template_name, context)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)

    def _save_metadata(self):
        project_pth = self.project_path
        data_path = self.app_data_path
        project_path_string = str(project_pth)
        project_data_path_string = str(data_path)
        jd = {
            "app-name": self.name,
            "project-path": project_path_string,
            "data-path": project_data_path_string
        }
        jds = json.dumps(jd)
        # dot = Dot(f"{ps}\\app_data.json")
        dot = JsonDot().loads(jds, f"{project_data_path_string}\\app_data.json")
        # dot.loads(jds)
        dot.dump()
