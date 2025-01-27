import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QSpacerItem, QSizePolicy, QMessageBox
)
from PyQt6.QtGui import QFont, QIcon, QAction
from PyQt6.QtCore import Qt

from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Presentacion.Menu import Menu

class ModernLogin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 550)
        self.setStyleSheet("background-color: white;")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.add_logo(layout)
        layout.addSpacerItem(self.create_spacer(20, 20))
        self.add_titles(layout)
        layout.addSpacerItem(self.create_spacer(20, 20))
        self.add_social_buttons(layout)
        layout.addSpacerItem(self.create_spacer(20, 20))
        self.add_separator(layout)
        layout.addSpacerItem(self.create_spacer(20, 10))
        self.add_input_fields(layout)
        layout.addSpacerItem(self.create_spacer(20, 10))
        self.add_options(layout)
        layout.addSpacerItem(self.create_spacer(20, 20))
        self.add_login_button(layout)
        layout.addSpacerItem(self.create_spacer(20, 20))
        self.add_create_account(layout)
        layout.addSpacerItem(self.create_spacer(20, 40))

        self.setLayout(layout)

    def create_spacer(self, width, height):
        return QSpacerItem(width, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    def add_logo(self, layout):
        logo_label = QLabel("🔵 ToDO-LIST")
        logo_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

    def add_titles(self, layout):
        title_label = QLabel("Log in to your Account")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Welcome back! Select method to log in:")
        subtitle_label.setFont(QFont("Arial", 10))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle_label)

    def add_social_buttons(self, layout):
        social_layout = QHBoxLayout()

        icon_path_google = self.get_icon_path("Google.png")
        icon_path_facebook = self.get_icon_path("Facebook.png")

        self.google_button = QPushButton(" Google")
        self.google_button.setIcon(QIcon(icon_path_google))
        self.google_button.setStyleSheet(self.button_style())
        social_layout.addWidget(self.google_button)

        self.facebook_button = QPushButton(" Facebook")
        self.facebook_button.setIcon(QIcon(icon_path_facebook))
        self.facebook_button.setStyleSheet(self.button_style())
        social_layout.addWidget(self.facebook_button)

        layout.addLayout(social_layout)

    def add_separator(self, layout):
        separator_label = QLabel("OR CONTINUE WITH EMAIL")
        separator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        separator_label.setStyleSheet("color: gray; margin-top: 10px; margin-bottom: 10px;")
        layout.addWidget(separator_label)

    def add_input_fields(self, layout):
        icon_path_email = self.get_icon_path("UserMale.png")
        icon_path_password = self.get_icon_path("Lock.png")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet(self.input_style())
        email_icon = QAction(QIcon(icon_path_email), "", self.email_input)
        self.email_input.addAction(email_icon, QLineEdit.ActionPosition.LeadingPosition)
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.input_style())
        password_icon = QAction(QIcon(icon_path_password), "", self.password_input)
        self.password_input.addAction(password_icon, QLineEdit.ActionPosition.LeadingPosition)
        layout.addWidget(self.password_input)

    def add_options(self, layout):
        options_layout = QHBoxLayout()
        self.remember_me = QCheckBox("Remember me")
        options_layout.addWidget(self.remember_me)

        self.forgot_password = QLabel('<a href="#">Forgot Password?</a>')
        self.forgot_password.setOpenExternalLinks(True)
        self.forgot_password.setStyleSheet("color: #0078D7; font-size: 14px; margin-left: 68px;")
        options_layout.addWidget(self.forgot_password)
        layout.addLayout(options_layout)

    def add_login_button(self, layout):
        self.login_button = QPushButton("Log in")
        self.login_button.setStyleSheet(self.login_button_style())
        self.login_button.clicked.connect(self.on_login_clicked)
        layout.addWidget(self.login_button)

    def add_create_account(self, layout):
        create_account_label = QLabel("Don't have an account? <a href='#'>Create an account</a>")
        create_account_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        create_account_label.setStyleSheet("color: #0078D7; font-size: 14px;")
        create_account_label.setOpenExternalLinks(True)
        layout.addWidget(create_account_label)

    def get_icon_path(self, icon_name):
        return os.path.join(os.path.dirname(__file__), f'../Resources/{icon_name}')

    def button_style(self):
        return """
        QPushButton { 
            background-color: white; 
            border: 1px solid #D1D5DB; 
            padding: 10px; 
            border-radius: 5px; 
            font-size: 14px; 
        }
        QPushButton:hover { 
            background-color: #F3F4F6; 
        }
        """

    def input_style(self):
        return """
        QLineEdit { 
            border: 1px solid #D1D5DB; 
            padding: 12px; 
            border-radius: 5px; 
            font-size: 14px; 
        }
        QLineEdit:focus { 
            border: 1px solid #0078D7; 
        }
        """

    def login_button_style(self):
        return """
        QPushButton { 
            background-color: #0078D7; 
            color: white; 
            font-size: 16px; 
            padding: 14px; 
            border-radius: 5px; 
        }
        QPushButton:hover { 
            background-color: #005BB5; 
        }
        """

    def on_login_clicked(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password.")
            return

        result = NegUsuarios.autenticar_usuario(email, password)

        if result.get('message') == "Login successful":
            QMessageBox.information(self, "Success", "Welcome")
            self.open_menu()
        else:
            QMessageBox.critical(self, "Error", result.get('message', "Invalid credentials."))

    def open_menu(self):
        self.menu_window = Menu()
        self.menu_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = ModernLogin()
    login_window.show()
    sys.exit(app.exec())
