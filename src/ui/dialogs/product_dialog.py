#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Product Dialog - Add/Edit Product
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox,
    QComboBox, QPushButton, QDialogButtonBox, QGroupBox
)
from PyQt6.QtCore import Qt

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.product_id = product_id
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("إضافة منتج" if not self.product_id else "تعديل منتج")
        self.setModal(True)
        self.resize(500, 600)
        
        layout = QVBoxLayout(self)
        
        # Basic info group
        basic_group = QGroupBox("المعلومات الأساسية")
        basic_layout = QFormLayout(basic_group)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم المنتج")
        basic_layout.addRow("اسم المنتج:", self.name_input)
        
        self.brand_input = QLineEdit()
        basic_layout.addRow("الماركة:", self.brand_input)
        
        self.model_input = QLineEdit()
        basic_layout.addRow("الموديل:", self.model_input)
        
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        basic_layout.addRow("الفئة:", self.category_input)
        
        layout.addWidget(basic_group)
        
        # Price group
        price_group = QGroupBox("الأسعار والمخزون")
        price_layout = QFormLayout(price_group)
        
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999.99)
        self.price_input.setSuffix(" ريال")
        price_layout.addRow("سعر البيع:", self.price_input)
        
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMaximum(999999.99)
        self.cost_input.setSuffix(" ريال")
        price_layout.addRow("سعر التكلفة:", self.cost_input)
        
        self.stock_input = QSpinBox()
        self.stock_input.setMaximum(99999)
        price_layout.addRow("المخزون الحالي:", self.stock_input)
        
        self.min_stock_input = QSpinBox()
        self.min_stock_input.setMaximum(9999)
        self.min_stock_input.setValue(5)
        price_layout.addRow("الحد الأدنى للمخزون:", self.min_stock_input)
        
        layout.addWidget(price_group)
        
        # Additional info group
        info_group = QGroupBox("معلومات إضافية")
        info_layout = QFormLayout(info_group)
        
        self.barcode_input = QLineEdit()
        info_layout.addRow("الباركود:", self.barcode_input)
        
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        info_layout.addRow("الوصف:", self.description_input)
        
        layout.addWidget(info_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)
        
    def load_data(self):
        """Load existing product data for editing"""
        if self.product_id:
            # Load product data from database
            pass
            
    def get_product_data(self):
        """Get product data from form"""
        return {
            'name': self.name_input.text(),
            'brand': self.brand_input.text(),
            'model': self.model_input.text(),
            'category': self.category_input.currentText(),
            'price': self.price_input.value(),
            'cost': self.cost_input.value(),
            'stock_quantity': self.stock_input.value(),
            'min_stock_level': self.min_stock_input.value(),
            'barcode': self.barcode_input.text(),
            'description': self.description_input.toPlainText()
        }