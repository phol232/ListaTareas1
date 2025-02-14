import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTableWidget, QTableWidgetItem, QComboBox, QApplication, QHBoxLayout, QListWidget,
    QFrame, QHeaderView, QToolButton, QListWidgetItem, QMenu, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from datetime import datetime


from CrearTarea import CategoryForm
from src.Capa_Conexion.ConexionMySql import ConexionMySql
from src.Capa_Negocio.negTareas import NegTareas
from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Presentacion.EditarTarea import EditarTarea



class ModernTodoListApp(QWidget):
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.neg_tareas = NegTareas()

        self.task_data = {}

        self.setWindowTitle("TODO - LIST")
        self.setGeometry(100, 100, 1250, 700)

        self.initUI()
        self.cargar_tareas()

    def cargar_tareas(self):
        try:
            print("🔄 Cargando tareas...")
            if not NegUsuarios.usuario_actual:
                QMessageBox.warning(self, "Advertencia", "❌ No hay un usuario logueado.")
                return

            response = self.neg_tareas.listar_tareas()

            self.task_table.setRowCount(0)
            self.task_data.clear()  # 📌 Limpiar datos en memoria antes de cargar

            if response.get('error'):
                print(f"❌ {response['error']}")
                QMessageBox.critical(self, "Error", response['error'])
            elif response.get('success') and response.get('tareas'):
                tareas = response['tareas']
                print(f"📋 {len(tareas)} tareas encontradas.")

                for tarea in tareas:
                    print(f"🔍 Datos de la tarea recibida: {tarea}")  # 📌 Confirmar que `idTarea` esté presente

                    id_tarea = tarea.get('idTarea')  # 📌 Asegurar que usamos la clave correcta

                    if not id_tarea:
                        print(f"⚠️ Advertencia: Tarea sin ID: {tarea}")
                        continue  # Omitir tareas sin ID

                    print(f"✅ Guardando en memoria: {id_tarea}")
                    self.task_data[id_tarea] = tarea  # 📌 Guardar ID correctamente

                    self.agregar_tarea(
                        id_tarea,
                        tarea.get("titulo", ""),
                        tarea.get("descripcion", ""),
                        tarea.get("categoria", ""),
                        tarea.get("prioridad", ""),
                        tarea.get("estado", ""),
                        tarea.get("fecha", "")
                    )

            else:
                print("ℹ️ No hay tareas registradas.")
                QMessageBox.information(self, "Información", "No hay tareas registradas.")

        except Exception as e:
            print(f"❌ Error al cargar tareas: {e}")
            QMessageBox.critical(self, "Error", f"Error al cargar tareas: {e}")




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

        search_button = QPushButton("BUSCAR")
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
        self.task_table.setColumnCount(8)
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
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        self.task_table.setColumnWidth(6, 310)
        self.task_table.setColumnWidth(4, 110)
        self.task_table.setColumnWidth(2, 100)

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


    def open_new_task_form(self):
        try:
            # ✅ Verificar si hay un usuario logueado
            if not NegUsuarios.usuario_actual:
                QMessageBox.warning(self, "Advertencia", "❌ No hay un usuario logueado.")
                return

            # ✅ Verificar si la conexión a la base de datos está activa
            if not NegUsuarios.conexion_sesion or not NegUsuarios.conexion_sesion.is_connected():
                print("🔄 Reconectando a la base de datos...")
                NegUsuarios.conexion_sesion = ConexionMySql.get_conexion_sesion()

                # Verificar si la reconexión fue exitosa
                if not NegUsuarios.conexion_sesion or not NegUsuarios.conexion_sesion.is_connected():
                    QMessageBox.critical(self, "Error de Conexión", "❌ No hay una conexión activa con la base de datos.")
                    return

            # ✅ Abrir el formulario para crear una nueva tarea si la conexión es exitosa
            self.new_task_window = CategoryForm()
            self.new_task_window.tarea_guardada.connect(self.agregar_tarea_desde_formulario)

            # 📍 Posicionar la ventana de crear tarea
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

        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            QMessageBox.critical(self, "Error", f"❌ Error inesperado: {str(e)}")

    def editar_tarea(self, row):
        try:
            print(f"🔎 Buscando tarea en la fila {row}")

            # ✅ Recupera el ID desde la columna oculta (columna 7)
            id_item = self.task_table.item(row, 7)

            # 🔴 Verifica si la celda está vacía
            if id_item is None:
                print(f"⚠️ Advertencia: No se encontró la celda de ID en la fila {row}.")
                QMessageBox.warning(self, "Error", "❌ No se encontró el ID de la tarea en la tabla.")
                return

            id_tarea = id_item.text().strip()

            print(f"✅ ID recuperado de la tabla: {id_tarea}")

            if not id_tarea:
                QMessageBox.warning(self, "Error", "❌ El ID de la tarea está vacío en la tabla.")
                return

            # 📌 Buscar en memoria
            print(f"📝 Buscando en memoria el ID: {id_tarea}")
            tarea = self.task_data.get(id_tarea)

            if not tarea:
                print(f"⚠️ No se encontró la tarea con ID {id_tarea} en memoria.")
                QMessageBox.warning(self, "Error", f"❌ No se encontró la tarea con ID {id_tarea} en memoria.")
                return

            print(f"✅ Tarea encontrada en memoria: {tarea}")

            # 📌 Crear el diccionario con los datos correctos
            tarea_editable = {
                "idTarea": id_tarea,
                "titulo": tarea.get("titulo", ""),
                "descripcion": tarea.get("descripcion", ""),
                "categoria": tarea.get("categoria", ""),
                "prioridad": tarea.get("prioridad", ""),
                "estado": tarea.get("estado", ""),
                "fecha": tarea.get("fecha", "")
            }

            # 📌 Abrir la ventana de edición con los datos correctos
            self.edit_task_window = EditarTarea(tarea_editable)
            self.edit_task_window.tarea_guardada.connect(lambda t: self.actualizar_tarea_en_tabla(row, t))
            self.edit_task_window.show()

        except Exception as e:
            print(f"❌ Error al abrir el editor de tarea: {e}")
            QMessageBox.critical(self, "Error", f"Error al abrir el editor: {str(e)}")






    def actualizar_tarea_en_tabla(self, row, tarea):
        try:
            print(f"Actualizando tarea en la fila {row}")
            self.task_table.item(row, 0).setText(tarea["titulo"])
            self.task_table.item(row, 1).setText(tarea["descripcion"])
            self.task_table.item(row, 2).setText(tarea["categoria"])
            self.task_table.item(row, 3).setText(tarea["prioridad"])
            self.task_table.item(row, 4).setText(tarea["estado"])
            self.task_table.item(row, 5).setText(tarea["fecha"])
            print("✅ Tarea actualizada correctamente en la tabla")
        except Exception as e:
            print(f"❌ Error al actualizar la tarea en la tabla: {e}")
            QMessageBox.critical(self, "Error", f"Error al actualizar la tarea: {str(e)}")

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





    def agregar_tarea(self, id_tarea, nombre, descripcion, categoria, prioridad, estado, fecha):
        row = self.task_table.rowCount()  # Obtiene el número de filas actuales
        self.task_table.insertRow(row)

        # ✅ Convertir la fecha a cadena si es un objeto datetime
        if isinstance(fecha, datetime):
           fecha = fecha.strftime('%Y-%m-%d')  # Formato Año-Mes-Día

        # 📌 Guardar el idTarea en memoria para recuperarlo después
        self.task_data[id_tarea] = {
            "idTarea": id_tarea,
            "titulo": nombre,
            "descripcion": descripcion,
            "categoria": categoria,
            "prioridad": prioridad,
            "estado": estado,
            "fecha": fecha
        }

        # ✅ Agrega los datos a cada celda de la fila
        self.task_table.setItem(row, 0, QTableWidgetItem(nombre))
        self.task_table.setItem(row, 1, QTableWidgetItem(descripcion))
        self.task_table.setItem(row, 2, QTableWidgetItem(categoria))
        self.task_table.setItem(row, 3, QTableWidgetItem(prioridad))
        self.task_table.setItem(row, 4, QTableWidgetItem(estado))
        self.task_table.setItem(row, 5, QTableWidgetItem(str(fecha)))  # Asegura que siempre sea string

        # 📌 Agregar el ID en una columna oculta (columna 7)
        id_item = QTableWidgetItem(id_tarea)
        self.task_table.setItem(row, 7, id_item)
        self.task_table.setColumnHidden(7, True)

        print(f"✅ ID almacenado en la tabla: {id_tarea} en la fila {row}")

        # 📌 Botones de acción (Editar, Eliminar)
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
        btn_edit.clicked.connect(lambda checked, r=row: self.editar_tarea(r))  # 📌 Recupera el idTarea en editar

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
        btn_delete.clicked.connect(lambda checked, r=row: self.eliminar_tarea(r))  # 📌 Recupera el idTarea en eliminar

        action_layout.addWidget(btn_edit)
        action_layout.addWidget(btn_delete)
        action_widget.setMinimumWidth(200)
        self.task_table.setCellWidget(row, 6, action_widget)




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