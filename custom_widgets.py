__author__ = "Raphael Aslanian"

from PyQt5.QtWidgets import QWidget, QLayout, QPushButton, QDoubleSpinBox, QHBoxLayout, QVBoxLayout, QGroupBox, QComboBox, QLineEdit
from enum import Enum


class CustomizableWidget(QWidget):

    def customize(self, layout=None, children_widgets=None, tag=None):
        self.tag = tag
        if layout is not None:
            if not isinstance(layout, QLayout):
                raise TypeError("The layout argument is not a layout.")
            self.setLayout(layout)
        if children_widgets is not None:
            if self.layout() is None:
                raise TypeError("The widget has no layout, so you cannot add any widget to it.")
            for child_widget in children_widgets:
                if not isinstance(child_widget, QWidget):
                    raise TypeError("One of the children is not a widget.")
                self.layout().addWidget(child_widget)

    def get_widget(self, tag):
        if self.tag == tag:
            return self
        layout = self.layout()
        if layout is None:
            return None
        for idx in range(layout.count()):
            widget = layout.itemAt(idx).widget().get_widget(tag)
            if widget is not None:
                return widget
        return None


class CustomWidget(CustomizableWidget):

    def __init__(self, layout=None, children_widgets=None, tag=None):
        super().__init__()
        self.customize(layout=layout, children_widgets=children_widgets, tag=tag)


class CustomPushButton(QPushButton, CustomizableWidget):

    def __init__(self, text="Button", function_to_connect=None, tag=None):
        super().__init__(text=text)
        self.customize(tag=tag)
        if function_to_connect is not None:
            if not callable(function_to_connect):
                raise TypeError("You must connect a function. No function found.")
            self.clicked.connect(function_to_connect)


class CustomDoubleSpinBox(QDoubleSpinBox, CustomizableWidget):

    class Actions(Enum):
        DECIMALS = 0,
        MIN = 1,
        MAX = 2,
        STEP = 3

    def __init__(self, settings=None, layout=None, children_widgets=None, tag=None):
        super().__init__()
        self.customize(layout, children_widgets, tag)
        self.actions = {
            self.Actions.MIN: self.setMinimum,
            self.Actions.MAX: self.setMaximum,
            self.Actions.STEP: self.setSingleStep,
            self.Actions.DECIMALS: self.setDecimals
        }
        self.edit_settings(settings)

    def edit_settings(self, settings=None):
        if settings is not None:
            if isinstance(settings, dict):
                for key, value in settings:
                    self.actions[key](value)
            elif isinstance(settings, list) or isinstance(settings, set):
                self.actions[self.Actions.DECIMALS](settings[0])
                self.actions[self.Actions.MIN](settings[1])
                self.actions[self.Actions.MAX](settings[2])
                self.actions[self.Actions.STEP](settings[3])
            else:
                raise TypeError("CustomDoubleSpinBox: The settings must be either in a dict or a list.")

    def get_value(self):
        return self.value()


class CustomGroupBox(QGroupBox, CustomizableWidget):

    def __init__(self, title="", layout=None, children_widgets=None, tag=None):
        super().__init__(title=title)
        self.customize(layout, children_widgets, tag)


class CustomComboBox(QComboBox, CustomizableWidget):

    def __init__(self, items, tag=None):
        super().__init__()
        self.customize(tag=tag)
        for item in items:
            self.addItem(item)

    def get_value(self):
        return self.currentText()


class CustomLineEdit(QLineEdit, CustomizableWidget):

    def __init__(self, tag=None):
        super().__init__()
        self.customize(tag=tag)

    def get_value(self):
        return self.text()


class CustomLayout(QLayout):

    def customize(self, spacing=None, contents_margins=None, alignment=None):
        if spacing is not None:
            self.setSpacing(spacing)
        if contents_margins is not None:
            self.setContentsMargins(*contents_margins)
        if alignment is not None:
            self.setAlignment(alignment)


class CustomHBoxLayout(QHBoxLayout, CustomLayout):

    def __init__(self, spacing=None, contents_margins=None, alignment=None):
        super().__init__()
        self.customize(spacing, contents_margins, alignment)


class CustomVBoxLayout(QVBoxLayout, CustomLayout):

    def __init__(self, spacing=None, contents_margins=None, alignment=None):
        super().__init__()
        self.customize(spacing, contents_margins, alignment)
