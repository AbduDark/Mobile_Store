#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customers Module - Customer Management Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFormLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QTextEdit,
    QTabWidget, QGroupBox, QLabel, QFrame, QHeaderView,
    QAbstractItemView, QDialog, QMessageBox, QSplitter,
    QComboBox, QDateEdit, QSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont

from .base_module import BaseModule
from ..widgets.data_table import EnhancedTableWidget
from ..dialogs.customer_dialog import CustomerDialog

class CustomersModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "العملاء")
        
    def setup_ui(self):
        """Setup customers module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Customers list tab
        self.customers_tab = self.create_customers_tab()
        self.tab_widget.addTab(self.customers_tab, "👥 قائمة العملاء")
        
        # Customer history tab
        self.history_tab = self.create_history_tab()
        self.tab_widget.addTab(self.history_tab, "📋 تاريخ المشتريات")
        
        # Loyalty program tab
        self.loyalty_tab = self.create_loyalty_tab()
        self.tab_widget.addTab(self.loyalty_tab, "⭐ برنامج الولاء")
        
        layout.addWidget(self.tab_widget)
        
    def create_customers_tab(self) -> QWidget:
        """Create the main customers management tab"""
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
        
        # Customers table
        self.customers_table = self.create_customers_table()
        splitter.addWidget(self.customers_table)
        
        # Customer details panel
        details_panel = self.create_details_panel()
        splitter.addWidget(details_panel)
        
        # Set splitter proportions
        splitter.setSizes([800, 300])
        
        layout.addWidget(splitter)
        
        return tab
        
    def create_toolbar(self) -> QFrame:
        """Create customers toolbar"""
        toolbar = QFrame()
        layout = QHBoxLayout(toolbar)
        
        # Add customer button
        self.add_btn = QPushButton("➕ إضافة عميل")
        self.add_btn.setObjectName("primary_button")
        self.add_btn.clicked.connect(self.add_customer)
        
        # Edit customer button
        self.edit_btn = QPushButton("✏️ تعديل")
        self.edit_btn.setObjectName("secondary_button")
        self.edit_btn.clicked.connect(self.edit_customer)
        self.edit_btn.setEnabled(False)
        
        # Delete customer button
        self.delete_btn = QPushButton("🗑️ حذف")
        self.delete_btn.setObjectName("danger_button")
        self.delete_btn.clicked.connect(self.delete_customer)
        self.delete_btn.setEnabled(False)
        
        # View purchases button
        self.purchases_btn = QPushButton("🛒 المشتريات")
        self.purchases_btn.setObjectName("secondary_button")
        self.purchases_btn.clicked.connect(self.view_purchases)
        self.purchases_btn.setEnabled(False)
        
        # Send message button
        self.message_btn = QPushButton("💬 إرسال رسالة")
        self.message_btn.setObjectName("secondary_button")
        self.message_btn.clicked.connect(self.send_message)
        self.message_btn.setEnabled(False)
        
        # Import/Export buttons
        self.import_btn = QPushButton("📥 استيراد")
        self.import_btn.setObjectName("secondary_button")
        
        self.export_btn = QPushButton("📤 تصدير")
        self.export_btn.setObjectName("secondary_button")
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 تحديث")
        self.refresh_btn.setObjectName("secondary_button")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Add to layout (RTL order)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        layout.addStretch()
        layout.addWidget(self.message_btn)
        layout.addWidget(self.purchases_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.add_btn)
        
        return toolbar
        
    def create_filters(self) -> QFrame:
        """Create search and filter controls"""
        filters_frame = QFrame()
        layout = QHBoxLayout(filters_frame)
        
        # Search box
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("البحث في العملاء...")
        self.search_input.textChanged.connect(self.filter_customers)
        
        # City filter
        self.city_filter = QComboBox()
        self.city_filter.addItem("جميع المدن", "")
        self.city_filter.currentTextChanged.connect(self.filter_customers)
        
        # Customer type filter
        self.type_filter = QComboBox()
        self.type_filter.addItems([
            "جميع العملاء",
            "عملاء VIP",
            "عملاء جدد",
            "عملاء نشطون",
            "عملاء غير نشطين"
        ])
        self.type_filter.currentTextChanged.connect(self.filter_customers)
        
        # Sort options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "ترتيب حسب الاسم",
            "ترتيب حسب المشتريات",
            "ترتيب حسب النقاط",
            "ترتيب حسب التاريخ"
        ])
        self.sort_combo.currentTextChanged.connect(self.sort_customers)
        
        # Results count
        self.results_label = QLabel("0 عميل")
        
        # Add to layout (RTL order)
        layout.addWidget(self.results_label)
        layout.addStretch()
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.type_filter)
        layout.addWidget(self.city_filter)
        layout.addWidget(self.search_input)
        
        return filters_frame
        
    def create_customers_table(self) -> EnhancedTableWidget:
        """Create the customers data table"""
        columns = [
            ("ID", 50, False),
            ("الاسم", 180, True),
            ("الهاتف", 120, True),
            ("البريد الإلكتروني", 200, True),
            ("المدينة", 100, True),
            ("إجمالي المشتريات", 120, True),
            ("نقاط الولاء", 100, True),
            ("تاريخ التسجيل", 120, True),
            ("آخر شراء", 120, True)
        ]
        
        table = EnhancedTableWidget(columns)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.itemSelectionChanged.connect(self.on_selection_changed)
        table.itemDoubleClicked.connect(self.edit_customer)
        
        return table
        
    def create_details_panel(self) -> QFrame:
        """Create customer details panel"""
        panel = QFrame()
        panel.setFixedWidth(300)
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("بيانات العميل")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Customer info group
        info_group = QGroupBox("المعلومات الأساسية")
        info_layout = QFormLayout(info_group)
        
        self.detail_labels = {
            'name': QLabel("-"),
            'phone': QLabel("-"),
            'email': QLabel("-"),
            'address': QLabel("-"),
            'city': QLabel("-")
        }
        
        info_layout.addRow("الاسم:", self.detail_labels['name'])
        info_layout.addRow("الهاتف:", self.detail_labels['phone'])
        info_layout.addRow("البريد:", self.detail_labels['email'])
        info_layout.addRow("العنوان:", self.detail_labels['address'])
        info_layout.addRow("المدينة:", self.detail_labels['city'])
        
        layout.addWidget(info_group)
        
        # Statistics group
        stats_group = QGroupBox("الإحصائيات")
        stats_layout = QFormLayout(stats_group)
        
        self.stats_labels = {
            'total_purchases': QLabel("-"),
            'loyalty_points': QLabel("-"),
            'last_purchase': QLabel("-"),
            'purchase_count': QLabel("-")
        }
        
        stats_layout.addRow("إجمالي المشتريات:", self.stats_labels['total_purchases'])
        stats_layout.addRow("نقاط الولاء:", self.stats_labels['loyalty_points'])
        stats_layout.addRow("آخر شراء:", self.stats_labels['last_purchase'])
        stats_layout.addRow("عدد المشتريات:", self.stats_labels['purchase_count'])
        
        layout.addWidget(stats_group)
        
        # Recent purchases
        recent_group = QGroupBox("آخر المشتريات")
        recent_layout = QVBoxLayout(recent_group)
        
        self.recent_purchases_list = QLabel("لا توجد مشتريات")
        self.recent_purchases_list.setWordWrap(True)
        self.recent_purchases_list.setStyleSheet("padding: 10px; border: 1px solid #ddd;")
        
        recent_layout.addWidget(self.recent_purchases_list)
        
        layout.addWidget(recent_group)
        
        layout.addStretch()
        
        return panel
        
    def create_history_tab(self) -> QWidget:
        """Create customer purchase history tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Customer selection
        customer_frame = QFrame()
        customer_layout = QHBoxLayout(customer_frame)
        
        customer_layout.addWidget(QLabel("العميل:"))
        
        self.customer_selector = QComboBox()
        self.customer_selector.setMinimumWidth(200)
        self.customer_selector.currentTextChanged.connect(self.load_customer_history)
        customer_layout.addWidget(self.customer_selector)
        
        # Date filters
        customer_layout.addWidget(QLabel("من تاريخ:"))
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        customer_layout.addWidget(self.start_date)
        
        customer_layout.addWidget(QLabel("إلى تاريخ:"))
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        customer_layout.addWidget(self.end_date)
        
        # Filter button
        filter_btn = QPushButton("🔍 عرض")
        filter_btn.setObjectName("primary_button")
        filter_btn.clicked.connect(self.load_customer_history)
        customer_layout.addWidget(filter_btn)
        
        customer_layout.addStretch()
        
        layout.addWidget(customer_frame)
        
        # Purchase history table
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "رقم الفاتورة", "التاريخ", "المبلغ", "الخصم", 
            "الضريبة", "طريقة الدفع", "الحالة"
        ])
        
        # Configure table
        header = self.history_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.history_table)
        
        # Summary
        summary_frame = QFrame()
        summary_layout = QHBoxLayout(summary_frame)
        
        self.history_summary = QLabel("اختر عميلاً لعرض تاريخ مشترياته")
        self.history_summary.setStyleSheet("font-size: 12pt; color: #7F8C8D;")
        
        summary_layout.addWidget(self.history_summary)
        summary_layout.addStretch()
        
        layout.addWidget(summary_frame)
        
        return tab
        
    def create_loyalty_tab(self) -> QWidget:
        """Create loyalty program management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Loyalty program info
        info_frame = self.create_loyalty_info()
        layout.addWidget(info_frame)
        
        # Top customers table
        top_customers_frame = self.create_top_customers()
        layout.addWidget(top_customers_frame)
        
        return tab
        
    def create_loyalty_info(self) -> QFrame:
        """Create loyalty program information panel"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        # Title
        title = QLabel("برنامج الولاء")
        title.setStyleSheet("font-size: 16pt; font-weight: bold; color: #F39C12;")
        layout.addWidget(title)
        
        # Program rules
        rules = QLabel("""
        قواعد برنامج الولاء:
        • نقطة واحدة لكل 10 ريال من المشتريات
        • 100 نقطة = خصم 10 ريال
        • العضوية الذهبية: أكثر من 1000 نقطة
        • العضوية البلاتينية: أكثر من 5000 نقطة
        """)
        rules.setStyleSheet("font-size: 11pt; color: #34495E; padding: 10px;")
        layout.addWidget(rules)
        
        # Statistics cards
        stats_layout = QHBoxLayout()
        
        # Create statistics cards
        stats = [
            ("إجمالي الأعضاء", "0", "#3498DB"),
            ("أعضاء ذهبيون", "0", "#F39C12"),
            ("أعضاء بلاتينيون", "0", "#9B59B6"),
            ("النقاط المستخدمة", "0", "#27AE60")
        ]
        
        self.loyalty_stats = {}
        
        for title_text, value, color in stats:
            card = self.create_stat_card(title_text, value, color)
            stats_layout.addWidget(card)
            
        layout.addLayout(stats_layout)
        
        return frame
        
    def create_stat_card(self, title: str, value: str, color: str) -> QFrame:
        """Create a statistics card"""
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
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 20pt; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 10pt; color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        # Store reference
        self.loyalty_stats[title] = value_label
        
        return card
        
    def create_top_customers(self) -> QFrame:
        """Create top customers by loyalty points"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        # Title
        title = QLabel("أفضل العملاء (حسب نقاط الولاء)")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Top customers table
        self.top_customers_table = QTableWidget()
        self.top_customers_table.setColumnCount(5)
        self.top_customers_table.setHorizontalHeaderLabels([
            "الترتيب", "اسم العميل", "نقاط الولاء", 
            "إجمالي المشتريات", "نوع العضوية"
        ])
        
        # Configure table
        header = self.top_customers_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.top_customers_table)
        
        return frame
        
    def load_data(self):
        """Load customers data"""
        try:
            # Load customers
            customers = self.db_manager.get_customers()
            self.populate_customers_table(customers)
            
            # Load customer selector for history
            self.populate_customer_selector(customers)
            
            # Load loyalty statistics
            self.update_loyalty_stats(customers)
            
            # Load top customers
            self.load_top_customers(customers)
            
        except Exception as e:
            print(f"Error loading customers data: {e}")
            
    def populate_customers_table(self, customers):
        """Populate customers table"""
        self.customers_table.setRowCount(len(customers))
        
        for row, customer in enumerate(customers):
            self.customers_table.setItem(row, 0, QTableWidgetItem(str(customer['id'])))
            self.customers_table.setItem(row, 1, QTableWidgetItem(customer['name'] or ''))
            self.customers_table.setItem(row, 2, QTableWidgetItem(customer['phone'] or ''))
            self.customers_table.setItem(row, 3, QTableWidgetItem(customer['email'] or ''))
            self.customers_table.setItem(row, 4, QTableWidgetItem(customer['city'] or ''))
            
            # Format purchases
            purchases = f"{customer['total_purchases']:,.2f} ريال" if customer['total_purchases'] else '0 ريال'
            self.customers_table.setItem(row, 5, QTableWidgetItem(purchases))
            
            # Loyalty points
            points = str(customer['loyalty_points']) if customer['loyalty_points'] else '0'
            self.customers_table.setItem(row, 6, QTableWidgetItem(points))
            
            # Registration date
            reg_date = customer['created_at'][:10] if customer['created_at'] else '-'
            self.customers_table.setItem(row, 7, QTableWidgetItem(reg_date))
            
            # Last purchase (placeholder)
            self.customers_table.setItem(row, 8, QTableWidgetItem('-'))
            
        # Update count
        self.results_label.setText(f"{len(customers)} عميل")
        
    def populate_customer_selector(self, customers):
        """Populate customer selector for history tab"""
        self.customer_selector.clear()
        self.customer_selector.addItem("-- اختر عميل --", 0)
        
        for customer in customers:
            self.customer_selector.addItem(
                f"{customer['name']} ({customer['phone']})",
                customer['id']
            )
            
    def update_loyalty_stats(self, customers):
        """Update loyalty program statistics"""
        total_members = len(customers)
        gold_members = len([c for c in customers if c['loyalty_points'] >= 1000])
        platinum_members = len([c for c in customers if c['loyalty_points'] >= 5000])
        total_points_used = 0  # This would come from transactions
        
        if "إجمالي الأعضاء" in self.loyalty_stats:
            self.loyalty_stats["إجمالي الأعضاء"].setText(str(total_members))
        if "أعضاء ذهبيون" in self.loyalty_stats:
            self.loyalty_stats["أعضاء ذهبيون"].setText(str(gold_members))
        if "أعضاء بلاتينيون" in self.loyalty_stats:
            self.loyalty_stats["أعضاء بلاتينيون"].setText(str(platinum_members))
        if "النقاط المستخدمة" in self.loyalty_stats:
            self.loyalty_stats["النقاط المستخدمة"].setText(str(total_points_used))
            
    def load_top_customers(self, customers):
        """Load top customers by loyalty points"""
        # Sort customers by loyalty points
        top_customers = sorted(customers, key=lambda x: x['loyalty_points'], reverse=True)[:10]
        
        self.top_customers_table.setRowCount(len(top_customers))
        
        for row, customer in enumerate(top_customers):
            # Rank
            self.top_customers_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # Name
            self.top_customers_table.setItem(row, 1, QTableWidgetItem(customer['name']))
            
            # Points
            points = str(customer['loyalty_points'])
            self.top_customers_table.setItem(row, 2, QTableWidgetItem(points))
            
            # Total purchases
            purchases = f"{customer['total_purchases']:,.2f} ريال"
            self.top_customers_table.setItem(row, 3, QTableWidgetItem(purchases))
            
            # Membership type
            points_value = customer['loyalty_points']
            if points_value >= 5000:
                membership = "بلاتيني"
                color = "#9B59B6"
            elif points_value >= 1000:
                membership = "ذهبي"
                color = "#F39C12"
            else:
                membership = "عادي"
                color = "#95A5A6"
                
            membership_item = QTableWidgetItem(membership)
            membership_item.setBackground(Qt.GlobalColor.white)
            self.top_customers_table.setItem(row, 4, membership_item)
            
    def on_selection_changed(self):
        """Handle table selection changes"""
        current_row = self.customers_table.currentRow()
        has_selection = current_row >= 0
        
        # Enable/disable buttons
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.purchases_btn.setEnabled(has_selection)
        self.message_btn.setEnabled(has_selection)
        
        # Update details panel
        if has_selection:
            self.update_details_panel(current_row)
        else:
            self.clear_details_panel()
            
    def update_details_panel(self, row: int):
        """Update customer details panel"""
        try:
            # Get customer data from table
            name = self.customers_table.item(row, 1).text()
            phone = self.customers_table.item(row, 2).text()
            email = self.customers_table.item(row, 3).text()
            city = self.customers_table.item(row, 4).text()
            purchases = self.customers_table.item(row, 5).text()
            points = self.customers_table.item(row, 6).text()
            
            # Update labels
            self.detail_labels['name'].setText(name)
            self.detail_labels['phone'].setText(phone)
            self.detail_labels['email'].setText(email)
            self.detail_labels['city'].setText(city)
            
            self.stats_labels['total_purchases'].setText(purchases)
            self.stats_labels['loyalty_points'].setText(points)
            
            # Load recent purchases (placeholder)
            self.recent_purchases_list.setText("لا توجد مشتريات حديثة")
            
        except Exception as e:
            print(f"Error updating customer details: {e}")
            
    def clear_details_panel(self):
        """Clear details panel"""
        for label in self.detail_labels.values():
            label.setText("-")
        for label in self.stats_labels.values():
            label.setText("-")
        self.recent_purchases_list.setText("لا توجد مشتريات")
        
    def filter_customers(self):
        """Filter customers based on criteria"""
        # Implementation would filter customers
        pass
        
    def sort_customers(self):
        """Sort customers based on selected criteria"""
        # Implementation would sort customers
        pass
        
    def add_customer(self):
        """Add a new customer"""
        try:
            dialog = CustomerDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_data = dialog.get_customer_data()
                customer_id = self.db_manager.add_customer(customer_data)
                if customer_id:
                    self.refresh_data()
                    self.status_message.emit("تم إضافة العميل بنجاح")
                    
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل في إضافة العميل:\n{str(e)}")
            
    def edit_customer(self):
        """Edit selected customer"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            return
            
        try:
            customer_id = int(self.customers_table.item(current_row, 0).text())
            dialog = CustomerDialog(self, customer_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                customer_data = dialog.get_customer_data()
                # Implementation would update customer
                self.refresh_data()
                self.status_message.emit("تم تحديث العميل بنجاح")
                
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل في تحديث العميل:\n{str(e)}")
            
    def delete_customer(self):
        """Delete selected customer"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            return
            
        customer_name = self.customers_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف العميل '{customer_name}'؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Implementation would delete customer
                self.refresh_data()
                self.status_message.emit("تم حذف العميل بنجاح")
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل في حذف العميل:\n{str(e)}")
                
    def view_purchases(self):
        """View customer purchase history"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            return
            
        # Switch to history tab and load customer
        customer_id = int(self.customers_table.item(current_row, 0).text())
        self.tab_widget.setCurrentIndex(1)  # History tab
        
        # Set customer in selector
        for i in range(self.customer_selector.count()):
            if self.customer_selector.itemData(i) == customer_id:
                self.customer_selector.setCurrentIndex(i)
                break
                
        self.load_customer_history()
        
    def send_message(self):
        """Send message to customer"""
        current_row = self.customers_table.currentRow()
        if current_row < 0:
            return
            
        customer_name = self.customers_table.item(current_row, 1).text()
        customer_phone = self.customers_table.item(current_row, 2).text()
        
        QMessageBox.information(
            self, "إرسال رسالة", 
            f"سيتم إرسال رسالة إلى {customer_name}\nرقم الهاتف: {customer_phone}"
        )
        
    def load_customer_history(self):
        """Load purchase history for selected customer"""
        customer_id = self.customer_selector.currentData()
        if not customer_id:
            self.history_table.setRowCount(0)
            self.history_summary.setText("اختر عميلاً لعرض تاريخ مشترياته")
            return
            
        # Get date range
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        try:
            # Load sales for customer
            sales = self.db_manager.get_sales_report(start_date, end_date)
            customer_sales = [s for s in sales if s.get('customer_id') == customer_id]
            
            # Populate history table
            self.history_table.setRowCount(len(customer_sales))
            
            total_amount = 0
            for row, sale in enumerate(customer_sales):
                self.history_table.setItem(row, 0, QTableWidgetItem(str(sale['id'])))
                self.history_table.setItem(row, 1, QTableWidgetItem(sale['created_at'][:10]))
                self.history_table.setItem(row, 2, QTableWidgetItem(f"{sale['total_amount']:.2f}"))
                self.history_table.setItem(row, 3, QTableWidgetItem(f"{sale['discount_amount']:.2f}"))
                self.history_table.setItem(row, 4, QTableWidgetItem(f"{sale['tax_amount']:.2f}"))
                self.history_table.setItem(row, 5, QTableWidgetItem(sale['payment_method'] or '-'))
                self.history_table.setItem(row, 6, QTableWidgetItem(sale['status'] or 'مكتمل'))
                
                total_amount += sale['total_amount']
                
            # Update summary
            self.history_summary.setText(
                f"إجمالي المشتريات: {len(customer_sales)} فاتورة "
                f"- إجمالي المبلغ: {total_amount:,.2f} ريال"
            )
            
        except Exception as e:
            print(f"Error loading customer history: {e}")
            
    def search(self, query: str):
        """Search customers from main search bar"""
        self.search_input.setText(query)
        self.filter_customers()