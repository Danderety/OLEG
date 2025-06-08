import os
import sys
import sqlite3
import platform
import shutil
import configparser
import hashlib
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QFileDialog, QColorDialog, QFontDialog,
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget, 
                             QLineEdit, QTableWidget, QDialog,
                             QTableWidgetItem, QMessageBox, QMenuBar, 
                             QMenu, QHeaderView, QInputDialog)
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QColor, QFont, QDesktopServices, QAction
from PyQt6.QtCore import QUrl

DB_FILE = "notes.db"
ATTACHMENTS_DIR = "attachments"
CONFIG_FILE = "config.ini"
PASSWORD_FILE = "password.ini"  # Отдельный файл для хранения пароля
SECRET_KEY = "mysecretkey123"  # Секретный ключ для сброса пароля
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

class PasswordManager:
    @staticmethod
    def save_password(password):
        """Сохраняет хеш пароля в отдельный файл"""
        config = configparser.ConfigParser()
        config["Security"] = {}
        
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        config["Security"]["salt"] = salt.hex()
        config["Security"]["password_hash"] = key.hex()
        
        with open(PASSWORD_FILE, 'w') as f:
            config.write(f)

    @staticmethod
    def check_password(password):
        """Проверяет соответствие пароля сохраненному хешу"""
        if not os.path.exists(PASSWORD_FILE):
            return False
            
        config = configparser.ConfigParser()
        config.read(PASSWORD_FILE)
        
        if not config.has_section("Security"):
            return False
            
        saved_hash = config["Security"].get("password_hash", "")
        salt = bytes.fromhex(config["Security"]["salt"])
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        return key.hex() == saved_hash

    @staticmethod
    def is_password_set():
        """Проверяет, установлен ли пароль"""
        return os.path.exists(PASSWORD_FILE) and os.path.getsize(PASSWORD_FILE) > 0

