#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products Management Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import DataTable, FormField, StatsCard, RTLButton, RTLLabel
from arabic_data import ArabicData

class ProductsModule:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.arabic_data = ArabicData()
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the products management interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_products_tab()
        self.create_inventory_tab()
        self.create_add_product_tab()
        
    def create_products_tab(self):
        """Create products list tab"""
        products_frame = tk.Frame(self.notebook)
        self.notebook.add(products_frame, text="قائمة المنتجات")
        
        # Stats cards frame
        stats_frame = tk.Frame(products_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create stats cards
        stats = [
            ("إجمالي المنتجات", "247", "📦", "#4CAF50"),
            ("منتجات قليلة", "12", "⚠️", "#FF9800"),
            ("نفدت من المخزن", "3", "❌", "#F44336"),
            ("قيمة المخزون", "125,000 ج.م", "💰", "#2196F3")
        ]
        
        for i, (title, value, icon, color) in enumerate(stats):
            card = StatsCard(stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Action buttons frame
        actions_frame = tk.Frame(products_frame)
        actions_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons
        btn_add = RTLButton(
            actions_frame,
            text="➕ إضافة منتج جديد",
            font=("Tahoma", 10),
            command=self.add_product
        )
        btn_add.pack(side=tk.RIGHT, padx=5)
        
        btn_import = RTLButton(
            actions_frame,
            text="📋 استيراد من ملف",
            font=("Tahoma", 10),
            command=self.import_products
        )
        btn_import.pack(side=tk.RIGHT, padx=5)
        
        btn_export = RTLButton(
            actions_frame,
            text="💾 تصدير البيانات",
            font=("Tahoma", 10),
            command=self.export_products
        )
        btn_export.pack(side=tk.RIGHT, padx=5)
        
        # Products table
        columns = {
            'barcode': 'الباركود',
            'name': 'اسم المنتج',
            'category': 'الفئة',
            'buy_price': 'سعر الشراء',
            'sell_price': 'سعر البيع',
            'profit': 'الربح',
            'stock': 'الكمية',
            'status': 'الحالة'
        }
        
        self.products_table = DataTable(products_frame, columns, self.theme_manager)
        self.products_table.pack(fill=tk.BOTH, expand=True)
        
        # Load sample data
        self.load_sample_products()
        
    def create_inventory_tab(self):
        """Create inventory management tab"""
        inventory_frame = tk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="إدارة المخزون")
        
        # Low stock alert frame
        alert_frame = tk.Frame(inventory_frame, bg="#FFF3CD", relief=tk.RAISED, borderwidth=1)
        alert_frame.pack(fill=tk.X, pady=(0, 20), padx=10, ipady=10)
        
        alert_icon = tk.Label(
            alert_frame,
            text="⚠️",
            font=("Tahoma", 16),
            bg="#FFF3CD"
        )
        alert_icon.pack(side=tk.RIGHT, padx=10)
        
        alert_text = RTLLabel(
            alert_frame,
            text="تحذير: يوجد 12 منتج تحتاج إلى إعادة تموين",
            font=("Tahoma", 12, "bold"),
            bg="#FFF3CD",
            fg="#856404"
        )
        alert_text.pack(side=tk.RIGHT, padx=10)
        
        # Inventory table
        inventory_columns = {
            'name': 'اسم المنتج',
            'current_stock': 'الكمية الحالية',
            'min_stock': 'الحد الأدنى',
            'max_stock': 'الحد الأقصى',
            'last_restock': 'آخر تموين',
            'supplier': 'المورد',
            'action': 'الإجراء'
        }
        
        self.inventory_table = DataTable(inventory_frame, inventory_columns, self.theme_manager)
        self.inventory_table.pack(fill=tk.BOTH, expand=True)
        
        # Load inventory data
        self.load_inventory_data()
        
    def create_add_product_tab(self):
        """Create add/edit product tab"""
        add_frame = tk.Frame(self.notebook)
        self.notebook.add(add_frame, text="إضافة/تعديل منتج")
        
        # Create scrollable frame
        canvas = tk.Canvas(add_frame)
        scrollbar = ttk.Scrollbar(add_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form frame
        form_frame = tk.Frame(scrollable_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Product information section
        info_section = tk.LabelFrame(form_frame, text="معلومات المنتج", font=("Tahoma", 12, "bold"))
        info_section.pack(fill=tk.X, pady=(0, 20))
        
        # Create form fields
        self.form_fields = {}
        
        # Two column layout
        left_frame = tk.Frame(info_section)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        right_frame = tk.Frame(info_section)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Right column fields
        self.form_fields['name'] = FormField(right_frame, "اسم المنتج *:")
        self.form_fields['name'].pack(fill=tk.X, pady=5)
        
        self.form_fields['barcode'] = FormField(right_frame, "الباركود:")
        self.form_fields['barcode'].pack(fill=tk.X, pady=5)
        
        self.form_fields['category'] = FormField(
            right_frame, 
            "الفئة *:", 
            'combobox',
            values=["موبايلات", "إكسسوارات", "شواحن", "شاشات حماية", "أخرى"]
        )
        self.form_fields['category'].pack(fill=tk.X, pady=5)
        
        self.form_fields['brand'] = FormField(right_frame, "الماركة:")
        self.form_fields['brand'].pack(fill=tk.X, pady=5)
        
        # Left column fields
        self.form_fields['buy_price'] = FormField(left_frame, "سعر الشراء:")
        self.form_fields['buy_price'].pack(fill=tk.X, pady=5)
        
        self.form_fields['sell_price'] = FormField(left_frame, "سعر البيع:")
        self.form_fields['sell_price'].pack(fill=tk.X, pady=5)
        
        self.form_fields['min_stock'] = FormField(left_frame, "الحد الأدنى للمخزون:")
        self.form_fields['min_stock'].pack(fill=tk.X, pady=5)
        
        self.form_fields['current_stock'] = FormField(left_frame, "الكمية الحالية:")
        self.form_fields['current_stock'].pack(fill=tk.X, pady=5)
        
        # Description section
        desc_section = tk.LabelFrame(form_frame, text="الوصف والملاحظات", font=("Tahoma", 12, "bold"))
        desc_section.pack(fill=tk.X, pady=(0, 20))
        
        self.form_fields['description'] = FormField(desc_section, "الوصف:", 'text')
        self.form_fields['description'].pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        save_btn = RTLButton(
            buttons_frame,
            text="💾 حفظ المنتج",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.save_product
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_btn = RTLButton(
            buttons_frame,
            text="🔄 مسح البيانات",
            font=("Tahoma", 11),
            command=self.clear_form
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Pack canvas and scrollbar
        canvas.pack(side="right", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def load_sample_products(self):
        """Load sample products data"""
        products_data = self.arabic_data.get_sample_products()
        
        for product in products_data:
            self.products_table.add_row([
                product['barcode'],
                product['name'],
                product['category'],
                f"{product['buy_price']} ج.م",
                f"{product['sell_price']} ج.م",
                f"{product['profit']} ج.م",
                product['stock'],
                product['status']
            ])
            
    def load_inventory_data(self):
        """Load inventory data"""
        inventory_data = self.arabic_data.get_inventory_data()
        
        for item in inventory_data:
            self.inventory_table.add_row([
                item['name'],
                item['current_stock'],
                item['min_stock'],
                item['max_stock'],
                item['last_restock'],
                item['supplier'],
                "إعادة تموين" if item['current_stock'] <= item['min_stock'] else "متوفر"
            ])
    
    def add_product(self):
        """Switch to add product tab"""
        self.notebook.select(2)  # Select add product tab
        
    def import_products(self):
        """Import products from file"""
        messagebox.showinfo("استيراد المنتجات", "سيتم تطبيق وظيفة استيراد المنتجات من ملف Excel/CSV")
        
    def export_products(self):
        """Export products to file"""
        messagebox.showinfo("تصدير المنتجات", "سيتم تطبيق وظيفة تصدير المنتجات إلى ملف Excel/CSV")
        
    def save_product(self):
        """Save product data"""
        # Validate required fields
        if not self.form_fields['name'].get_value():
            messagebox.showerror("خطأ", "يجب إدخال اسم المنتج")
            return
            
        if not self.form_fields['category'].get_value():
            messagebox.showerror("خطأ", "يجب اختيار فئة المنتج")
            return
            
        messagebox.showinfo("نجح الحفظ", "تم حفظ بيانات المنتج بنجاح")
        self.clear_form()
        
    def clear_form(self):
        """Clear form fields"""
        for field in self.form_fields.values():
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
