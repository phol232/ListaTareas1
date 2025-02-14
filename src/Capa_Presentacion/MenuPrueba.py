from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QComboBox, QApplication, QHBoxLayout, QListWidget,
    QFrame, QHeaderView, QToolButton, QListWidgetItem, QButtonGroup, QMenu
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import sys
from CrearTarea import CategoryForm
class ModernTodoListApp2(QWidget):
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
                border: 3px solid #dcdde1;
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
                background-color: #2965f1;
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
            color: white;
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
           font-size: 14px;
           background-color: #2965f1;
           color: white;
        }
        QListWidget::item {
           padding: 10px 10px;
           margin: 0px;
        }
        QListWidget::item:selected {
           background-color: white;
           color: #6c5ce7;
           font-weight: bold;
        }
        QListWidget::item:hover {
           background-color: white;
           color: black;
        }
        QListWidget:focus {
           outline: none; 
           border: none;
        }
        QListWidget::item:focus {
           outline: none; 
           border: none;
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

        # Header
        header_layout = QVBoxLayout()
        top_header = QHBoxLayout()
        welcome_label = QLabel("Welcome back Phol, Taquiri")
        welcome_label.setStyleSheet("font-size: 14px; color: #666666;")
        top_header.addWidget(welcome_label)
        top_header.addStretch()

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

        # Campos rectangulares
        rectangles_layout = QHBoxLayout()
        rect1 = QFrame()
        rect1.setFixedSize(200, 100)
        rect1.setStyleSheet("""
            background-color: white;
            border: 3px solid #dcdde1;
            border-radius: 5px;
        """)
        rectangles_layout.addWidget(rect1)

        rect2 = QFrame()
        rect2.setFixedHeight(100)
        rect2.setStyleSheet("""
            background-color: white;
            border: 3px solid #dcdde1;
            border-radius: 5px;
        """)
        rectangles_layout.addWidget(rect2)

        header_layout.addLayout(rectangles_layout)
        content_layout.addLayout(header_layout)

        # 🚀 **Filtros y búsqueda**
        filter_layout = QHBoxLayout()

        # 🔹 **Menú desplegable con botones (en lugar de QComboBox)**
        self.priority_button = QPushButton("PRIORIDAD")
        self.priority_button.setStyleSheet("""
            QPushButton {
                background-color: #ffd32a;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)

        # Crear menú desplegable
        self.priority_menu = QMenu()

        # Opciones dentro del menú
        high_priority = self.priority_menu.addAction("Alta")
        medium_priority = self.priority_menu.addAction("Media")
        low_priority = self.priority_menu.addAction("Baja")

        # Conectar eventos para cambiar el texto del botón al seleccionar una opción
        high_priority.triggered.connect(lambda: self.priority_button.setText("Alta 🔴"))
        medium_priority.triggered.connect(lambda: self.priority_button.setText("Media 🟡"))
        low_priority.triggered.connect(lambda: self.priority_button.setText("Baja 🟢"))

        # Hacer que el botón abra el menú desplegable
        self.priority_button.setMenu(self.priority_menu)

        filter_layout.addWidget(self.priority_button)

        # Nuevo input y botón de búsqueda con altura ajustada
        input_wrapper = QFrame()
        input_wrapper.setStyleSheet("""
        QFrame {
            background-color: white;
            border-radius: 5px;
            padding: 0px;
            height: 20px;
            border: 1px solid #dcdde1;
        }
        """)
        input_layout = QHBoxLayout(input_wrapper)
        input_layout.setContentsMargins(2, 0, 2, 0)
        input_layout.setSpacing(2)

        # Icono de lupa
        icon_label = QLabel("🔍")
        icon_label.setStyleSheet("color: black; margin: 0px; font-size: 14px; border: none;")
        input_layout.addWidget(icon_label)

        # Input de búsqueda
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Categorias o estado")
        self.email_input.setMinimumSize(140, 30)
        self.email_input.setFixedHeight(25)
        self.email_input.setStyleSheet("""
        QLineEdit {
            border: none;
            background-color: white;
            color: black;
            padding: 0 8px;
            font-size: 14px;
            height: 25px;
        }
        """)
        input_layout.addWidget(self.email_input)

        # Botón de búsqueda
        subscribe_button = QPushButton("Buscar")
        subscribe_button.setFixedHeight(30)
        subscribe_button.setStyleSheet("""
        QPushButton {
            background-color: #ffc61a;
            border-radius: 5px;
            padding: 0 15px;
            font-size: 14px;
            font-weight: bold;
            color: black;
            height: 30px;
        }
        QPushButton:hover {
            background-color: #e1a500;
            color: white;
        }
        """)
        input_layout.addWidget(subscribe_button)
        filter_layout.addWidget(input_wrapper)
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
                border: 3px solid #dcdde1;
                border-radius: 10px;
                gridline-color: #f5f6fa;
            }
            QHeaderView::section {
                background-color: white;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #dcdde1;
                font-weight: bold;
                color: #2f3640;
            }
            QTableWidget::item {
                padding: 10px;
                margin: 5px;
                border-bottom: 1px solid #f5f6fa;
            }
        """)
        content_layout.addWidget(self.task_table)
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)

        # Conectar el botón de "CREAR TAREA"
        self.create_button.clicked.connect(self.open_new_task_form)

    def open_new_task_form(self):

        self.new_task_window = CategoryForm()

        # Obtener la geometría de la ventana principal
        main_window_geometry = self.geometry()
        main_x = main_window_geometry.x()
        main_y = main_window_geometry.y()
        main_width = main_window_geometry.width()

        # Tamaño de la ventana de nueva tarea
        window_width = 350  # Ajusta según el tamaño de tu ventana
        window_height = 500  # Ajusta según el tamaño de tu ventana

        # Calcular la posición en la esquina derecha de la ventana principal
        x_position = main_x + main_width - window_width
        y_position = main_y  # Mantener en la parte superior

        # Mover la ventana emergente a la posición calculada
        self.new_task_window.resize(window_width, window_height)
        self.new_task_window.move(x_position, y_position)

        # Mostrar la ventana
        self.new_task_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernTodoListApp2()
    window.show()
    sys.exit(app.exec())