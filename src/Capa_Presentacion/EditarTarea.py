import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QLineEdit, QComboBox, QVBoxLayout, QPushButton,
    QTextEdit, QHBoxLayout, QDateEdit, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt, QDate

from src.Capa_Negocio.negTareas import NegTareas
from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Conexion.ConexionMySql import ConexionMySql


class EditarTarea(QMainWindow):
    # Se define la señal que se emitirá cuando la tarea se guarde exitosamente
    tarea_guardada = pyqtSignal(dict)

    def __init__(self, tarea=None):
        super().__init__()

        try:
           self.neg_tareas = NegTareas()
           print("✅ Lógica de negocio inicializada correctamente.")
        except Exception as e:
           QMessageBox.critical(self, "Error de Conexión", f"❌ Error al conectar con la base de datos: {e}")
           sys.exit(1)

        # Configuración de la ventana
        self.setWindowTitle("Editar Tarea" if tarea else "Nueva Tarea")
        self.setFixedWidth(330)
        self.setFixedHeight(500)
        self.tarea = tarea or {}

        print("✅ Inicializando la UI de edición...")
        self.init_ui()

        if self.tarea:
           print("📝 Cargando datos de la tarea existente...")
           self.llenar_datos()

        print("✅ UI cargada correctamente.")

        # Asegurarse que la ventana se muestre siempre encima
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Campo para el título de la tarea
        self.titulo_input = self.create_form_field("NOMBRE:", "✏️", main_layout)

        # Campo para la descripción
        desc_label = QLabel("DESCRIPCIÓN:")
        main_layout.addWidget(desc_label)
        self.description = QTextEdit()
        self.description.setPlaceholderText("📝 Escribir aquí...")
        self.description.setFixedHeight(80)
        main_layout.addWidget(self.description)

        # Combos para categoría, prioridad y estado
        self.categoria_combo = self.create_combo_field("CATEGORÍA:", ["Software", "Hardware", "Red"], main_layout)
        self.prioridad_combo = self.create_combo_field("PRIORIDAD:", ["⚡ Alta", "⚡ Media", "⚡ Baja"], main_layout)
        self.estado_combo = self.create_combo_field("ESTADO:", ["🔄 Terminado", "🔄 En Proceso"], main_layout)

        # Campo para seleccionar la fecha
        date_label = QLabel("FECHA:")
        main_layout.addWidget(date_label)
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDate(QDate.currentDate())
        main_layout.addWidget(self.date_edit)

        # Botones para guardar o volver
        button_layout = QHBoxLayout()
        save_btn = QPushButton("GUARDAR")
        save_btn.clicked.connect(self.guardar_tarea)
        button_layout.addWidget(save_btn)

        back_btn = QPushButton("VOLVER")
        back_btn.clicked.connect(self.hide)
        button_layout.addWidget(back_btn)

        main_layout.addLayout(button_layout)

    def create_form_field(self, label_text, emoji, layout):
        """Crea un campo de formulario con etiqueta y QLineEdit."""
        layout.addWidget(QLabel(label_text))
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"{emoji} Escribir aquí...")
        layout.addWidget(line_edit)
        return line_edit

    def create_combo_field(self, label_text, items, layout):
        """Crea un campo con etiqueta y un QComboBox."""
        layout.addWidget(QLabel(label_text))
        combo = QComboBox()
        combo.addItems(items)
        layout.addWidget(combo)
        return combo

    def llenar_datos(self):
        """Carga los datos de la tarea en los campos de entrada."""
        try:
            print(f"📌 Cargando datos en formulario de edición: {self.tarea}")

            self.titulo_input.setText(self.tarea.get("titulo", ""))
            self.description.setPlainText(self.tarea.get("descripcion", ""))
            self.categoria_combo.setCurrentText(self.tarea.get("categoria", "Software"))
            self.prioridad_combo.setCurrentText(self.tarea.get("prioridad", "⚡ Media"))
            self.estado_combo.setCurrentText(self.tarea.get("estado", "🔄 En Proceso"))

            # Convertir la fecha almacenada (cadena) a QDate
            fecha_str = str(self.tarea.get("fecha", QDate.currentDate().toString("yyyy-MM-dd")))
            fecha_qdate = QDate.fromString(fecha_str, "yyyy-MM-dd")
            if not fecha_qdate.isValid():
                fecha_qdate = QDate.currentDate()
            self.date_edit.setDate(fecha_qdate)

        except Exception as e:
            print(f"❌ Error al cargar los datos en EditarTarea: {e}")

    def guardar_tarea(self):
        """Recoge los datos ingresados, los valida y actualiza la tarea existente."""
        try:
           print("💾 Iniciando el proceso para actualizar la tarea...")

           if not NegUsuarios.usuario_actual:
              raise Exception("❌ No hay un usuario logueado para asignar la tarea.")


           id_tarea = self.tarea.get("idTarea")
           if not id_tarea:
              raise ValueError("❗ No se puede actualizar la tarea sin un ID válido.")

           tarea_actualizada = {
              "idTarea": id_tarea,
              "titulo": self.titulo_input.text().strip(),
              "descripcion": self.description.toPlainText().strip(),
              "categoria": self.categoria_combo.currentText(),
              "prioridad": self.prioridad_combo.currentText(),
              "estado": self.estado_combo.currentText(),
              "fecha": self.date_edit.date().toString("yyyy-MM-dd")
           }

           # Validaciones básicas
           if not tarea_actualizada['titulo']:
              raise ValueError("❗ El título de la tarea es obligatorio.")
           if not tarea_actualizada['descripcion']:
              raise ValueError("❗ La descripción de la tarea es obligatoria.")

           # 📌 Llamamos a actualizar_tarea en lugar de crear_tarea
           resultado = self.neg_tareas.actualizar_tarea(
             id_tarea=tarea_actualizada['idTarea'],
             titulo=tarea_actualizada['titulo'],
             descripcion=tarea_actualizada['descripcion'],
             cat_id=tarea_actualizada['categoria'],
             prioridad=tarea_actualizada['prioridad'],
             estado=tarea_actualizada['estado'],
             fecha=tarea_actualizada['fecha']
           )

           if 'error' in resultado:
              QMessageBox.critical(self, "Error", resultado['error'])
           else:
              QMessageBox.information(self, "Éxito", resultado.get('message', '✅ Tarea actualizada exitosamente.'))
              # Emitir la señal para notificar que la tarea se ha actualizado
              self.tarea_guardada.emit(tarea_actualizada)
              self.limpiar_formulario()

        except ValueError as ve:
          QMessageBox.warning(self, "Campos Obligatorios", str(ve))
        except Exception as e:
          QMessageBox.critical(self, "Error Inesperado", f"❌ Error inesperado: {str(e)}")


    def limpiar_formulario(self):
        """Limpia los campos del formulario tras guardar la tarea."""
        self.titulo_input.clear()
        self.description.clear()
        self.categoria_combo.setCurrentIndex(0)
        self.prioridad_combo.setCurrentIndex(0)
        self.estado_combo.setCurrentIndex(0)
        self.date_edit.setDate(QDate.currentDate())


if __name__ == '__main__':
    ConexionMySql.iniciar_pool()

    app = QApplication(sys.argv)
    window = EditarTarea()
    window.show()
    sys.exit(app.exec())
