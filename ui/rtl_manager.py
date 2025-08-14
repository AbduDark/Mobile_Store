#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RTL (Right-to-Left) Layout Manager for Arabic UI
"""

import tkinter as tk
from tkinter import ttk

class RTLManager:
    def __init__(self):
        self.rtl_enabled = True
        self.arabic_fonts = ["Tahoma", "Arial Unicode MS", "Times New Roman", "Cairo", "Amiri"]
        self.default_font = "Tahoma"
        
    def configure_rtl_widget(self, widget, widget_type=None):
        """Configure a widget for RTL layout"""
        if not self.rtl_enabled:
            return
            
        try:
            if isinstance(widget, tk.Entry):
                widget.configure(justify='right')
            elif isinstance(widget, tk.Label):
                widget.configure(anchor='e')
            elif isinstance(widget, tk.Button):
                widget.configure(anchor='e')
            elif isinstance(widget, tk.Text):
                # Configure text widget for RTL
                widget.tag_configure("rtl", justify="right")
                widget.tag_add("rtl", "1.0", "end")
            elif isinstance(widget, tk.Listbox):
                # Listbox doesn't have direct RTL support, but we can align text
                pass
            elif isinstance(widget, ttk.Treeview):
                # Configure treeview headings for RTL
                for col in widget['columns']:
                    widget.heading(col, anchor='e')
                    widget.column(col, anchor='e')
        except tk.TclError:
            # Some widgets might not support certain options
            pass
            
    def set_arabic_font(self, widget, size=10, weight="normal"):
        """Set Arabic-friendly font for a widget"""
        font = (self.default_font, size, weight)
        try:
            widget.configure(font=font)
        except tk.TclError:
            pass
            
    def create_rtl_frame(self, parent, **kwargs):
        """Create a frame configured for RTL layout"""
        frame = tk.Frame(parent, **kwargs)
        return frame
        
    def create_rtl_entry(self, parent, **kwargs):
        """Create an entry widget configured for RTL"""
        kwargs['justify'] = 'right'
        entry = tk.Entry(parent, **kwargs)
        self.set_arabic_font(entry)
        return entry
        
    def create_rtl_label(self, parent, text="", **kwargs):
        """Create a label widget configured for RTL"""
        kwargs['anchor'] = kwargs.get('anchor', 'e')
        label = tk.Label(parent, text=text, **kwargs)
        self.set_arabic_font(label)
        return label
        
    def create_rtl_button(self, parent, text="", **kwargs):
        """Create a button widget configured for RTL"""
        kwargs['anchor'] = kwargs.get('anchor', 'e')
        button = tk.Button(parent, text=text, **kwargs)
        self.set_arabic_font(button)
        return button
        
    def create_rtl_text(self, parent, **kwargs):
        """Create a text widget configured for RTL"""
        text = tk.Text(parent, **kwargs)
        text.tag_configure("rtl", justify="right")
        text.tag_add("rtl", "1.0", "end")
        self.set_arabic_font(text)
        return text
        
    def configure_form_layout(self, parent_frame):
        """Configure a form frame for RTL layout"""
        # Ensure proper grid configuration for RTL
        for i in range(parent_frame.grid_size()[0]):
            parent_frame.grid_columnconfigure(i, weight=1)
            
    def pack_rtl(self, widget, side=tk.RIGHT, **kwargs):
        """Pack widget with RTL considerations"""
        if side == tk.LEFT:
            side = tk.RIGHT
        elif side == tk.RIGHT:
            side = tk.LEFT
        widget.pack(side=side, **kwargs)
        
    def grid_rtl(self, widget, row=0, column=0, **kwargs):
        """Grid widget with RTL considerations"""
        # For RTL, we might want to reverse column order in some cases
        widget.grid(row=row, column=column, **kwargs)
        
    def configure_menu_rtl(self, menu):
        """Configure menu for RTL layout"""
        # Tkinter menus don't have great RTL support
        # This is a placeholder for future enhancement
        pass
        
    def format_arabic_number(self, number):
        """Format numbers for Arabic display"""
        # Convert to Arabic-Indic numerals if needed
        arabic_numerals = "٠١٢٣٤٥٦٧٨٩"
        western_numerals = "0123456789"
        
        # For this implementation, we'll keep Western numerals
        # but format with proper thousand separators
        if isinstance(number, (int, float)):
            return f"{number:,}"
        return str(number)
        
    def format_arabic_date(self, date_obj):
        """Format date for Arabic display"""
        if hasattr(date_obj, 'strftime'):
            # Format date in Arabic style (DD/MM/YYYY)
            return date_obj.strftime("%d/%m/%Y")
        return str(date_obj)
        
    def configure_scrollbar_rtl(self, scrollbar, widget):
        """Configure scrollbar for RTL layout"""
        # For RTL, scrollbars should be on the left side
        if hasattr(widget, 'configure'):
            widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=widget.yview)
        
    def create_rtl_combobox(self, parent, **kwargs):
        """Create a combobox configured for RTL"""
        combobox = ttk.Combobox(parent, **kwargs)
        self.set_arabic_font(combobox)
        return combobox
        
    def configure_table_rtl(self, treeview):
        """Configure treeview table for RTL display"""
        # Configure all columns and headings for RTL
        for col in treeview['columns']:
            treeview.heading(col, anchor='e')
            treeview.column(col, anchor='e')
            
        # Configure the tree column as well
        treeview.heading('#0', anchor='e')
        treeview.column('#0', anchor='e')
        
    def wrap_text_rtl(self, text, width=40):
        """Wrap text properly for RTL display"""
        # Simple text wrapping that respects Arabic text direction
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= width:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return '\n'.join(lines)
        
    def set_window_rtl(self, window):
        """Configure main window for RTL layout"""
        # Set window properties for RTL
        try:
            # This would require platform-specific code for full RTL support
            # For now, we'll just ensure proper font configuration
            window.option_add("*Font", f"{self.default_font} 10")
        except:
            pass
            
    def create_message_box_rtl(self, title, message, type="info"):
        """Create an RTL-aware message box"""
        from tkinter import messagebox
        
        # Tkinter's messagebox doesn't support RTL directly
        # We'll use the standard one but ensure Arabic text displays correctly
        if type == "info":
            return messagebox.showinfo(title, message)
        elif type == "warning":
            return messagebox.showwarning(title, message)
        elif type == "error":
            return messagebox.showerror(title, message)
        elif type == "question":
            return messagebox.askyesno(title, message)
        else:
            return messagebox.showinfo(title, message)
            
    def configure_notebook_rtl(self, notebook):
        """Configure notebook tabs for RTL"""
        # Notebook tabs will show in the order added
        # Arabic text should display correctly with proper fonts
        pass
        
    def get_text_direction(self, text):
        """Determine text direction (RTL/LTR)"""
        # Simple heuristic: if text contains Arabic characters, it's RTL
        arabic_range = range(0x0600, 0x06FF)  # Arabic Unicode block
        
        for char in text:
            if ord(char) in arabic_range:
                return "rtl"
        return "ltr"
        
    def mirror_layout(self, container):
        """Mirror the layout of a container for RTL"""
        # This would involve repositioning widgets from right to left
        # For now, this is a placeholder for future enhancement
        pass
        
    def configure_entry_validation_rtl(self, entry, validation_type="none"):
        """Configure entry validation for RTL input"""
        # Set up validation for Arabic text input
        def validate_arabic(text):
            if validation_type == "arabic_only":
                # Allow only Arabic characters and numbers
                arabic_range = range(0x0600, 0x06FF)
                allowed_chars = set(range(0x0030, 0x0039))  # Numbers
                allowed_chars.update(arabic_range)
                allowed_chars.update([ord(' '), ord('-'), ord('.')])  # Common punctuation
                
                return all(ord(char) in allowed_chars for char in text)
            return True
            
        if validation_type != "none":
            vcmd = (entry.register(lambda text: validate_arabic(text)), '%P')
            entry.configure(validate='key', validatecommand=vcmd)
