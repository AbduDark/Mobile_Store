#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Manager - Application Settings Management
"""

import json
import os
from typing import Any, Dict
from PyQt6.QtCore import QSettings, QObject, pyqtSignal

class SettingsManager(QObject):
    # Signals for settings changes
    theme_changed = pyqtSignal(str)
    language_changed = pyqtSignal(str)
    settings_changed = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("MobileShop", "ManagementSystem")
        self.setup_default_settings()
        
    def setup_default_settings(self):
        """Setup default application settings"""
        defaults = {
            'theme': 'light',
            'language': 'ar',
            'auto_backup': True,
            'backup_frequency': 'daily',
            'tax_rate': 15.0,
            'currency': 'ريال',
            'low_stock_alert': True,
            'window_geometry': '',
            'window_state': '',
            'font_family': 'Tahoma',
            'font_size': 10,
            'auto_save': True,
            'notification_sound': True,
            'backup_location': 'local'
        }
        
        for key, value in defaults.items():
            if not self.settings.contains(key):
                self.settings.setValue(key, value)
    
    def get(self, key: str, default_value: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.value(key, default_value)
    
    def set(self, key: str, value: Any):
        """Set a setting value"""
        old_value = self.get(key)
        self.settings.setValue(key, value)
        
        # Emit specific signals for important settings
        if key == 'theme' and old_value != value:
            self.theme_changed.emit(value)
        elif key == 'language' and old_value != value:
            self.language_changed.emit(value)
        
        # Emit general settings change signal
        self.settings_changed.emit(key, str(value))
    
    def get_theme(self) -> str:
        """Get current theme"""
        return self.get('theme', 'light')
    
    def set_theme(self, theme: str):
        """Set current theme"""
        self.set('theme', theme)
    
    def get_language(self) -> str:
        """Get current language"""
        return self.get('language', 'ar')
    
    def set_language(self, language: str):
        """Set current language"""
        self.set('language', language)
    
    def is_auto_backup_enabled(self) -> bool:
        """Check if auto backup is enabled"""
        return self.get('auto_backup', True)
    
    def get_backup_frequency(self) -> str:
        """Get backup frequency"""
        return self.get('backup_frequency', 'daily')
    
    def get_tax_rate(self) -> float:
        """Get tax rate"""
        return float(self.get('tax_rate', 15.0))
    
    def get_currency(self) -> str:
        """Get currency symbol"""
        return self.get('currency', 'ريال')
    
    def is_low_stock_alert_enabled(self) -> bool:
        """Check if low stock alerts are enabled"""
        return self.get('low_stock_alert', True)
    
    def export_settings(self, file_path: str) -> bool:
        """Export settings to a JSON file"""
        try:
            settings_dict = {}
            for key in self.settings.allKeys():
                settings_dict[key] = self.settings.value(key)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str) -> bool:
        """Import settings from a JSON file"""
        try:
            if not os.path.exists(file_path):
                return False
                
            with open(file_path, 'r', encoding='utf-8') as f:
                settings_dict = json.load(f)
            
            for key, value in settings_dict.items():
                self.set(key, value)
            
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
            return False
    
    def reset_to_defaults(self):
        """Reset all settings to default values"""
        self.settings.clear()
        self.setup_default_settings()