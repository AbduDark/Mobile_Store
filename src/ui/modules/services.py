#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Services Module - Mobile and Payment Services Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QLabel, QFrame, QHeaderView,
    QAbstractItemView, QDialog, QMessageBox, QSplitter,
    QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate, QTimer
from PyQt6.QtGui import QFont

from .base_module import BaseModule

class ServicesModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "الخدمات")
        
    def setup_ui(self):
        """Setup services module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Mobile recharge tab
        self.recharge_tab = self.create_recharge_tab()
        self.tab_widget.addTab(self.recharge_tab, "📱 شحن الجوال")
        
        # Payment services tab
        self.payment_tab = self.create_payment_tab()
        self.tab_widget.addTab(self.payment_tab, "💳 خدمات الدفع")
        
        # Services history tab
        self.history_tab = self.create_history_tab()
        self.tab_widget.addTab(self.history_tab, "📋 سجل الخدمات")
        
        layout.addWidget(self.tab_widget)
        
    def create_recharge_tab(self) -> QWidget:
        """Create mobile recharge services tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Recharge form
        recharge_form = self.create_recharge_form()
        layout.addWidget(recharge_form)
        
        # Quick recharge buttons
        quick_frame = self.create_quick_recharge()
        layout.addWidget(quick_frame)
        
        # Recent transactions
        recent_group = QGroupBox("آخر العمليات")
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_recharge_table = QTableWidget()
        self.recent_recharge_table.setColumnCount(6)
        self.recent_recharge_table.setHorizontalHeaderLabels([
            "الوقت", "رقم الجوال", "الشبكة", "المبلغ", "العمولة", "الحالة"
        ])
        self.recent_recharge_table.setMaximumHeight(200)
        
        recent_layout.addWidget(self.recent_recharge_table)
        layout.addWidget(recent_group)
        
        return tab
        
    def create_recharge_form(self) -> QGroupBox:
        """Create mobile recharge form"""
        group = QGroupBox("شحن رصيد الجوال")
        layout = QFormLayout(group)
        
        # Mobile number input
        self.mobile_input = QLineEdit()
        self.mobile_input.setPlaceholderText("05xxxxxxxx")
        self.mobile_input.setMaxLength(10)
        layout.addRow("رقم الجوال:", self.mobile_input)
        
        # Network selection
        self.network_combo = QComboBox()
        self.network_combo.addItems([
            "-- اختر الشبكة --",
            "STC - الاتصالات السعودية",
            "Mobily - موبايلي", 
            "Zain - زين",
            "Virgin - فيرجن"
        ])
        layout.addRow("الشبكة:", self.network_combo)
        
        # Amount input
        self.amount_input = QComboBox()
        self.amount_input.setEditable(True)
        self.amount_input.addItems([
            "10", "20", "30", "50", "100", "200", "500"
        ])
        layout.addRow("مبلغ الشحن (ريال):", self.amount_input)
        
        # Customer selection
        self.customer_combo = QComboBox()
        self.customer_combo.addItem("-- عميل جديد --", 0)
        layout.addRow("العميل:", self.customer_combo)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.recharge_btn = QPushButton("📱 تنفيذ الشحن")
        self.recharge_btn.setObjectName("primary_button")
        self.recharge_btn.clicked.connect(self.process_recharge)
        
        self.check_balance_btn = QPushButton("💰 فحص الرصيد")
        self.check_balance_btn.setObjectName("secondary_button")
        self.check_balance_btn.clicked.connect(self.check_balance)
        
        button_layout.addWidget(self.check_balance_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.recharge_btn)
        
        layout.addRow("", button_layout)
        
        return group
        
    def create_quick_recharge(self) -> QFrame:
        """Create quick recharge buttons"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        title = QLabel("شحن سريع")
        title.setStyleSheet("font-size: 12pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Quick buttons grid
        buttons_layout = QHBoxLayout()
        
        amounts = [10, 20, 30, 50, 100]
        for amount in amounts:
            btn = QPushButton(f"{amount} ريال")
            btn.setObjectName("secondary_button")
            btn.clicked.connect(lambda checked, a=amount: self.quick_recharge(a))
            buttons_layout.addWidget(btn)
            
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        return frame
        
    def create_payment_tab(self) -> QWidget:
        """Create payment services tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Payment services grid
        services_frame = self.create_payment_services()
        layout.addWidget(services_frame)
        
        # Bill payment form
        bill_form = self.create_bill_payment_form()
        layout.addWidget(bill_form)
        
        # Recent payments
        recent_payments = QGroupBox("آخر المدفوعات")
        payments_layout = QVBoxLayout(recent_payments)
        
        self.recent_payments_table = QTableWidget()
        self.recent_payments_table.setColumnCount(6)
        self.recent_payments_table.setHorizontalHeaderLabels([
            "الوقت", "نوع الخدمة", "رقم الحساب", "المبلغ", "العمولة", "الحالة"
        ])
        self.recent_payments_table.setMaximumHeight(200)
        
        payments_layout.addWidget(self.recent_payments_table)
        layout.addWidget(recent_payments)
        
        return tab
        
    def create_payment_services(self) -> QFrame:
        """Create payment services grid"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        title = QLabel("خدمات الدفع المتاحة")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Services grid
        services_layout = QHBoxLayout()
        
        services = [
            ("💡 فواتير الكهرباء", "electricity"),
            ("💧 فواتير المياه", "water"),
            ("📞 فواتير الاتصالات", "telecom"),
            ("🏠 فواتير الغاز", "gas"),
            ("🌐 فواتير الإنترنت", "internet")
        ]
        
        for service_name, service_id in services:
            btn = QPushButton(service_name)
            btn.setObjectName("secondary_button")
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda checked, sid=service_id: self.select_payment_service(sid))
            services_layout.addWidget(btn)
            
        layout.addLayout(services_layout)
        
        return frame
        
    def create_bill_payment_form(self) -> QGroupBox:
        """Create bill payment form"""
        group = QGroupBox("دفع الفواتير")
        layout = QFormLayout(group)
        
        # Service type
        self.payment_service_combo = QComboBox()
        self.payment_service_combo.addItems([
            "-- اختر نوع الخدمة --",
            "فواتير الكهرباء - SEC",
            "فواتير المياه - NWC",
            "فواتير الاتصالات - STC",
            "فواتير الغاز - NGC",
            "فواتير الإنترنت - ISP"
        ])
        layout.addRow("نوع الخدمة:", self.payment_service_combo)
        
        # Account number
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("رقم الحساب أو العداد")
        layout.addRow("رقم الحساب:", self.account_input)
        
        # Amount
        self.payment_amount = QDoubleSpinBox()
        self.payment_amount.setMaximum(99999.99)
        self.payment_amount.setSuffix(" ريال")
        layout.addRow("المبلغ:", self.payment_amount)
        
        # Customer
        self.payment_customer = QComboBox()
        self.payment_customer.addItem("-- عميل جديد --", 0)
        layout.addRow("العميل:", self.payment_customer)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.inquiry_btn = QPushButton("🔍 استعلام")
        self.inquiry_btn.setObjectName("secondary_button")
        self.inquiry_btn.clicked.connect(self.inquiry_bill)
        
        self.pay_btn = QPushButton("💳 دفع")
        self.pay_btn.setObjectName("primary_button")
        self.pay_btn.clicked.connect(self.process_payment)
        
        button_layout.addWidget(self.inquiry_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.pay_btn)
        
        layout.addRow("", button_layout)
        
        return group
        
    def create_history_tab(self) -> QWidget:
        """Create services history tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Filter controls
        filter_frame = QFrame()
        filter_layout = QHBoxLayout(filter_frame)
        
        filter_layout.addWidget(QLabel("نوع الخدمة:"))
        
        self.history_service_filter = QComboBox()
        self.history_service_filter.addItems([
            "جميع الخدمات",
            "شحن الجوال",
            "فواتير الكهرباء",
            "فواتير المياه",
            "فواتير الاتصالات"
        ])
        filter_layout.addWidget(self.history_service_filter)
        
        filter_layout.addWidget(QLabel("من تاريخ:"))
        
        self.history_start_date = QDateEdit()
        self.history_start_date.setDate(QDate.currentDate().addDays(-30))
        self.history_start_date.setCalendarPopup(True)
        filter_layout.addWidget(self.history_start_date)
        
        filter_layout.addWidget(QLabel("إلى تاريخ:"))
        
        self.history_end_date = QDateEdit()
        self.history_end_date.setDate(QDate.currentDate())
        self.history_end_date.setCalendarPopup(True)
        filter_layout.addWidget(self.history_end_date)
        
        search_btn = QPushButton("🔍 بحث")
        search_btn.setObjectName("primary_button")
        search_btn.clicked.connect(self.search_history)
        filter_layout.addWidget(search_btn)
        
        filter_layout.addStretch()
        layout.addWidget(filter_frame)
        
        # Summary cards
        summary_frame = self.create_services_summary()
        layout.addWidget(summary_frame)
        
        # History table
        history_group = QGroupBox("سجل الخدمات")
        history_layout = QVBoxLayout(history_group)
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(8)
        self.history_table.setHorizontalHeaderLabels([
            "التاريخ", "نوع الخدمة", "رقم الحساب", "العميل", 
            "المبلغ", "العمولة", "الحالة", "المرجع"
        ])
        
        history_layout.addWidget(self.history_table)
        layout.addWidget(history_group)
        
        return tab
        
    def create_services_summary(self) -> QFrame:
        """Create services summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        cards = [
            ("إجمالي العمليات", "0", "#3498DB"),
            ("إجمالي المبالغ", "0 ريال", "#27AE60"),
            ("إجمالي العمولات", "0 ريال", "#F39C12"),
            ("العمليات اليوم", "0", "#9B59B6")
        ]
        
        self.services_summary_labels = {}
        
        for title, value, color in cards:
            card = self.create_summary_card(title, value, color)
            layout.addWidget(card)
            
        return frame
        
    def create_summary_card(self, title: str, value: str, color: str) -> QFrame:
        """Create summary card"""
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
        value_label.setStyleSheet(f"font-size: 18pt; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 9pt; color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        self.services_summary_labels[title] = value_label
        
        return card
        
    def load_data(self):
        """Load services data"""
        try:
            # Load recent recharge transactions
            self.load_recent_recharge()
            
            # Load recent payments
            self.load_recent_payments()
            
            # Load customers for combos
            self.load_customers()
            
            # Update summary
            self.update_services_summary()
            
        except Exception as e:
            print(f"Error loading services data: {e}")
            
    def load_recent_recharge(self):
        """Load recent recharge transactions"""
        # Sample data - would come from database
        recharge_data = []
        
        self.recent_recharge_table.setRowCount(len(recharge_data))
        for row, transaction in enumerate(recharge_data):
            self.recent_recharge_table.setItem(row, 0, QTableWidgetItem(transaction.get('time', '')))
            self.recent_recharge_table.setItem(row, 1, QTableWidgetItem(transaction.get('mobile', '')))
            self.recent_recharge_table.setItem(row, 2, QTableWidgetItem(transaction.get('network', '')))
            self.recent_recharge_table.setItem(row, 3, QTableWidgetItem(f"{transaction.get('amount', 0)} ريال"))
            self.recent_recharge_table.setItem(row, 4, QTableWidgetItem(f"{transaction.get('commission', 0)} ريال"))
            self.recent_recharge_table.setItem(row, 5, QTableWidgetItem(transaction.get('status', '')))
            
    def load_recent_payments(self):
        """Load recent payment transactions"""
        # Sample data - would come from database
        payment_data = []
        
        self.recent_payments_table.setRowCount(len(payment_data))
        for row, payment in enumerate(payment_data):
            self.recent_payments_table.setItem(row, 0, QTableWidgetItem(payment.get('time', '')))
            self.recent_payments_table.setItem(row, 1, QTableWidgetItem(payment.get('service', '')))
            self.recent_payments_table.setItem(row, 2, QTableWidgetItem(payment.get('account', '')))
            self.recent_payments_table.setItem(row, 3, QTableWidgetItem(f"{payment.get('amount', 0)} ريال"))
            self.recent_payments_table.setItem(row, 4, QTableWidgetItem(f"{payment.get('commission', 0)} ريال"))
            self.recent_payments_table.setItem(row, 5, QTableWidgetItem(payment.get('status', '')))
            
    def load_customers(self):
        """Load customers for combo boxes"""
        try:
            customers = self.db_manager.get_customers()
            
            for combo in [self.customer_combo, self.payment_customer]:
                combo.clear()
                combo.addItem("-- عميل جديد --", 0)
                
                for customer in customers:
                    combo.addItem(
                        f"{customer['name']} ({customer['phone']})",
                        customer['id']
                    )
                    
        except Exception as e:
            print(f"Error loading customers: {e}")
            
    def update_services_summary(self):
        """Update services summary"""
        # Sample calculations - would come from database
        total_transactions = 0
        total_amount = 0.0
        total_commission = 0.0
        today_transactions = 0
        
        if "إجمالي العمليات" in self.services_summary_labels:
            self.services_summary_labels["إجمالي العمليات"].setText(str(total_transactions))
        if "إجمالي المبالغ" in self.services_summary_labels:
            self.services_summary_labels["إجمالي المبالغ"].setText(f"{total_amount:,.2f} ريال")
        if "إجمالي العمولات" in self.services_summary_labels:
            self.services_summary_labels["إجمالي العمولات"].setText(f"{total_commission:,.2f} ريال")
        if "العمليات اليوم" in self.services_summary_labels:
            self.services_summary_labels["العمليات اليوم"].setText(str(today_transactions))
            
    def quick_recharge(self, amount: int):
        """Quick recharge with predefined amount"""
        self.amount_input.setCurrentText(str(amount))
        
    def process_recharge(self):
        """Process mobile recharge"""
        mobile = self.mobile_input.text().strip()
        network = self.network_combo.currentText()
        amount = self.amount_input.currentText()
        customer_id = self.customer_combo.currentData()
        
        # Validation
        if not mobile or len(mobile) != 10:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال رقم جوال صحيح")
            return
            
        if network == "-- اختر الشبكة --":
            QMessageBox.warning(self, "خطأ", "يرجى اختيار الشبكة")
            return
            
        if not amount or float(amount) <= 0:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال مبلغ صحيح")
            return
            
        # Process recharge (simulation)
        reply = QMessageBox.question(
            self, "تأكيد الشحن",
            f"هل تريد شحن {amount} ريال لرقم {mobile}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Here would be the actual API call to recharge service
            QMessageBox.information(self, "نجح الشحن", f"تم شحن {amount} ريال بنجاح")
            
            # Clear form
            self.mobile_input.clear()
            self.network_combo.setCurrentIndex(0)
            self.amount_input.setCurrentText("")
            
            # Refresh data
            self.load_recent_recharge()
            
    def check_balance(self):
        """Check mobile balance"""
        mobile = self.mobile_input.text().strip()
        
        if not mobile or len(mobile) != 10:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال رقم جوال صحيح")
            return
            
        # Simulate balance check
        QMessageBox.information(self, "رصيد الجوال", f"رصيد الجوال {mobile}: 25.50 ريال")
        
    def select_payment_service(self, service_id: str):
        """Select payment service"""
        service_map = {
            "electricity": "فواتير الكهرباء - SEC",
            "water": "فواتير المياه - NWC",
            "telecom": "فواتير الاتصالات - STC",
            "gas": "فواتير الغاز - NGC",
            "internet": "فواتير الإنترنت - ISP"
        }
        
        service_name = service_map.get(service_id)
        if service_name:
            # Find and set the service in combo box
            index = self.payment_service_combo.findText(service_name)
            if index >= 0:
                self.payment_service_combo.setCurrentIndex(index)
                
            # Switch to payment tab
            self.tab_widget.setCurrentIndex(1)
            
    def inquiry_bill(self):
        """Inquire about bill details"""
        service = self.payment_service_combo.currentText()
        account = self.account_input.text().strip()
        
        if service == "-- اختر نوع الخدمة --":
            QMessageBox.warning(self, "خطأ", "يرجى اختيار نوع الخدمة")
            return
            
        if not account:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال رقم الحساب")
            return
            
        # Simulate bill inquiry
        QMessageBox.information(
            self, "تفاصيل الفاتورة",
            f"رقم الحساب: {account}\n"
            f"المبلغ المستحق: 150.75 ريال\n"
            f"تاريخ الاستحقاق: 2024/02/15"
        )
        
        self.payment_amount.setValue(150.75)
        
    def process_payment(self):
        """Process bill payment"""
        service = self.payment_service_combo.currentText()
        account = self.account_input.text().strip()
        amount = self.payment_amount.value()
        customer_id = self.payment_customer.currentData()
        
        # Validation
        if service == "-- اختر نوع الخدمة --":
            QMessageBox.warning(self, "خطأ", "يرجى اختيار نوع الخدمة")
            return
            
        if not account:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال رقم الحساب")
            return
            
        if amount <= 0:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال مبلغ صحيح")
            return
            
        # Process payment (simulation)
        reply = QMessageBox.question(
            self, "تأكيد الدفع",
            f"هل تريد دفع {amount:.2f} ريال لحساب {account}؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Here would be the actual API call to payment service
            QMessageBox.information(self, "نجح الدفع", f"تم دفع {amount:.2f} ريال بنجاح")
            
            # Clear form
            self.payment_service_combo.setCurrentIndex(0)
            self.account_input.clear()
            self.payment_amount.setValue(0)
            
            # Refresh data
            self.load_recent_payments()
            
    def search_history(self):
        """Search services history"""
        service_filter = self.history_service_filter.currentText()
        start_date = self.history_start_date.date().toString("yyyy-MM-dd")
        end_date = self.history_end_date.date().toString("yyyy-MM-dd")
        
        # Load and filter history data
        self.load_services_history(service_filter, start_date, end_date)
        
    def load_services_history(self, service_filter: str, start_date: str, end_date: str):
        """Load services history with filters"""
        try:
            # Load services from database with filters
            services = self.db_manager.get_services_history(start_date, end_date, service_filter)
            
            self.history_table.setRowCount(len(services))
            for row, service in enumerate(services):
                self.history_table.setItem(row, 0, QTableWidgetItem(service.get('created_at', '')[:16]))
                self.history_table.setItem(row, 1, QTableWidgetItem(service.get('service_type', '')))
                self.history_table.setItem(row, 2, QTableWidgetItem(service.get('description', '')))
                self.history_table.setItem(row, 3, QTableWidgetItem(service.get('customer_name', 'غير محدد')))
                self.history_table.setItem(row, 4, QTableWidgetItem(f"{service.get('amount', 0):.2f}"))
                self.history_table.setItem(row, 5, QTableWidgetItem(f"{service.get('commission', 0):.2f}"))
                self.history_table.setItem(row, 6, QTableWidgetItem(service.get('status', '')))
                self.history_table.setItem(row, 7, QTableWidgetItem(service.get('reference_number', '')))
                
        except Exception as e:
            print(f"Error loading services history: {e}")
            
    def search(self, query: str):
        """Search services from main search bar"""
        # Could search by mobile number, account number, etc.
        pass