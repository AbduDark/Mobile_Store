#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Suppliers Module - Supplier Management Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QLabel, QFrame, QHeaderView,
    QAbstractItemView, QDialog, QMessageBox, QSplitter,
    QComboBox, QDateEdit, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

from .base_module import BaseModule
from ..widgets.data_table import EnhancedTableWidget

class SuppliersModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "الموردين")
        
    def setup_ui(self):
        """Setup suppliers module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Suppliers list tab
        self.suppliers_tab = self.create_suppliers_tab()
        self.tab_widget.addTab(self.suppliers_tab, "🏪 قائمة الموردين")
        
        # Orders tab
        self.orders_tab = self.create_orders_tab()
        self.tab_widget.addTab(self.orders_tab, "📋 الطلبات")
        
        # Payments tab
        self.payments_tab = self.create_payments_tab()
        self.tab_widget.addTab(self.payments_tab, "💰 المدفوعات")
        
        layout.addWidget(self.tab_widget)
        
    def create_suppliers_tab(self) -> QWidget:
        """Create suppliers management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # Search and filters
        filters = self.create_filters()
        layout.addWidget(filters)
        
        # Main content with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Suppliers table
        self.suppliers_table = self.create_suppliers_table()
        splitter.addWidget(self.suppliers_table)
        
        # Supplier details panel
        details_panel = self.create_details_panel()
        splitter.addWidget(details_panel)
        
        splitter.setSizes([800, 300])
        layout.addWidget(splitter)
        
        return tab
        
    def create_suppliers_table(self) -> EnhancedTableWidget:
        """Create suppliers table"""
        columns = [
            ("ID", 50, False),
            ("اسم المورد", 180, True),
            ("الشركة", 150, True),
            ("الهاتف", 120, True),
            ("البريد الإلكتروني", 180, True),
            ("إجمالي الطلبات", 120, True),
            ("الرصيد المستحق", 120, True),
            ("تاريخ التسجيل", 120, True)
        ]
        
        table = EnhancedTableWidget(columns)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.itemSelectionChanged.connect(self.on_selection_changed)
        
        return table
        
    def create_toolbar(self) -> QFrame:
        """Create suppliers toolbar"""
        toolbar = QFrame()
        layout = QHBoxLayout(toolbar)
        
        self.add_btn = QPushButton("➕ إضافة مورد")
        self.add_btn.setObjectName("primary_button")
        
        self.edit_btn = QPushButton("✏️ تعديل")
        self.edit_btn.setObjectName("secondary_button")
        self.edit_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("🗑️ حذف")
        self.delete_btn.setObjectName("danger_button")
        self.delete_btn.setEnabled(False)
        
        self.orders_btn = QPushButton("📋 الطلبات")
        self.orders_btn.setObjectName("secondary_button")
        self.orders_btn.setEnabled(False)
        
        self.payment_btn = QPushButton("💰 دفع")
        self.payment_btn.setObjectName("success_button")
        self.payment_btn.setEnabled(False)
        
        layout.addWidget(self.payment_btn)
        layout.addWidget(self.orders_btn)
        layout.addStretch()
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.add_btn)
        
        return toolbar
        
    def create_filters(self) -> QFrame:
        """Create search filters"""
        filters_frame = QFrame()
        layout = QHBoxLayout(filters_frame)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("البحث في الموردين...")
        
        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "جميع الموردين",
            "موردين نشطين",
            "موردين معلقين",
            "لديهم مستحقات"
        ])
        
        self.results_label = QLabel("0 مورد")
        
        layout.addWidget(self.results_label)
        layout.addStretch()
        layout.addWidget(self.status_filter)
        layout.addWidget(self.search_input)
        
        return filters_frame
        
    def create_details_panel(self) -> QFrame:
        """Create supplier details panel"""
        panel = QFrame()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        title = QLabel("بيانات المورد")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Basic info
        info_group = QGroupBox("المعلومات الأساسية")
        info_layout = QFormLayout(info_group)
        
        self.detail_labels = {
            'name': QLabel("-"),
            'company': QLabel("-"),
            'phone': QLabel("-"),
            'email': QLabel("-"),
            'address': QLabel("-")
        }
        
        for field, label in self.detail_labels.items():
            info_layout.addRow(f"{field}:", label)
            
        layout.addWidget(info_group)
        
        # Financial info
        financial_group = QGroupBox("المعلومات المالية")
        financial_layout = QFormLayout(financial_group)
        
        self.financial_labels = {
            'total_orders': QLabel("-"),
            'outstanding_balance': QLabel("-"),
            'payment_terms': QLabel("-"),
            'last_order': QLabel("-")
        }
        
        financial_layout.addRow("إجمالي الطلبات:", self.financial_labels['total_orders'])
        financial_layout.addRow("الرصيد المستحق:", self.financial_labels['outstanding_balance'])
        financial_layout.addRow("شروط الدفع:", self.financial_labels['payment_terms'])
        financial_layout.addRow("آخر طلب:", self.financial_labels['last_order'])
        
        layout.addWidget(financial_group)
        layout.addStretch()
        
        return panel
        
    def create_orders_tab(self) -> QWidget:
        """Create orders management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Orders toolbar
        orders_toolbar = QHBoxLayout()
        
        new_order_btn = QPushButton("➕ طلب جديد")
        new_order_btn.setObjectName("primary_button")
        
        receive_order_btn = QPushButton("📦 استلام طلب")
        receive_order_btn.setObjectName("success_button")
        
        cancel_order_btn = QPushButton("❌ إلغاء طلب")
        cancel_order_btn.setObjectName("danger_button")
        
        orders_toolbar.addWidget(cancel_order_btn)
        orders_toolbar.addWidget(receive_order_btn)
        orders_toolbar.addStretch()
        orders_toolbar.addWidget(new_order_btn)
        
        layout.addLayout(orders_toolbar)
        
        # Orders table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(8)
        self.orders_table.setHorizontalHeaderLabels([
            "رقم الطلب", "المورد", "تاريخ الطلب", "تاريخ التوقع",
            "المبلغ", "الحالة", "المدفوع", "المتبقي"
        ])
        
        layout.addWidget(self.orders_table)
        
        return tab
        
    def create_payments_tab(self) -> QWidget:
        """Create payments management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Payment form
        payment_form = QGroupBox("تسجيل دفعة جديدة")
        form_layout = QFormLayout(payment_form)
        
        self.supplier_combo = QComboBox()
        form_layout.addRow("المورد:", self.supplier_combo)
        
        self.payment_amount = QDoubleSpinBox()
        self.payment_amount.setMaximum(999999.99)
        self.payment_amount.setSuffix(" ريال")
        form_layout.addRow("المبلغ:", self.payment_amount)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems(["نقداً", "بنك", "شيك", "تحويل"])
        form_layout.addRow("طريقة الدفع:", self.payment_method)
        
        self.payment_notes = QTextEdit()
        self.payment_notes.setMaximumHeight(60)
        form_layout.addRow("ملاحظات:", self.payment_notes)
        
        record_payment_btn = QPushButton("💰 تسجيل الدفعة")
        record_payment_btn.setObjectName("primary_button")
        form_layout.addRow("", record_payment_btn)
        
        layout.addWidget(payment_form)
        
        # Payments history
        history_group = QGroupBox("سجل المدفوعات")
        history_layout = QVBoxLayout(history_group)
        
        self.payments_table = QTableWidget()
        self.payments_table.setColumnCount(6)
        self.payments_table.setHorizontalHeaderLabels([
            "التاريخ", "المورد", "المبلغ", "طريقة الدفع", "ملاحظات", "المستخدم"
        ])
        
        history_layout.addWidget(self.payments_table)
        layout.addWidget(history_group)
        
        return tab
        
    def load_data(self):
        """Load suppliers data"""
        try:
            # Load suppliers from database
            suppliers = []  # self.db_manager.get_suppliers()
            self.populate_suppliers_table(suppliers)
            
        except Exception as e:
            print(f"Error loading suppliers data: {e}")
            
    def populate_suppliers_table(self, suppliers):
        """Populate suppliers table"""
        self.suppliers_table.setRowCount(len(suppliers))
        
        for row, supplier in enumerate(suppliers):
            self.suppliers_table.setItem(row, 0, QTableWidgetItem(str(supplier.get('id', ''))))
            self.suppliers_table.setItem(row, 1, QTableWidgetItem(supplier.get('name', '')))
            self.suppliers_table.setItem(row, 2, QTableWidgetItem(supplier.get('company', '')))
            self.suppliers_table.setItem(row, 3, QTableWidgetItem(supplier.get('phone', '')))
            self.suppliers_table.setItem(row, 4, QTableWidgetItem(supplier.get('email', '')))
            
            total_orders = f"{supplier.get('total_orders', 0):,.2f} ريال"
            self.suppliers_table.setItem(row, 5, QTableWidgetItem(total_orders))
            
            balance = f"{supplier.get('outstanding_balance', 0):,.2f} ريال"
            self.suppliers_table.setItem(row, 6, QTableWidgetItem(balance))
            
            created_date = supplier.get('created_at', '')[:10] if supplier.get('created_at') else '-'
            self.suppliers_table.setItem(row, 7, QTableWidgetItem(created_date))
            
        self.results_label.setText(f"{len(suppliers)} مورد")
        
    def on_selection_changed(self):
        """Handle selection changes"""
        current_row = self.suppliers_table.currentRow()
        has_selection = current_row >= 0
        
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.orders_btn.setEnabled(has_selection)
        self.payment_btn.setEnabled(has_selection)
        
        if has_selection:
            self.update_details_panel(current_row)
        else:
            self.clear_details_panel()
            
    def update_details_panel(self, row):
        """Update supplier details panel"""
        try:
            name = self.suppliers_table.item(row, 1).text()
            company = self.suppliers_table.item(row, 2).text()
            phone = self.suppliers_table.item(row, 3).text()
            email = self.suppliers_table.item(row, 4).text()
            
            self.detail_labels['name'].setText(name)
            self.detail_labels['company'].setText(company)
            self.detail_labels['phone'].setText(phone)
            self.detail_labels['email'].setText(email)
            
        except Exception as e:
            print(f"Error updating supplier details: {e}")
            
    def clear_details_panel(self):
        """Clear details panel"""
        for label in self.detail_labels.values():
            label.setText("-")
        for label in self.financial_labels.values():
            label.setText("-")