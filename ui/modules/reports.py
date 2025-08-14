#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports Module
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import DataTable, FormField, StatsCard, RTLButton, RTLLabel
from arabic_data import ArabicData

class ReportsModule:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.arabic_data = ArabicData()
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the reports interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_sales_reports_tab()
        self.create_inventory_reports_tab()
        self.create_financial_reports_tab()
        self.create_custom_reports_tab()
        
    def create_sales_reports_tab(self):
        """Create sales reports tab"""
        sales_frame = tk.Frame(self.notebook)
        self.notebook.add(sales_frame, text="تقارير المبيعات")
        
        # Controls frame
        controls_frame = tk.Frame(sales_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Date range selection
        date_frame = tk.Frame(controls_frame)
        date_frame.pack(anchor='e', pady=10)
        
        RTLLabel(date_frame, text="من تاريخ:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        self.from_date = tk.Entry(date_frame, font=("Tahoma", 10), width=12, justify='right')
        self.from_date.pack(side=tk.RIGHT, padx=5)
        self.from_date.insert(0, "2024-01-01")
        
        RTLLabel(date_frame, text="إلى تاريخ:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        self.to_date = tk.Entry(date_frame, font=("Tahoma", 10), width=12, justify='right')
        self.to_date.pack(side=tk.RIGHT, padx=5)
        self.to_date.insert(0, "2024-12-31")
        
        generate_btn = RTLButton(
            date_frame,
            text="📊 إنشاء التقرير",
            font=("Tahoma", 10),
            command=self.generate_sales_report
        )
        generate_btn.pack(side=tk.RIGHT, padx=10)
        
        # Stats cards for sales
        stats_frame = tk.Frame(sales_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        sales_stats = [
            ("إجمالي المبيعات", "487,500 ج.م", "💰", "#4CAF50"),
            ("عدد الفواتير", "1,247", "🧾", "#2196F3"),
            ("متوسط الفاتورة", "391 ج.م", "📊", "#FF9800"),
            ("أعلى مبيعات يومية", "15,780 ج.م", "📈", "#9C27B0")
        ]
        
        for title, value, icon, color in sales_stats:
            card = StatsCard(stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Charts frame (mock chart representation)
        charts_frame = tk.LabelFrame(sales_frame, text="الرسوم البيانية", font=("Tahoma", 12, "bold"))
        charts_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Mock chart
        chart_canvas = tk.Canvas(charts_frame, height=200, bg="white")
        chart_canvas.pack(fill=tk.X, padx=10, pady=10)
        
        # Draw a simple mock bar chart
        chart_canvas.create_text(400, 20, text="رسم بياني للمبيعات الشهرية", font=("Tahoma", 14, "bold"), anchor="center")
        
        # Draw bars (mock data)
        months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"]
        values = [30000, 45000, 35000, 50000, 40000, 55000]
        
        bar_width = 80
        max_height = 120
        start_x = 50
        
        for i, (month, value) in enumerate(zip(months, values)):
            x = start_x + i * 120
            height = (value / max(values)) * max_height
            
            # Draw bar
            chart_canvas.create_rectangle(x, 180, x + bar_width, 180 - height, 
                                        fill="#4CAF50", outline="#2E7D32")
            
            # Draw value
            chart_canvas.create_text(x + bar_width/2, 180 - height - 10, 
                                   text=f"{value:,}", font=("Tahoma", 8))
            
            # Draw month label
            chart_canvas.create_text(x + bar_width/2, 190, 
                                   text=month, font=("Tahoma", 9))
            
    def create_inventory_reports_tab(self):
        """Create inventory reports tab"""
        inventory_frame = tk.Frame(self.notebook)
        self.notebook.add(inventory_frame, text="تقارير المخزون")
        
        # Control buttons
        controls_frame = tk.Frame(inventory_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        RTLButton(
            controls_frame,
            text="📦 تقرير المخزون الحالي",
            font=("Tahoma", 10),
            command=self.show_current_inventory
        ).pack(side=tk.RIGHT, padx=5)
        
        RTLButton(
            controls_frame,
            text="⚠️ المنتجات قليلة المخزون",
            font=("Tahoma", 10),
            command=self.show_low_stock
        ).pack(side=tk.RIGHT, padx=5)
        
        RTLButton(
            controls_frame,
            text="📈 حركة المخزون",
            font=("Tahoma", 10),
            command=self.show_stock_movement
        ).pack(side=tk.RIGHT, padx=5)
        
        # Inventory stats
        inv_stats_frame = tk.Frame(inventory_frame)
        inv_stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        inv_stats = [
            ("قيمة المخزون", "125,000 ج.م", "💰", "#4CAF50"),
            ("عدد الأصناف", "247", "📦", "#2196F3"),
            ("منتجات قليلة", "12", "⚠️", "#FF9800"),
            ("منتجات نافدة", "3", "❌", "#F44336")
        ]
        
        for title, value, icon, color in inv_stats:
            card = StatsCard(inv_stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Inventory table
        inventory_columns = {
            'product_name': 'اسم المنتج',
            'category': 'الفئة',
            'current_stock': 'المخزون الحالي',
            'min_stock': 'الحد الأدنى',
            'unit_cost': 'تكلفة الوحدة',
            'total_value': 'القيمة الإجمالية',
            'last_update': 'آخر تحديث',
            'status': 'الحالة'
        }
        
        self.inventory_table = DataTable(inventory_frame, inventory_columns, self.theme_manager)
        self.inventory_table.pack(fill=tk.BOTH, expand=True)
        
        # Load inventory data
        self.load_inventory_report_data()
        
    def create_financial_reports_tab(self):
        """Create financial reports tab"""
        financial_frame = tk.Frame(self.notebook)
        self.notebook.add(financial_frame, text="التقارير المالية")
        
        # Report selection frame
        selection_frame = tk.Frame(financial_frame)
        selection_frame.pack(fill=tk.X, pady=(0, 20))
        
        RTLLabel(
            selection_frame,
            text="نوع التقرير:",
            font=("Tahoma", 12, "bold")
        ).pack(anchor='e', pady=10)
        
        # Report type buttons
        reports_frame = tk.Frame(selection_frame)
        reports_frame.pack(anchor='e', pady=10)
        
        report_buttons = [
            ("📊 تقرير الأرباح والخسائر", self.show_profit_loss),
            ("💰 تقرير التدفقات النقدية", self.show_cash_flow),
            ("📈 تقرير الأداء المالي", self.show_financial_performance),
            ("🧾 تقرير الضرائب", self.show_tax_report)
        ]
        
        for text, command in report_buttons:
            RTLButton(
                reports_frame,
                text=text,
                font=("Tahoma", 10),
                command=command
            ).pack(side=tk.RIGHT, padx=5)
            
        # Financial summary
        summary_frame = tk.LabelFrame(financial_frame, text="الملخص المالي", font=("Tahoma", 12, "bold"))
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        summary_stats_frame = tk.Frame(summary_frame)
        summary_stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        financial_stats = [
            ("إجمالي الإيرادات", "487,500 ج.م", "💰", "#4CAF50"),
            ("إجمالي التكاليف", "312,000 ج.م", "💸", "#FF5722"),
            ("صافي الربح", "175,500 ج.م", "📈", "#2196F3"),
            ("هامش الربح", "36%", "📊", "#9C27B0")
        ]
        
        for title, value, icon, color in financial_stats:
            card = StatsCard(summary_stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Financial details table
        financial_columns = {
            'period': 'الفترة',
            'revenue': 'الإيرادات',
            'costs': 'التكاليف',
            'profit': 'الربح',
            'margin': 'هامش الربح',
            'expenses': 'المصروفات',
            'net_profit': 'صافي الربح'
        }
        
        self.financial_table = DataTable(financial_frame, financial_columns, self.theme_manager)
        self.financial_table.pack(fill=tk.BOTH, expand=True)
        
        # Load financial data
        self.load_financial_report_data()
        
    def create_custom_reports_tab(self):
        """Create custom reports tab"""
        custom_frame = tk.Frame(self.notebook)
        self.notebook.add(custom_frame, text="تقارير مخصصة")
        
        # Report builder frame
        builder_frame = tk.LabelFrame(custom_frame, text="منشئ التقارير", font=("Tahoma", 12, "bold"))
        builder_frame.pack(fill=tk.X, pady=(0, 20))
        
        builder_content = tk.Frame(builder_frame)
        builder_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Report parameters
        params_frame = tk.Frame(builder_content)
        params_frame.pack(fill=tk.X, pady=10)
        
        # Right side parameters
        right_params = tk.Frame(params_frame)
        right_params.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Left side parameters
        left_params = tk.Frame(params_frame)
        left_params.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Data source
        RTLLabel(right_params, text="مصدر البيانات:", font=("Tahoma", 10)).pack(anchor='e')
        data_source = ttk.Combobox(
            right_params,
            values=["المبيعات", "المخزون", "العملاء", "الموردين", "الخدمات"],
            state="readonly",
            font=("Tahoma", 10)
        )
        data_source.pack(fill=tk.X, pady=(0, 10))
        
        # Report type
        RTLLabel(right_params, text="نوع التقرير:", font=("Tahoma", 10)).pack(anchor='e')
        report_type = ttk.Combobox(
            right_params,
            values=["جدول", "رسم بياني", "إحصائيات", "مقارنة"],
            state="readonly",
            font=("Tahoma", 10)
        )
        report_type.pack(fill=tk.X, pady=(0, 10))
        
        # Time period
        RTLLabel(left_params, text="الفترة الزمنية:", font=("Tahoma", 10)).pack(anchor='e')
        time_period = ttk.Combobox(
            left_params,
            values=["اليوم", "هذا الأسبوع", "هذا الشهر", "هذا العام", "مخصص"],
            state="readonly",
            font=("Tahoma", 10)
        )
        time_period.pack(fill=tk.X, pady=(0, 10))
        
        # Grouping
        RTLLabel(left_params, text="التجميع حسب:", font=("Tahoma", 10)).pack(anchor='e')
        grouping = ttk.Combobox(
            left_params,
            values=["يوم", "أسبوع", "شهر", "فئة المنتج", "العميل"],
            state="readonly",
            font=("Tahoma", 10)
        )
        grouping.pack(fill=tk.X, pady=(0, 10))
        
        # Generate button
        generate_custom_btn = RTLButton(
            builder_content,
            text="📊 إنشاء التقرير المخصص",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.generate_custom_report
        )
        generate_custom_btn.pack(anchor='e', pady=20)
        
        # Saved reports frame
        saved_frame = tk.LabelFrame(custom_frame, text="التقارير المحفوظة", font=("Tahoma", 12, "bold"))
        saved_frame.pack(fill=tk.BOTH, expand=True)
        
        # Saved reports table
        saved_columns = {
            'name': 'اسم التقرير',
            'type': 'النوع',
            'created_date': 'تاريخ الإنشاء',
            'last_run': 'آخر تشغيل',
            'description': 'الوصف'
        }
        
        self.saved_reports_table = DataTable(saved_frame, saved_columns, self.theme_manager)
        self.saved_reports_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load saved reports
        self.load_saved_reports()
        
    def generate_sales_report(self):
        """Generate sales report"""
        messagebox.showinfo("تقرير المبيعات", "تم إنشاء تقرير المبيعات بنجاح")
        
    def show_current_inventory(self):
        """Show current inventory report"""
        messagebox.showinfo("تقرير المخزون", "عرض تقرير المخزون الحالي")
        
    def show_low_stock(self):
        """Show low stock items"""
        messagebox.showinfo("المنتجات قليلة المخزون", "عرض المنتجات التي تحتاج إعادة تموين")
        
    def show_stock_movement(self):
        """Show stock movement report"""
        messagebox.showinfo("حركة المخزون", "عرض تقرير حركة المخزون")
        
    def show_profit_loss(self):
        """Show profit and loss report"""
        messagebox.showinfo("الأرباح والخسائر", "عرض تقرير الأرباح والخسائر")
        
    def show_cash_flow(self):
        """Show cash flow report"""
        messagebox.showinfo("التدفقات النقدية", "عرض تقرير التدفقات النقدية")
        
    def show_financial_performance(self):
        """Show financial performance report"""
        messagebox.showinfo("الأداء المالي", "عرض تقرير الأداء المالي")
        
    def show_tax_report(self):
        """Show tax report"""
        messagebox.showinfo("تقرير الضرائب", "عرض تقرير الضرائب")
        
    def generate_custom_report(self):
        """Generate custom report"""
        messagebox.showinfo("التقرير المخصص", "تم إنشاء التقرير المخصص بنجاح")
        
    def load_inventory_report_data(self):
        """Load inventory report data"""
        inventory_data = self.arabic_data.get_inventory_report_data()
        
        for item in inventory_data:
            self.inventory_table.add_row([
                item['product_name'],
                item['category'],
                item['current_stock'],
                item['min_stock'],
                f"{item['unit_cost']} ج.م",
                f"{item['total_value']} ج.م",
                item['last_update'],
                item['status']
            ])
            
    def load_financial_report_data(self):
        """Load financial report data"""
        financial_data = self.arabic_data.get_financial_report_data()
        
        for period in financial_data:
            self.financial_table.add_row([
                period['period'],
                f"{period['revenue']} ج.م",
                f"{period['costs']} ج.م",
                f"{period['profit']} ج.م",
                f"{period['margin']}%",
                f"{period['expenses']} ج.م",
                f"{period['net_profit']} ج.م"
            ])
            
    def load_saved_reports(self):
        """Load saved reports"""
        saved_reports = self.arabic_data.get_saved_reports()
        
        for report in saved_reports:
            self.saved_reports_table.add_row([
                report['name'],
                report['type'],
                report['created_date'],
                report['last_run'],
                report['description']
            ])
    
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
