from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import sys
from PyQt6.QtWidgets import QApplication

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        layout = QVBoxLayout()
        self.label = QLabel("Bienvenido al Menú Principal")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu_window = Menu()
    menu_window.show()
    sys.exit(app.exec())
