#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reports Module - Reporting and Analytics Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QLabel, QFrame, QHeaderView,
    QAbstractItemView, QDialog, QMessageBox, QSplitter,
    QComboBox, QDateEdit, QDoubleSpinBox, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .base_module import BaseModule

class ReportsModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "التقارير")
        
    def setup_ui(self):
        """Setup reports module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Sales reports tab
        self.sales_tab = self.create_sales_tab()
        self.tab_widget.addTab(self.sales_tab, "📊 تقارير المبيعات")
        
        # Inventory reports tab
        self.inventory_tab = self.create_inventory_tab()
        self.tab_widget.addTab(self.inventory_tab, "📦 تقارير المخزون")
        
        # Financial reports tab
        self.financial_tab = self.create_financial_tab()
        self.tab_widget.addTab(self.financial_tab, "💰 التقارير المالية")
        
        # Customer reports tab
        self.customer_tab = self.create_customer_tab()
        self.tab_widget.addTab(self.customer_tab, "👥 تقارير العملاء")
        
        layout.addWidget(self.tab_widget)
        
    def create_sales_tab(self) -> QWidget:
        """Create sales reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Date range selector
        date_frame = QFrame()
        date_layout = QHBoxLayout(date_frame)
        
        date_layout.addWidget(QLabel("من تاريخ:"))
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        date_layout.addWidget(self.start_date)
        
        date_layout.addWidget(QLabel("إلى تاريخ:"))
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        date_layout.addWidget(self.end_date)
        
        # Quick date buttons
        quick_dates = [
            ("اليوم", 0),
            ("أسبوع", 7),
            ("شهر", 30),
            ("3 أشهر", 90)
        ]
        
        for text, days in quick_dates:
            btn = QPushButton(text)
            btn.setObjectName("secondary_button")
            btn.clicked.connect(lambda checked, d=days: self.set_quick_date(d))
            date_layout.addWidget(btn)
            
        generate_btn = QPushButton("📊 إنشاء التقرير")
        generate_btn.setObjectName("primary_button")
        generate_btn.clicked.connect(self.generate_sales_report)
        date_layout.addWidget(generate_btn)
        
        date_layout.addStretch()
        layout.addWidget(date_frame)
        
        # Summary cards
        summary_frame = self.create_sales_summary()
        layout.addWidget(summary_frame)
        
        # Sales chart
        self.sales_chart = self.create_sales_chart()
        layout.addWidget(self.sales_chart)
        
        # Detailed sales table
        details_group = QGroupBox("تفاصيل المبيعات")
        details_layout = QVBoxLayout(details_group)
        
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "رقم الفاتورة", "التاريخ", "العميل", "المبلغ",
            "الخصم", "الضريبة", "طريقة الدفع"
        ])
        
        details_layout.addWidget(self.sales_table)
        layout.addWidget(details_group)
        
        return tab
        
    def create_sales_summary(self) -> QFrame:
        """Create sales summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        # Summary statistics
        cards = [
            ("إجمالي المبيعات", "0 ريال", "#27AE60"),
            ("عدد الفواتير", "0", "#3498DB"),
            ("متوسط الفاتورة", "0 ريال", "#F39C12"),
            ("إجمالي الضريبة", "0 ريال", "#E74C3C")
        ]
        
        self.sales_summary_labels = {}
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            layout.addWidget(card)
            
        return frame
        
    def create_summary_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a summary statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #E1E8ED;
                border-left: 4px solid {color};
                border-radius: 6px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 10pt; color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        self.sales_summary_labels[title] = value_label
        
        return card
        
    def create_sales_chart(self) -> QFrame:
        """Create sales chart widget"""
        chart_frame = QFrame()
        layout = QVBoxLayout(chart_frame)
        
        # Create matplotlib figure
        self.sales_figure = Figure(figsize=(12, 6))
        self.sales_canvas = FigureCanvas(self.sales_figure)
        
        layout.addWidget(self.sales_canvas)
        
        return chart_frame
        
    def create_inventory_tab(self) -> QWidget:
        """Create inventory reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Report type selector
        type_frame = QFrame()
        type_layout = QHBoxLayout(type_frame)
        
        type_layout.addWidget(QLabel("نوع التقرير:"))
        
        self.inventory_type = QComboBox()
        self.inventory_type.addItems([
            "تقرير المخزون الحالي",
            "المنتجات منخفضة المخزون",
            "المنتجات غير المتوفرة",
            "أعلى المنتجات مبيعاً",
            "أقل المنتجات مبيعاً"
        ])
        type_layout.addWidget(self.inventory_type)
        
        generate_inventory_btn = QPushButton("📦 إنشاء التقرير")
        generate_inventory_btn.setObjectName("primary_button")
        generate_inventory_btn.clicked.connect(self.generate_inventory_report)
        type_layout.addWidget(generate_inventory_btn)
        
        type_layout.addStretch()
        layout.addWidget(type_frame)
        
        # Inventory summary
        inventory_summary = self.create_inventory_summary()
        layout.addWidget(inventory_summary)
        
        # Inventory chart
        self.inventory_chart = self.create_inventory_chart()
        layout.addWidget(self.inventory_chart)
        
        # Inventory table
        inventory_group = QGroupBox("تفاصيل المخزون")
        inventory_layout = QVBoxLayout(inventory_group)
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(6)
        self.inventory_table.setHorizontalHeaderLabels([
            "المنتج", "الفئة", "المخزون الحالي", "الحد الأدنى",
            "قيمة المخزون", "الحالة"
        ])
        
        inventory_layout.addWidget(self.inventory_table)
        layout.addWidget(inventory_group)
        
        return tab
        
    def create_inventory_summary(self) -> QFrame:
        """Create inventory summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        cards = [
            ("إجمالي المنتجات", "0", "#3498DB"),
            ("قيمة المخزون", "0 ريال", "#27AE60"),
            ("مخزون منخفض", "0", "#F39C12"),
            ("غير متوفر", "0", "#E74C3C")
        ]
        
        self.inventory_summary_labels = {}
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            layout.addWidget(card)
            
        return frame
        
    def create_inventory_chart(self) -> QFrame:
        """Create inventory chart"""
        chart_frame = QFrame()
        layout = QVBoxLayout(chart_frame)
        
        self.inventory_figure = Figure(figsize=(12, 6))
        self.inventory_canvas = FigureCanvas(self.inventory_figure)
        
        layout.addWidget(self.inventory_canvas)
        
        return chart_frame
        
    def create_financial_tab(self) -> QWidget:
        """Create financial reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Financial period selector
        period_frame = QFrame()
        period_layout = QHBoxLayout(period_frame)
        
        period_layout.addWidget(QLabel("الفترة المالية:"))
        
        self.financial_period = QComboBox()
        self.financial_period.addItems([
            "الشهر الحالي",
            "الربع الحالي", 
            "النصف الأول",
            "النصف الثاني",
            "السنة الحالية",
            "فترة مخصصة"
        ])
        period_layout.addWidget(self.financial_period)
        
        generate_financial_btn = QPushButton("💰 إنشاء التقرير")
        generate_financial_btn.setObjectName("primary_button")
        generate_financial_btn.clicked.connect(self.generate_financial_report)
        period_layout.addWidget(generate_financial_btn)
        
        period_layout.addStretch()
        layout.addWidget(period_frame)
        
        # Financial summary
        financial_summary = self.create_financial_summary()
        layout.addWidget(financial_summary)
        
        # Profit/Loss chart
        self.financial_chart = self.create_financial_chart()
        layout.addWidget(self.financial_chart)
        
        # Financial details table
        financial_group = QGroupBox("التفاصيل المالية")
        financial_layout = QVBoxLayout(financial_group)
        
        self.financial_table = QTableWidget()
        self.financial_table.setColumnCount(5)
        self.financial_table.setHorizontalHeaderLabels([
            "البند", "الإيرادات", "التكاليف", "الربح", "الهامش %"
        ])
        
        financial_layout.addWidget(self.financial_table)
        layout.addWidget(financial_group)
        
        return tab
        
    def create_financial_summary(self) -> QFrame:
        """Create financial summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        cards = [
            ("الإيرادات", "0 ريال", "#27AE60"),
            ("التكاليف", "0 ريال", "#E74C3C"),
            ("الربح الإجمالي", "0 ريال", "#3498DB"),
            ("هامش الربح", "0%", "#F39C12")
        ]
        
        self.financial_summary_labels = {}
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            layout.addWidget(card)
            
        return frame
        
    def create_financial_chart(self) -> QFrame:
        """Create financial chart"""
        chart_frame = QFrame()
        layout = QVBoxLayout(chart_frame)
        
        self.financial_figure = Figure(figsize=(12, 6))
        self.financial_canvas = FigureCanvas(self.financial_figure)
        
        layout.addWidget(self.financial_canvas)
        
        return chart_frame
        
    def create_customer_tab(self) -> QWidget:
        """Create customer reports tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Customer analysis toolbar
        analysis_frame = QFrame()
        analysis_layout = QHBoxLayout(analysis_frame)
        
        analysis_layout.addWidget(QLabel("تحليل العملاء:"))
        
        self.customer_analysis = QComboBox()
        self.customer_analysis.addItems([
            "أفضل العملاء",
            "العملاء الجدد",
            "العملاء النشطين",
            "العملاء غير النشطين",
            "تحليل نقاط الولاء"
        ])
        analysis_layout.addWidget(self.customer_analysis)
        
        generate_customer_btn = QPushButton("👥 إنشاء التقرير")
        generate_customer_btn.setObjectName("primary_button")
        generate_customer_btn.clicked.connect(self.generate_customer_report)
        analysis_layout.addWidget(generate_customer_btn)
        
        analysis_layout.addStretch()
        layout.addWidget(analysis_frame)
        
        # Customer summary
        customer_summary = self.create_customer_summary()
        layout.addWidget(customer_summary)
        
        # Customer chart
        self.customer_chart = self.create_customer_chart()
        layout.addWidget(self.customer_chart)
        
        # Customer details table
        customer_group = QGroupBox("تفاصيل العملاء")
        customer_layout = QVBoxLayout(customer_group)
        
        self.customer_table = QTableWidget()
        self.customer_table.setColumnCount(6)
        self.customer_table.setHorizontalHeaderLabels([
            "العميل", "عدد المشتريات", "إجمالي المشتريات",
            "نقاط الولاء", "آخر شراء", "الحالة"
        ])
        
        customer_layout.addWidget(self.customer_table)
        layout.addWidget(customer_group)
        
        return tab
        
    def create_customer_summary(self) -> QFrame:
        """Create customer summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        cards = [
            ("إجمالي العملاء", "0", "#3498DB"),
            ("عملاء جدد", "0", "#27AE60"),
            ("عملاء نشطين", "0", "#F39C12"),
            ("متوسط الشراء", "0 ريال", "#9B59B6")
        ]
        
        self.customer_summary_labels = {}
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            layout.addWidget(card)
            
        return frame
        
    def create_customer_chart(self) -> QFrame:
        """Create customer chart"""
        chart_frame = QFrame()
        layout = QVBoxLayout(chart_frame)
        
        self.customer_figure = Figure(figsize=(12, 6))
        self.customer_canvas = FigureCanvas(self.customer_figure)
        
        layout.addWidget(self.customer_canvas)
        
        return chart_frame
        
    def load_data(self):
        """Load reports data"""
        # Load initial data for all reports
        self.generate_sales_report()
        self.generate_inventory_report()
        self.generate_financial_report()
        self.generate_customer_report()
        
    def set_quick_date(self, days_back: int):
        """Set quick date range"""
        end_date = QDate.currentDate()
        start_date = end_date.addDays(-days_back)
        
        self.start_date.setDate(start_date)
        self.end_date.setDate(end_date)
        
    def generate_sales_report(self):
        """Generate sales report"""
        try:
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
            
            # Load sales data
            sales = self.db_manager.get_sales_report(start_date, end_date)
            
            # Update summary
            total_sales = sum(s['total_amount'] for s in sales)
            total_invoices = len(sales)
            avg_invoice = total_sales / total_invoices if total_invoices > 0 else 0
            total_tax = sum(s['tax_amount'] for s in sales)
            
            if "إجمالي المبيعات" in self.sales_summary_labels:
                self.sales_summary_labels["إجمالي المبيعات"].setText(f"{total_sales:,.2f} ريال")
            if "عدد الفواتير" in self.sales_summary_labels:
                self.sales_summary_labels["عدد الفواتير"].setText(str(total_invoices))
            if "متوسط الفاتورة" in self.sales_summary_labels:
                self.sales_summary_labels["متوسط الفاتورة"].setText(f"{avg_invoice:,.2f} ريال")
            if "إجمالي الضريبة" in self.sales_summary_labels:
                self.sales_summary_labels["إجمالي الضريبة"].setText(f"{total_tax:,.2f} ريال")
                
            # Update table
            self.populate_sales_table(sales)
            
            # Update chart
            self.update_sales_chart(sales)
            
        except Exception as e:
            print(f"Error generating sales report: {e}")
            
    def populate_sales_table(self, sales):
        """Populate sales table"""
        self.sales_table.setRowCount(len(sales))
        
        for row, sale in enumerate(sales):
            self.sales_table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['created_at'][:10]))
            self.sales_table.setItem(row, 2, QTableWidgetItem(sale.get('customer_name', 'غير محدد')))
            self.sales_table.setItem(row, 3, QTableWidgetItem(f"{sale['total_amount']:,.2f}"))
            self.sales_table.setItem(row, 4, QTableWidgetItem(f"{sale['discount_amount']:,.2f}"))
            self.sales_table.setItem(row, 5, QTableWidgetItem(f"{sale['tax_amount']:,.2f}"))
            self.sales_table.setItem(row, 6, QTableWidgetItem(sale.get('payment_method', '-')))
            
    def update_sales_chart(self, sales):
        """Update sales chart"""
        self.sales_figure.clear()
        
        if not sales:
            return
            
        # Group sales by date
        daily_sales = {}
        for sale in sales:
            date = sale['created_at'][:10]
            daily_sales[date] = daily_sales.get(date, 0) + sale['total_amount']
            
        # Create chart
        ax = self.sales_figure.add_subplot(111)
        dates = list(daily_sales.keys())
        amounts = list(daily_sales.values())
        
        ax.plot(dates, amounts, marker='o', linewidth=2, markersize=6)
        ax.set_title('المبيعات اليومية', fontsize=14, fontweight='bold')
        ax.set_xlabel('التاريخ')
        ax.set_ylabel('المبلغ (ريال)')
        ax.grid(True, alpha=0.3)
        
        # Format dates on x-axis
        ax.tick_params(axis='x', rotation=45)
        
        self.sales_figure.tight_layout()
        self.sales_canvas.draw()
        
    def generate_inventory_report(self):
        """Generate inventory report"""
        try:
            # Load inventory data
            products = self.db_manager.get_products()
            
            # Update summary
            total_products = len(products)
            total_value = sum(p['price'] * p['stock_quantity'] for p in products if p['price'] and p['stock_quantity'])
            low_stock = len([p for p in products if p['stock_quantity'] <= p['min_stock_level']])
            out_of_stock = len([p for p in products if p['stock_quantity'] == 0])
            
            if "إجمالي المنتجات" in self.inventory_summary_labels:
                self.inventory_summary_labels["إجمالي المنتجات"].setText(str(total_products))
            if "قيمة المخزون" in self.inventory_summary_labels:
                self.inventory_summary_labels["قيمة المخزون"].setText(f"{total_value:,.2f} ريال")
            if "مخزون منخفض" in self.inventory_summary_labels:
                self.inventory_summary_labels["مخزون منخفض"].setText(str(low_stock))
            if "غير متوفر" in self.inventory_summary_labels:
                self.inventory_summary_labels["غير متوفر"].setText(str(out_of_stock))
                
            # Update inventory chart
            self.update_inventory_chart(products)
            
        except Exception as e:
            print(f"Error generating inventory report: {e}")
            
    def update_inventory_chart(self, products):
        """Update inventory chart"""
        self.inventory_figure.clear()
        
        if not products:
            return
            
        # Create stock status pie chart
        ax = self.inventory_figure.add_subplot(111)
        
        in_stock = len([p for p in products if p['stock_quantity'] > p['min_stock_level']])
        low_stock = len([p for p in products if 0 < p['stock_quantity'] <= p['min_stock_level']])
        out_of_stock = len([p for p in products if p['stock_quantity'] == 0])
        
        labels = ['متوفر', 'مخزون منخفض', 'غير متوفر']
        sizes = [in_stock, low_stock, out_of_stock]
        colors = ['#27AE60', '#F39C12', '#E74C3C']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title('حالة المخزون', fontsize=14, fontweight='bold')
        
        self.inventory_figure.tight_layout()
        self.inventory_canvas.draw()
        
    def generate_financial_report(self):
        """Generate financial report"""
        # Placeholder for financial report generation
        pass
        
    def generate_customer_report(self):
        """Generate customer report"""
        # Placeholder for customer report generation
        pass