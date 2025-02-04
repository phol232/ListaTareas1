import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QComboBox, QVBoxLayout, QPushButton,
    QTextEdit, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from src.Capa_Negocio.negTareas import NegTareas
from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Conexion.ConexionMySql import ConexionMySql

class CategoryForm(QMainWindow):
    tarea_guardada = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        try:
            self.neg_tareas = NegTareas()
            print("✅ Lógica de negocio inicializada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error de Conexión", f"❌ Error al conectar con la base de datos: {e}")
            sys.exit(1)

        self.setFixedWidth(330)
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.titulo_input = self.create_form_field("NOMBRE:", "✏️", main_layout)

        desc_label = QLabel("DESCRIPCIÓN:")
        main_layout.addWidget(desc_label)

        self.description = QTextEdit()
        self.description.setPlaceholderText("📝 Escribir aquí...")
        self.description.setFixedHeight(80)
        main_layout.addWidget(self.description)

        self.categoria_combo = self.create_combo_field("CATEGORÍA:", ["Software", "Hardware", "Red"], main_layout)
        self.prioridad_combo = self.create_combo_field("PRIORIDAD:", ["⚡ Alta", "⚡ Media", "⚡ Baja"], main_layout)
        self.estado_combo = self.create_combo_field("ESTADO:", ["🔄 Terminado", "🔄 En Proceso"], main_layout)

        date_label = QLabel("FECHA:")
        main_layout.addWidget(date_label)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        main_layout.addWidget(self.date_edit)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("GUARDAR")
        save_btn.clicked.connect(self.guardar_tarea)
        button_layout.addWidget(save_btn)

        back_btn = QPushButton("VOLVER")
        back_btn.clicked.connect(self.hide)
        button_layout.addWidget(back_btn)

        main_layout.addLayout(button_layout)

    def create_form_field(self, label_text, emoji, layout):
        layout.addWidget(QLabel(label_text))
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"{emoji} Escribir aquí...")
        layout.addWidget(line_edit)
        return line_edit

    def create_combo_field(self, label_text, items, layout):
        layout.addWidget(QLabel(label_text))
        combo = QComboBox()
        combo.addItems(items)
        layout.addWidget(combo)
        return combo

    def guardar_tarea(self):
        try:
            print("💾 Iniciando el proceso para guardar la tarea...")

            if not NegUsuarios.usuario_actual:
                raise Exception("❌ No hay un usuario logueado para asignar la tarea.")

            nueva_tarea = {
                "titulo": self.titulo_input.text().strip(),
                "descripcion": self.description.toPlainText().strip(),
                "categoria": self.categoria_combo.currentText(),
                "prioridad": self.prioridad_combo.currentText(),
                "estado": self.estado_combo.currentText(),
                "fecha": self.date_edit.date().toString("yyyy-MM-dd")
            }

            # Validaciones básicas
            if not nueva_tarea['titulo']:
                raise ValueError("❗ El título de la tarea es obligatorio.")
            if not nueva_tarea['descripcion']:
                raise ValueError("❗ La descripción de la tarea es obligatoria.")

            resultado = self.neg_tareas.crear_tarea(
                titulo=nueva_tarea['titulo'],
                descripcion=nueva_tarea['descripcion'],
                cat_id=nueva_tarea['categoria'],
                prioridad=nueva_tarea['prioridad'],
                estado=nueva_tarea['estado'],
                fecha=nueva_tarea['fecha']
            )

            if 'error' in resultado:
                QMessageBox.critical(self, "Error", resultado['error'])
            else:
                QMessageBox.information(self, "Éxito", resultado.get('message', '✅ Tarea guardada exitosamente.'))
                self.tarea_guardada.emit(nueva_tarea)
                self.limpiar_formulario()

        except ValueError as ve:
            QMessageBox.warning(self, "Campos Obligatorios", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error Inesperado", f"❌ Error inesperado: {str(e)}")

    def limpiar_formulario(self):
        self.titulo_input.clear()
        self.description.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.prioridad_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())


if __name__ == '__main__':
    ConexionMySql.iniciar_pool()

    app = QApplication(sys.argv)
    window = CategoryForm()
    window.show()
    sys.exit(app.exec())
