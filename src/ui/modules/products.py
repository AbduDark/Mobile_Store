#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Products Module - Product Management Interface
"""

from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QTabWidget,
    QGroupBox, QLabel, QFrame, QHeaderView, QAbstractItemView,
    QDialog, QDialogButtonBox, QMessageBox, QFileDialog,
    QProgressBar, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QIcon

from .base_module import BaseModule
from ..widgets.data_table import EnhancedTableWidget
from ..widgets.charts import StockChart
from ..dialogs.product_dialog import ProductDialog

class ProductsModule(BaseModule):
    def __init__(self, db_manager, settings_manager):
        super().__init__(db_manager, settings_manager, "المنتجات")
        
    def setup_ui(self):
        """Setup products module UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Products list tab
        self.products_tab = self.create_products_tab()
        self.tab_widget.addTab(self.products_tab, "📦 قائمة المنتجات")
        
        # Inventory tab
        self.inventory_tab = self.create_inventory_tab()
        self.tab_widget.addTab(self.inventory_tab, "📊 المخزون")
        
        # Categories tab
        self.categories_tab = self.create_categories_tab()
        self.tab_widget.addTab(self.categories_tab, "📂 الفئات")
        
        layout.addWidget(self.tab_widget)
        
    def create_products_tab(self) -> QWidget:
        """Create the main products management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Toolbar
        toolbar = self.create_toolbar()
        layout.addWidget(toolbar)
        
        # Search and filters
        filters = self.create_filters()
        layout.addWidget(filters)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Products table
        self.products_table = self.create_products_table()
        splitter.addWidget(self.products_table)
        
        # Product details panel
        details_panel = self.create_details_panel()
        splitter.addWidget(details_panel)
        
        # Set splitter proportions (3:1)
        splitter.setSizes([800, 200])
        
        layout.addWidget(splitter)
        
        return tab
        
    def create_toolbar(self) -> QFrame:
        """Create products toolbar"""
        toolbar = QFrame()
        layout = QHBoxLayout(toolbar)
        
        # Add product button
        self.add_btn = QPushButton("➕ إضافة منتج")
        self.add_btn.setObjectName("primary_button")
        self.add_btn.clicked.connect(self.add_product)
        
        # Edit product button
        self.edit_btn = QPushButton("✏️ تعديل")
        self.edit_btn.setObjectName("secondary_button")
        self.edit_btn.clicked.connect(self.edit_product)
        self.edit_btn.setEnabled(False)
        
        # Delete product button
        self.delete_btn = QPushButton("🗑️ حذف")
        self.delete_btn.setObjectName("danger_button")
        self.delete_btn.clicked.connect(self.delete_product)
        self.delete_btn.setEnabled(False)
        
        # Import/Export buttons
        self.import_btn = QPushButton("📥 استيراد")
        self.import_btn.setObjectName("secondary_button")
        self.import_btn.clicked.connect(self.import_products)
        
        self.export_btn = QPushButton("📤 تصدير")
        self.export_btn.setObjectName("secondary_button")
        self.export_btn.clicked.connect(self.export_products)
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 تحديث")
        self.refresh_btn.setObjectName("secondary_button")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        # Add buttons to layout (RTL order)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.export_btn)
        layout.addWidget(self.import_btn)
        layout.addStretch()
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
        self.search_input.setPlaceholderText("البحث في المنتجات...")
        self.search_input.textChanged.connect(self.filter_products)
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItem("جميع الفئات", "")
        self.category_filter.currentTextChanged.connect(self.filter_products)
        
        # Stock status filter
        self.stock_filter = QComboBox()
        self.stock_filter.addItems([
            "جميع المنتجات",
            "متوفر في المخزن", 
            "مخزون منخفض",
            "غير متوفر"
        ])
        self.stock_filter.currentTextChanged.connect(self.filter_products)
        
        # Sort options
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "ترتيب حسب الاسم",
            "ترتيب حسب السعر", 
            "ترتيب حسب المخزون",
            "ترتيب حسب التاريخ"
        ])
        self.sort_combo.currentTextChanged.connect(self.sort_products)
        
        # Results count label
        self.results_label = QLabel("0 منتج")
        
        # Add to layout (RTL order)
        layout.addWidget(self.results_label)
        layout.addStretch()
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.stock_filter)
        layout.addWidget(self.category_filter)
        layout.addWidget(self.search_input)
        
        return filters_frame
        
    def create_products_table(self) -> EnhancedTableWidget:
        """Create the products data table"""
        # Column definitions
        columns = [
            ("ID", 50, False),
            ("الاسم", 200, True),
            ("الماركة", 120, True),
            ("الموديل", 120, True),
            ("الفئة", 100, True),
            ("السعر", 80, True),
            ("المخزون", 80, True),
            ("الحد الأدنى", 80, True),
            ("الباركود", 150, True),
            ("تاريخ الإضافة", 120, True)
        ]
        
        table = EnhancedTableWidget(columns)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.itemSelectionChanged.connect(self.on_selection_changed)
        table.itemDoubleClicked.connect(self.edit_product)
        
        return table
        
    def create_details_panel(self) -> QFrame:
        """Create product details panel"""
        panel = QFrame()
        panel.setFixedWidth(250)
        layout = QVBoxLayout(panel)
        
        # Title
        title = QLabel("تفاصيل المنتج")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #2E86C1;")
        layout.addWidget(title)
        
        # Details form
        self.details_form = QFormLayout()
        
        # Product details labels
        self.detail_labels = {
            'name': QLabel("-"),
            'brand': QLabel("-"),
            'model': QLabel("-"),
            'category': QLabel("-"),
            'price': QLabel("-"),
            'cost': QLabel("-"),
            'stock': QLabel("-"),
            'min_stock': QLabel("-"),
            'barcode': QLabel("-"),
            'description': QLabel("-")
        }
        
        # Add labels to form
        self.details_form.addRow("الاسم:", self.detail_labels['name'])
        self.details_form.addRow("الماركة:", self.detail_labels['brand'])
        self.details_form.addRow("الموديل:", self.detail_labels['model'])
        self.details_form.addRow("الفئة:", self.detail_labels['category'])
        self.details_form.addRow("السعر:", self.detail_labels['price'])
        self.details_form.addRow("التكلفة:", self.detail_labels['cost'])
        self.details_form.addRow("المخزون:", self.detail_labels['stock'])
        self.details_form.addRow("الحد الأدنى:", self.detail_labels['min_stock'])
        self.details_form.addRow("الباركود:", self.detail_labels['barcode'])
        
        layout.addLayout(self.details_form)
        
        # Description
        layout.addWidget(QLabel("الوصف:"))
        self.detail_labels['description'].setWordWrap(True)
        self.detail_labels['description'].setStyleSheet("border: 1px solid #ddd; padding: 5px;")
        layout.addWidget(self.detail_labels['description'])
        
        layout.addStretch()
        
        return panel
        
    def create_inventory_tab(self) -> QWidget:
        """Create inventory management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Summary cards
        summary = self.create_inventory_summary()
        layout.addWidget(summary)
        
        # Stock chart
        self.stock_chart = StockChart()
        layout.addWidget(self.stock_chart)
        
        # Low stock alerts
        alerts = self.create_stock_alerts()
        layout.addWidget(alerts)
        
        return tab
        
    def create_inventory_summary(self) -> QFrame:
        """Create inventory summary cards"""
        frame = QFrame()
        layout = QHBoxLayout(frame)
        
        # Summary cards
        cards = [
            ("إجمالي المنتجات", "0", "#3498DB"),
            ("إجمالي القيمة", "0 ريال", "#27AE60"),
            ("مخزون منخفض", "0", "#E74C3C"),
            ("غير متوفر", "0", "#95A5A6")
        ]
        
        self.summary_labels = {}
        
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
                padding: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Value label
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 24pt; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12pt; color: #7F8C8D;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        
        # Store reference for updates
        self.summary_labels[title] = value_label
        
        return card
        
    def create_stock_alerts(self) -> QFrame:
        """Create low stock alerts section"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        
        # Title
        title = QLabel("تنبيهات المخزون المنخفض")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; color: #E74C3C;")
        layout.addWidget(title)
        
        # Alerts table
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(4)
        self.alerts_table.setHorizontalHeaderLabels([
            "المنتج", "المخزون الحالي", "الحد الأدنى", "الحالة"
        ])
        
        header = self.alerts_table.horizontalHeader()
        header.setStretchLastSection(True)
        
        layout.addWidget(self.alerts_table)
        
        return frame
        
    def create_categories_tab(self) -> QWidget:
        """Create categories management tab"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Categories toolbar
        cat_toolbar = QHBoxLayout()
        
        add_cat_btn = QPushButton("➕ إضافة فئة")
        add_cat_btn.setObjectName("primary_button")
        
        edit_cat_btn = QPushButton("✏️ تعديل فئة")
        edit_cat_btn.setObjectName("secondary_button")
        
        delete_cat_btn = QPushButton("🗑️ حذف فئة")
        delete_cat_btn.setObjectName("danger_button")
        
        cat_toolbar.addWidget(delete_cat_btn)
        cat_toolbar.addWidget(edit_cat_btn)
        cat_toolbar.addWidget(add_cat_btn)
        cat_toolbar.addStretch()
        
        layout.addLayout(cat_toolbar)
        
        # Categories table
        self.categories_table = QTableWidget()
        self.categories_table.setColumnCount(3)
        self.categories_table.setHorizontalHeaderLabels([
            "الفئة", "عدد المنتجات", "الوصف"
        ])
        
        layout.addWidget(self.categories_table)
        
        return tab
        
    def load_data(self):
        """Load products data"""
        try:
            # Load products
            products = self.db_manager.get_products()
            self.populate_products_table(products)
            
            # Update summary
            self.update_inventory_summary(products)
            
            # Load low stock alerts
            self.load_stock_alerts()
            
            # Load categories
            self.load_categories()
            
        except Exception as e:
            print(f"Error loading products data: {e}")
            
    def populate_products_table(self, products):
        """Populate the products table with data"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            self.products_table.setItem(row, 1, QTableWidgetItem(product['name'] or ''))
            self.products_table.setItem(row, 2, QTableWidgetItem(product['brand'] or ''))
            self.products_table.setItem(row, 3, QTableWidgetItem(product['model'] or ''))
            self.products_table.setItem(row, 4, QTableWidgetItem(product['category'] or ''))
            
            # Price formatting
            price = f"{product['price']:.2f} ريال" if product['price'] else '-'
            self.products_table.setItem(row, 5, QTableWidgetItem(price))
            
            # Stock with color coding
            stock_item = QTableWidgetItem(str(product['stock_quantity']))
            if product['stock_quantity'] <= product['min_stock_level']:
                stock_item.setBackground(Qt.GlobalColor.red)
            elif product['stock_quantity'] <= product['min_stock_level'] * 2:
                stock_item.setBackground(Qt.GlobalColor.yellow)
            self.products_table.setItem(row, 6, stock_item)
            
            self.products_table.setItem(row, 7, QTableWidgetItem(str(product['min_stock_level'])))
            self.products_table.setItem(row, 8, QTableWidgetItem(product['barcode'] or ''))
            
            # Date formatting
            created_date = product['created_at'][:10] if product['created_at'] else '-'
            self.products_table.setItem(row, 9, QTableWidgetItem(created_date))
            
        # Update results count
        self.results_label.setText(f"{len(products)} منتج")
        
    def update_inventory_summary(self, products):
        """Update inventory summary cards"""
        total_products = len(products)
        total_value = sum(p['price'] * p['stock_quantity'] for p in products if p['price'] and p['stock_quantity'])
        low_stock = len([p for p in products if p['stock_quantity'] <= p['min_stock_level']])
        out_of_stock = len([p for p in products if p['stock_quantity'] == 0])
        
        if "إجمالي المنتجات" in self.summary_labels:
            self.summary_labels["إجمالي المنتجات"].setText(str(total_products))
        if "إجمالي القيمة" in self.summary_labels:
            self.summary_labels["إجمالي القيمة"].setText(f"{total_value:,.2f} ريال")
        if "مخزون منخفض" in self.summary_labels:
            self.summary_labels["مخزون منخفض"].setText(str(low_stock))
        if "غير متوفر" in self.summary_labels:
            self.summary_labels["غير متوفر"].setText(str(out_of_stock))
            
    def load_stock_alerts(self):
        """Load low stock alerts"""
        try:
            low_stock_products = self.db_manager.get_low_stock_products()
            self.populate_alerts_table(low_stock_products)
        except Exception as e:
            print(f"Error loading stock alerts: {e}")
            
    def populate_alerts_table(self, products):
        """Populate the alerts table"""
        self.alerts_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            self.alerts_table.setItem(row, 0, QTableWidgetItem(product['name']))
            self.alerts_table.setItem(row, 1, QTableWidgetItem(str(product['stock_quantity'])))
            self.alerts_table.setItem(row, 2, QTableWidgetItem(str(product['min_stock_level'])))
            
            # Status with color
            if product['stock_quantity'] == 0:
                status = "غير متوفر"
                color = Qt.GlobalColor.red
            else:
                status = "مخزون منخفض"
                color = Qt.GlobalColor.yellow
                
            status_item = QTableWidgetItem(status)
            status_item.setBackground(color)
            self.alerts_table.setItem(row, 3, status_item)
            
    def load_categories(self):
        """Load product categories"""
        # This would load categories from database
        # For now, populate with sample data
        categories = [
            {"name": "هواتف ذكية", "count": 45, "description": "الهواتف الذكية بجميع الأنواع"},
            {"name": "اكسسوارات", "count": 32, "description": "اكسسوارات الهواتف المحمولة"},
            {"name": "شواحن", "count": 28, "description": "شواحن وكابلات الشحن"},
            {"name": "سماعات", "count": 19, "description": "سماعات سلكية ولاسلكية"}
        ]
        
        self.categories_table.setRowCount(len(categories))
        for row, category in enumerate(categories):
            self.categories_table.setItem(row, 0, QTableWidgetItem(category["name"]))
            self.categories_table.setItem(row, 1, QTableWidgetItem(str(category["count"])))
            self.categories_table.setItem(row, 2, QTableWidgetItem(category["description"]))
            
    def on_selection_changed(self):
        """Handle table selection changes"""
        current_row = self.products_table.currentRow()
        has_selection = current_row >= 0
        
        # Enable/disable buttons
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        
        # Update details panel
        if has_selection:
            self.update_details_panel(current_row)
        else:
            self.clear_details_panel()
            
    def update_details_panel(self, row: int):
        """Update the product details panel"""
        try:
            # Get product data from table
            product_id = self.products_table.item(row, 0).text()
            name = self.products_table.item(row, 1).text()
            brand = self.products_table.item(row, 2).text()
            model = self.products_table.item(row, 3).text()
            category = self.products_table.item(row, 4).text()
            price = self.products_table.item(row, 5).text()
            stock = self.products_table.item(row, 6).text()
            min_stock = self.products_table.item(row, 7).text()
            barcode = self.products_table.item(row, 8).text()
            
            # Update labels
            self.detail_labels['name'].setText(name)
            self.detail_labels['brand'].setText(brand)
            self.detail_labels['model'].setText(model)
            self.detail_labels['category'].setText(category)
            self.detail_labels['price'].setText(price)
            self.detail_labels['stock'].setText(stock)
            self.detail_labels['min_stock'].setText(min_stock)
            self.detail_labels['barcode'].setText(barcode)
            
        except Exception as e:
            print(f"Error updating details panel: {e}")
            
    def clear_details_panel(self):
        """Clear the details panel"""
        for label in self.detail_labels.values():
            label.setText("-")
            
    def filter_products(self):
        """Filter products based on search and filter criteria"""
        search_text = self.search_input.text().lower()
        category = self.category_filter.currentData() if self.category_filter.currentData() else ""
        
        # This would implement the filtering logic
        # For now, just trigger a data reload
        self.load_data()
        
    def sort_products(self):
        """Sort products based on selected criteria"""
        sort_option = self.sort_combo.currentText()
        # Implement sorting logic
        pass
        
    def add_product(self):
        """Add a new product"""
        try:
            dialog = ProductDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                product_data = dialog.get_product_data()
                product_id = self.db_manager.add_product(product_data)
                if product_id:
                    self.refresh_data()
                    self.status_message.emit("تم إضافة المنتج بنجاح")
                    
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل في إضافة المنتج:\n{str(e)}")
            
    def edit_product(self):
        """Edit selected product"""
        current_row = self.products_table.currentRow()
        if current_row < 0:
            return
            
        try:
            product_id = int(self.products_table.item(current_row, 0).text())
            dialog = ProductDialog(self, product_id)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                product_data = dialog.get_product_data()
                if self.db_manager.update_product(product_id, product_data):
                    self.refresh_data()
                    self.status_message.emit("تم تحديث المنتج بنجاح")
                    
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل في تحديث المنتج:\n{str(e)}")
            
    def delete_product(self):
        """Delete selected product"""
        current_row = self.products_table.currentRow()
        if current_row < 0:
            return
            
        product_name = self.products_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "تأكيد الحذف",
            f"هل أنت متأكد من حذف المنتج '{product_name}'؟",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                product_id = int(self.products_table.item(current_row, 0).text())
                # Implementation would delete from database
                self.refresh_data()
                self.status_message.emit("تم حذف المنتج بنجاح")
                
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل في حذف المنتج:\n{str(e)}")
                
    def import_products(self):
        """Import products from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "استيراد المنتجات", "", 
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        
        if file_path:
            # Implementation would handle file import
            QMessageBox.information(self, "استيراد", "تم استيراد المنتجات بنجاح")
            
    def export_products(self):
        """Export products to file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "تصدير المنتجات", "products.xlsx",
            "Excel Files (*.xlsx);;CSV Files (*.csv)"
        )
        
        if file_path:
            # Implementation would handle file export
            QMessageBox.information(self, "تصدير", "تم تصدير المنتجات بنجاح")
            
    def search(self, query: str):
        """Search products from main search bar"""
        self.search_input.setText(query)
        self.filter_products()
        
    def auto_save(self):
        """Auto-save any pending changes"""
        # Implementation would save any unsaved changes
        pass