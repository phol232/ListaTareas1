import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QComboBox, QVBoxLayout, QPushButton,
                             QTextEdit, QHBoxLayout, QDateEdit, QFrame)
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt, QDate

class CategoryForm(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedWidth(330)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)
        main_widget.setLayout(main_layout)

        # Header layout with category button
        header_layout = QHBoxLayout()

        new_category_btn = QPushButton("NUEVA CATEGORÍA")
        new_category_btn.setObjectName("newCategoryButton")
        new_category_btn.setFixedSize(120, 30)
        header_layout.addWidget(new_category_btn, alignment=Qt.AlignmentFlag.AlignRight)

        main_layout.addLayout(header_layout)

        # Form fields con emojis dentro de los inputs
        self.create_form_field("NOMBRE:", "✏️", main_layout)

        # Description field
        desc_label = QLabel("DESCRIPCIÓN:")
        desc_label.setObjectName("label")
        main_layout.addWidget(desc_label)

        self.description = QTextEdit()
        self.description.setObjectName("description")
        self.description.setPlaceholderText("📝 Escribir aquí...")
        self.description.setFixedHeight(80)
        main_layout.addWidget(self.description)

        # Combo boxes con emojis dentro
        self.create_combo_field("CATEGORÍA:", ["🏷️ SOFTWARE", "🏷️ HARDWARE", "🏷️ RED"], main_layout)
        self.create_combo_field("PRIORIDAD:", ["⚡ ALTA", "⚡ MEDIA", "⚡ BAJA"], main_layout)
        self.create_combo_field("ESTADO:", ["🔄 TERMINADO", "🔄 EN PROCESO", "🔄 PENDIENTE"], main_layout)

        # Date field with calendar
        date_label = QLabel("FECHA:")
        date_label.setObjectName("label")
        main_layout.addWidget(date_label)

        self.date_edit = QDateEdit()
        self.date_edit.setObjectName("dateEdit")
        self.date_edit.setFixedHeight(25)
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        main_layout.addWidget(self.date_edit)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        save_btn = QPushButton("GUARDAR")
        save_btn.setObjectName("saveButton")
        save_btn.setFixedSize(125, 35)
        button_layout.addWidget(save_btn)

        back_btn = QPushButton("VOLVER")
        back_btn.setObjectName("backButton")
        back_btn.setFixedSize(125, 35)
        back_btn.clicked.connect(self.hide)  # Oculta la ventana al hacer clic en Volver
        button_layout.addWidget(back_btn)

        main_layout.addLayout(button_layout)

        # Apply stylesheet
        self.setStyleSheet('''
            QMainWindow {
                background-color: white;
            }
            #newCategoryButton {
                background-color: #ffd700;
                color: black;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                font-size: 11px;
            }
            #label {
                color: #444;
                font-weight: bold;
                font-size: 12px;
                margin-top: 5px;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                height: 25px;
                font-size: 12px;
            }
            #dateEdit {
                padding-left: 25px;
            }
            QTextEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 3px;
                background-color: white;
                font-size: 12px;
            }
            #description {
                min-height: 60px;
            }
            #saveButton, #backButton {
                padding: 8px;
                border: none;
                border-radius: 3px;
                font-weight: bold;
                font-size: 12px;
                background-color: #ffd700;
                color: black;
            }
            #saveButton:hover, #backButton:hover, #newCategoryButton:hover {
                background-color: #ffc700;
            }
        ''')

    def create_form_field(self, label_text, emoji, layout):
        label = QLabel(label_text)
        label.setObjectName("label")
        layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(f"{emoji} Escribir aquí...")
        line_edit.setObjectName("input")
        line_edit.setFixedHeight(25)
        layout.addWidget(line_edit)

    def create_combo_field(self, label_text, items, layout):
        label = QLabel(label_text)
        label.setObjectName("label")
        layout.addWidget(label)

        combo = QComboBox()
        combo.addItems(items)
        combo.setObjectName("combo")
        combo.setFixedHeight(25)
        layout.addWidget(combo)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CategoryForm()
    window.show()
    sys.exit(app.exec())
