from enum import Enum

from PySide6.QtCore import QObject, QSize, Qt, QMargins, Signal
from PySide6.QtGui import QAction, QFont, QPainter, QColor
from PySide6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QTabWidget, QWidget, QBoxLayout, QToolBar, QSizePolicy, QSplitter)


class ViewController(QObject):
    """Controlador de las vistas y componentes visuales."""

    def __init__(self):
        self.main_window = MitsMainWindow()


class MitsMainWindowSignals:
    notify_init_finished_sig = Signal(str)


class MitsMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = self.set_menu_bar()
        self.tool_bar = self.set_tool_bar()
        self.main_widget = MitsPanel("main_widget")
        self.status_bar = self.set_status_bar()
        self.main_widget_setup()
        self.setMinimumSize(940, 540)
        self.setCentralWidget(self.main_widget)
        e = self.main_widget_internal.get_element_by_id("right_column")
        self.debug_point = "shit"

    def main_widget_setup(self):
        label = QLabel("Welcome to GUIA!!!")
        label_sq = QLabel("The best making sqares")
        self.set_element_text_format(label, "Roboto", 48)
        self.set_element_text_format(label_sq, "Roboto", 48)
        self.main_widget_internal = self.main_widget.add_panel(
            MitsPanel("right_column"), "right_column", PanelPosition.RIGHT.value)
        self.main_widget_internal_B = self.main_widget_internal.add_panel(
            MitsPanel("down_file"), "down_file", PanelPosition.DOWN.value)
        self.main_widget_internal_C = self.main_widget_internal.add_panel(
            MitsPanel("down_down_file"), "down_down_file", PanelPosition.DOWN.value)
        self.main_widget.princeps.add_widget(label)
        self.main_widget_internal.widgets.container[0].add_widget(label_sq)

    def set_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Archivo")

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        return menu_bar

    def set_tool_bar(self):
        toolbar_items = [
            QPushButton("Nuevo"),
            "spacer",
            QPushButton("Guardar")
        ]

        toolbar = MitsToolBar("Principal", parent=self, items=toolbar_items)
        self.addToolBar(toolbar)

        return toolbar

    def set_status_bar(self):
        status_bar = self.statusBar()

        status_bar.showMessage("Ready")

        return status_bar

    def set_element_text_format(self, elem: QWidget, font_type, font_size):
        elem.setFont(QFont(font_type, font_size))


class WidgetDirection(Enum):
    DOWNWARDS = QBoxLayout.Direction.TopToBottom
    UPWARDS = QBoxLayout.Direction.BottomToTop
    RIGHTWARDS = QBoxLayout.Direction.LeftToRight
    LEFTWARDS = QBoxLayout.Direction.RightToLeft


DIRECTIONS = {
    "downwards": QBoxLayout.Direction.TopToBottom,
    "upwards": QBoxLayout.Direction.BottomToTop,
    "rightwards": QBoxLayout.Direction.LeftToRight,
    "leftwards": QBoxLayout.Direction.RightToLeft
}


class MitsWidget(QWidget):
    """
    Base widget with configurable layout direction.
    """

    def __init__(self, *args, direction="downwards", **kwargs):
        super().__init__(*args, **kwargs)

        direction_value = (
            DIRECTIONS.get(direction.lower(), QBoxLayout.Direction.TopToBottom)
            if isinstance(direction, str)
            else direction
        )

        layout = QBoxLayout(direction_value)
        layout.setContentsMargins(QMargins(0, 0, 0, 0))
        layout.setSpacing(0)
        self.setLayout(layout)

    def add_widget(self, widget: QWidget):
        self.layout().addWidget(widget)
        return widget

    def set_direction(self, direction):
        old_layout = self.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
            QWidget().setLayout(old_layout)

        direction_value = (
            DIRECTIONS.get(direction.lower(), QBoxLayout.Direction.TopToBottom)
            if isinstance(direction, str)
            else direction
        )

        new_layout = QBoxLayout(direction_value)
        new_layout.setContentsMargins(0, 0, 0, 0)
        new_layout.setSpacing(0)
        self.setLayout(new_layout)


