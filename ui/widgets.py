#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Widgets for Arabic RTL Layout
"""

import tkinter as tk
from tkinter import ttk

class RTLEntry(tk.Entry):
    """RTL-aware Entry widget"""
    def __init__(self, parent, **kwargs):
        kwargs['justify'] = 'right'
        super().__init__(parent, **kwargs)
        
class RTLText(tk.Text):
    """RTL-aware Text widget"""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        # Configure text direction
        self.tag_configure("rtl", justify="right")
        self.tag_add("rtl", "1.0", "end")
        
class RTLLabel(tk.Label):
    """RTL-aware Label widget"""
    def __init__(self, parent, **kwargs):
        if 'anchor' not in kwargs:
            kwargs['anchor'] = 'e'
        super().__init__(parent, **kwargs)
        
class RTLButton(tk.Button):
    """RTL-aware Button widget"""
    def __init__(self, parent, **kwargs):
        if 'anchor' not in kwargs:
            kwargs['anchor'] = 'e'
        super().__init__(parent, **kwargs)

class DataTable(tk.Frame):
    """Custom data table with RTL support"""
    def __init__(self, parent, columns, theme_manager=None):
        super().__init__(parent)
        self.columns = columns
        self.theme_manager = theme_manager
        self.data = []
        self.setup_table()
        
    def setup_table(self):
        """Setup the table structure"""
        # Search frame
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Search entry (RTL)
        self.search_var = tk.StringVar()
        search_entry = RTLEntry(
            search_frame,
            textvariable=self.search_var,
            font=("Tahoma", 10)
        )
        search_entry.pack(side=tk.RIGHT, padx=(0, 10))
        
        search_label = RTLLabel(
            search_frame,
            text="البحث:",
            font=("Tahoma", 10)
        )
        search_label.pack(side=tk.RIGHT)
        
        # Table frame with scrollbars
        table_frame = tk.Frame(self)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create Treeview
        self.tree = ttk.Treeview(table_frame, columns=list(self.columns.keys()), show='headings')
        
        # Configure columns
        for col_id, col_name in self.columns.items():
            self.tree.heading(col_id, text=col_name, anchor='e')
            self.tree.column(col_id, anchor='e', width=150)
            
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack everything
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind search
        self.search_var.trace('w', self.on_search)
        
    def add_row(self, values):
        """Add a row to the table"""
        self.data.append(values)
        self.tree.insert('', 'end', values=values)
        
    def clear_table(self):
        """Clear all table data"""
        self.data = []
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def on_search(self, *args):
        """Handle search functionality"""
        query = self.search_var.get().lower()
        
        # Clear current display
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Filter and display data
        for row_data in self.data:
            if any(query in str(cell).lower() for cell in row_data):
                self.tree.insert('', 'end', values=row_data)

class FormField(tk.Frame):
    """Custom form field with RTL support"""
    def __init__(self, parent, label_text, field_type='entry', **kwargs):
        super().__init__(parent)
        self.setup_field(label_text, field_type, **kwargs)
        
    def setup_field(self, label_text, field_type, **kwargs):
        """Setup the form field"""
        # Label
        label = RTLLabel(
            self,
            text=label_text,
            font=("Tahoma", 10),
            anchor='e'
        )
        label.pack(anchor='e', pady=(0, 5))
        
        # Field based on type
        if field_type == 'entry':
            self.field = RTLEntry(self, font=("Tahoma", 10), **kwargs)
        elif field_type == 'text':
            self.field = RTLText(self, font=("Tahoma", 10), height=4, **kwargs)
        elif field_type == 'combobox':
            self.field = ttk.Combobox(self, font=("Tahoma", 10), **kwargs)
            
        self.field.pack(fill=tk.X, pady=(0, 10))
        
    def get_value(self):
        """Get field value"""
        if isinstance(self.field, tk.Text):
            return self.field.get("1.0", tk.END).strip()
        else:
            return self.field.get()
            
    def set_value(self, value):
        """Set field value"""
        if isinstance(self.field, tk.Text):
            self.field.delete("1.0", tk.END)
            self.field.insert("1.0", str(value))
        else:
            self.field.delete(0, tk.END)
            self.field.insert(0, str(value))

class StatsCard(tk.Frame):
    """Statistics card widget"""
    def __init__(self, parent, title, value, icon="📊", color="#4CAF50"):
        super().__init__(parent, relief=tk.RAISED, borderwidth=1)
        self.setup_card(title, value, icon, color)
        
    def setup_card(self, title, value, icon, color):
        """Setup the stats card"""
        # Icon
        icon_label = tk.Label(
            self,
            text=icon,
            font=("Tahoma", 20),
            fg=color
        )
        icon_label.pack(pady=(10, 5))
        
        # Value
        value_label = tk.Label(
            self,
            text=str(value),
            font=("Tahoma", 16, "bold")
        )
        value_label.pack()
        
        # Title
        title_label = tk.Label(
            self,
            text=title,
            font=("Tahoma", 10),
            wraplength=120
        )
        title_label.pack(pady=(5, 10))
        
    def update_value(self, new_value):
        """Update the card value"""
        # Find value label and update it
        for child in self.winfo_children():
            if isinstance(child, tk.Label) and child.cget('font')[1] == 16:
                child.config(text=str(new_value))
                break
