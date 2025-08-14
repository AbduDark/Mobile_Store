#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window - PyQt6 Main Application Window
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QStackedWidget, QMenuBar, QStatusBar, QLabel, QPushButton,
    QFrame, QToolBar, QLineEdit, QTabWidget, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction

from .theme_manager import ThemeManager
from .sidebar import Sidebar
from .notifications import NotificationManager
from .modules.products import ProductsModule
from .modules.customers import CustomersModule  
from .modules.suppliers import SuppliersModule
from .modules.reports import ReportsModule
from .modules.services import ServicesModule
from .modules.settings import SettingsModule
from ..database.db_manager import DatabaseManager
from ..utils.settings_manager import SettingsManager

class MainWindow(QMainWindow):
    # Signals
    module_changed = pyqtSignal(str)
    
    def __init__(self, db_manager: DatabaseManager, settings_manager: SettingsManager):
        super().__init__()
        
        self.db_manager = db_manager
        self.settings_manager = settings_manager
        self.theme_manager = ThemeManager()
        self.notification_manager = NotificationManager(self)
        
        self.current_module = 'products'
        self.open_tabs = {}  # Track open tabs for multi-tab support
        
        self.setup_ui()
        self.setup_connections()
        self.setup_auto_features()
        self.apply_initial_theme()
        
        # Show main window
        self.show_maximized()
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("نظام إدارة محل الموبايل - Mobile Shop Management System")
        self.setMinimumSize(1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create splitter for resizable layout
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create sidebar
        self.sidebar = Sidebar(self.on_module_selected)
        splitter.addWidget(self.sidebar)
        
        # Create content area
        self.setup_content_area(splitter)
        
        # Set splitter proportions (sidebar: content = 1:4)
        splitter.setSizes([200, 1000])
        splitter.setChildrenCollapsible(False)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create tool bar
        self.create_tool_bar()
        
        # Create status bar
        self.create_status_bar()
        
    def setup_content_area(self, parent):
        """Setup the main content area with tabs"""
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create header with title and search
        header_frame = self.create_header()
        content_layout.addWidget(header_frame)
        
        # Create tab widget for multi-tab support
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        content_layout.addWidget(self.tab_widget)
        
        # Initialize modules
        self.modules = self.create_modules()
        
        # Add default tab (Products)
        self.add_tab('products', 'المنتجات 📦')
        
        parent.addWidget(content_frame)
        
    def create_header(self) -> QFrame:
        """Create the header with title and search"""
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        # Theme toggle button
        self.theme_button = QPushButton("🌙")
        self.theme_button.setObjectName("secondary_button")
        self.theme_button.setFixedSize(40, 40)
        self.theme_button.setToolTip("تبديل المظهر")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        # Title label
        self.title_label = QLabel("المنتجات")
        self.title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #2E86C1;")
        
        # Quick search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("البحث السريع... (المنتجات، العملاء، الموردين)")
        self.search_bar.setMinimumWidth(300)
        self.search_bar.textChanged.connect(self.on_quick_search)
        
        # Add to layout (RTL order)
        header_layout.addWidget(self.theme_button)
        header_layout.addStretch()
        header_layout.addWidget(self.search_bar)
        header_layout.addStretch()
        header_layout.addWidget(self.title_label)
        
        return header_frame
        
    def create_modules(self) -> dict:
        """Create all application modules"""
        modules = {}
        
        try:
            modules['products'] = ProductsModule(self.db_manager, self.settings_manager)
            modules['customers'] = CustomersModule(self.db_manager, self.settings_manager)
            modules['suppliers'] = SuppliersModule(self.db_manager, self.settings_manager)
            modules['reports'] = ReportsModule(self.db_manager, self.settings_manager)
            modules['services'] = ServicesModule(self.db_manager, self.settings_manager)
            modules['settings'] = SettingsModule(self.db_manager, self.settings_manager)
            
        except Exception as e:
            print(f"Error creating modules: {e}")
            # Create empty modules as fallback
            from .modules.base_module import BaseModule
            for module_name in ['products', 'customers', 'suppliers', 'reports', 'services', 'settings']:
                modules[module_name] = BaseModule(self.db_manager, self.settings_manager, module_name)
        
        return modules
        
    def create_menu_bar(self):
        """Create the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('ملف')
        
        new_action = QAction('جديد', self)
        new_action.setShortcut('Ctrl+N')
        file_menu.addAction(new_action)
        
        save_action = QAction('حفظ', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction('نسخ احتياطي', self)
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('خروج', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('تحرير')
        
        # Tools menu
        tools_menu = menubar.addMenu('أدوات')
        
        # Help menu
        help_menu = menubar.addMenu('مساعدة')
        
        about_action = QAction('حول البرنامج', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_tool_bar(self):
        """Create the application toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Add common actions to toolbar
        toolbar.addAction("جديد")
        toolbar.addAction("حفظ")
        toolbar.addSeparator()
        toolbar.addAction("طباعة")
        toolbar.addSeparator()
        toolbar.addAction("نسخ احتياطي")
        
    def create_status_bar(self):
        """Create the application status bar"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # Status labels
        self.status_label = QLabel("جاهز")
        self.user_label = QLabel("المستخدم: Admin")
        self.time_label = QLabel()
        
        status_bar.addWidget(self.status_label)
        status_bar.addPermanentWidget(self.user_label)
        status_bar.addPermanentWidget(self.time_label)
        
        # Update time every second
        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        self.update_time()
        
    def setup_connections(self):
        """Setup signal-slot connections"""
        # Theme manager connections
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # Settings manager connections
        self.settings_manager.theme_changed.connect(self.theme_manager.apply_theme)
        
    def setup_auto_features(self):
        """Setup auto-save and other automatic features"""
        # Auto-save timer
        if self.settings_manager.get('auto_save', True):
            self.auto_save_timer = QTimer()
            self.auto_save_timer.timeout.connect(self.auto_save)
            self.auto_save_timer.start(60000)  # Auto-save every minute
            
        # Low stock check timer
        if self.settings_manager.is_low_stock_alert_enabled():
            self.stock_check_timer = QTimer()
            self.stock_check_timer.timeout.connect(self.check_low_stock)
            self.stock_check_timer.start(300000)  # Check every 5 minutes
            
        # Auto backup timer
        if self.settings_manager.is_auto_backup_enabled():
            self.auto_backup_timer = QTimer()
            self.auto_backup_timer.timeout.connect(self.auto_backup)
            # Set backup frequency
            frequency = self.settings_manager.get_backup_frequency()
            if frequency == 'hourly':
                interval = 3600000  # 1 hour
            elif frequency == 'daily':
                interval = 86400000  # 24 hours
            else:
                interval = 86400000  # Default to daily
            self.auto_backup_timer.start(interval)
            
    def apply_initial_theme(self):
        """Apply the initial theme based on settings"""
        theme = self.settings_manager.get_theme()
        self.theme_manager.apply_theme(theme)
        self.update_theme_button()
        
    def on_module_selected(self, module_name: str):
        """Handle module selection from sidebar"""
        # Get module title
        titles = {
            'products': 'المنتجات',
            'customers': 'العملاء', 
            'suppliers': 'الموردين',
            'reports': 'التقارير',
            'services': 'الخدمات',
            'settings': 'الإعدادات'
        }
        
        title = titles.get(module_name, module_name)
        
        # Add tab if not already open
        if module_name not in self.open_tabs:
            self.add_tab(module_name, f"{title} 📋")
        else:
            # Switch to existing tab
            self.tab_widget.setCurrentIndex(self.open_tabs[module_name])
            
        self.current_module = module_name
        self.title_label.setText(title)
        self.module_changed.emit(module_name)
        
    def add_tab(self, module_name: str, tab_title: str):
        """Add a new tab for a module"""
        if module_name in self.modules:
            module_widget = self.modules[module_name]
            index = self.tab_widget.addTab(module_widget, tab_title)
            self.open_tabs[module_name] = index
            self.tab_widget.setCurrentIndex(index)
            
    def close_tab(self, index: int):
        """Close a tab"""
        # Find module name for this tab
        module_name = None
        for name, tab_index in self.open_tabs.items():
            if tab_index == index:
                module_name = name
                break
                
        if module_name:
            # Don't close the last tab
            if self.tab_widget.count() <= 1:
                self.notification_manager.show_warning("تحذير", "لا يمكن إغلاق آخر تبويب")
                return
                
            self.tab_widget.removeTab(index)
            del self.open_tabs[module_name]
            
            # Update indices for remaining tabs
            for name in self.open_tabs:
                if self.open_tabs[name] > index:
                    self.open_tabs[name] -= 1
                    
    def on_tab_changed(self, index: int):
        """Handle tab change"""
        if index >= 0:
            # Find current module
            current_module = None
            for name, tab_index in self.open_tabs.items():
                if tab_index == index:
                    current_module = name
                    break
                    
            if current_module:
                self.current_module = current_module
                # Update title and sidebar
                titles = {
                    'products': 'المنتجات',
                    'customers': 'العملاء',
                    'suppliers': 'الموردين', 
                    'reports': 'التقارير',
                    'services': 'الخدمات',
                    'settings': 'الإعدادات'
                }
                self.title_label.setText(titles.get(current_module, current_module))
                self.sidebar.select_module(current_module)
                
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        current_theme = self.theme_manager.get_current_theme()
        new_theme = 'dark' if current_theme == 'light' else 'light'
        
        self.theme_manager.apply_theme(new_theme)
        self.settings_manager.set_theme(new_theme)
        self.update_theme_button()
        
    def update_theme_button(self):
        """Update theme button icon"""
        current_theme = self.theme_manager.get_current_theme()
        icon = "☀️" if current_theme == 'dark' else "🌙"
        self.theme_button.setText(icon)
        
    def on_theme_changed(self, theme_name: str):
        """Handle theme change"""
        self.update_theme_button()
        
    def on_quick_search(self, text: str):
        """Handle quick search"""
        if len(text) >= 2:  # Start searching after 2 characters
            current_module = self.modules.get(self.current_module)
            if current_module and hasattr(current_module, 'search'):
                current_module.search(text)
                
    def auto_save(self):
        """Auto-save current work"""
        try:
            current_module = self.modules.get(self.current_module)
            if current_module and hasattr(current_module, 'auto_save'):
                current_module.auto_save()
                self.status_label.setText("تم الحفظ التلقائي")
                QTimer.singleShot(3000, lambda: self.status_label.setText("جاهز"))
        except Exception as e:
            print(f"Auto-save error: {e}")
            
    def check_low_stock(self):
        """Check for low stock products and show notifications"""
        try:
            low_stock_products = self.db_manager.get_low_stock_products()
            if low_stock_products:
                count = len(low_stock_products)
                message = f"تحذير: يوجد {count} منتج بمخزون منخفض"
                self.notification_manager.show_warning("تنبيه المخزون", message)
        except Exception as e:
            print(f"Low stock check error: {e}")
            
    def auto_backup(self):
        """Perform automatic backup"""
        try:
            backup_path = self.db_manager.backup_database()
            self.status_label.setText(f"تم إنشاء نسخة احتياطية: {backup_path}")
            QTimer.singleShot(5000, lambda: self.status_label.setText("جاهز"))
        except Exception as e:
            print(f"Auto backup error: {e}")
            
    def create_backup(self):
        """Create manual backup"""
        try:
            backup_path = self.db_manager.backup_database()
            self.notification_manager.show_success(
                "نسخ احتياطي", 
                f"تم إنشاء النسخة الاحتياطية بنجاح:\n{backup_path}"
            )
        except Exception as e:
            self.notification_manager.show_error(
                "خطأ", 
                f"فشل في إنشاء النسخة الاحتياطية:\n{str(e)}"
            )
            
    def update_time(self):
        """Update time display"""
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S - %Y/%m/%d")
        self.time_label.setText(current_time)
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "حول البرنامج", 
            "نظام إدارة محل الموبايل\n"
            "الإصدار 2.0.0\n\n"
            "نظام شامل لإدارة محلات الموبايل\n"
            "يشمل إدارة المنتجات والعملاء والموردين\n"
            "والتقارير والخدمات"
        )
        
    def closeEvent(self, event):
        """Handle application close"""
        # Save current window state
        self.settings_manager.set('window_geometry', self.saveGeometry())
        self.settings_manager.set('window_state', self.saveState())
        
        # Stop all timers
        if hasattr(self, 'auto_save_timer'):
            self.auto_save_timer.stop()
        if hasattr(self, 'stock_check_timer'):
            self.stock_check_timer.stop()
        if hasattr(self, 'auto_backup_timer'):
            self.auto_backup_timer.stop()
        if hasattr(self, 'time_timer'):
            self.time_timer.stop()
            
        event.accept()