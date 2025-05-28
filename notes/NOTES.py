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