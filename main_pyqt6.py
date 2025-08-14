#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Shop Management System - PyQt6 Version
Main Application Entry Point
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir, QLocale, QTranslator
from PyQt6.QtGui import QFont, QFontDatabase

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ui.main_window import MainWindow
from database.db_manager import DatabaseManager
from utils.settings_manager import SettingsManager

class MobileShopApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_application()
        
    def setup_application(self):
        """Setup application properties and resources"""
        # Set application properties
        self.app.setApplicationName("Mobile Shop Management System")
        self.app.setApplicationDisplayName("نظام إدارة محل الموبايل")
        self.app.setApplicationVersion("2.0.0")
        self.app.setOrganizationName("Mobile Shop Solutions")
        
        # Set layout direction to RTL for Arabic
        self.app.setLayoutDirection(2)  # Qt.RightToLeft
        
        # Load Arabic fonts
        self.load_fonts()
        
        # Set default font
        self.set_default_font()
        
        # Initialize settings
        self.settings_manager = SettingsManager()
        
        # Initialize database
        self.db_manager = DatabaseManager()
        self.db_manager.initialize_database()
        
    def load_fonts(self):
        """Load Arabic fonts"""
        font_paths = [
            "assets/fonts/Cairo-Regular.ttf",
            "assets/fonts/Amiri-Regular.ttf",
            "assets/fonts/NotoSansArabic-Regular.ttf"
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                QFontDatabase.addApplicationFont(font_path)
                
    def set_default_font(self):
        """Set the default application font"""
        # Try Arabic fonts in order of preference
        font_families = ["Cairo", "Amiri", "Noto Sans Arabic", "Tahoma", "Arial"]
        
        for family in font_families:
            font = QFont(family, 10)
            if QFontDatabase.families().contains(family):
                self.app.setFont(font)
                break
        else:
            # Fallback to system default with Arabic support
            font = QFont("Tahoma", 10)
            self.app.setFont(font)
    
    def run(self):
        """Run the application"""
        # Create main window
        self.main_window = MainWindow(self.db_manager, self.settings_manager)
        self.main_window.show()
        
        # Start the application event loop
        return self.app.exec()

def main():
    """Main application entry point"""
    app = MobileShopApp()
    sys.exit(app.run())

if __name__ == "__main__":
    main()