#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suppliers Management Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import DataTable, FormField, StatsCard, RTLButton, RTLLabel
from arabic_data import ArabicData

class SuppliersModule:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.arabic_data = ArabicData()
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the suppliers management interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_suppliers_tab()
        self.create_add_supplier_tab()
        self.create_invoices_tab()
        
    def create_suppliers_tab(self):
        """Create suppliers list tab"""
        suppliers_frame = tk.Frame(self.notebook)
        self.notebook.add(suppliers_frame, text="قائمة الموردين")
        
        # Stats cards frame
        stats_frame = tk.Frame(suppliers_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stats cards
        stats = [
            ("إجمالي الموردين", "23", "🏪", "#4CAF50"),
            ("فواتير مدفوعة", "156", "✅", "#2196F3"),
            ("فواتير آجلة", "12", "⏳", "#FF9800"),
            ("إجمالي المديونيات", "45,000 ج.م", "💰", "#F44336")
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            card = StatsCard(stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Action buttons frame
        actions_frame = tk.Frame(suppliers_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_add = RTLButton(
            actions_frame,
            text="➕ إضافة مورد جديد",
            font=("Tahoma", 10),
            command=self.add_supplier
        )
        btn_add.pack(side=tk.RIGHT, padx=5)
        
        btn_payment = RTLButton(
            actions_frame,
            text="💳 تسجيل دفعة",
            font=("Tahoma", 10),
            command=self.record_payment
        )
        btn_payment.pack(side=tk.RIGHT, padx=5)
        
        btn_statement = RTLButton(
            actions_frame,
            text="📋 كشف حساب",
            font=("Tahoma", 10),
            command=self.show_statement
        )
        btn_statement.pack(side=tk.RIGHT, padx=5)
        
        # Suppliers table
        columns = {
            'id': 'رقم المورد',
            'name': 'اسم المورد',
            'contact_person': 'الشخص المسؤول',
            'phone': 'رقم الهاتف',
            'address': 'العنوان',
            'total_purchases': 'إجمالي المشتريات',
            'outstanding_balance': 'الرصيد المستحق',
            'status': 'الحالة'
        }
        
        self.suppliers_table = DataTable(suppliers_frame, columns, self.theme_manager)
        self.suppliers_table.pack(fill=tk.BOTH, expand=True)
        
        # Load sample data
        self.load_sample_suppliers()
        
    def create_add_supplier_tab(self):
        """Create add/edit supplier tab"""
        add_frame = tk.Frame(self.notebook)
        self.notebook.add(add_frame, text="إضافة/تعديل مورد")
        
        # Form container
        form_container = tk.Frame(add_frame)
        form_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Title
        title_label = RTLLabel(
            form_container,
            text="بيانات المورد",
            font=("Tahoma", 16, "bold")
        )
        title_label.pack(anchor='e', pady=(0, 20))
        
        # Form sections
        # Company Information
        company_section = tk.LabelFrame(form_container, text="بيانات الشركة", font=("Tahoma", 12, "bold"))
        company_section.pack(fill=tk.X, pady=(0, 20))
        
        company_frame = tk.Frame(company_section)
        company_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Two columns for company info
        company_right = tk.Frame(company_frame)
        company_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        company_left = tk.Frame(company_frame)
        company_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Create form fields
        self.supplier_fields = {}
        
        # Company information fields
        self.supplier_fields['company_name'] = FormField(company_right, "اسم الشركة *:")
        self.supplier_fields['company_name'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['tax_number'] = FormField(company_right, "الرقم الضريبي:")
        self.supplier_fields['tax_number'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['commercial_register'] = FormField(company_left, "السجل التجاري:")
        self.supplier_fields['commercial_register'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['business_type'] = FormField(
            company_left,
            "نوع النشاط:",
            'combobox',
            values=["تجارة جملة", "تجارة تجزئة", "استيراد", "تصنيع", "خدمات"]
        )
        self.supplier_fields['business_type'].pack(fill=tk.X, pady=5)
        
        # Contact Information
        contact_section = tk.LabelFrame(form_container, text="بيانات الاتصال", font=("Tahoma", 12, "bold"))
        contact_section.pack(fill=tk.X, pady=(0, 20))
        
        contact_frame = tk.Frame(contact_section)
        contact_frame.pack(fill=tk.X, padx=10, pady=10)
        
        contact_right = tk.Frame(contact_frame)
        contact_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        contact_left = tk.Frame(contact_frame)
        contact_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Contact fields
        self.supplier_fields['contact_person'] = FormField(contact_right, "الشخص المسؤول *:")
        self.supplier_fields['contact_person'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['phone'] = FormField(contact_right, "رقم الهاتف *:")
        self.supplier_fields['phone'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['mobile'] = FormField(contact_right, "رقم الموبايل:")
        self.supplier_fields['mobile'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['email'] = FormField(contact_left, "البريد الإلكتروني:")
        self.supplier_fields['email'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['website'] = FormField(contact_left, "الموقع الإلكتروني:")
        self.supplier_fields['website'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['address'] = FormField(contact_left, "العنوان:", 'text')
        self.supplier_fields['address'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Payment Terms
        payment_section = tk.LabelFrame(form_container, text="شروط الدفع", font=("Tahoma", 12, "bold"))
        payment_section.pack(fill=tk.X, pady=(0, 20))
        
        payment_frame = tk.Frame(payment_section)
        payment_frame.pack(fill=tk.X, padx=10, pady=10)
        
        payment_right = tk.Frame(payment_frame)
        payment_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        payment_left = tk.Frame(payment_frame)
        payment_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.supplier_fields['payment_terms'] = FormField(
            payment_right,
            "شروط الدفع:",
            'combobox',
            values=["نقداً", "آجل 15 يوم", "آجل 30 يوم", "آجل 45 يوم", "آجل 60 يوم"]
        )
        self.supplier_fields['payment_terms'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['credit_limit'] = FormField(payment_right, "حد الائتمان:")
        self.supplier_fields['credit_limit'].pack(fill=tk.X, pady=5)
        
        self.supplier_fields['notes'] = FormField(payment_left, "ملاحظات:", 'text')
        self.supplier_fields['notes'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_container)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        save_btn = RTLButton(
            buttons_frame,
            text="💾 حفظ المورد",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_supplier
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_btn = RTLButton(
            buttons_frame,
            text="🔄 مسح البيانات",
            font=("Tahoma", 11),
            command=self.clear_supplier_form
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
    def create_invoices_tab(self):
        """Create supplier invoices tab"""
        invoices_frame = tk.Frame(self.notebook)
        self.notebook.add(invoices_frame, text="الفواتير والمدفوعات")
        
        # Filter frame
        filter_frame = tk.Frame(invoices_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Supplier selection
        RTLLabel(
            filter_frame,
            text="المورد:",
            font=("Tahoma", 10)
        ).pack(side=tk.RIGHT, padx=5)
        
        self.supplier_filter = ttk.Combobox(
            filter_frame,
            font=("Tahoma", 10),
            state="readonly",
            width=25
        )
        self.supplier_filter.pack(side=tk.RIGHT, padx=10)
        
        # Status filter
        RTLLabel(
            filter_frame,
            text="الحالة:",
            font=("Tahoma", 10)
        ).pack(side=tk.RIGHT, padx=5)
        
        self.status_filter = ttk.Combobox(
            filter_frame,
            font=("Tahoma", 10),
            state="readonly",
            values=["جميع الفواتير", "مدفوعة", "آجلة", "متأخرة"],
            width=15
        )
        self.status_filter.pack(side=tk.RIGHT, padx=10)
        self.status_filter.set("جميع الفواتير")
        
        filter_btn = RTLButton(
            filter_frame,
            text="🔍 تصفية",
            font=("Tahoma", 10),
            command=self.filter_invoices
        )
        filter_btn.pack(side=tk.RIGHT, padx=10)
        
        # Invoices table
        invoices_columns = {
            'invoice_no': 'رقم الفاتورة',
            'supplier': 'المورد',
            'date': 'التاريخ',
            'due_date': 'تاريخ الاستحقاق',
            'total': 'المبلغ الإجمالي',
            'paid': 'المبلغ المدفوع',
            'remaining': 'المبلغ المتبقي',
            'status': 'الحالة'
        }
        
        self.invoices_table = DataTable(invoices_frame, invoices_columns, self.theme_manager)
        self.invoices_table.pack(fill=tk.BOTH, expand=True)
        
        # Load invoice data
        self.load_invoice_data()
        
    def load_sample_suppliers(self):
        """Load sample suppliers data"""
        suppliers_data = self.arabic_data.get_sample_suppliers()
        
        for supplier in suppliers_data:
            self.suppliers_table.add_row([
                supplier['id'],
                supplier['name'],
                supplier['contact_person'],
                supplier['phone'],
                supplier['address'],
                f"{supplier['total_purchases']} ج.م",
                f"{supplier['outstanding_balance']} ج.م",
                supplier['status']
            ])
            
    def load_invoice_data(self):
        """Load invoice data"""
        invoice_data = self.arabic_data.get_supplier_invoices()
        
        for invoice in invoice_data:
            self.invoices_table.add_row([
                invoice['invoice_no'],
                invoice['supplier'],
                invoice['date'],
                invoice['due_date'],
                f"{invoice['total']} ج.م",
                f"{invoice['paid']} ج.م",
                f"{invoice['remaining']} ج.م",
                invoice['status']
            ])
            
    def filter_invoices(self):
        """Filter invoices based on selection"""
        messagebox.showinfo("تصفية الفواتير", "سيتم تطبيق تصفية الفواتير حسب المورد والحالة")
        
    def add_supplier(self):
        """Switch to add supplier tab"""
        self.notebook.select(1)  # Select add supplier tab
        
    def record_payment(self):
        """Record supplier payment"""
        messagebox.showinfo("تسجيل دفعة", "سيتم تطبيق وظيفة تسجيل دفعة للمورد")
        
    def show_statement(self):
        """Show supplier statement"""
        messagebox.showinfo("كشف حساب", "سيتم تطبيق وظيفة عرض كشف حساب المورد")
        
    def save_supplier(self):
        """Save supplier data"""
        # Validate required fields
        if not self.supplier_fields['company_name'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال اسم الشركة")
            return
            
        if not self.supplier_fields['contact_person'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال اسم الشخص المسؤول")
            return
            
        if not self.supplier_fields['phone'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال رقم الهاتف")
            return
            
        messagebox.showinfo("نجح الحفظ", "تم حفظ بيانات المورد بنجاح")
        self.clear_supplier_form()
        
    def clear_supplier_form(self):
        """Clear supplier form fields"""
        for field in self.supplier_fields.values():
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
