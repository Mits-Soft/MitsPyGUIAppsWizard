# cli/templates/app_template.py
from PySide6.QtWidgets import QApplication
from core.logic.logic_controller import LogicController
from core.view.view_controller import ViewController
from core.logging.logging_controller import LoggingController
from core.settings.settings_controller import SettingsController

class TestapplicationApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.logic = LogicController()
        self.view = ViewController()
        self.logger = LoggingController()
        self.settings = SettingsController()