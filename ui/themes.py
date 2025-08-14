#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Theme Manager for Arabic Mobile Shop Management System
"""

import tkinter as tk

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = {
            "light": {
                "bg": "#FFFFFF",
                "fg": "#000000",
                "text": "#333333",
                "sidebar_bg": "#F5F5F5",
                "button_bg": "#E0E0E0",
                "button_active": "#D0D0D0",
                "entry_bg": "#FFFFFF",
                "entry_fg": "#000000",
                "accent": "#2196F3",
                "success": "#4CAF50",
                "warning": "#FF9800",
                "error": "#F44336",
                "card_bg": "#FAFAFA",
                "card_border": "#E0E0E0",
                "table_header": "#F0F0F0",
                "table_row": "#FFFFFF",
                "table_alt_row": "#F9F9F9"
            },
            "dark": {
                "bg": "#2E2E2E",
                "fg": "#FFFFFF",
                "text": "#E0E0E0",
                "sidebar_bg": "#1E1E1E",
                "button_bg": "#404040",
                "button_active": "#505050",
                "entry_bg": "#404040",
                "entry_fg": "#FFFFFF",
                "accent": "#64B5F6",
                "success": "#66BB6A",
                "warning": "#FFB74D",
                "error": "#EF5350",
                "card_bg": "#383838",
                "card_border": "#555555",
                "table_header": "#404040",
                "table_row": "#2E2E2E",
                "table_alt_row": "#353535"
            }
        }
        
    def get_colors(self):
        """Get colors for current theme"""
        return self.themes[self.current_theme]
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        
    def apply_theme(self, widget):
        """Apply theme to a widget and its children"""
        colors = self.get_colors()
        
        try:
            # Apply basic colors
            if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
                widget.configure(bg=colors['bg'])
            elif isinstance(widget, tk.Frame):
                widget.configure(bg=colors['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=colors['bg'],
                    fg=colors['text']
                )
            elif isinstance(widget, tk.Button):
                widget.configure(
                    bg=colors['button_bg'],
                    fg=colors['text'],
                    activebackground=colors['button_active'],
                    activeforeground=colors['text']
                )
            elif isinstance(widget, tk.Entry):
                widget.configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['text']
                )
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg'],
                    insertbackground=colors['text']
                )
            elif isinstance(widget, tk.Listbox):
                widget.configure(
                    bg=colors['entry_bg'],
                    fg=colors['entry_fg']
                )
                
            # Apply to child widgets recursively
            for child in widget.winfo_children():
                self.apply_theme(child)
                
        except tk.TclError:
            # Some widgets might not support certain options
            pass
            
    def get_themed_style(self, style_type):
        """Get themed style for specific UI elements"""
        colors = self.get_colors()
        
        styles = {
            "card": {
                "bg": colors['card_bg'],
                "relief": "raised",
                "borderwidth": 1,
                "highlightbackground": colors['card_border']
            },
            "success_button": {
                "bg": colors['success'],
                "fg": "white",
                "activebackground": self._darken_color(colors['success']),
                "activeforeground": "white"
            },
            "warning_button": {
                "bg": colors['warning'],
                "fg": "white",
                "activebackground": self._darken_color(colors['warning']),
                "activeforeground": "white"
            },
            "error_button": {
                "bg": colors['error'],
                "fg": "white",
                "activebackground": self._darken_color(colors['error']),
                "activeforeground": "white"
            },
            "accent_button": {
                "bg": colors['accent'],
                "fg": "white",
                "activebackground": self._darken_color(colors['accent']),
                "activeforeground": "white"
            }
        }
        
        return styles.get(style_type, {})
        
    def _darken_color(self, color):
        """Darken a color for hover effects"""
        # Simple color darkening - in production, you might want a more sophisticated approach
        color_map = {
            "#4CAF50": "#45A049",  # success
            "#FF9800": "#F57C00",  # warning
            "#F44336": "#D32F2F",  # error
            "#2196F3": "#1976D2",  # accent
            "#66BB6A": "#4CAF50",  # dark success
            "#FFB74D": "#FF9800",  # dark warning
            "#EF5350": "#F44336",  # dark error
            "#64B5F6": "#2196F3"   # dark accent
        }
        return color_map.get(color, color)
        
    def configure_treeview_style(self, tree):
        """Configure treeview with current theme"""
        colors = self.get_colors()
        
        # Create a style for the treeview
        import tkinter.ttk as ttk
        style = ttk.Style()
        
        # Configure treeview colors
        style.configure("Themed.Treeview",
                       background=colors['table_row'],
                       foreground=colors['text'],
                       fieldbackground=colors['table_row'])
        
        style.configure("Themed.Treeview.Heading",
                       background=colors['table_header'],
                       foreground=colors['text'])
        
        # Apply the style
        tree.configure(style="Themed.Treeview")
        
    def get_status_color(self, status):
        """Get color for status indicators"""
        colors = self.get_colors()
        
        status_colors = {
            "active": colors['success'],
            "inactive": colors['error'],
            "pending": colors['warning'],
            "available": colors['success'],
            "low_stock": colors['warning'],
            "out_of_stock": colors['error'],
            "paid": colors['success'],
            "overdue": colors['error'],
            "partial": colors['warning']
        }
        
        return status_colors.get(status.lower(), colors['text'])
        
    def create_gradient_frame(self, parent, start_color=None, end_color=None):
        """Create a frame with gradient background (simplified)"""
        colors = self.get_colors()
        
        if not start_color:
            start_color = colors['bg']
        if not end_color:
            end_color = colors['card_bg']
            
        # For simplicity, just use the start color
        # In a full implementation, you might use Canvas to create actual gradients
        frame = tk.Frame(parent, bg=start_color)
        return frame
        
    def apply_button_style(self, button, style_type="default"):
        """Apply specific button styles"""
        colors = self.get_colors()
        
        if style_type == "primary":
            button.configure(
                bg=colors['accent'],
                fg="white",
                activebackground=self._darken_color(colors['accent']),
                activeforeground="white"
            )
        elif style_type == "success":
            button.configure(
                bg=colors['success'],
                fg="white",
                activebackground=self._darken_color(colors['success']),
                activeforeground="white"
            )
        elif style_type == "warning":
            button.configure(
                bg=colors['warning'],
                fg="white",
                activebackground=self._darken_color(colors['warning']),
                activeforeground="white"
            )
        elif style_type == "error":
            button.configure(
                bg=colors['error'],
                fg="white",
                activebackground=self._darken_color(colors['error']),
                activeforeground="white"
            )
        else:  # default
            button.configure(
                bg=colors['button_bg'],
                fg=colors['text'],
                activebackground=colors['button_active'],
                activeforeground=colors['text']
            )
