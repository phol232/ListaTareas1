import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QComboBox, QVBoxLayout, QPushButton,
    QTextEdit, QHBoxLayout, QDateEdit, QMessageBox, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.Capa_Negocio.negTareas import NegTareas
from src.Capa_Conexion.ConexionMySql import ConexionMySql

class CategoryForm(QMainWindow):
    tarea_guardada = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        # ✅ Inicializar la lógica de negocio con manejo de errores
        try:
            self.neg_tareas = NegTareas()
            print("✅ Lógica de negocio inicializada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", f"❌ Error al conectar con la base de datos: {e}")
            sys.exit(1)

        self.setFixedWidth(330)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        main_widget.setLayout(main_layout)

        # Form fields
        self.titulo_input = self.create_form_field("NOMBRE:", "✏️", main_layout)

        # Description field
        desc_label = QLabel("DESCRIPCIÓN:")
        desc_label.setObjectName("label")
        main_layout.addWidget(desc_label)

        self.description = QTextEdit()
        self.description.setPlaceholderText("📝 Escribir aquí...")
        self.description.setFixedHeight(80)
        main_layout.addWidget(self.description)

        # Combo boxes
        self.categoria_combo = self.create_combo_field("CATEGORÍA:", ["Software", "Hardware", "Red"], main_layout)
        self.prioridad_combo = self.create_combo_field("PRIORIDAD:", ["⚡ Alta", "⚡ Media", "⚡ Baja"], main_layout)
        self.estado_combo = self.create_combo_field("ESTADO:", ["🔄 Terminado", "🔄 En Proceso"], main_layout)

        # Date field with calendar emoji
        date_label = QLabel("FECHA:")
        date_label.setObjectName("label")
        main_layout.addWidget(date_label)

        date_layout = QHBoxLayout()
        calendar_icon = QLabel("📅")
        calendar_icon.setFixedWidth(20)
        calendar_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())

        date_layout.addWidget(calendar_icon)
        date_layout.addWidget(self.date_edit)
        main_layout.addLayout(date_layout)

        # Bottom buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("GUARDAR")
        save_btn.clicked.connect(self.guardar_tarea)
        button_layout.addWidget(save_btn)

        back_btn = QPushButton("VOLVER")
        back_btn.clicked.connect(self.hide)
        button_layout.addWidget(back_btn)

        main_layout.addLayout(button_layout)

    def create_form_field(self, label_text, emoji, layout):
        label = QLabel(label_text)
        layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"{emoji} Escribir aquí...")
        layout.addWidget(line_edit)

        return line_edit

    def create_combo_field(self, label_text, items, layout):
        label = QLabel(label_text)
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(items)
        layout.addWidget(combo)

        return combo


    def guardar_tarea(self):
        try:
            print("💾 Iniciando proceso de guardado...")

            # ✅ Obtener los datos del formulario
            nueva_tarea = {
                "titulo": self.titulo_input.text(),
                "descripcion": self.description.toPlainText(),
                "categoria": self.categoria_combo.currentText(),
                "prioridad": self.prioridad_combo.currentText(),
                "estado": self.estado_combo.currentText(),
                "fecha": self.date_edit.date().toString("yyyy-MM-dd")
            }

            # ✅ Guardar la tarea en la base de datos
            resultado = self.neg_tareas.crear_tarea(
                titulo=nueva_tarea['titulo'],
                descripcion=nueva_tarea['descripcion'],
                cat_id=nueva_tarea['categoria'],
                prioridad=nueva_tarea['prioridad'],
                estado=nueva_tarea['estado'],
                fecha=nueva_tarea['fecha']
            )

            # ✅ Verificación del resultado
            if 'error' in resultado:
                print(f"❌ Error al guardar la tarea: {resultado['error']}")
                QMessageBox.critical(self, "Error Crítico", resultado.get('error'))
            else:
                print("✅ Tarea guardada exitosamente en la base de datos.")
                QMessageBox.information(self, "Tarea Guardada", resultado.get('message', 'Tarea guardada exitosamente.'))

                # ✅ Emitir la señal para actualizar la tabla
                self.tarea_guardada.emit(nueva_tarea)  # ✅ Ahora envía la clave 'categoria'

                # ✅ Limpiar el formulario después de guardar
                self.limpiar_formulario()

        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            QMessageBox.critical(self, "Error Inesperado", str(e))


    def limpiar_formulario(self):
        self.titulo_input.clear()
        self.description.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.prioridad_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())


if __name__ == '__main__':
    ConexionMySql.iniciar_pool()  # Iniciar el pool de conexiones

    app = QApplication(sys.argv)
    window = CategoryForm()
    window.show()
    sys.exit(app.exec())
