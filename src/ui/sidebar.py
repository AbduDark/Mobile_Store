#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sidebar Navigation - PyQt6 Sidebar Component
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QButtonGroup, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class Sidebar(QFrame):
    module_selected = pyqtSignal(str)
    
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setup_ui()
        
    def setup_ui(self):
        """Setup sidebar UI"""
        self.setObjectName("sidebar")
        self.setFixedWidth(200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)
        
        # Create button group for exclusive selection
        self.button_group = QButtonGroup(self)
        self.buttons = {}
        
        # Navigation items
        nav_items = [
            ('products', '📦 المنتجات', 'إدارة المنتجات والمخزون'),
            ('customers', '👥 العملاء', 'إدارة بيانات العملاء'),
            ('suppliers', '🏪 الموردين', 'إدارة الموردين والطلبات'),
            ('reports', '📊 التقارير', 'التقارير والإحصائيات'),
            ('services', '🔧 الخدمات', 'خدمات الدفع والشحن'),
            ('settings', '⚙️ الإعدادات', 'إعدادات النظام')
        ]
        
        for module_id, text, tooltip in nav_items:
            button = self.create_nav_button(module_id, text, tooltip)
            layout.addWidget(button)
            self.buttons[module_id] = button
            self.button_group.addButton(button)
            
        # Add spacer to push buttons to top
        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addSpacerItem(spacer)
        
        # Select products by default
        self.buttons['products'].setChecked(True)
        
    def create_nav_button(self, module_id: str, text: str, tooltip: str) -> QPushButton:
        """Create a navigation button"""
        button = QPushButton(text)
        button.setObjectName("sidebar_button")
        button.setCheckable(True)
        button.setToolTip(tooltip)
        button.setMinimumHeight(50)
        
        # Set font
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Weight.Medium)
        button.setFont(font)
        
        # Connect click event
        button.clicked.connect(lambda: self.on_button_clicked(module_id))
        
        return button
        
    def on_button_clicked(self, module_id: str):
        """Handle button click"""
        self.callback(module_id)
        self.module_selected.emit(module_id)
        
    def select_module(self, module_id: str):
        """Programmatically select a module"""
        if module_id in self.buttons:
            self.buttons[module_id].setChecked(True)