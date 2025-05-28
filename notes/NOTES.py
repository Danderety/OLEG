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
DB_FILE="notes.db"
attachments_dir="attachments"
os.makedirs(attachments_dir, exist_ok=True)
class NotesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        self.setGeometry(200,200,800,600)
        self.load_theme_preference()
        self.init_db()
        self.init_ui()
        self.load_notes()
        self.schedule_notification()
        self.apply_theme()
    def init_db(self):
        self.conn=sqlite3.connect(DB_FILE)
        self.cursor=self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  # Уникальный ID
                timestamp TEXT,                       # Время создания
                content TEXT,                         # Текст заметки
                attachment TEXT                       # Путь к вложению
            )
        """)
        self.conn.commit()

            
