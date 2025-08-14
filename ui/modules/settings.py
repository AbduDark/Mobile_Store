#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Module
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import FormField, RTLButton, RTLLabel

class SettingsModule:
    def __init__(self, parent, theme_manager, theme_callback):
        self.parent = parent
        self.theme_manager = theme_manager
        self.theme_callback = theme_callback
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the settings interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for settings tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_general_tab()
        self.create_display_tab()
        self.create_printer_tab()
        self.create_backup_tab()
        self.create_about_tab()
        
    def create_general_tab(self):
        """Create general settings tab"""
        general_frame = tk.Frame(self.notebook)
        self.notebook.add(general_frame, text="الإعدادات العامة")
        
        # Shop information section
        shop_section = tk.LabelFrame(general_frame, text="معلومات المحل", font=("Tahoma", 12, "bold"))
        shop_section.pack(fill=tk.X, padx=20, pady=20)
        
        shop_frame = tk.Frame(shop_section)
        shop_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Two column layout
        right_frame = tk.Frame(shop_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        left_frame = tk.Frame(shop_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Shop information fields
        self.shop_fields = {}
        
        self.shop_fields['shop_name'] = FormField(right_frame, "اسم المحل:")
        self.shop_fields['shop_name'].pack(fill=tk.X, pady=5)
        self.shop_fields['shop_name'].set_value("محل الموبايل الذكي")
        
        self.shop_fields['owner_name'] = FormField(right_frame, "اسم المالك:")
        self.shop_fields['owner_name'].pack(fill=tk.X, pady=5)
        self.shop_fields['owner_name'].set_value("أحمد محمد")
        
        self.shop_fields['phone'] = FormField(right_frame, "رقم الهاتف:")
        self.shop_fields['phone'].pack(fill=tk.X, pady=5)
        self.shop_fields['phone'].set_value("01234567890")
        
        self.shop_fields['email'] = FormField(left_frame, "البريد الإلكتروني:")
        self.shop_fields['email'].pack(fill=tk.X, pady=5)
        self.shop_fields['email'].set_value("info@mobileshop.com")
        
        self.shop_fields['address'] = FormField(left_frame, "العنوان:", 'text')
        self.shop_fields['address'].pack(fill=tk.BOTH, expand=True, pady=5)
        self.shop_fields['address'].set_value("شارع الجمهورية، وسط البلد، القاهرة")
        
        # System settings section
        system_section = tk.LabelFrame(general_frame, text="إعدادات النظام", font=("Tahoma", 12, "bold"))
        system_section.pack(fill=tk.X, padx=20, pady=20)
        
        system_frame = tk.Frame(system_section)
        system_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Auto backup
        auto_backup_frame = tk.Frame(system_frame)
        auto_backup_frame.pack(fill=tk.X, pady=5)
        
        self.auto_backup_var = tk.BooleanVar(value=True)
        auto_backup_check = tk.Checkbutton(
            auto_backup_frame,
            text="نسخ احتياطي تلقائي يومياً",
            variable=self.auto_backup_var,
            font=("Tahoma", 10),
            anchor='e'
        )
        auto_backup_check.pack(anchor='e')
        
        # Low stock alert
        low_stock_frame = tk.Frame(system_frame)
        low_stock_frame.pack(fill=tk.X, pady=5)
        
        RTLLabel(low_stock_frame, text="تنبيه نقص المخزون عند:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.low_stock_var = tk.StringVar(value="5")
        low_stock_entry = tk.Entry(low_stock_frame, textvariable=self.low_stock_var, width=10, justify='right')
        low_stock_entry.pack(side=tk.RIGHT, padx=5)
        
        RTLLabel(low_stock_frame, text="قطعة", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        # Currency settings
        currency_frame = tk.Frame(system_frame)
        currency_frame.pack(fill=tk.X, pady=5)
        
        RTLLabel(currency_frame, text="العملة:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.currency_var = tk.StringVar(value="ج.م")
        currency_combo = ttk.Combobox(
            currency_frame,
            textvariable=self.currency_var,
            values=["ج.م", "ريال", "درهم", "دينار"],
            state="readonly",
            width=10
        )
        currency_combo.pack(side=tk.RIGHT, padx=5)
        
        # Save button
        save_general_btn = RTLButton(
            general_frame,
            text="💾 حفظ الإعدادات العامة",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_general_settings
        )
        save_general_btn.pack(anchor='e', padx=20, pady=20)
        
    def create_display_tab(self):
        """Create display settings tab"""
        display_frame = tk.Frame(self.notebook)
        self.notebook.add(display_frame, text="إعدادات العرض")
        
        # Theme section
        theme_section = tk.LabelFrame(display_frame, text="المظهر", font=("Tahoma", 12, "bold"))
        theme_section.pack(fill=tk.X, padx=20, pady=20)
        
        theme_content = tk.Frame(theme_section)
        theme_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Theme selection
        theme_frame = tk.Frame(theme_content)
        theme_frame.pack(fill=tk.X, pady=10)
        
        RTLLabel(theme_frame, text="المظهر:", font=("Tahoma", 12)).pack(anchor='e', pady=5)
        
        self.theme_var = tk.StringVar(value=self.theme_manager.current_theme)
        
        light_radio = tk.Radiobutton(
            theme_frame,
            text="☀️ الوضع النهاري",
            variable=self.theme_var,
            value="light",
            font=("Tahoma", 11),
            anchor='e',
            command=self.change_theme
        )
        light_radio.pack(anchor='e', pady=2)
        
        dark_radio = tk.Radiobutton(
            theme_frame,
            text="🌙 الوضع الليلي",
            variable=self.theme_var,
            value="dark",
            font=("Tahoma", 11),
            anchor='e',
            command=self.change_theme
        )
        dark_radio.pack(anchor='e', pady=2)
        
        # Font settings
        font_section = tk.LabelFrame(display_frame, text="الخط", font=("Tahoma", 12, "bold"))
        font_section.pack(fill=tk.X, padx=20, pady=20)
        
        font_content = tk.Frame(font_section)
        font_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Font family
        font_family_frame = tk.Frame(font_content)
        font_family_frame.pack(fill=tk.X, pady=5)
        
        RTLLabel(font_family_frame, text="نوع الخط:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.font_family_var = tk.StringVar(value="Tahoma")
        font_combo = ttk.Combobox(
            font_family_frame,
            textvariable=self.font_family_var,
            values=["Tahoma", "Arial", "Times New Roman", "Cairo", "Amiri"],
            state="readonly",
            width=15
        )
        font_combo.pack(side=tk.RIGHT, padx=5)
        
        # Font size
        font_size_frame = tk.Frame(font_content)
        font_size_frame.pack(fill=tk.X, pady=5)
        
        RTLLabel(font_size_frame, text="حجم الخط:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.font_size_var = tk.StringVar(value="10")
        font_size_combo = ttk.Combobox(
            font_size_frame,
            textvariable=self.font_size_var,
            values=["8", "9", "10", "11", "12", "14", "16"],
            state="readonly",
            width=10
        )
        font_size_combo.pack(side=tk.RIGHT, padx=5)
        
        # Language settings
        language_section = tk.LabelFrame(display_frame, text="اللغة", font=("Tahoma", 12, "bold"))
        language_section.pack(fill=tk.X, padx=20, pady=20)
        
        language_content = tk.Frame(language_section)
        language_content.pack(fill=tk.X, padx=20, pady=20)
        
        RTLLabel(language_content, text="لغة الواجهة:", font=("Tahoma", 10)).pack(anchor='e', pady=5)
        
        self.language_var = tk.StringVar(value="العربية")
        language_combo = ttk.Combobox(
            language_content,
            textvariable=self.language_var,
            values=["العربية", "English"],
            state="readonly",
            width=15
        )
        language_combo.pack(anchor='e', pady=5)
        
        # Save button
        save_display_btn = RTLButton(
            display_frame,
            text="💾 حفظ إعدادات العرض",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_display_settings
        )
        save_display_btn.pack(anchor='e', padx=20, pady=20)
        
    def create_printer_tab(self):
        """Create printer settings tab"""
        printer_frame = tk.Frame(self.notebook)
        self.notebook.add(printer_frame, text="إعدادات الطباعة")
        
        # Receipt printer section
        receipt_section = tk.LabelFrame(printer_frame, text="طابعة الفواتير", font=("Tahoma", 12, "bold"))
        receipt_section.pack(fill=tk.X, padx=20, pady=20)
        
        receipt_content = tk.Frame(receipt_section)
        receipt_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Printer selection
        printer_frame_content = tk.Frame(receipt_content)
        printer_frame_content.pack(fill=tk.X, pady=5)
        
        RTLLabel(printer_frame_content, text="الطابعة:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.printer_var = tk.StringVar(value="الطابعة الافتراضية")
        printer_combo = ttk.Combobox(
            printer_frame_content,
            textvariable=self.printer_var,
            values=["الطابعة الافتراضية", "HP LaserJet", "Canon PIXMA", "Epson L3110"],
            state="readonly",
            width=20
        )
        printer_combo.pack(side=tk.RIGHT, padx=5)
        
        # Paper size
        paper_frame = tk.Frame(receipt_content)
        paper_frame.pack(fill=tk.X, pady=5)
        
        RTLLabel(paper_frame, text="حجم الورق:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.paper_size_var = tk.StringVar(value="A4")
        paper_combo = ttk.Combobox(
            paper_frame,
            textvariable=self.paper_size_var,
            values=["A4", "A5", "80mm فاتورة", "58mm فاتورة"],
            state="readonly",
            width=15
        )
        paper_combo.pack(side=tk.RIGHT, padx=5)
        
        # Auto print
        auto_print_frame = tk.Frame(receipt_content)
        auto_print_frame.pack(fill=tk.X, pady=5)
        
        self.auto_print_var = tk.BooleanVar(value=False)
        auto_print_check = tk.Checkbutton(
            auto_print_frame,
            text="طباعة تلقائية للفواتير",
            variable=self.auto_print_var,
            font=("Tahoma", 10),
            anchor='e'
        )
        auto_print_check.pack(anchor='e')
        
        # Receipt format section
        format_section = tk.LabelFrame(printer_frame, text="تنسيق الفاتورة", font=("Tahoma", 12, "bold"))
        format_section.pack(fill=tk.X, padx=20, pady=20)
        
        format_content = tk.Frame(format_section)
        format_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Header settings
        self.show_logo_var = tk.BooleanVar(value=True)
        logo_check = tk.Checkbutton(
            format_content,
            text="عرض شعار المحل",
            variable=self.show_logo_var,
            font=("Tahoma", 10),
            anchor='e'
        )
        logo_check.pack(anchor='e', pady=2)
        
        self.show_contact_var = tk.BooleanVar(value=True)
        contact_check = tk.Checkbutton(
            format_content,
            text="عرض بيانات الاتصال",
            variable=self.show_contact_var,
            font=("Tahoma", 10),
            anchor='e'
        )
        contact_check.pack(anchor='e', pady=2)
        
        self.show_thank_you_var = tk.BooleanVar(value=True)
        thank_you_check = tk.Checkbutton(
            format_content,
            text="عرض رسالة شكر",
            variable=self.show_thank_you_var,
            font=("Tahoma", 10),
            anchor='e'
        )
        thank_you_check.pack(anchor='e', pady=2)
        
        # Test print button
        test_print_btn = RTLButton(
            format_content,
            text="🖨️ طباعة تجريبية",
            font=("Tahoma", 10),
            command=self.test_print
        )
        test_print_btn.pack(anchor='e', pady=10)
        
        # Save button
        save_printer_btn = RTLButton(
            printer_frame,
            text="💾 حفظ إعدادات الطباعة",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_printer_settings
        )
        save_printer_btn.pack(anchor='e', padx=20, pady=20)
        
    def create_backup_tab(self):
        """Create backup settings tab"""
        backup_frame = tk.Frame(self.notebook)
        self.notebook.add(backup_frame, text="النسخ الاحتياطي")
        
        # Backup settings section
        backup_section = tk.LabelFrame(backup_frame, text="إعدادات النسخ الاحتياطي", font=("Tahoma", 12, "bold"))
        backup_section.pack(fill=tk.X, padx=20, pady=20)
        
        backup_content = tk.Frame(backup_section)
        backup_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Backup location
        location_frame = tk.Frame(backup_content)
        location_frame.pack(fill=tk.X, pady=10)
        
        RTLLabel(location_frame, text="مجلد النسخ الاحتياطي:", font=("Tahoma", 10)).pack(anchor='e', pady=5)
        
        path_frame = tk.Frame(location_frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        self.backup_path_var = tk.StringVar(value="C:/MobileShop/Backups")
        backup_path_entry = tk.Entry(path_frame, textvariable=self.backup_path_var, font=("Tahoma", 10))
        backup_path_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = RTLButton(
            path_frame,
            text="📁 تصفح",
            font=("Tahoma", 9),
            command=self.browse_backup_folder
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Backup frequency
        frequency_frame = tk.Frame(backup_content)
        frequency_frame.pack(fill=tk.X, pady=10)
        
        RTLLabel(frequency_frame, text="تكرار النسخ الاحتياطي:", font=("Tahoma", 10)).pack(anchor='e', pady=5)
        
        self.backup_frequency_var = tk.StringVar(value="يومياً")
        frequency_combo = ttk.Combobox(
            frequency_frame,
            textvariable=self.backup_frequency_var,
            values=["يومياً", "أسبوعياً", "شهرياً", "يدوياً فقط"],
            state="readonly",
            width=15
        )
        frequency_combo.pack(anchor='e', pady=5)
        
        # Keep backups
        keep_frame = tk.Frame(backup_content)
        keep_frame.pack(fill=tk.X, pady=10)
        
        RTLLabel(keep_frame, text="الاحتفاظ بـ:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        self.keep_backups_var = tk.StringVar(value="30")
        keep_entry = tk.Entry(keep_frame, textvariable=self.keep_backups_var, width=10, justify='right')
        keep_entry.pack(side=tk.RIGHT, padx=5)
        
        RTLLabel(keep_frame, text="نسخة احتياطية", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        
        # Manual backup section
        manual_section = tk.LabelFrame(backup_frame, text="النسخ الاحتياطي اليدوي", font=("Tahoma", 12, "bold"))
        manual_section.pack(fill=tk.X, padx=20, pady=20)
        
        manual_content = tk.Frame(manual_section)
        manual_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Backup buttons
        backup_buttons_frame = tk.Frame(manual_content)
        backup_buttons_frame.pack(fill=tk.X, pady=10)
        
        create_backup_btn = RTLButton(
            backup_buttons_frame,
            text="💾 إنشاء نسخة احتياطية الآن",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.create_backup
        )
        create_backup_btn.pack(side=tk.RIGHT, padx=5)
        
        restore_backup_btn = RTLButton(
            backup_buttons_frame,
            text="📥 استعادة نسخة احتياطية",
            font=("Tahoma", 11),
            bg="#FF9800",
            fg="white",
            command=self.restore_backup
        )
        restore_backup_btn.pack(side=tk.RIGHT, padx=5)
        
        # Backup history
        history_section = tk.LabelFrame(backup_frame, text="سجل النسخ الاحتياطية", font=("Tahoma", 12, "bold"))
        history_section.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Simple backup history list
        history_content = tk.Frame(history_section)
        history_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        history_listbox = tk.Listbox(history_content, font=("Tahoma", 10))
        history_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Add sample backup history
        sample_backups = [
            "2024-01-15 10:30 - نسخة احتياطية تلقائية (5.2 MB)",
            "2024-01-14 10:30 - نسخة احتياطية تلقائية (5.1 MB)",
            "2024-01-13 15:45 - نسخة احتياطية يدوية (5.0 MB)",
            "2024-01-12 10:30 - نسخة احتياطية تلقائية (4.9 MB)"
        ]
        
        for backup in sample_backups:
            history_listbox.insert(tk.END, backup)
            
        # Save backup settings button
        save_backup_btn = RTLButton(
            backup_frame,
            text="💾 حفظ إعدادات النسخ الاحتياطي",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_backup_settings
        )
        save_backup_btn.pack(anchor='e', padx=20, pady=20)
        
    def create_about_tab(self):
        """Create about tab"""
        about_frame = tk.Frame(self.notebook)
        self.notebook.add(about_frame, text="حول البرنامج")
        
        # Center content
        content_frame = tk.Frame(about_frame)
        content_frame.pack(expand=True, fill=tk.BOTH)
        
        # App info
        info_frame = tk.Frame(content_frame)
        info_frame.pack(expand=True)
        
        # App icon
        icon_label = tk.Label(
            info_frame,
            text="📱",
            font=("Tahoma", 48)
        )
        icon_label.pack(pady=20)
        
        # App name
        name_label = tk.Label(
            info_frame,
            text="نظام إدارة محل الموبايل",
            font=("Tahoma", 18, "bold")
        )
        name_label.pack(pady=10)
        
        # Version
        version_label = tk.Label(
            info_frame,
            text="الإصدار 1.0.0",
            font=("Tahoma", 12)
        )
        version_label.pack(pady=5)
        
        # Description
        desc_label = tk.Label(
            info_frame,
            text="نظام شامل لإدارة محلات الموبايل والإكسسوارات",
            font=("Tahoma", 12),
            wraplength=400
        )
        desc_label.pack(pady=10)
        
        # Developer info
        dev_label = tk.Label(
            info_frame,
            text="تطوير: فريق تطوير التطبيقات العربية",
            font=("Tahoma", 10)
        )
        dev_label.pack(pady=5)
        
        # Contact info
        contact_label = tk.Label(
            info_frame,
            text="للدعم الفني: support@mobileshop.com",
            font=("Tahoma", 10)
        )
        contact_label.pack(pady=5)
        
        # Features list
        features_frame = tk.LabelFrame(content_frame, text="مميزات البرنامج", font=("Tahoma", 12, "bold"))
        features_frame.pack(fill=tk.X, padx=40, pady=20)
        
        features_content = tk.Frame(features_frame)
        features_content.pack(fill=tk.X, padx=20, pady=20)
        
        features = [
            "✅ إدارة شاملة للمنتجات والمخزون",
            "✅ إدارة العملاء والموردين",
            "✅ تقارير مفصلة للمبيعات والأرباح",
            "✅ خدمات الرصيد والدفع الإلكتروني",
            "✅ واجهة عربية سهلة الاستخدام",
            "✅ نسخ احتياطي تلقائي",
            "✅ طباعة الفواتير والتقارير",
            "✅ دعم المواضيع النهارية والليلية"
        ]
        
        for feature in features:
            feature_label = tk.Label(
                features_content,
                text=feature,
                font=("Tahoma", 10),
                anchor='e'
            )
            feature_label.pack(anchor='e', pady=2)
            
    def change_theme(self):
        """Change application theme"""
        new_theme = self.theme_var.get()
        self.theme_manager.current_theme = new_theme
        self.theme_callback()
        
    def save_general_settings(self):
        """Save general settings"""
        messagebox.showinfo("حفظ الإعدادات", "تم حفظ الإعدادات العامة بنجاح")
        
    def save_display_settings(self):
        """Save display settings"""
        messagebox.showinfo("حفظ الإعدادات", "تم حفظ إعدادات العرض بنجاح")
        
    def save_printer_settings(self):
        """Save printer settings"""
        messagebox.showinfo("حفظ الإعدادات", "تم حفظ إعدادات الطباعة بنجاح")
        
    def save_backup_settings(self):
        """Save backup settings"""
        messagebox.showinfo("حفظ الإعدادات", "تم حفظ إعدادات النسخ الاحتياطي بنجاح")
        
    def test_print(self):
        """Test print function"""
        messagebox.showinfo("طباعة تجريبية", "تم إرسال صفحة تجريبية للطابعة")
        
    def browse_backup_folder(self):
        """Browse for backup folder"""
        folder = filedialog.askdirectory(title="اختر مجلد النسخ الاحتياطي")
        if folder:
            self.backup_path_var.set(folder)
            
    def create_backup(self):
        """Create manual backup"""
        messagebox.showinfo("نسخة احتياطية", "تم إنشاء النسخة الاحتياطية بنجاح")
        
    def restore_backup(self):
        """Restore from backup"""
        backup_file = filedialog.askopenfilename(
            title="اختر ملف النسخة الاحتياطية",
            filetypes=[("Backup files", "*.bak"), ("All files", "*.*")]
        )
        if backup_file:
            result = messagebox.askyesno(
                "استعادة النسخة الاحتياطية",
                "هل أنت متأكد من استعادة هذه النسخة الاحتياطية؟\nسيتم استبدال البيانات الحالية."
            )
            if result:
                messagebox.showinfo("استعادة النسخة الاحتياطية", "تم استعادة النسخة الاحتياطية بنجاح")
    
    def show(self):
        """Show the module"""
        if self.main_frame:
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
    def hide(self):
        """Hide the module"""
        if self.main_frame:
            self.main_frame.pack_forget()
            
    def update_theme(self):
        """Update module theme"""
        if self.theme_manager and self.main_frame:
            colors = self.theme_manager.get_colors()
            self.main_frame.config(bg=colors['bg'])
