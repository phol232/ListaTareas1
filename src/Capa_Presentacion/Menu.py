from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QComboBox, QApplication, QHBoxLayout, QListWidget,
    QFrame, QTableWidgetItem, QHeaderView, QToolButton, QListWidgetItem
)
from PyQt6.QtCore import Qt
import sys

class ModernTodoListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TODO - LIST")
        self.setGeometry(100, 100, 1200, 700)

        # Estilo global de la aplicación
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: 'Segoe UI', Arial;
            }
            QPushButton {
                background-color: #ffd32a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                color: #2f3640;
            }
            QPushButton:hover {
                background-color: #ffc61a;
            }
            QToolButton {
                border: none;
                padding: 5px;
            }
            QLineEdit {
                padding: 10px;
                border: 2px solid #dcdde1;
                border-radius: 5px;
                background: white;
                font-size: 14px;
            }
            QComboBox {
                padding: 10px;
                border: 2px solid #dcdde1;
                border-radius: 5px;
                background: white;
                min-width: 150px;
                font-size: 14px;
            }
        """)

        main_layout = QHBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar_frame = QFrame()
        sidebar_frame.setFixedWidth(250)
        sidebar_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #dcdde1;
            }
        """)
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(10)

        # Título en sidebar
        logo_label = QLabel("TODO - LIST")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #6c5ce7;
            margin-bottom: 20px;
        """)
        sidebar_layout.addWidget(logo_label)

        # Lista de menú con iconos
        self.sidebar = QListWidget()
        menu_items = [
            (" ALL TASKS", "☰"),
            (" CALENDAR", "📅"),
            (" SETTINGS", "⚙️")
        ]
        for text, icon in menu_items:
            item = QListWidgetItem(f"{icon} {text}")
            self.sidebar.addItem(item)

        self.sidebar.setStyleSheet("""
            QListWidget {
                border: none;
                font-size: 16px;
                background-color: white;
                color: #666666;
            }
            QListWidget::item {
                padding: 10px 5px;
            }
            QListWidget::item:selected {
                background-color: transparent;
                color: #6c5ce7;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #f1f2f6;
            }
        """)
        sidebar_layout.addWidget(self.sidebar)

        sidebar_layout.addStretch()
        sidebar_frame.setLayout(sidebar_layout)
        main_layout.addWidget(sidebar_frame)

        # Contenido principal
        content_frame = QFrame()
        content_frame.setStyleSheet("background-color: #f5f6fa;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)

        # Header con welcome y botón de notificaciones
        header_layout = QVBoxLayout()
        top_header = QHBoxLayout()

        # Welcome text
        welcome_label = QLabel("Welcome back Phol, Taquiri")
        welcome_label.setStyleSheet("""
            font-size: 14px;
            color: #666666;
        """)
        top_header.addWidget(welcome_label)

        top_header.addStretch()

        # Botón de notificaciones
        notification_button = QToolButton()
        notification_button.setText("🔔")
        notification_button.setStyleSheet("""
            QToolButton {
                font-size: 20px;
                padding: 5px;
                border-radius: 5px;
            }
            QToolButton:hover {
                background-color: #e0e0e0;
            }
        """)
        top_header.addWidget(notification_button)

        header_layout.addLayout(top_header)

        # Los dos campos rectangulares
        rectangles_layout = QHBoxLayout()

        rect1 = QFrame()
        rect1.setFixedSize(200, 100)
        rect1.setStyleSheet("""
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 5px;
        """)
        rectangles_layout.addWidget(rect1)

        rect2 = QFrame()
        rect2.setFixedHeight(100)
        rect2.setStyleSheet("""
            background-color: white;
            border: 1px solid #dcdde1;
            border-radius: 5px;
        """)
        rectangles_layout.addWidget(rect2)

        header_layout.addLayout(rectangles_layout)
        content_layout.addLayout(header_layout)

        # Filtros y búsqueda
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["PRIORIDAD", "Alta", "Media", "Baja"])
        filter_layout.addWidget(self.priority_combo)

        self.filter_button = QPushButton("🔍 FILTRAR")
        filter_layout.addWidget(self.filter_button)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 SEARCH.....")
        self.search_input.setMinimumWidth(300)
        filter_layout.addWidget(self.search_input)

        filter_layout.addStretch()

        self.create_button = QPushButton("➕ CREAR TAREA")
        self.create_button.setStyleSheet("""
            QPushButton {
                background-color: #ffd32a;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffc61a;
            }
        """)
        filter_layout.addWidget(self.create_button)

        content_layout.addLayout(filter_layout)

        # Tabla de tareas
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(7)
        self.task_table.setHorizontalHeaderLabels([
            "NOMBRE", "DESCRIPCION", "CATEGORIA", "PRIORIDAD", "STATUS", "FECHA", "ACCIONES"
        ])

        self.task_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #dcdde1;
                border-radius: 10px;
                gridline-color: #f5f6fa;
            }
            QHeaderView::section {
                background-color: white;
                padding: 15px;
                border: none;
                border-bottom: 2px solid #dcdde1;
                font-weight: bold;
                color: #2f3640;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f5f6fa;
            }
        """)

        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        content_layout.addWidget(self.task_table)
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernTodoListApp()
    window.show()
    sys.exit(app.exec())