class PasswordDialog(QDialog):
    def __init__(self, parent=None, theme="dark", mode="login"):
        super().__init__(parent)
        self.mode = mode
        self.theme = theme
        
        titles = {
            "create": "Создать пароль",
            "reset": "Сброс пароля", 
            "login": "Введите пароль"
        }
        self.setWindowTitle(titles.get(mode, "Введите пароль"))
        self.setFixedSize(350, 200 if mode == "reset" else 180)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        layout = QVBoxLayout()

        if self.mode == "reset":
            self.secret_input = QLineEdit()
            self.secret_input.setPlaceholderText("Введите секретный ключ")
            layout.addWidget(QLabel("Секретный ключ:"))
            layout.addWidget(self.secret_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        if self.mode in ("create", "reset"):
            self.confirm_input = QLineEdit()
            self.confirm_input.setPlaceholderText("Повторите пароль")
            self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(QLabel("Пароль:"))
            layout.addWidget(self.password_input)
            layout.addWidget(QLabel("Подтвердите пароль:"))
            layout.addWidget(self.confirm_input)
        else:
            layout.addWidget(QLabel("Пароль:"))
            layout.addWidget(self.password_input)
        
        self.message_label = QLabel()
        self.message_label.setVisible(False)

        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.check_password)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addWidget(self.message_label)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def apply_theme(self):
        theme_styles = {
            "dark": """
                QDialog { background-color: #1e1e1e; color: #f0f0f0; }
                QLineEdit, QPushButton, QLabel {
                    background-color: #2b2b2b; color: #f0f0f0;
                    border: 1px solid #3a3a3a; border-radius: 6px; padding: 4px;
                }
                QPushButton { min-width: 80px; }
            """,
            "light": """
                QDialog { background-color: #ffffff; color: #000000; }
                QLineEdit, QPushButton, QLabel {
                    background-color: #f9f9f9; color: #000000;
                    border: 1px solid #cccccc; border-radius: 6px; padding: 4px;
                }
                QPushButton { min-width: 80px; }
            """
        }
        self.setStyleSheet(theme_styles.get(self.theme, ""))

    def check_password(self):
        if self.mode == "reset":
            if self.secret_input.text() != SECRET_KEY:
                self.show_error("Неверный секретный ключ!")
                return
            
            new_password = self.password_input.text()
            confirm_password = self.confirm_input.text()
            
            if not self.validate_password(new_password, confirm_password):
                return
                
            PasswordManager.save_password(new_password)
            QMessageBox.information(self, "Успех", "Пароль успешно изменен!")
            self.accept()
            return
        
        if self.mode == "create":
            new_password = self.password_input.text()
            confirm_password = self.confirm_input.text()
            
            if not self.validate_password(new_password, confirm_password):
                return
                
            PasswordManager.save_password(new_password)
            self.accept()
            return
        
        # Режим входа
        entered_password = self.password_input.text()
        
        if not PasswordManager.is_password_set():
            self.show_error("Пароль не установлен!")
            return
            
        if PasswordManager.check_password(entered_password):
            self.accept()
        else:
            self.show_error("Неверный пароль!")

    def validate_password(self, password, confirm_password):
        if password != confirm_password:
            self.show_error("Пароли не совпадают!")
            return False
            
        if len(password) < 4:
            self.show_error("Пароль должен содержать минимум 4 символа!")
            return False
            
        return True

    def show_error(self, message):
        self.message_label.setText(message)
        self.message_label.setStyleSheet("color: red;")
        self.message_label.setVisible(True)

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.authenticated = False
        self.initialize_authentication()
        
        if not self.authenticated:
            sys.exit(0)
            
        self.setup_main_window()

    def initialize_authentication(self):
        # Первый запуск - создаем пароль
        if not PasswordManager.is_password_set():
            dialog = PasswordDialog(theme="dark", mode="create")
            if dialog.exec():
                self.authenticated = True
            return
        
        # Обычный вход
        attempts = 3
        while attempts > 0:
            dialog = PasswordDialog(theme=self.get_initial_theme(), mode="login")
            if dialog.exec():
                self.authenticated = True
                return
                
            attempts -= 1
            if attempts > 0:
                QMessageBox.warning(self, "Ошибка", 
                                  f"Неверный пароль. Осталось попыток: {attempts}")
        
        # После 3 неудачных попыток - предлагаем сброс
        msg = QMessageBox()
        msg.setWindowTitle("Забыли пароль?")
        msg.setText("Хотите сбросить пароль с помощью секретного ключа?")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            reset_dialog = PasswordDialog(theme=self.get_initial_theme(), mode="reset")
            if reset_dialog.exec():
                self.authenticated = True
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сбросить пароль")
        else:
            QMessageBox.information(self, "Выход", "Приложение будет закрыто")

    def setup_main_window(self):
        self.setWindowTitle("Заметки")
        self.setGeometry(200, 200, 800, 600)
        self.load_theme_preference()
        self.init_db()
        self.init_ui()
        self.load_notes()
        self.schedule_notification()
        self.apply_theme()

    def get_initial_theme(self):
        config = configparser.ConfigParser()
        if config.read(CONFIG_FILE) and "Preferences" in config and "theme" in config["Preferences"]:
            return config["Preferences"]["theme"]
        return "dark"

    def init_db(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                content TEXT,
                attachment TEXT
            )
        """)
        self.conn.commit()

    def init_ui(self):
        menu_bar = self.menuBar()
        
        # Меню темы
        theme_menu = menu_bar.addMenu("Тема")
        self.light_action = QAction("Светлая", self)
        self.dark_action = QAction("Тёмная", self)
        self.light_action.triggered.connect(lambda: self.set_theme("light"))
        self.dark_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(self.light_action)
        theme_menu.addAction(self.dark_action)
        
        # Меню безопасности
        security_menu = menu_bar.addMenu("Безопасность")
        change_pass_action = QAction("Сменить пароль", self)
        change_pass_action.triggered.connect(self.change_password)
        security_menu.addAction(change_pass_action)

        # Остальные элементы UI...
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Дата", "Текст", "Вложение"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.horizontalHeader().setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.horizontalHeader().customContextMenuRequested.connect(self.header_context_menu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        self.table.cellDoubleClicked.connect(self.handle_cell_double_click)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Новая заметка")

        self.save_button = QPushButton("Сохранить", self)
        self.save_button.clicked.connect(self.save_note)

        self.photo_button = QPushButton("Фото", self)
        self.video_button = QPushButton("Видео", self)
        self.photo_button.clicked.connect(self.attach_photo)
        self.video_button.clicked.connect(self.attach_video)

        attach_layout = QHBoxLayout()
        attach_layout.addWidget(self.photo_button)
        attach_layout.addWidget(self.video_button)

        layout = QVBoxLayout()
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Поиск по заметкам")
        self.search_field.textChanged.connect(self.load_notes)
        layout.addWidget(self.search_field)
        layout.addWidget(self.table)
        layout.addWidget(self.input_field)
        layout.addWidget(self.save_button)
        layout.addLayout(attach_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.attachment = None

    def change_password(self):
        dialog = PasswordDialog(parent=self, theme=self.current_theme, mode="reset")
        dialog.exec()

    def save_theme_preference(self):
        config = configparser.ConfigParser()
        config["Preferences"] = {"theme": self.current_theme}
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)

    def load_theme_preference(self):
        config = configparser.ConfigParser()
        if config.read(CONFIG_FILE) and "Preferences" in config and "theme" in config["Preferences"]:
            self.current_theme = config["Preferences"]["theme"]
        else:
            self.current_theme = "dark"

    def set_theme(self, theme):
        self.current_theme = theme
        self.save_theme_preference()
        self.apply_theme()
        self.load_notes()

    def apply_theme(self):
        common_dark_menu = '''
            QScrollBar:vertical { background: #2b2b2b; width: 12px; margin: 0px; }
            QScrollBar::handle:vertical { background: #2b2b2b; border-radius: 4px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QMenu { background-color: #2b2b2b; color: white; border: 1px solid #3a3a3a; }
            QMenu::item:selected { background-color: #505050; }
            QHeaderView::section { background-color: #2b2b2b; color: white; border: 1px solid #3a3a3a; }
            QMenuBar { background-color: #2b2b2b; color: white; }
            QMenuBar::item:selected { background-color: #3c3c3c; }
        '''
        common_light_menu = '''
            QScrollBar:vertical { background: #000000; width: 12px; margin: 0px; }
            QScrollBar::handle:vertical { background:#000000; border-radius: 4px; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QMenu { background-color: #ffffff; color: black; border: 1px solid #cccccc; }
            QMenu::item:selected { background-color: #d2e4ff; }
            QHeaderView::section { background-color: #f0f0f0; color: black; border: 1px solid #cccccc; }
            QMenuBar { background-color: #f0f0f0; color: black; }
            QMenuBar::item:selected { background-color: #e0e0e0; }
        '''

        if self.current_theme == "dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #1e1e1e; color: #f0f0f0; }
                QLineEdit, QTableWidget, QPushButton, QLabel {
                    background-color: #2b2b2b; color: #f0f0f0;
                    border: 1px solid #3a3a3a; border-radius: 6px; padding: 4px;
                }
                QTableWidget::item:selected { background-color: #505050; }
            """ + common_dark_menu)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #ffffff; color: #000000; }
                QLineEdit, QPushButton, QLabel {
                    background-color: #f9f9f9; color: #000000;
                    border: 1px solid #cccccc; border-radius: 6px; padding: 4px;
                }
                QTableWidget {
                    background-color: #ffffff; color: #000000;
                    gridline-color: #dddddd; border: 1px solid #ccc;
                }
                QTableWidget::item:selected { background-color: #d2e4ff; }
            """ + common_light_menu)


    def save_note(self):
        text = self.input_field.text().strip()
        if text:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            saved_attachment = self.copy_attachment() if self.attachment else None
            self.cursor.execute("INSERT INTO notes (timestamp, content, attachment) VALUES (?, ?, ?)",
                              (timestamp, text, saved_attachment))
            self.conn.commit()
            self.input_field.clear()
            self.attachment = None
            self.load_notes()

    def copy_attachment(self):
        if not self.attachment:
            return None
        filename = os.path.basename(self.attachment)
        new_path = os.path.join(ATTACHMENTS_DIR, f"{datetime.now().timestamp()}_{filename}")
        shutil.copy2(self.attachment, new_path)
        return new_path

    def load_notes(self, filter_attachments=None):
        self.table.setRowCount(0)
        filter_text = self.search_field.text().lower()
        notes = list(self.cursor.execute("SELECT id, timestamp, content, attachment FROM notes"))
        notes = [note for note in notes if filter_text in note[2].lower()]
        
        if filter_attachments is True:
            notes = [note for note in notes if note[3]]
        elif filter_attachments is False:
            notes = [note for note in notes if not note[3]]
            
        for row_idx, (note_id, timestamp, content, attachment) in enumerate(notes):
            self.table.insertRow(row_idx)
            item_0 = QTableWidgetItem(timestamp)
            item_0.setFlags(item_0.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_1 = QTableWidgetItem(content)
            item_1.setFlags(item_1.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_2 = QTableWidgetItem("Есть" if attachment else "Нет")
            item_2.setFlags(item_2.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_2.setData(Qt.ItemDataRole.UserRole, (note_id, attachment))
            self.table.setItem(row_idx, 0, item_0)
            self.table.setItem(row_idx, 1, item_1)
            self.table.setItem(row_idx, 2, item_2)

    def header_context_menu(self, pos):
        col = self.table.horizontalHeader().logicalIndexAt(pos)
        menu = QMenu(self)

        reset_action = QAction("Сбросить фильтры", self)
        reset_action.triggered.connect(self.reset_filters)
        menu.addAction(reset_action)
        menu.addSeparator()

        if col == 0:
            menu.addAction("Сортировать по новизне", lambda: self.sort_notes("timestamp DESC"))
            menu.addAction("Сортировать по старине", lambda: self.sort_notes("timestamp ASC"))
            menu.addAction("Фильтр по дате...", self.filter_by_date)
        elif col == 1:
            menu.addAction("По алфавиту", lambda: self.sort_notes("content ASC"))
            menu.addAction("По алфавиту (обратный порядок)", lambda: self.sort_notes("content DESC"))
        elif col == 2:
            menu.addAction("Показать только с вложениями", lambda: self.load_notes(filter_attachments=True))
            menu.addAction("Показать только без вложений", lambda: self.load_notes(filter_attachments=False))

        menu.exec(self.table.mapToGlobal(pos))

    def reset_filters(self):
        self.search_field.clear()
        self.load_notes()

    def sort_notes(self, order_by):
        self.table.setRowCount(0)
        notes = list(self.cursor.execute(f"SELECT id, timestamp, content, attachment FROM notes ORDER BY {order_by}"))
        for row_idx, (note_id, timestamp, content, attachment) in enumerate(notes):
            self.table.insertRow(row_idx)
            item_0 = QTableWidgetItem(timestamp)
            item_0.setFlags(item_0.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_1 = QTableWidgetItem(content)
            item_1.setFlags(item_1.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_2 = QTableWidgetItem("Есть" if attachment else "Нет")
            item_2.setFlags(item_2.flags() & ~Qt.ItemFlag.ItemIsEditable)
            item_2.setData(Qt.ItemDataRole.UserRole, (note_id, attachment))
            self.table.setItem(row_idx, 0, item_0)
            self.table.setItem(row_idx, 1, item_1)
            self.table.setItem(row_idx, 2, item_2)

    def filter_by_date(self):
        text, ok = QInputDialog.getText(self, "Фильтр по дате", "Введите дату (например, 2024-12-31):")
        if ok and text:
            self.table.setRowCount(0)
            notes = list(self.cursor.execute("SELECT id, timestamp, content, attachment FROM notes"))
            filtered = [n for n in notes if text in n[1]]
            for row_idx, (note_id, timestamp, content, attachment) in enumerate(filtered):
                self.table.insertRow(row_idx)
                item_0 = QTableWidgetItem(timestamp)
                item_0.setFlags(item_0.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item_1 = QTableWidgetItem(content)
                item_1.setFlags(item_1.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item_2 = QTableWidgetItem("Есть" if attachment else "Нет")
                item_2.setFlags(item_2.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item_2.setData(Qt.ItemDataRole.UserRole, (note_id, attachment))
                self.table.setItem(row_idx, 0, item_0)
                self.table.setItem(row_idx, 1, item_1)
                self.table.setItem(row_idx, 2, item_2)

    def open_context_menu(self, position):
        index = self.table.indexAt(position)
        if not index.isValid():
            return

        menu = QMenu()
        edit_name_action = QAction("Редактировать имя", self)
        edit_file_action = QAction("Редактировать файл", self)
        delete_action = QAction("Удалить", self)

        edit_name_action.triggered.connect(lambda: self.edit_note_name(index.row()))
        edit_file_action.triggered.connect(lambda: self.edit_note_file(index.row()))
        delete_action.triggered.connect(lambda: self.delete_note(index.row()))

        menu.addAction(edit_name_action)
        menu.addAction(edit_file_action)
        menu.addAction(delete_action)
        menu.exec(self.table.viewport().mapToGlobal(position))

    def delete_note(self, row):
        note_id = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)[0]
        self.cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        self.conn.commit()
        self.load_notes()

    def edit_note_name(self, row):
        note_id, attachment = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)
        current_text = self.table.item(row, 1).text()
        new_name, ok = QInputDialog.getText(self, "Редактировать имя", "Новый текст заметки:", text=current_text)
        if ok:
            self.cursor.execute("UPDATE notes SET content = ? WHERE id = ?", (new_name, note_id))
            self.conn.commit()
            self.load_notes()

    def edit_note_file(self, row):
        note_id, old_attachment = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)
        file_path, ok = QFileDialog.getOpenFileName(self, "Выбрать новый файл")
        if ok and file_path:
            filename = os.path.basename(file_path)
            new_path = os.path.join(ATTACHMENTS_DIR, f"{datetime.now().timestamp()}_{filename}")
            shutil.copy2(file_path, new_path)
            self.cursor.execute("UPDATE notes SET attachment = ? WHERE id = ?", (new_path, note_id))
            self.conn.commit()
            self.load_notes()

    def handle_cell_double_click(self, row, column):
        attachment_data = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)
        if attachment_data:
            _, path = attachment_data
            if path:
                self.open_attachment(path)

    def attach_photo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать фото", "", "Изображения (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.attachment = file_name
            self.input_field.setPlaceholderText("Напишите название заметки, пожалуйста")

    def attach_video(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать видео", "", "Видео (*.mp4 *.avi *.mov *.mkv)")
        if file_name:
            self.attachment = file_name
            self.input_field.setPlaceholderText("Напишите название заметки, пожалуйста")

    def open_attachment(self, path):
        if os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))
        else:
            QMessageBox.warning(self, "Ошибка", "Файл не найден")

    def schedule_notification(self):
        now = QTime.currentTime()
        target = QTime(19, 0)

        if now < target:
            msecs_until = now.msecsTo(target)
        else:
            self.show_reminder()
            return

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.show_reminder)
        self.timer.start(msecs_until)

    def show_reminder(self):
        try:
            from plyer import notification
            notification.notify(
                title="Заметки дня",
                message="Опишите как прошел ваш день",
                app_icon=None,
                timeout=10
            )
        except Exception as e:
            print(f"Ошибка показа уведомления: {e}")

if __name__ == '__main__':
    if platform.system() == "Windows":
        import winreg
        exe_path = os.path.abspath(sys.argv[0])
        key = winreg.HKEY_CURRENT_USER
        reg_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(key, reg_path, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "NotesApp", 0, winreg.REG_SZ, exe_path)

    app = QApplication(sys.argv)
    window = NotesApp()
    window.show()
    sys.exit(app.exec())