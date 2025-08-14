#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sidebar Navigation - Mobile Shop Management System
"""

import tkinter as tk
from tkinter import ttk

class Sidebar:
    def __init__(self, parent, callback, theme_manager):
        self.parent = parent
        self.callback = callback
        self.theme_manager = theme_manager
        self.selected_button = None
        
        self.setup_sidebar()
        
    def setup_sidebar(self):
        """Setup the sidebar navigation"""
        # Main sidebar frame
        self.frame = tk.Frame(self.parent, width=200)
        self.frame.pack_propagate(False)
        
        # Logo/Header section
        header_frame = tk.Frame(self.frame)
        header_frame.pack(fill=tk.X, pady=20)
        
        logo_label = tk.Label(
            header_frame,
            text="📱",
            font=("Tahoma", 24),
            anchor="center"
        )
        logo_label.pack()
        
        app_name = tk.Label(
            header_frame,
            text="محل الموبايل",
            font=("Tahoma", 12, "bold"),
            anchor="center"
        )
        app_name.pack(pady=(5, 0))
        
        # Navigation buttons
        self.buttons = {}
        nav_items = [
            ('products', 'المنتجات', '📦'),
            ('customers', 'العملاء', '👥'),
            ('suppliers', 'الموردين', '🏪'),
            ('reports', 'التقارير', '📊'),
            ('services', 'الخدمات', '💳'),
            ('settings', 'الإعدادات', '⚙️')
        ]
        
        for key, text, icon in nav_items:
            self.create_nav_button(key, text, icon)
            
    def create_nav_button(self, key, text, icon):
        """Create a navigation button"""
        button_frame = tk.Frame(self.frame)
        button_frame.pack(fill=tk.X, padx=10, pady=2)
        
        button = tk.Button(
            button_frame,
            text=f"{icon}  {text}",
            font=("Tahoma", 11),
            anchor="e",
            relief=tk.FLAT,
            compound=tk.RIGHT,
            command=lambda: self.select_button(key)
        )
        button.pack(fill=tk.X, ipady=8)
        
        self.buttons[key] = button
        
        # Select first button by default
        if key == 'products':
            self.select_button(key)
            
    def select_button(self, key):
        """Handle button selection"""
        # Reset all buttons
        for btn_key, btn in self.buttons.items():
            if btn_key == key:
                # Selected state
                btn.config(relief=tk.SOLID, borderwidth=1)
            else:
                # Normal state
                btn.config(relief=tk.FLAT, borderwidth=0)
                
        self.selected_button = key
        self.callback(key)
        
    def update_theme(self):
        """Update sidebar theme"""
        colors = self.theme_manager.get_colors()
        
        # Update frame colors
        self.frame.config(bg=colors['sidebar_bg'])
        
        # Update all child widgets
        for widget in self.frame.winfo_children():
            self.update_widget_theme(widget, colors)
            
    def update_widget_theme(self, widget, colors):
        """Recursively update widget themes"""
        try:
            if isinstance(widget, tk.Label):
                widget.config(
                    bg=colors['sidebar_bg'],
                    fg=colors['text']
                )
            elif isinstance(widget, tk.Button):
                widget.config(
                    bg=colors['button_bg'],
                    fg=colors['text'],
                    activebackground=colors['button_active'],
                    activeforeground=colors['text']
                )
            elif isinstance(widget, tk.Frame):
                widget.config(bg=colors['sidebar_bg'])
                
            # Recursively update children
            for child in widget.winfo_children():
                self.update_widget_theme(child, colors)
        except tk.TclError:
            # Some widgets might not support certain options
            pass
