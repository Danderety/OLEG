import os
import sys
import sqlite3
import platform
import shutil
import configparser

from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QFileDialog, QColorDialog, QFontDialog,
                             QLabel, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QTableWidget,
                             QTableWidgetItem, QMessageBox, QMenuBar, QMenu, QHeaderView, QMenu, QInputDialog)
from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtGui import QColor, QFont, QDesktopServices, QAction
from PyQt6.QtCore import QUrl

DB_FILE = "notes.db"
ATTACHMENTS_DIR = "attachments"
os.makedirs(ATTACHMENTS_DIR, exist_ok=True)

class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.setGeometry(200, 200, 800, 600)

        self.load_theme_preference()

        self.init_db()
        self.init_ui()
        self.load_notes()
        self.schedule_notification()
        self.apply_theme()

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
        theme_menu = menu_bar.addMenu("Тема")
        self.light_action = QAction("Светлая", self)
        self.dark_action = QAction("Тёмная", self)
        self.light_action.triggered.connect(lambda: self.set_theme("light"))
        self.dark_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(self.light_action)
        theme_menu.addAction(self.dark_action)

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
    def save_theme_preference(self):
        config = configparser.ConfigParser()
        config["Preferences"] = {"theme": self.current_theme}
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def load_theme_preference(self):
        config = configparser.ConfigParser()
        if config.read("config.ini") and "Preferences" in config and "theme" in config["Preferences"]:
            self.current_theme = config["Preferences"]["theme"]
        else:
            self.current_theme = "dark"  # по умолчанию

    def set_theme(self, theme):
        self.current_theme = theme
        self.save_theme_preference()

        self.apply_theme()
        self.load_notes()

    def apply_theme(self):
        common_dark_menu = '''
            QScrollBar:vertical {
                background: #2b2b2b;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #2b2b2b;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3a3a3a;
            }
            QMenu::item:selected {
                background-color: #505050;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3a3a3a;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3a3a3a;
            }
            QMenu::item:selected {
                background-color: #505050;
            }
        '''
        common_light_menu = '''
            QScrollBar:vertical {
                background: #000000;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background:#000000;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QMenu {
                background-color: #ffffff;
                color: black;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #d2e4ff;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #cccccc;
            }
            QMenuBar {
                background-color: #f0f0f0;
                color: black;
            }
            QMenuBar::item:selected {
                background-color: #e0e0e0;
            }
            QMenu {
                background-color: #ffffff;
                color: black;
                border: 1px solid #cccccc;
            }
            QMenu::item:selected {
                background-color: #d2e4ff;
            }
        '''

        if self.current_theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                    color: #f0f0f0;
                }
                QLineEdit, QTableWidget, QPushButton, QLabel {
                    background-color: #2b2b2b;
                    color: #f0f0f0;
                    border: 1px solid #3a3a3a;
                    border-radius: 6px;
                    padding: 4px;
                }
                QTableWidget::item:selected {
                    background-color: #505050;
                }
            """ + common_dark_menu)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffffff;
                    color: #000000;
                }
                QLineEdit, QPushButton, QLabel {
                    background-color: #f9f9f9;
                    color: #000000;
                    border: 1px solid #cccccc;
                    border-radius: 6px;
                    padding: 4px;
                }
                QTableWidget {
                    background-color: #ffffff;
                    color: #000000;
                    gridline-color: #dddddd;
                    border: 1px solid #ccc;
                }
                QTableWidget::item:selected {
                    background-color: #d2e4ff;
                }
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
        filter_text = self.search_field.text().lower() if hasattr(self, 'search_field') else ''
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

        # Специальные действия для сброса фильтров и сортировки
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
    def reset_filters(self):
        self.search_field.clear()  # сброс поиска
        self.load_notes()          # перезагрузка всех заметок
  
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
            # если уже после 19:00 — показываем уведомление сразу
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
