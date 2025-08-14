#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Data Table Widget
"""

from PyQt6.QtWidgets import QTableWidget, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt
from typing import List, Tuple

class EnhancedTableWidget(QTableWidget):
    def __init__(self, columns: List[Tuple[str, int, bool]]):
        super().__init__()
        self.setup_table(columns)
        
    def setup_table(self, columns: List[Tuple[str, int, bool]]):
        """Setup table with column definitions"""
        self.setColumnCount(len(columns))
        
        headers = []
        for i, (header, width, resizable) in enumerate(columns):
            headers.append(header)
            self.setColumnWidth(i, width)
            
        self.setHorizontalHeaderLabels(headers)
        
        # Configure headers
        h_header = self.horizontalHeader()
        h_header.setStretchLastSection(True)
        
        # Configure selection
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        
        # Configure scrolling
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)