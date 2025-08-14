#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Dialog - Add/Edit Customer
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QComboBox, QPushButton,
    QDialogButtonBox, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt

class CustomerDialog(QDialog):
    def __init__(self, parent=None, customer_id=None):
        super().__init__(parent)
        self.customer_id = customer_id
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup dialog UI"""
        self.setWindowTitle("إضافة عميل" if not self.customer_id else "تعديل عميل")
        self.setModal(True)
        self.resize(450, 500)
        
        layout = QVBoxLayout(self)
        
        # Basic info group
        basic_group = QGroupBox("المعلومات الأساسية")
        basic_layout = QFormLayout(basic_group)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم العميل")
        basic_layout.addRow("الاسم الكامل:", self.name_input)
        
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("05xxxxxxxx")
        basic_layout.addRow("رقم الهاتف:", self.phone_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@email.com")
        basic_layout.addRow("البريد الإلكتروني:", self.email_input)
        
        layout.addWidget(basic_group)
        
        # Address group
        address_group = QGroupBox("العنوان")
        address_layout = QFormLayout(address_group)
        
        self.city_input = QComboBox()
        self.city_input.setEditable(True)
        self.city_input.addItems([
            "الرياض", "جدة", "الدمام", "مكة", "المدينة",
            "تبوك", "أبها", "حائل", "الجبيل", "الطائف"
        ])
        address_layout.addRow("المدينة:", self.city_input)
        
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("العنوان التفصيلي")
        address_layout.addRow("العنوان:", self.address_input)
        
        layout.addWidget(address_group)
        
        # Additional info
        info_group = QGroupBox("معلومات إضافية")
        info_layout = QFormLayout(info_group)
        
        self.loyalty_points_input = QSpinBox()
        self.loyalty_points_input.setMaximum(999999)
        info_layout.addRow("نقاط الولاء:", self.loyalty_points_input)
        
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setPlaceholderText("ملاحظات حول العميل")
        info_layout.addRow("ملاحظات:", self.notes_input)
        
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
        """Load existing customer data for editing"""
        if self.customer_id:
            # Load customer data from database
            pass
            
    def get_customer_data(self):
        """Get customer data from form"""
        return {
            'name': self.name_input.text(),
            'phone': self.phone_input.text(),
            'email': self.email_input.text(),
            'city': self.city_input.currentText(),
            'address': self.address_input.toPlainText(),
            'loyalty_points': self.loyalty_points_input.value(),
            'notes': self.notes_input.toPlainText()
        }