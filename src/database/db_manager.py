#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Manager - SQLite Database Operations
"""

import sqlite3
import os
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "data/mobile_shop.db"):
        self.db_path = db_path
        self.backup_dir = "backups"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Ensure database and backup directories exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper settings"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return conn
        
    def initialize_database(self):
        """Initialize database with all required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    brand TEXT,
                    model TEXT,
                    category TEXT,
                    price DECIMAL(10,2) NOT NULL,
                    cost DECIMAL(10,2),
                    stock_quantity INTEGER DEFAULT 0,
                    min_stock_level INTEGER DEFAULT 5,
                    barcode TEXT UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Customers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT,
                    address TEXT,
                    city TEXT,
                    total_purchases DECIMAL(10,2) DEFAULT 0,
                    loyalty_points INTEGER DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Suppliers table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    company TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT,
                    payment_terms TEXT,
                    total_orders DECIMAL(10,2) DEFAULT 0,
                    outstanding_balance DECIMAL(10,2) DEFAULT 0,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Sales table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    total_amount DECIMAL(10,2) NOT NULL,
                    discount_amount DECIMAL(10,2) DEFAULT 0,
                    tax_amount DECIMAL(10,2) DEFAULT 0,
                    payment_method TEXT,
                    status TEXT DEFAULT 'completed',
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Sale items table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10,2) NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            
            # Services table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER,
                    service_type TEXT NOT NULL,
                    description TEXT,
                    amount DECIMAL(10,2) NOT NULL,
                    commission DECIMAL(10,2) DEFAULT 0,
                    status TEXT DEFAULT 'completed',
                    reference_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (customer_id) REFERENCES customers (id)
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            
        # Insert default settings if they don't exist
        self.setup_default_settings()
        
    def setup_default_settings(self):
        """Insert default application settings"""
        default_settings = {
            'theme': 'light',
            'language': 'ar',
            'auto_backup': 'true',
            'backup_frequency': 'daily',
            'tax_rate': '15.0',
            'currency': 'ريال',
            'low_stock_alert': 'true'
        }
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for key, value in default_settings.items():
                cursor.execute('''
                    INSERT OR IGNORE INTO settings (key, value)
                    VALUES (?, ?)
                ''', (key, value))
            conn.commit()
    
    def backup_database(self) -> str:
        """Create a backup of the database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"mobile_shop_backup_{timestamp}.db"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        shutil.copy2(self.db_path, backup_path)
        return backup_path
    
    def auto_cleanup_backups(self, keep_days: int = 30):
        """Clean up old backup files"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for backup_file in os.listdir(self.backup_dir):
            if backup_file.endswith('.db'):
                file_path = os.path.join(self.backup_dir, backup_file)
                file_time = datetime.fromtimestamp(os.path.getctime(file_path))
                if file_time < cutoff_date:
                    os.remove(file_path)
    
    # Product operations
    def add_product(self, product_data: Dict[str, Any]) -> int:
        """Add a new product to the database"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, brand, model, category, price, cost, 
                                    stock_quantity, min_stock_level, barcode, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('name'),
                product_data.get('brand'),
                product_data.get('model'),
                product_data.get('category'),
                product_data.get('price'),
                product_data.get('cost'),
                product_data.get('stock_quantity', 0),
                product_data.get('min_stock_level', 5),
                product_data.get('barcode'),
                product_data.get('description')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_products(self, search_term: str = '', category: str = '') -> List[Dict]:
        """Get products with optional filtering"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM products WHERE 1=1"
            params = []
            
            if search_term:
                query += " AND (name LIKE ? OR brand LIKE ? OR model LIKE ? OR barcode LIKE ?)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern] * 4)
                
            if category:
                query += " AND category = ?"
                params.append(category)
                
            query += " ORDER BY name"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def update_product(self, product_id: int, product_data: Dict[str, Any]) -> bool:
        """Update product information"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE products SET 
                    name = ?, brand = ?, model = ?, category = ?, price = ?, 
                    cost = ?, stock_quantity = ?, min_stock_level = ?, 
                    barcode = ?, description = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                product_data.get('name'),
                product_data.get('brand'),
                product_data.get('model'),
                product_data.get('category'),
                product_data.get('price'),
                product_data.get('cost'),
                product_data.get('stock_quantity'),
                product_data.get('min_stock_level'),
                product_data.get('barcode'),
                product_data.get('description'),
                product_id
            ))
            conn.commit()
            return cursor.rowcount > 0
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with stock below minimum level"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM products 
                WHERE stock_quantity <= min_stock_level 
                ORDER BY stock_quantity ASC
            ''')
            return [dict(row) for row in cursor.fetchall()]
    
    # Customer operations
    def add_customer(self, customer_data: Dict[str, Any]) -> int:
        """Add a new customer"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO customers (name, phone, email, address, city, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                customer_data.get('name'),
                customer_data.get('phone'),
                customer_data.get('email'),
                customer_data.get('address'),
                customer_data.get('city'),
                customer_data.get('notes')
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_customers(self, search_term: str = '') -> List[Dict]:
        """Get customers with optional search"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            if search_term:
                cursor.execute('''
                    SELECT * FROM customers 
                    WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
                    ORDER BY name
                ''', (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
            else:
                cursor.execute("SELECT * FROM customers ORDER BY name")
                
            return [dict(row) for row in cursor.fetchall()]
    
    # Sales operations
    def add_sale(self, sale_data: Dict[str, Any], sale_items: List[Dict]) -> int:
        """Add a new sale with items"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Add sale record
            cursor.execute('''
                INSERT INTO sales (customer_id, total_amount, discount_amount, 
                                 tax_amount, payment_method, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                sale_data.get('customer_id'),
                sale_data.get('total_amount'),
                sale_data.get('discount_amount', 0),
                sale_data.get('tax_amount', 0),
                sale_data.get('payment_method'),
                sale_data.get('status', 'completed'),
                sale_data.get('notes')
            ))
            
            sale_id = cursor.lastrowid
            
            # Add sale items and update stock
            for item in sale_items:
                cursor.execute('''
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    sale_id,
                    item['product_id'],
                    item['quantity'],
                    item['unit_price'],
                    item['total_price']
                ))
                
                # Update product stock
                cursor.execute('''
                    UPDATE products SET stock_quantity = stock_quantity - ?
                    WHERE id = ?
                ''', (item['quantity'], item['product_id']))
            
            # Update customer total purchases
            if sale_data.get('customer_id'):
                cursor.execute('''
                    UPDATE customers SET 
                        total_purchases = total_purchases + ?,
                        loyalty_points = loyalty_points + ?
                    WHERE id = ?
                ''', (
                    sale_data.get('total_amount'),
                    int(sale_data.get('total_amount', 0) / 10),  # 1 point per 10 units
                    sale_data.get('customer_id')
                ))
            
            conn.commit()
            return sale_id
    
    def get_sales_report(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get sales report with date filtering"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = '''
                SELECT s.*, c.name as customer_name, c.phone as customer_phone
                FROM sales s
                LEFT JOIN customers c ON s.customer_id = c.id
                WHERE 1=1
            '''
            params = []
            
            if start_date:
                query += " AND DATE(s.created_at) >= ?"
                params.append(start_date)
                
            if end_date:
                query += " AND DATE(s.created_at) <= ?"
                params.append(end_date)
                
            query += " ORDER BY s.created_at DESC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    # Settings operations
    def get_setting(self, key: str, default_value: str = '') -> str:
        """Get a setting value"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row['value'] if row else default_value
    
    def set_setting(self, key: str, value: str):
        """Set a setting value"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
            ''', (key, value))
            conn.commit()