class MitsVerticWidget(MitsWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(direction=QBoxLayout.Direction.TopToBottom, *args, **kwargs)


class MitsHorizontWidget(MitsWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(direction=QBoxLayout.Direction.LeftToRight, *args, **kwargs)


class MitsToolBar(QToolBar):
    """
    Custom toolbar supporting actions, buttons and spacers.
    """

    def __init__(self, title="", parent=None, items=None):
        super().__init__(title, parent)
        if items:
            for item in items:
                self.add_element(item)

    def add_element(self, item):
        if isinstance(item, QAction):
            self.addAction(item)
        elif isinstance(item, QPushButton):
            self.addWidget(item)
        elif item == "spacer":
            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            self.addWidget(spacer)


class PanelPosition(Enum):
    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    PARENT = "parent"
    PRINCEPS = "princeps"


class MitsSplitterHandle(QWidget):
    def __init__(self, parent=None, orientation="vertical", id: str = "new_splitter_handle"):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.orientation = orientation
        self.id = id

        if orientation == "vertical":
            self.setFixedHeight(5)
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setFixedWidth(5)
            self.setCursor(Qt.SizeHorCursor)

        self.dragging = False
        self.last_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.last_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.globalPosition().toPoint() - self.last_pos
            self.last_pos = event.globalPosition().toPoint()
            self.parent().resize_panels(self, delta, self.orientation)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#888888"))


class MitsPanelWidgetContainer(QObject):
    """
    Container for widgets in a MitsPanel.
    """

    def __init__(self):
        super().__init__()
        self.container = []
        self.index: dict[str, int] = {}

    def add_panel_element_at_end(self, widget: QWidget, id: str = "widget_"):
        self.container.append(widget)
        if hasattr(widget, id) and widget.id != None:
            self.register_widget(widget, widget.id)
        else:
            self.register_widget(widget, f"{id}{len(self.container) + 1}")

    def add_panel_element_at_beggining(self, widget: QWidget, id: str = "widget_"):
        self.container.insert(0, widget)
        if hasattr(widget, id) and widget.id != None:
            self.register_widget(widget, widget.id)
        else:
            self.register_widget(widget, f"{id}{len(self.container) + 1}")

    def register_widget(self, widget: QWidget, id: str = " "):
        if widget.id.startswith("widget_"):
            id = f"{widget.id}{str(len(self.container) - 1)}"
        self.index[id] = len(self.container) - 1

    def register_princeps(self, widget: QWidget, id: str = " "):
        if type(widget) != MitsSplitterHandle:
            self.container.append(widget)
        if widget.id.startswith("widget_"):
            id = f"{widget.id}{str(len(self.container) - 1)}"
        self.index[id] = len(self.container) - 1

    def update_index(self):
        self.index: dict[str, int] = {}
        for i, elem in enumerate(self.container):
            self.index[elem.id] = i


class MitsPanel(MitsWidget):
    def __init__(self, id="panel", is_princeps=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgets = MitsPanelWidgetContainer()

        if id == "panel":
            id = f"panel{len(self.widgets.container) - 1}"
        self.id = id
        self.position = PanelPosition.PARENT.value
        self.direction = WidgetDirection.DOWNWARDS.value
        if is_princeps == False:
            self.princeps = self.add_panel(MitsPanel("princeps", True))
        elif is_princeps == True:
            self.position = PanelPosition.PRINCEPS.value

    def add_panel(self, panel: 'MitsPanel', id: str = "princeps", position: str = "princeps"):
        if id == "princeps":
            new_panel = self.add_widget(panel)
            self.widgets.register_princeps(new_panel, id)
            return new_panel
        return self.order_panels(panel, id, position)

    def get_element_by_id(self, id):
        if id in self.widgets.index.keys():
            index = self.widgets.index[id]
        else:
            return False
        return self.widgets.container[index]

    def order_panels(self, panel: 'MitsPanel', id: str, position: str):
        last_panel = self.widgets.container[-1] if self.widgets.container else None

        # if not last_panel:

        #     self.add_widget(panel)
        #     # self.widgets.container.append(panel)
        #     self.widgets.register_widget(panel, "princeps")
        #     return panel

        if position in [PanelPosition.DOWN.value, PanelPosition.UP.value]:
            orientation = "vertical"
        else:  # LEFT or RIGHT
            orientation = "horizontal"

        splitter_handle = MitsSplitterHandle(
            self, orientation, f"{id}_splitter")

        self.clear_layout()

        if position in [PanelPosition.DOWN.value, PanelPosition.RIGHT.value]:
            if position == PanelPosition.DOWN.value:
                self.direction = WidgetDirection.DOWNWARDS
                self.set_direction("downwards")
            elif position == PanelPosition.RIGHT.value:
                self.direction = WidgetDirection.RIGHTWARDS
                self.set_direction("rightwards")
            self.widgets.add_panel_element_at_end(splitter_handle)
            self.widgets.add_panel_element_at_end(panel)
            self.widgets.update_index()
            self.add_widgets(self.widgets.container)

        else:  # UP or LEFT
            if position == PanelPosition.UP.value:
                self.direction = WidgetDirection.UPWARDS
                self.set_direction("upwards")
            elif position == PanelPosition.LEFT.value:
                self.direction = WidgetDirection.LEFTWARDS
                self.set_direction("leftwards")
            self.widgets.add_panel_element_at_beggining(splitter_handle)
            self.widgets.add_panel_element_at_beggining(panel)
            self.add_widgets(self.widgets.container)

        return panel

    def add_widgets(self, widgets: list):
        for widget in widgets:
            self.add_widget(widget)

    def clear_layout(self):
        while self.layout().count():
            item = self.layout().takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def resize_panels(self, splitter_handle, delta, orientation):
        splitter_index = self.widgets.container.index(splitter_handle)

        panel_before = self.widgets.container[splitter_index - 1]
        panel_after = self.widgets.container[splitter_index + 1]

        if orientation == "vertical":
            new_height_before = panel_before.height() + delta.y()
            new_height_after = panel_after.height() - delta.y()

            if new_height_before > 0 and new_height_after > 0:
                panel_before.setMinimumHeight(new_height_before)
                panel_after.setMinimumHeight(new_height_after)
        else:
            new_width_before = panel_before.width() + delta.x()
            new_width_after = panel_after.width() - delta.x()

            if new_width_before > 0 and new_width_after > 0:
                panel_before.setMinimumWidth(new_width_before)
                panel_after.setMinimumWidth(new_width_after)
