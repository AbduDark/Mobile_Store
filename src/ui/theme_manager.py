#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager - PyQt6 Theme Management System
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
from typing import Dict, Any

class ThemeManager(QObject):
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_theme = 'light'
        self.themes = self.get_themes()
    
    def get_themes(self) -> Dict[str, Dict[str, str]]:
        """Define all available themes"""
        return {
            'light': {
                # Primary colors
                'primary': '#2E86C1',
                'primary_dark': '#1B4F72',
                'primary_light': '#85C1E9',
                'secondary': '#28B463',
                'accent': '#F39C12',
                
                # Background colors
                'background': '#FFFFFF',
                'surface': '#F8F9FA',
                'card': '#FFFFFF',
                'sidebar': '#F5F6FA',
                
                # Text colors
                'text_primary': '#2C3E50',
                'text_secondary': '#7F8C8D',
                'text_disabled': '#BDC3C7',
                'text_on_primary': '#FFFFFF',
                
                # Border and divider colors
                'border': '#E1E8ED',
                'divider': '#EBEDEF',
                'shadow': 'rgba(0, 0, 0, 0.1)',
                
                # Status colors
                'success': '#27AE60',
                'warning': '#F39C12',
                'error': '#E74C3C',
                'info': '#3498DB',
                
                # Input colors
                'input_background': '#FFFFFF',
                'input_border': '#D5DBDB',
                'input_focus': '#2E86C1',
                'input_error': '#E74C3C',
                
                # Button colors
                'button_primary': '#2E86C1',
                'button_primary_hover': '#1B4F72',
                'button_secondary': '#95A5A6',
                'button_secondary_hover': '#7F8C8D',
                'button_success': '#27AE60',
                'button_success_hover': '#1E8449',
                'button_danger': '#E74C3C',
                'button_danger_hover': '#C0392B',
                
                # Table colors
                'table_header': '#ECF0F1',
                'table_row_even': '#FFFFFF',
                'table_row_odd': '#FAFBFC',
                'table_hover': '#EBF5FF',
                'table_selected': '#D6EAF8'
            },
            
            'dark': {
                # Primary colors
                'primary': '#3498DB',
                'primary_dark': '#2980B9',
                'primary_light': '#85C1E9',
                'secondary': '#2ECC71',
                'accent': '#F39C12',
                
                # Background colors
                'background': '#1A1A1A',
                'surface': '#2C2C2C',
                'card': '#363636',
                'sidebar': '#252525',
                
                # Text colors
                'text_primary': '#FFFFFF',
                'text_secondary': '#B0B0B0',
                'text_disabled': '#666666',
                'text_on_primary': '#FFFFFF',
                
                # Border and divider colors
                'border': '#404040',
                'divider': '#333333',
                'shadow': 'rgba(0, 0, 0, 0.3)',
                
                # Status colors
                'success': '#2ECC71',
                'warning': '#F39C12',
                'error': '#E74C3C',
                'info': '#3498DB',
                
                # Input colors
                'input_background': '#404040',
                'input_border': '#555555',
                'input_focus': '#3498DB',
                'input_error': '#E74C3C',
                
                # Button colors
                'button_primary': '#3498DB',
                'button_primary_hover': '#2980B9',
                'button_secondary': '#7F8C8D',
                'button_secondary_hover': '#95A5A6',
                'button_success': '#2ECC71',
                'button_success_hover': '#27AE60',
                'button_danger': '#E74C3C',
                'button_danger_hover': '#C0392B',
                
                # Table colors
                'table_header': '#404040',
                'table_row_even': '#363636',
                'table_row_odd': '#2C2C2C',
                'table_hover': '#1E3A8A',
                'table_selected': '#1E40AF'
            }
        }
    
    def apply_theme(self, theme_name: str, app: QApplication = None):
        """Apply a theme to the application"""
        if theme_name not in self.themes:
            theme_name = 'light'
        
        self.current_theme = theme_name
        theme = self.themes[theme_name]
        
        if app is None:
            app = QApplication.instance()
        
        # Create stylesheet
        stylesheet = self.create_stylesheet(theme)
        app.setStyleSheet(stylesheet)
        
        # Apply palette for native widgets
        self.apply_palette(theme, app)
        
        self.theme_changed.emit(theme_name)
    
    def create_stylesheet(self, theme: Dict[str, str]) -> str:
        """Create comprehensive stylesheet for the application"""
        return f"""
        /* Main Application */
        QMainWindow {{
            background-color: {theme['background']};
            color: {theme['text_primary']};
        }}
        
        /* General Widget Styling */
        QWidget {{
            background-color: {theme['background']};
            color: {theme['text_primary']};
            font-family: 'Cairo', 'Tahoma', 'Arial';
            font-size: 10pt;
        }}
        
        /* Sidebar Styling */
        QFrame#sidebar {{
            background-color: {theme['sidebar']};
            border-right: 1px solid {theme['border']};
            min-width: 200px;
            max-width: 200px;
        }}
        
        /* Sidebar Buttons */
        QPushButton#sidebar_button {{
            background-color: transparent;
            color: {theme['text_primary']};
            border: none;
            padding: 12px 16px;
            text-align: left;
            font-size: 11pt;
            font-weight: 500;
        }}
        
        QPushButton#sidebar_button:hover {{
            background-color: {theme['primary_light']};
            color: {theme['primary_dark']};
        }}
        
        QPushButton#sidebar_button:checked {{
            background-color: {theme['primary']};
            color: {theme['text_on_primary']};
            border-left: 4px solid {theme['accent']};
        }}
        
        /* Primary Buttons */
        QPushButton#primary_button {{
            background-color: {theme['button_primary']};
            color: {theme['text_on_primary']};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 10pt;
        }}
        
        QPushButton#primary_button:hover {{
            background-color: {theme['button_primary_hover']};
        }}
        
        QPushButton#primary_button:pressed {{
            background-color: {theme['primary_dark']};
        }}
        
        /* Secondary Buttons */
        QPushButton#secondary_button {{
            background-color: {theme['button_secondary']};
            color: {theme['text_on_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 9pt;
        }}
        
        QPushButton#secondary_button:hover {{
            background-color: {theme['button_secondary_hover']};
        }}
        
        /* Success Buttons */
        QPushButton#success_button {{
            background-color: {theme['button_success']};
            color: {theme['text_on_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }}
        
        QPushButton#success_button:hover {{
            background-color: {theme['button_success_hover']};
        }}
        
        /* Danger Buttons */
        QPushButton#danger_button {{
            background-color: {theme['button_danger']};
            color: {theme['text_on_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
        }}
        
        QPushButton#danger_button:hover {{
            background-color: {theme['button_danger_hover']};
        }}
        
        /* Input Fields */
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {theme['input_background']};
            color: {theme['text_primary']};
            border: 2px solid {theme['input_border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 10pt;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {theme['input_focus']};
            outline: none;
        }}
        
        QLineEdit:disabled, QTextEdit:disabled, QPlainTextEdit:disabled {{
            background-color: {theme['surface']};
            color: {theme['text_disabled']};
        }}
        
        /* ComboBox */
        QComboBox {{
            background-color: {theme['input_background']};
            color: {theme['text_primary']};
            border: 2px solid {theme['input_border']};
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 120px;
        }}
        
        QComboBox:focus {{
            border-color: {theme['input_focus']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {theme['text_secondary']};
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {theme['card']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 6px;
            padding: 5px;
        }}
        
        /* Tables */
        QTableWidget {{
            background-color: {theme['card']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 6px;
            gridline-color: {theme['divider']};
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border-bottom: 1px solid {theme['divider']};
        }}
        
        QTableWidget::item:alternate {{
            background-color: {theme['table_row_odd']};
        }}
        
        QTableWidget::item:selected {{
            background-color: {theme['table_selected']};
            color: {theme['text_primary']};
        }}
        
        QTableWidget::item:hover {{
            background-color: {theme['table_hover']};
        }}
        
        QHeaderView::section {{
            background-color: {theme['table_header']};
            color: {theme['text_primary']};
            border: none;
            border-bottom: 2px solid {theme['primary']};
            padding: 10px;
            font-weight: bold;
        }}
        
        /* Scrollbars */
        QScrollBar:vertical {{
            background: {theme['surface']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background: {theme['text_secondary']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {theme['primary']};
        }}
        
        QScrollBar:horizontal {{
            background: {theme['surface']};
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {theme['text_secondary']};
            border-radius: 6px;
            min-width: 20px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {theme['primary']};
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            border: 1px solid {theme['border']};
            border-radius: 6px;
            background-color: {theme['card']};
        }}
        
        QTabBar::tab {{
            background-color: {theme['surface']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-bottom: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin: 0px 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme['primary']};
            color: {theme['text_on_primary']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {theme['primary_light']};
        }}
        
        /* Menu and Context Menus */
        QMenuBar {{
            background-color: {theme['surface']};
            color: {theme['text_primary']};
            border-bottom: 1px solid {theme['border']};
        }}
        
        QMenuBar::item {{
            padding: 8px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme['primary']};
            color: {theme['text_on_primary']};
        }}
        
        QMenu {{
            background-color: {theme['card']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 6px;
        }}
        
        QMenu::item {{
            padding: 8px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme['primary']};
            color: {theme['text_on_primary']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {theme['surface']};
            color: {theme['text_secondary']};
            border-top: 1px solid {theme['border']};
        }}
        
        /* Tool Tips */
        QToolTip {{
            background-color: {theme['card']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 4px;
            padding: 5px;
        }}
        
        /* Group Box */
        QGroupBox {{
            font-weight: bold;
            border: 2px solid {theme['border']};
            border-radius: 6px;
            margin-top: 10px;
            padding-top: 10px;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }}
        
        /* Progress Bar */
        QProgressBar {{
            border: 1px solid {theme['border']};
            border-radius: 6px;
            text-align: center;
            background-color: {theme['surface']};
        }}
        
        QProgressBar::chunk {{
            background-color: {theme['primary']};
            border-radius: 5px;
        }}
        
        /* Notifications */
        QFrame#notification {{
            background-color: {theme['card']};
            border: 1px solid {theme['border']};
            border-left: 4px solid {theme['primary']};
            border-radius: 6px;
        }}
        
        QFrame#notification_success {{
            border-left-color: {theme['success']};
        }}
        
        QFrame#notification_warning {{
            border-left-color: {theme['warning']};
        }}
        
        QFrame#notification_error {{
            border-left-color: {theme['error']};
        }}
        """
    
    def apply_palette(self, theme: Dict[str, str], app: QApplication):
        """Apply color palette for native widgets"""
        palette = QPalette()
        
        # Window colors
        palette.setColor(QPalette.ColorRole.Window, QColor(theme['background']))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(theme['text_primary']))
        
        # Base colors (for input widgets)
        palette.setColor(QPalette.ColorRole.Base, QColor(theme['input_background']))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(theme['surface']))
        
        # Text colors
        palette.setColor(QPalette.ColorRole.Text, QColor(theme['text_primary']))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(theme['text_on_primary']))
        
        # Button colors
        palette.setColor(QPalette.ColorRole.Button, QColor(theme['surface']))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(theme['text_primary']))
        
        # Highlight colors
        palette.setColor(QPalette.ColorRole.Highlight, QColor(theme['primary']))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(theme['text_on_primary']))
        
        app.setPalette(palette)
    
    def get_color(self, color_name: str) -> str:
        """Get a color value from current theme"""
        return self.themes[self.current_theme].get(color_name, '#000000')
    
    def get_current_theme(self) -> str:
        """Get current theme name"""
        return self.current_theme