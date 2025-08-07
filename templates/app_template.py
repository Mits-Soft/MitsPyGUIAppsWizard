# cli/templates/app_template.py
import sys

from PySide6.QtWidgets import QApplication
from core.logic.logic_controller import LogicController
from core.view.view_controller import ViewController
from core.logging.logging_controller import LoggingController
from core.settings.settings_controller import SettingsController

class {{app_name|capitalize}}App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        self.logic = LogicController()
        self.view = ViewController()
        self.logger = LoggingController()
        self.settings = SettingsController()
        
        self.view.main_window.show()

if __name__ == "__main__":
    app = {{app_name|capitalize}}App(sys.argv)
    sys.exit(app.exec())