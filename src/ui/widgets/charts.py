#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chart Widgets using PyQtGraph
"""

import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

class StockChart(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_chart()
        
    def setup_chart(self):
        """Setup the stock chart"""
        layout = QVBoxLayout(self)
        
        # Create plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.setLabel('left', 'الكمية')
        self.plot_widget.setLabel('bottom', 'المنتجات')
        self.plot_widget.showGrid(True, True)
        
        layout.addWidget(self.plot_widget)
        
    def update_data(self, products):
        """Update chart with product data"""
        # Clear previous data
        self.plot_widget.clear()
        
        # Sample data visualization
        x = list(range(len(products)))
        y = [p.get('stock_quantity', 0) for p in products]
        
        self.plot_widget.plot(x, y, pen='b', symbol='o')