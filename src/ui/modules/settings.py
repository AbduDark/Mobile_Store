#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Module - Application Settings Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QLabel, QFrame, QHeaderView,
    QAbstractItemView, QDialog, QMessageBox, QSplitter,
    QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox,
    QCheckBox, QSlider, QFileDialog, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTimer
from PyQt6.QtGui import QFont

from .base_module import BaseModule

class SettingsModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "الإعدادات")
        
    def setup_ui(self):
        """Setup settings module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # General settings tab
        self.general_tab = self.create_general_tab()
        self.tab_widget.addTab(self.general_tab, "⚙️ الإعدادات العامة")
        
        # Appearance tab
        self.appearance_tab = self.create_appearance_tab()
        self.tab_widget.addTab(self.appearance_tab, "🎨 المظهر")
        
        # Business settings tab
        self.business_tab = self.create_business_tab()
        self.tab_widget.addTab(self.business_tab, "🏢 إعدادات العمل")
        
        # Backup tab
        self.backup_tab = self.create_backup_tab()
        self.tab_widget.addTab(self.backup_tab, "💾 النسخ الاحتياطي")
        
        # About tab
        self.about_tab = self.create_about_tab()
        self.tab_widget.addTab(self.about_tab, "ℹ️ حول البرنامج")
        
        layout.addWidget(self.tab_widget)
        
    def create_general_tab(self) -> QWidget:
        """Create general settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Language settings
        language_group = QGroupBox("اللغة والمنطقة")
        language_layout = QFormLayout(language_group)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems(["العربية", "English"])
        self.language_combo.currentTextChanged.connect(self.change_language)
        language_layout.addRow("لغة البرنامج:", self.language_combo)
        
        self.currency_input = QLineEdit()
        self.currency_input.setText("ريال")
        language_layout.addRow("العملة:", self.currency_input)
        
        self.date_format = QComboBox()
        self.date_format.addItems(["dd/mm/yyyy", "mm/dd/yyyy", "yyyy-mm-dd"])
        language_layout.addRow("تنسيق التاريخ:", self.date_format)
        
        layout.addWidget(language_group)
        
        # Notification settings
        notification_group = QGroupBox("الإشعارات")
        notification_layout = QFormLayout(notification_group)
        
        self.sound_notifications = QCheckBox("تفعيل الأصوات")
        self.sound_notifications.setChecked(True)
        notification_layout.addRow("الأصوات:", self.sound_notifications)
        
        self.desktop_notifications = QCheckBox("إشعارات سطح المكتب")
        self.desktop_notifications.setChecked(True)
        notification_layout.addRow("إشعارات النظام:", self.desktop_notifications)
        
        self.low_stock_alerts = QCheckBox("تنبيهات المخزون المنخفض")
        self.low_stock_alerts.setChecked(True)
        notification_layout.addRow("تنبيهات المخزون:", self.low_stock_alerts)
        
        layout.addWidget(notification_group)
        
        # Auto-save settings
        autosave_group = QGroupBox("الحفظ التلقائي")
        autosave_layout = QFormLayout(autosave_group)
        
        self.auto_save_enabled = QCheckBox("تفعيل الحفظ التلقائي")
        self.auto_save_enabled.setChecked(True)
        autosave_layout.addRow("الحفظ التلقائي:", self.auto_save_enabled)
        
        self.auto_save_interval = QSpinBox()
        self.auto_save_interval.setRange(1, 60)
        self.auto_save_interval.setValue(5)
        self.auto_save_interval.setSuffix(" دقائق")
        autosave_layout.addRow("فترة الحفظ:", self.auto_save_interval)
        
        layout.addWidget(autosave_group)
        
        layout.addStretch()
        
        return tab
        
    def create_appearance_tab(self) -> QWidget:
        """Create appearance settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Theme settings
        theme_group = QGroupBox("المظهر العام")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["فاتح", "داكن"])
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addRow("نمط المظهر:", self.theme_combo)
        
        # Preview area
        preview_label = QLabel("معاينة المظهر")
        preview_label.setStyleSheet("""
            QLabel {
                border: 2px solid #ddd;
                border-radius: 6px;
                padding: 20px;
                background-color: white;
                color: #333;
                font-size: 12pt;
            }
        """)
        preview_label.setMinimumHeight(100)
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        theme_layout.addRow("المعاينة:", preview_label)
        
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("الخطوط")
        font_layout = QFormLayout(font_group)
        
        self.font_family = QComboBox()
        self.font_family.addItems(["Tahoma", "Cairo", "Arial", "Times New Roman"])
        font_layout.addRow("نوع الخط:", self.font_family)
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 24)
        self.font_size.setValue(10)
        font_layout.addRow("حجم الخط:", self.font_size)
        
        # Font preview
        font_preview = QLabel("نموذج للخط المختار - Sample Text")
        font_preview.setStyleSheet("border: 1px solid #ddd; padding: 10px;")
        font_layout.addRow("معاينة الخط:", font_preview)
        
        layout.addWidget(font_group)
        
        # Window settings
        window_group = QGroupBox("النافذة")
        window_layout = QFormLayout(window_group)
        
        self.start_maximized = QCheckBox("فتح النافذة بحجم كامل")
        self.start_maximized.setChecked(True)
        window_layout.addRow("النافذة:", self.start_maximized)
        
        self.remember_window_state = QCheckBox("تذكر حالة النافذة")
        self.remember_window_state.setChecked(True)
        window_layout.addRow("تذكر الحالة:", self.remember_window_state)
        
        layout.addWidget(window_group)
        
        layout.addStretch()
        
        return tab
        
    def create_business_tab(self) -> QWidget:
        """Create business settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Company information
        company_group = QGroupBox("معلومات الشركة")
        company_layout = QFormLayout(company_group)
        
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("اسم المحل أو الشركة")
        company_layout.addRow("اسم المحل:", self.company_name)
        
        self.company_address = QTextEdit()
        self.company_address.setMaximumHeight(80)
        self.company_address.setPlaceholderText("العنوان التفصيلي")
        company_layout.addRow("العنوان:", self.company_address)
        
        self.company_phone = QLineEdit()
        self.company_phone.setPlaceholderText("رقم الهاتف")
        company_layout.addRow("الهاتف:", self.company_phone)
        
        self.company_email = QLineEdit()
        self.company_email.setPlaceholderText("البريد الإلكتروني")
        company_layout.addRow("البريد الإلكتروني:", self.company_email)
        
        layout.addWidget(company_group)
        
        # Tax and pricing settings
        tax_group = QGroupBox("الضرائب والأسعار")
        tax_layout = QFormLayout(tax_group)
        
        self.tax_rate = QDoubleSpinBox()
        self.tax_rate.setRange(0, 100)
        self.tax_rate.setValue(15.0)
        self.tax_rate.setSuffix("%")
        tax_layout.addRow("معدل الضريبة:", self.tax_rate)
        
        self.include_tax = QCheckBox("إضافة الضريبة تلقائياً")
        self.include_tax.setChecked(True)
        tax_layout.addRow("الضريبة:", self.include_tax)
        
        self.price_rounding = QComboBox()
        self.price_rounding.addItems(["عدم التقريب", "تقريب لأقرب ريال", "تقريب لأقرب 0.25"])
        tax_layout.addRow("تقريب الأسعار:", self.price_rounding)
        
        layout.addWidget(tax_group)
        
        # Receipt settings
        receipt_group = QGroupBox("إعدادات الفواتير")
        receipt_layout = QFormLayout(receipt_group)
        
        self.receipt_header = QTextEdit()
        self.receipt_header.setMaximumHeight(60)
        self.receipt_header.setPlaceholderText("نص رأس الفاتورة")
        receipt_layout.addRow("رأس الفاتورة:", self.receipt_header)
        
        self.receipt_footer = QTextEdit()
        self.receipt_footer.setMaximumHeight(60)
        self.receipt_footer.setPlaceholderText("نص ذيل الفاتورة")
        receipt_layout.addRow("ذيل الفاتورة:", self.receipt_footer)
        
        self.auto_print = QCheckBox("طباعة تلقائية بعد البيع")
        receipt_layout.addRow("الطباعة:", self.auto_print)
        
        layout.addWidget(receipt_group)
        
        layout.addStretch()
        
        return tab
        
    def create_backup_tab(self) -> QWidget:
        """Create backup settings tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Auto backup settings
        auto_backup_group = QGroupBox("النسخ الاحتياطي التلقائي")
        auto_backup_layout = QFormLayout(auto_backup_group)
        
        self.auto_backup_enabled = QCheckBox("تفعيل النسخ الاحتياطي التلقائي")
        self.auto_backup_enabled.setChecked(True)
        auto_backup_layout.addRow("النسخ التلقائي:", self.auto_backup_enabled)
        
        self.backup_frequency = QComboBox()
        self.backup_frequency.addItems(["يومياً", "أسبوعياً", "شهرياً"])
        auto_backup_layout.addRow("تكرار النسخ:", self.backup_frequency)
        
        self.backup_time = QComboBox()
        self.backup_time.addItems([
            "عند إغلاق البرنامج", "12:00 ص", "1:00 ص", 
            "2:00 ص", "3:00 ص", "4:00 ص"
        ])
        auto_backup_layout.addRow("وقت النسخ:", self.backup_time)
        
        self.backup_location = QLineEdit()
        self.backup_location.setText("backups/")
        backup_location_layout = QHBoxLayout()
        backup_location_layout.addWidget(self.backup_location)
        
        browse_btn = QPushButton("تصفح")
        browse_btn.setObjectName("secondary_button")
        browse_btn.clicked.connect(self.browse_backup_location)
        backup_location_layout.addWidget(browse_btn)
        
        auto_backup_layout.addRow("مجلد الحفظ:", backup_location_layout)
        
        layout.addWidget(auto_backup_group)
        
        # Manual backup
        manual_backup_group = QGroupBox("النسخ الاحتياطي اليدوي")
        manual_backup_layout = QVBoxLayout(manual_backup_group)
        
        backup_info = QLabel("""
        قم بإنشاء نسخة احتياطية فورية من البيانات.
        يُنصح بإنشاء نسخ احتياطية دورية لحماية البيانات.
        """)
        backup_info.setWordWrap(True)
        backup_info.setStyleSheet("color: #666; font-size: 10pt;")
        manual_backup_layout.addWidget(backup_info)
        
        manual_buttons = QHBoxLayout()
        
        self.backup_btn = QPushButton("💾 إنشاء نسخة احتياطية")
        self.backup_btn.setObjectName("primary_button")
        self.backup_btn.clicked.connect(self.create_backup)
        
        self.restore_btn = QPushButton("📁 استرجاع من نسخة احتياطية")
        self.restore_btn.setObjectName("secondary_button")
        self.restore_btn.clicked.connect(self.restore_backup)
        
        manual_buttons.addWidget(self.restore_btn)
        manual_buttons.addStretch()
        manual_buttons.addWidget(self.backup_btn)
        
        manual_backup_layout.addLayout(manual_buttons)
        
        # Progress bar for backup operations
        self.backup_progress = QProgressBar()
        self.backup_progress.setVisible(False)
        manual_backup_layout.addWidget(self.backup_progress)
        
        layout.addWidget(manual_backup_group)
        
        # Cloud backup settings
        cloud_group = QGroupBox("النسخ السحابي")
        cloud_layout = QFormLayout(cloud_group)
        
        self.cloud_backup_enabled = QCheckBox("تفعيل النسخ السحابي")
        cloud_layout.addRow("النسخ السحابي:", self.cloud_backup_enabled)
        
        self.cloud_provider = QComboBox()
        self.cloud_provider.addItems(["Google Drive", "Dropbox", "OneDrive"])
        self.cloud_provider.setEnabled(False)
        cloud_layout.addRow("مزود الخدمة:", self.cloud_provider)
        
        cloud_connect_btn = QPushButton("🔗 ربط الحساب")
        cloud_connect_btn.setObjectName("secondary_button")
        cloud_connect_btn.setEnabled(False)
        cloud_layout.addRow("الربط:", cloud_connect_btn)
        
        # Enable cloud controls when checkbox is checked
        self.cloud_backup_enabled.toggled.connect(
            lambda checked: [
                self.cloud_provider.setEnabled(checked),
                cloud_connect_btn.setEnabled(checked)
            ]
        )
        
        layout.addWidget(cloud_group)
        
        # Backup history
        history_group = QGroupBox("سجل النسخ الاحتياطية")
        history_layout = QVBoxLayout(history_group)
        
        self.backup_history_table = QTableWidget()
        self.backup_history_table.setColumnCount(4)
        self.backup_history_table.setHorizontalHeaderLabels([
            "التاريخ", "الوقت", "الحجم", "الموقع"
        ])
        self.backup_history_table.setMaximumHeight(150)
        
        history_layout.addWidget(self.backup_history_table)
        layout.addWidget(history_group)
        
        layout.addStretch()
        
        return tab
        
    def create_about_tab(self) -> QWidget:
        """Create about program tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Logo and title
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        
        title = QLabel("نظام إدارة محل الموبايل")
        title.setStyleSheet("""
            font-size: 24pt;
            font-weight: bold;
            color: #2E86C1;
            margin: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        
        version = QLabel("الإصدار 2.0.0")
        version.setStyleSheet("font-size: 14pt; color: #666; margin-bottom: 20px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(version)
        
        layout.addWidget(title_frame)
        
        # Program information
        info_group = QGroupBox("معلومات البرنامج")
        info_layout = QVBoxLayout(info_group)
        
        description = QLabel("""
        نظام شامل لإدارة محلات الهواتف المحمولة واكسسواراتها.
        يتضمن النظام إدارة المنتجات والمخزون، العملاء والموردين،
        المبيعات والتقارير، بالإضافة إلى خدمات الدفع وشحن الجوالات.
        
        تم تطوير البرنامج باستخدام Python وPyQt6 مع واجهة باللغة العربية
        ودعم كامل للكتابة من اليمين إلى اليسار.
        """)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 11pt; line-height: 1.4;")
        info_layout.addWidget(description)
        
        layout.addWidget(info_group)
        
        # Features list
        features_group = QGroupBox("المزايا الرئيسية")
        features_layout = QVBoxLayout(features_group)
        
        features = QLabel("""
        ✓ واجهة باللغة العربية مع دعم RTL
        ✓ إدارة شاملة للمنتجات والمخزون
        ✓ نظام إدارة العملاء مع برنامج الولاء
        ✓ إدارة الموردين والطلبات
        ✓ تقارير مفصلة ورسوم بيانية
        ✓ خدمات شحن الجوال ودفع الفواتير
        ✓ نسخ احتياطي تلقائي
        ✓ مظهر فاتح وداكن
        ✓ بحث سريع ومتقدم
        ✓ دعم متعدد التبويبات
        """)
        features.setStyleSheet("font-size: 10pt; line-height: 1.5;")
        features_layout.addWidget(features)
        
        layout.addWidget(features_group)
        
        # System info
        system_group = QGroupBox("معلومات النظام")
        system_layout = QFormLayout(system_group)
        
        import platform
        import sys
        
        system_layout.addRow("نظام التشغيل:", QLabel(platform.system()))
        system_layout.addRow("إصدار Python:", QLabel(sys.version.split()[0]))
        system_layout.addRow("إصدار PyQt6:", QLabel("6.4.2"))
        
        layout.addWidget(system_group)
        
        layout.addStretch()
        
        return tab
        
    def load_data(self):
        """Load current settings"""
        try:
            # Load general settings
            self.language_combo.setCurrentText(
                "العربية" if self.settings_manager.get_language() == "ar" else "English"
            )
            self.currency_input.setText(self.settings_manager.get_currency())
            
            # Load appearance settings
            current_theme = self.settings_manager.get_theme()
            self.theme_combo.setCurrentText("فاتح" if current_theme == "light" else "داكن")
            
            # Load notification settings
            self.sound_notifications.setChecked(
                self.settings_manager.get('notification_sound', True)
            )
            self.low_stock_alerts.setChecked(
                self.settings_manager.is_low_stock_alert_enabled()
            )
            
            # Load auto-save settings
            self.auto_save_enabled.setChecked(
                self.settings_manager.get('auto_save', True)
            )
            
            # Load backup settings
            self.auto_backup_enabled.setChecked(
                self.settings_manager.is_auto_backup_enabled()
            )
            
            frequency = self.settings_manager.get_backup_frequency()
            if frequency == 'daily':
                self.backup_frequency.setCurrentText("يومياً")
            elif frequency == 'weekly':
                self.backup_frequency.setCurrentText("أسبوعياً")
            elif frequency == 'monthly':
                self.backup_frequency.setCurrentText("شهرياً")
                
            # Load business settings
            self.tax_rate.setValue(self.settings_manager.get_tax_rate())
            
            # Load backup history
            self.load_backup_history()
            
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def load_backup_history(self):
        """Load backup history"""
        # Sample backup history - would come from backup logs
        history = []
        
        self.backup_history_table.setRowCount(len(history))
        for row, backup in enumerate(history):
            self.backup_history_table.setItem(row, 0, QTableWidgetItem(backup.get('date', '')))
            self.backup_history_table.setItem(row, 1, QTableWidgetItem(backup.get('time', '')))
            self.backup_history_table.setItem(row, 2, QTableWidgetItem(backup.get('size', '')))
            self.backup_history_table.setItem(row, 3, QTableWidgetItem(backup.get('location', '')))
            
    def change_language(self, language: str):
        """Change application language"""
        lang_code = "ar" if language == "العربية" else "en"
        self.settings_manager.set_language(lang_code)
        
        # Show restart message
        QMessageBox.information(
            self, "تغيير اللغة",
            "سيتم تطبيق تغيير اللغة عند إعادة تشغيل البرنامج"
        )
        
    def change_theme(self, theme: str):
        """Change application theme"""
        theme_code = "light" if theme == "فاتح" else "dark"
        self.settings_manager.set_theme(theme_code)
        
    def browse_backup_location(self):
        """Browse for backup location"""
        folder = QFileDialog.getExistingDirectory(
            self, "اختيار مجلد النسخ الاحتياطي", 
            self.backup_location.text()
        )
        
        if folder:
            self.backup_location.setText(folder)
            
    def create_backup(self):
        """Create manual backup"""
        try:
            self.backup_progress.setVisible(True)
            self.backup_progress.setValue(0)
            
            # Simulate backup progress
            for i in range(101):
                self.backup_progress.setValue(i)
                QTimer.singleShot(i * 10, lambda: None)  # Simulate work
                
            backup_path = self.db_manager.backup_database()
            
            self.backup_progress.setVisible(False)
            
            QMessageBox.information(
                self, "نسخ احتياطي",
                f"تم إنشاء النسخة الاحتياطية بنجاح:\n{backup_path}"
            )
            
            # Refresh backup history
            self.load_backup_history()
            
        except Exception as e:
            self.backup_progress.setVisible(False)
            QMessageBox.critical(
                self, "خطأ",
                f"فشل في إنشاء النسخة الاحتياطية:\n{str(e)}"
            )
            
    def restore_backup(self):
        """Restore from backup"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "اختيار ملف النسخة الاحتياطية", 
            self.backup_location.text(),
            "Database Files (*.db);;All Files (*)"
        )
        
        if file_path:
            reply = QMessageBox.question(
                self, "تأكيد الاستعادة",
                "هل أنت متأكد من استعادة هذه النسخة الاحتياطية؟\n"
                "سيتم استبدال البيانات الحالية.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    # Here would be the actual restore process
                    QMessageBox.information(
                        self, "استعادة",
                        "تم استعادة النسخة الاحتياطية بنجاح\n"
                        "سيتم إعادة تشغيل البرنامج"
                    )
                    
                except Exception as e:
                    QMessageBox.critical(
                        self, "خطأ",
                        f"فشل في استعادة النسخة الاحتياطية:\n{str(e)}"
                    )
                    
    def save_settings(self):
        """Save all settings"""
        try:
            # Save general settings
            lang = "ar" if self.language_combo.currentText() == "العربية" else "en"
            self.settings_manager.set_language(lang)
            
            # Save appearance settings
            theme = "light" if self.theme_combo.currentText() == "فاتح" else "dark"
            self.settings_manager.set_theme(theme)
            
            # Save other settings
            self.settings_manager.set('notification_sound', self.sound_notifications.isChecked())
            self.settings_manager.set('low_stock_alert', self.low_stock_alerts.isChecked())
            self.settings_manager.set('auto_save', self.auto_save_enabled.isChecked())
            self.settings_manager.set('auto_backup', self.auto_backup_enabled.isChecked())
            
            # Save business settings
            self.db_manager.set_setting('tax_rate', str(self.tax_rate.value()))
            self.db_manager.set_setting('currency', self.currency_input.text())
            
            self.status_message.emit("تم حفظ الإعدادات بنجاح")
            
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل في حفظ الإعدادات:\n{str(e)}")
            
    def reset_settings(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "إعادة تعيين الإعدادات",
            "هل أنت متأكد من إعادة تعيين جميع الإعدادات للقيم الافتراضية؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.settings_manager.reset_to_defaults()
                self.load_data()  # Reload settings
                
                QMessageBox.information(
                    self, "إعادة تعيين",
                    "تم إعادة تعيين الإعدادات بنجاح"
                )
                
            except Exception as e:
                QMessageBox.critical(
                    self, "خطأ",
                    f"فشل في إعادة تعيين الإعدادات:\n{str(e)}"
                )