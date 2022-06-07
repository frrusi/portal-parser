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
    def set_color_bar(obj):
        match obj.value():
            case 100:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: green; }")
            case num if 50 <= num < 100:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: yellow; }")
            case _:
                obj.setStyleSheet("QProgressBar::chunk:horizontal { background-color: red; }")
