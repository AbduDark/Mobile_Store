#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window Class - Mobile Shop Management System
"""

import tkinter as tk
from tkinter import ttk
from sidebar import Sidebar
from themes import ThemeManager
from rtl_manager import RTLManager
from modules.products import ProductsModule
from modules.customers import CustomersModule
from modules.suppliers import SuppliersModule
from modules.reports import ReportsModule
from modules.services import ServicesModule
from modules.settings import SettingsModule

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.theme_manager = ThemeManager()
        self.rtl_manager = RTLManager()
        
        # Initialize UI
        self.setup_ui()
        
        # Show default module (products)
        self.show_module('products')
        
    def setup_ui(self):
        """Setup the main UI layout"""
        # Apply initial theme
        self.theme_manager.apply_theme(self.root)
        
        # Create main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create content area first
        self.content_frame = tk.Frame(self.main_frame)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(2, 0))
        
        # Create header first
        self.create_header()
        
        # Initialize modules
        self.modules = {
            'products': ProductsModule(self.content_frame, self.theme_manager),
            'customers': CustomersModule(self.content_frame, self.theme_manager),
            'suppliers': SuppliersModule(self.content_frame, self.theme_manager),
            'reports': ReportsModule(self.content_frame, self.theme_manager),
            'services': ServicesModule(self.content_frame, self.theme_manager),
            'settings': SettingsModule(self.content_frame, self.theme_manager, self.on_theme_change)
        }
        
        # Create sidebar after modules are initialized
        self.sidebar = Sidebar(self.main_frame, self.on_module_select, self.theme_manager)
        self.sidebar.frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 2))
        
    def create_header(self):
        """Create the header section"""
        header_frame = tk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        self.title_label = tk.Label(
            header_frame,
            text="نظام إدارة محل الموبايل",
            font=("Tahoma", 16, "bold"),
            anchor="e"
        )
        self.title_label.pack(side=tk.RIGHT, padx=20)
        
        # Theme toggle button
        self.theme_button = tk.Button(
            header_frame,
            text="🌙" if self.theme_manager.current_theme == "light" else "☀️",
            font=("Tahoma", 12),
            command=self.toggle_theme,
            width=3
        )
        self.theme_button.pack(side=tk.LEFT, padx=20)
        
        # Separator
        separator = ttk.Separator(header_frame, orient=tk.HORIZONTAL)
        separator.pack(fill=tk.X, pady=10)
        
    def on_module_select(self, module_name):
        """Handle module selection from sidebar"""
        self.show_module(module_name)
        
    def show_module(self, module_name):
        """Show the selected module"""
        # Hide all modules
        for module in self.modules.values():
            module.hide()
            
        # Show selected module
        if module_name in self.modules:
            self.modules[module_name].show()
            
        # Update header title based on module
        titles = {
            'products': 'إدارة المنتجات والمخزون',
            'customers': 'إدارة العملاء',
            'suppliers': 'إدارة الموردين',
            'reports': 'التقارير',
            'services': 'خدمات الرصيد والدفع',
            'settings': 'الإعدادات'
        }
        self.title_label.config(text=titles.get(module_name, 'نظام إدارة محل الموبايل'))
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme_manager.toggle_theme()
        self.on_theme_change()
        
    def on_theme_change(self):
        """Handle theme change"""
        # Apply new theme to root
        self.theme_manager.apply_theme(self.root)
        
        # Update theme button icon
        self.theme_button.config(
            text="🌙" if self.theme_manager.current_theme == "light" else "☀️"
        )
        
        # Update sidebar
        self.sidebar.update_theme()
        
        # Update all modules
        for module in self.modules.values():
            module.update_theme()
