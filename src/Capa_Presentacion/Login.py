import sys
import os
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QCheckBox, QSpacerItem, QSizePolicy, QMessageBox, QAction
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from src.Capa_Negocio.negUsuarios import NegUsuarios
from src.Capa_Presentacion.Menu import Menu

class ModernLogin(QWidget):
    """
    A modern login window implementation using PyQt6.
    """

    WINDOW_TITLE = "Login"
    WINDOW_GEOMETRY = (100, 100, 400, 550)
    RESOURCES_PATH = "../Resources"

    # Style constants
    STYLES = {
        'WINDOW': "background-color: white;",
        'BUTTON': """
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
        """,
        'INPUT': """
            QLineEdit { 
                border: 1px solid #D1D5DB; 
                padding: 12px; 
                border-radius: 5px; 
                font-size: 14px; 
            }
            QLineEdit:focus { 
                border: 1px solid #0078D7; 
            }
        """,
        'LOGIN_BUTTON': """
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
    }

    def __init__(self):
        super().__init__()
        self.init_window()
        self.setup_ui_components()

    def init_window(self):
        """Initialize the main window properties."""
        self.setWindowTitle(self.WINDOW_TITLE)
        self.setGeometry(*self.WINDOW_GEOMETRY)
        self.setStyleSheet(self.STYLES['WINDOW'])

    def setup_ui_components(self):
        """Set up all UI components and layouts."""
        main_layout = QVBoxLayout()
        self._setup_header_section(main_layout)
        self._setup_social_login_section(main_layout)
        self._setup_email_login_section(main_layout)
        self._setup_footer_section(main_layout)
        self.setLayout(main_layout)

    def _setup_header_section(self, layout: QVBoxLayout):
        """Set up the header section with logo and titles."""
        self._add_logo(layout)
        self._add_spacer(layout)
        self._add_titles(layout)
        self._add_spacer(layout)

    def _setup_social_login_section(self, layout: QVBoxLayout):
        """Set up the social login buttons section."""
        social_layout = QHBoxLayout()
        self._create_social_button(social_layout, "Google", "Google.png")
        self._create_social_button(social_layout, "Facebook", "Facebook.png")
        layout.addLayout(social_layout)
        self._add_separator(layout)

    def _setup_email_login_section(self, layout: QVBoxLayout):
        """Set up the email login section with input fields."""
        self.email_input = self._create_input_field("Email", "UserMale.png")
        self.password_input = self._create_input_field("Password", "Lock.png", is_password=True)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        self._setup_login_options(layout)

    def _setup_footer_section(self, layout: QVBoxLayout):
        """Set up the footer section with login button and create account link."""
        self._add_login_button(layout)
        self._add_create_account_link(layout)

    def _create_input_field(self, placeholder: str, icon_name: str, is_password: bool = False) -> QLineEdit:
        """Create an input field with the specified properties."""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setStyleSheet(self.STYLES['INPUT'])
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        icon_path = self._get_resource_path(icon_name)
        icon_action = QAction(QIcon(icon_path), "", input_field)
        input_field.addAction(icon_action, QLineEdit.ActionPosition.LeadingPosition)
        return input_field

    def _setup_login_options(self, layout: QVBoxLayout):
        """Set up the remember me checkbox and forgot password link."""
        options_layout = QHBoxLayout()
        self.remember_me = QCheckBox("Remember me")
        self.forgot_password = self._create_link_label("Forgot Password?", margin_left="68px")
        options_layout.addWidget(self.remember_me)
        options_layout.addWidget(self.forgot_password)
        layout.addLayout(options_layout)

    @staticmethod
    def _add_spacer(layout: QVBoxLayout, width: int = 20, height: int = 20):
        """Add a spacer item to the layout."""
        spacer = QSpacerItem(width, height, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(spacer)

    def _get_resource_path(self, resource_name: str) -> str:
        """Get the full path for a resource file."""
        return os.path.join(os.path.dirname(__file__), self.RESOURCES_PATH, resource_name)

    def _create_link_label(self, text: str, margin_left: str = "0px") -> QLabel:
        """Create a clickable link label."""
        label = QLabel(f'<a href="#">{text}</a>')
        label.setOpenExternalLinks(True)
        label.setStyleSheet(f"color: #0078D7; font-size: 14px; margin-left: {margin_left};")
        return label

    def on_login_clicked(self):
        """Handle login button click event."""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not self._validate_login_input(email, password):
            return

        self._process_login(email, password)

    def _validate_login_input(self, email: str, password: str) -> bool:
        """Validate login input fields."""
        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password.")
            return False
        return True

    def _process_login(self, email: str, password: str):
        """Process the login attempt."""
        result = NegUsuarios.autenticar_usuario(email, password)
        if result.get('message') == "Login successful":
            QMessageBox.information(self, "Success", "Welcome")
            self._open_menu()
        else:
            QMessageBox.critical(self, "Error", result.get('message', "Invalid credentials."))

    def _open_menu(self):
        """Open the menu window and close the login window."""
        self.menu_window = Menu()
        self.menu_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = ModernLogin()
    login_window.show()
    sys.exit(app.exec())