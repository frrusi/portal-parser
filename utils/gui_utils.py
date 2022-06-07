from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit


class GuiUtils:
    def __init__(self):
        pass

    @staticmethod
    def set_color_and_text(obj, message, config, bool_value: bool) -> None:
        if bool_value:
            obj.setStyleSheet(config.green_color)
            obj.setText(f"✓ {message}")
        else:
            obj.setStyleSheet(config.red_color)
            obj.setText(f"× {message}")

    @staticmethod
    def get_password_visibility_settings(password_obj, icon_obj, visibility: bool):
        visible_icon = QIcon("gui/icons/visible_icon.svg")
        hidden_icon = QIcon("gui/icons/hidden_icon.svg")

        match visibility:
            case True:
                password_obj.setEchoMode(QLineEdit.Password)
                icon_obj.setIcon(visible_icon)
            case _:
                password_obj.setEchoMode(QLineEdit.Normal)
                icon_obj.setIcon(hidden_icon)

    @staticmethod
    def set_color_bar(obj):
        match obj.value():
            case 100:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: green; }")
            case num if 50 <= num < 100:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: yellow; }")
            case _:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: red; }")

    @staticmethod
    def create_message_box(icon, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(icon)
        msg.setWindowTitle(title)
        msg.setText(text)
        return msg
