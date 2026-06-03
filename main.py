import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui.window import MainWindow
from core.dispatcher import Dispatcher
from core.registry import load_plugins, FUNCTIONS


def main():
    app = QApplication(sys.argv)

    # 设置程序图标
    app.setWindowIcon(QIcon("assets/app.ico"))

    # 加载插件
    load_plugins()

    dispatcher = Dispatcher()
    window = MainWindow(dispatcher)

    window.set_functions(FUNCTIONS)

    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()