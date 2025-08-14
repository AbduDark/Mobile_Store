#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Shop Management System - Main Entry Point
Arabic UI/UX Mockup for Windows Desktop Application
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add UI modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from ui.main_window import MainWindow

def main():
    """Initialize and run the Mobile Shop Management System"""
    # Create root window
    root = tk.Tk()
    
    # Configure root window
    root.title("نظام إدارة محل الموبايل")
    root.geometry("1400x900")
    root.minsize(1200, 800)
    
    # Center window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 1400) // 2
    y = (screen_height - 900) // 2
    root.geometry(f"1400x900+{x}+{y}")
    
    # Set window icon (would use actual icon file in production)
    try:
        # In production, you would use an actual .ico file
        # root.iconbitmap("assets/icon.ico")
        pass
    except:
        pass
    
    # Configure Arabic fonts support
    try:
        root.option_add("*Font", "Tahoma 10")
    except:
        # Fallback to default font if Tahoma not available
        pass
    
    # Create main application window
    app = MainWindow(root)
    
    # Handle window closing
    def on_closing():
        root.quit()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
