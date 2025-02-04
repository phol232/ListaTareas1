import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QApplication, QHBoxLayout, QListWidget,
    QFrame, QHeaderView, QToolButton, QListWidgetItem, QMenu, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


from CrearTarea import CategoryForm
from src.Capa_Negocio.negTareas import NegTareas
from src.Capa_Negocio.negUsuarios import NegUsuarios


class ModernTodoListApp(QWidget):
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.neg_tareas = NegTareas()

        self.setWindowTitle("TODO - LIST")
        self.setGeometry(100, 100, 1250, 700)

        self.initUI()
        self.cargar_tareas()

    def initUI(self):
        # ✅ Mostrar el nombre del usuario logueado si existe
        if self.usuario:
            welcome_label = QLabel(f"👋 Bienvenido de nuevo, {self.usuario}")
        else:
            welcome_label = QLabel("Bienvenido al TODO-LIST")

        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

        logo_label = QLabel("TODO - LIST")
        logo_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        sidebar_layout.addWidget(logo_label)

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
        welcome_label = QLabel(f"Welcome back {self.get_current_user()}")
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

        # Rectángulos informativos
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

        # Filtros y búsqueda
        filter_layout = QHBoxLayout()

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
        self.priority_menu = QMenu()
        high_priority = self.priority_menu.addAction("Alta")
        medium_priority = self.priority_menu.addAction("Media")
        low_priority = self.priority_menu.addAction("Baja")
        high_priority.triggered.connect(lambda: self.priority_button.setText("Alta 🔴"))
        medium_priority.triggered.connect(lambda: self.priority_button.setText("Media 🟡"))
        low_priority.triggered.connect(lambda: self.priority_button.setText("Baja 🟢"))
        self.priority_button.setMenu(self.priority_menu)
        filter_layout.addWidget(self.priority_button)

        # Barra de búsqueda
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

        icon_label = QLabel("🔍")
        icon_label.setStyleSheet("color: black; margin: 0px; font-size: 14px; border: none;")
        input_layout.addWidget(icon_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Categorias o estado")
        self.search_input.setMinimumSize(140, 30)
        self.search_input.setFixedHeight(25)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: none;
                background-color: white;
                color: black;
                padding: 0 8px;
                font-size: 14px;
                height: 25px;
            }
        """)
        input_layout.addWidget(self.search_input)

        search_button = QPushButton("Buscar")
        search_button.setFixedHeight(30)
        search_button.setStyleSheet("""
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
        input_layout.addWidget(search_button)
        filter_layout.addWidget(input_wrapper)
        filter_layout.addStretch()

        # Botón crear tarea
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
                border: 2px solid #9c9c9c;
                border-radius: 10px;
                gridline-color: #f5f6fa;
                outline: none;  /* Elimina el contorno al hacer clic */
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
                border: none;
            }
            QTableWidget::item:selected {
                background: transparent;
                color: black;
            }
            QTableWidget::item:focus {
                background: transparent;
                outline: none;
            }
            QTableWidget QWidget {
                background-color: transparent;
            }
        """)

        # Configuraciones adicionales para la tabla
        self.task_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.task_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.task_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.task_table.setShowGrid(False)

        header = self.task_table.horizontalHeader()
        for i in range(6):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.task_table.setColumnWidth(6, 310)
        self.task_table.setColumnWidth(4, 130)

        content_layout.addWidget(self.task_table)
        content_frame.setLayout(content_layout)
        main_layout.addWidget(content_frame)
        self.setLayout(main_layout)

        # Conexiones de señales
        self.create_button.clicked.connect(self.open_new_task_form)

        # 📏 Aumentar la altura de todas las filas
        self.task_table.verticalHeader().setDefaultSectionSize(50)

    def get_current_user(self):
        return "phol232"

    def cargar_tareas(self):
        try:
            print("🔄 Cargando tareas...")
            if not NegUsuarios.usuario_actual:
                QMessageBox.warning(self, "Advertencia", "❌ No hay un usuario logueado.")
                return

            response = self.neg_tareas.listar_tareas()

            self.task_table.setRowCount(0)

            if response.get('error'):
                print(f"❌ {response['error']}")
                QMessageBox.critical(self, "Error", response['error'])
            elif response.get('success') and response.get('tareas'):
                tareas = response['tareas']
                print(f"📋 {len(tareas)} tareas encontradas.")
                for tarea in tareas:
                    self.agregar_tarea(
                        tarea.get('titulo', ''),
                        tarea.get('descripcion', ''),
                        tarea.get('categoria', ''),
                        tarea.get('prioridad', ''),
                        tarea.get('estado', ''),
                        tarea.get('fecha', ''),
                    )
            else:
                print("ℹ️ No hay tareas registradas.")
                QMessageBox.information(self, "Información", "No hay tareas registradas.")

        except Exception as e:
            print(f"❌ Error al cargar tareas: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar tareas: {e}")



    def open_new_task_form(self):
        self.new_task_window = CategoryForm()
        self.new_task_window.tarea_guardada.connect(self.agregar_tarea_desde_formulario)

        main_window_geometry = self.geometry()
        main_x = main_window_geometry.x()
        main_y = main_window_geometry.y()
        main_width = main_window_geometry.width()
        window_width = 350
        window_height = 500
        x_position = main_x + main_width - window_width
        y_position = main_y
        self.new_task_window.resize(window_width, window_height)
        self.new_task_window.move(x_position, y_position)
        self.new_task_window.show()


    def agregar_tarea_desde_formulario(self, tarea):
        try:
           print("✅ Agregando tarea desde el formulario:", tarea)

           self.agregar_tarea(
             tarea.get("titulo", ""),
             tarea.get("descripcion", ""),
             tarea.get("categoria", ""),
             tarea.get("prioridad", ""),
             tarea.get("estado", ""),
             tarea.get("fecha", "")
           )

        except Exception as e:
           print(f"❌ Error al agregar la tarea desde el formulario: {e}")
           QMessageBox.critical(self, "Error", f"Error al agregar la tarea: {e}")



    def agregar_tarea(self, nombre, descripcion, categoria, prioridad, estado, fecha):
        row = self.task_table.rowCount()  # Obtiene el número de filas actuales
        self.task_table.insertRow(row)    # Inserta una nueva fila al final de la tabla

        # Agrega los datos de la tarea a cada celda de la nueva fila
        self.task_table.setItem(row, 0, QTableWidgetItem(nombre))
        self.task_table.setItem(row, 1, QTableWidgetItem(descripcion))
        self.task_table.setItem(row, 2, QTableWidgetItem(categoria))
        self.task_table.setItem(row, 3, QTableWidgetItem(prioridad))
        self.task_table.setItem(row, 4, QTableWidgetItem(estado))
        self.task_table.setItem(row, 5, QTableWidgetItem(fecha))

        # Botones de acción (Editar, Completar, Eliminar)
        action_widget = QWidget()
        action_layout = QHBoxLayout(action_widget)
        action_layout.setContentsMargins(5, 2, 5, 2)
        action_layout.setSpacing(5)

        # Botón Editar
        btn_edit = QPushButton("Editar")
        btn_edit.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: black;
            border: 1px solid #6c5ce7;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #6c5ce7;
            color: white;
        }
        """)
        btn_edit.clicked.connect(lambda: self.editar_tarea(row))

        # Botón Completar
        btn_complete = QPushButton("Completar")
        btn_complete.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: green;
            border: 1px solid green;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: green;
            color: white;
        }
        """)
        btn_complete.clicked.connect(lambda: self.completar_tarea(row))

        # Botón Eliminar
        btn_delete = QPushButton("Eliminar")
        btn_delete.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: red;
            border: 1px solid red;
            padding: 5px 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: red;
            color: white;
        }
        """)
        btn_delete.clicked.connect(lambda: self.eliminar_tarea(row))

        # Añade los botones al layout
        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_complete)
        action_layout.addWidget(btn_delete)


        action_widget.setMinimumWidth(300)
        self.task_table.setCellWidget(row, 6, action_widget)



    def editar_tarea(self, row):
        print(f"Editar tarea en la fila {row}")

    def completar_tarea(self, row):
        self.task_table.item(row, 4).setText("Completada ✅")
        # Cambiar el color del texto a gris para tareas completadas
        for col in range(self.task_table.columnCount() - 1):
            item = self.task_table.item(row, col)
            if item:
                item.setForeground(Qt.GlobalColor.gray)

    def eliminar_tarea(self, row):

       confirm_dialog = QMessageBox()
       confirm_dialog.setIcon(QMessageBox.Icon.Warning)
       confirm_dialog.setWindowTitle("Confirmar Eliminación")
       confirm_dialog.setText("¿Estás seguro de que deseas eliminar esta tarea?")
       confirm_dialog.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
       confirm_dialog.setDefaultButton(QMessageBox.StandardButton.No)


       respuesta = confirm_dialog.exec()


       if respuesta == QMessageBox.StandardButton.Yes:
          self.task_table.removeRow(row)
          print(f"Tarea eliminada en la fila {row}")
       else:
         print("Eliminación cancelada.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModernTodoListApp()
    window.show()
    sys.exit(app.exec())