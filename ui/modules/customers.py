#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers Management Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import DataTable, FormField, StatsCard, RTLButton, RTLLabel
from arabic_data import ArabicData

class CustomersModule:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.arabic_data = ArabicData()
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the customers management interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_customers_tab()
        self.create_add_customer_tab()
        self.create_customer_history_tab()
        
    def create_customers_tab(self):
        """Create customers list tab"""
        customers_frame = tk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="قائمة العملاء")
        
        # Stats cards frame
        stats_frame = tk.Frame(customers_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stats cards
        stats = [
            ("إجمالي العملاء", "1,247", "👥", "#4CAF50"),
            ("عملاء نشطين", "892", "✅", "#2196F3"),
            ("عملاء جدد هذا الشهر", "47", "🆕", "#FF9800"),
            ("إجمالي المبيعات", "487,500 ج.م", "💰", "#9C27B0")
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            card = StatsCard(stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Action buttons frame
        actions_frame = tk.Frame(customers_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_add = RTLButton(
            actions_frame,
            text="➕ إضافة عميل جديد",
            font=("Tahoma", 10),
            command=self.add_customer
        )
        btn_add.pack(side=tk.RIGHT, padx=5)
        
        btn_send_sms = RTLButton(
            actions_frame,
            text="📱 إرسال رسائل",
            font=("Tahoma", 10),
            command=self.send_sms
        )
        btn_send_sms.pack(side=tk.RIGHT, padx=5)
        
        btn_export = RTLButton(
            actions_frame,
            text="💾 تصدير العملاء",
            font=("Tahoma", 10),
            command=self.export_customers
        )
        btn_export.pack(side=tk.RIGHT, padx=5)
        
        # Customers table
        columns = {
            'id': 'رقم العميل',
            'name': 'الاسم',
            'phone': 'رقم الهاتف',
            'email': 'البريد الإلكتروني',
            'address': 'العنوان',
            'total_purchases': 'إجمالي المشتريات',
            'last_visit': 'آخر زيارة',
            'status': 'الحالة'
        }
        
        self.customers_table = DataTable(customers_frame, columns, self.theme_manager)
        self.customers_table.pack(fill=tk.BOTH, expand=True)
        
        # Load sample data
        self.load_sample_customers()
        
    def create_add_customer_tab(self):
        """Create add/edit customer tab"""
        add_frame = tk.Frame(self.notebook)
        self.notebook.add(add_frame, text="إضافة/تعديل عميل")
        
        # Form container
        form_container = tk.Frame(add_frame)
        form_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title_label = RTLLabel(
            form_container,
            text="بيانات العميل",
            font=("Tahoma", 16, "bold")
        )
        title_label.pack(anchor='e', pady=(0, 20))
        
        # Form frame with two columns
        form_frame = tk.Frame(form_container)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Right column
        right_frame = tk.Frame(form_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Left column
        left_frame = tk.Frame(form_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Create form fields
        self.customer_fields = {}
        
        # Right column fields
        self.customer_fields['name'] = FormField(right_frame, "الاسم الكامل *:")
        self.customer_fields['name'].pack(fill=tk.X, pady=5)
        
        self.customer_fields['phone'] = FormField(right_frame, "رقم الهاتف *:")
        self.customer_fields['phone'].pack(fill=tk.X, pady=5)
        
        self.customer_fields['email'] = FormField(right_frame, "البريد الإلكتروني:")
        self.customer_fields['email'].pack(fill=tk.X, pady=5)
        
        self.customer_fields['national_id'] = FormField(right_frame, "الرقم القومي:")
        self.customer_fields['national_id'].pack(fill=tk.X, pady=5)
        
        # Left column fields
        self.customer_fields['address'] = FormField(left_frame, "العنوان:", 'text')
        self.customer_fields['address'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.customer_fields['notes'] = FormField(left_frame, "ملاحظات:", 'text')
        self.customer_fields['notes'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_container)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        save_btn = RTLButton(
            buttons_frame,
            text="💾 حفظ العميل",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_customer
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_btn = RTLButton(
            buttons_frame,
            text="🔄 مسح البيانات",
            font=("Tahoma", 11),
            command=self.clear_customer_form
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_customer_history_tab(self):
        """Create customer purchase history tab"""
        history_frame = tk.Frame(self.notebook)
        self.notebook.add(history_frame, text="تاريخ المشتريات")
        
        # Customer selection frame
        selection_frame = tk.Frame(history_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        RTLLabel(
            selection_frame,
            text="اختر العميل:",
            font=("Tahoma", 12)
        ).pack(side=tk.RIGHT, padx=10)
        
        self.customer_combo = ttk.Combobox(
            selection_frame,
            font=("Tahoma", 10),
            state="readonly",
            width=30
        )
        self.customer_combo.pack(side=tk.RIGHT, padx=10)
        
        # Load customer names
        customer_names = self.arabic_data.get_customer_names()
        self.customer_combo['values'] = customer_names
        
        search_btn = RTLButton(
            selection_frame,
            text="🔍 عرض التاريخ",
            font=("Tahoma", 10),
            command=self.load_customer_history
        )
        search_btn.pack(side=tk.RIGHT, padx=10)
        
        # Purchase history table
        history_columns = {
            'date': 'التاريخ',
            'invoice_no': 'رقم الفاتورة',
            'items': 'المنتجات',
            'total': 'الإجمالي',
            'payment_method': 'طريقة الدفع',
            'status': 'الحالة'
        }
        
        self.history_table = DataTable(history_frame, history_columns, self.theme_manager)
        self.history_table.pack(fill=tk.BOTH, expand=True)
        
    def load_sample_customers(self):
        """Load sample customers data"""
        customers_data = self.arabic_data.get_sample_customers()
        
        for customer in customers_data:
            self.customers_table.add_row([
                customer['id'],
                customer['name'],
                customer['phone'],
                customer['email'],
                customer['address'],
                f"{customer['total_purchases']} ج.م",
                customer['last_visit'],
                customer['status']
            ])
            
    def load_customer_history(self):
        """Load customer purchase history"""
        selected_customer = self.customer_combo.get()
        if not selected_customer:
            messagebox.showwarning("تحذير", "يجب اختيار عميل أولاً")
            return
            
        # Clear current history
        self.history_table.clear_table()
        
        # Load history data
        history_data = self.arabic_data.get_customer_history()
        
        for record in history_data:
            self.history_table.add_row([
                record['date'],
                record['invoice_no'],
                record['items'],
                f"{record['total']} ج.م",
                record['payment_method'],
                record['status']
            ])
            
    def add_customer(self):
        """Switch to add customer tab"""
        self.notebook.select(1)  # Select add customer tab
        
    def send_sms(self):
        """Send SMS to customers"""
        messagebox.showinfo("إرسال رسائل", "سيتم تطبيق وظيفة إرسال الرسائل القصيرة للعملاء")
        
    def export_customers(self):
        """Export customers to file"""
        messagebox.showinfo("تصدير العملاء", "سيتم تطبيق وظيفة تصدير بيانات العملاء")
        
    def save_customer(self):
        """Save customer data"""
        # Validate required fields
        if not self.customer_fields['name'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال اسم العميل")
            return
            
        if not self.customer_fields['phone'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال رقم الهاتف")
            return
            
        messagebox.showinfo("نجح الحفظ", "تم حفظ بيانات العميل بنجاح")
        self.clear_customer_form()
        
    def clear_customer_form(self):
        """Clear customer form fields"""
        for field in self.customer_fields.values():
            field.set_value("")
    
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
