#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Module - Base class for all application modules
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal
from ...database.db_manager import DatabaseManager
from ...utils.settings_manager import SettingsManager

class BaseModule(QWidget):
    # Common signals
    data_changed = pyqtSignal()
    status_message = pyqtSignal(str)
    
    def __init__(self, db_manager: DatabaseManager, settings_manager: SettingsManager, module_name: str = ""):
        super().__init__()
        
        self.db_manager = db_manager
        self.settings_manager = settings_manager
        self.module_name = module_name
        
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup the base UI - to be overridden by subclasses"""
        layout = QVBoxLayout(self)
        
        # Placeholder content
        label = QLabel(f"وحدة {self.module_name}")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18pt; color: #888;")
        
        layout.addWidget(label)
        
    def load_data(self):
        """Load data for the module - to be overridden"""
        pass
        
    def refresh_data(self):
        """Refresh module data"""
        self.load_data()
        self.data_changed.emit()
        
    def search(self, query: str):
        """Search functionality - to be overridden"""
        pass
        
    def auto_save(self):
        """Auto-save functionality - to be overridden"""
        pass
        
    def export_data(self, format_type: str = 'csv'):
        """Export module data - to be overridden"""
        pass
        
    def import_data(self, file_path: str):
        """Import module data - to be overridden"""  
        pass