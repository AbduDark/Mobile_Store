#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Sample Data Provider for Mobile Shop Management System
"""

from datetime import datetime, timedelta
import random

class ArabicData:
    def __init__(self):
        # Arabic names and data for demonstration
        self.arabic_names = [
            "أحمد محمد علي", "فاطمة حسن", "محمد عبدالله", "عائشة أحمد", "علي حسين",
            "زينب محمود", "عمر سعد", "خديجة علي", "يوسف إبراهيم", "مريم حسن",
            "حسام الدين", "نورا عبدالرحمن", "خالد محمد", "هدى السيد", "أحمد صلاح"
        ]
        
        self.phone_operators = ["فودافون", "أورانج", "إتصالات", "WE"]
        self.product_categories = ["موبايلات", "إكسسوارات", "شواحن", "سماعات", "جرابات"]
        self.product_brands = ["سامسونج", "آيفون", "هواوي", "شاومي", "ريلمي", "أوبو"]
        self.cities = ["القاهرة", "الجيزة", "الاسكندرية", "طنطا", "المنصورة", "أسيوط"]
        
    def get_sample_products(self):
        """Generate sample products data"""
        products = []
        for i in range(50):
            category = random.choice(self.product_categories)
            brand = random.choice(self.product_brands)
            
            if category == "موبايلات":
                name = f"{brand} - موديل {random.randint(10, 15)} برو"
                buy_price = random.randint(8000, 25000)
                sell_price = buy_price + random.randint(1000, 5000)
            else:
                name = f"{category} {brand}"
                buy_price = random.randint(50, 500)
                sell_price = buy_price + random.randint(20, 200)
                
            profit = sell_price - buy_price
            stock = random.randint(0, 50)
            
            if stock == 0:
                status = "نفد من المخزن"
            elif stock <= 5:
                status = "قليل"
            else:
                status = "متوفر"
                
            products.append({
                'barcode': f"200{i:04d}",
                'name': name,
                'category': category,
                'buy_price': buy_price,
                'sell_price': sell_price,
                'profit': profit,
                'stock': stock,
                'status': status
            })
            
        return products
        
    def get_inventory_data(self):
        """Generate inventory management data"""
        inventory = []
        products = self.get_sample_products()[:20]  # First 20 products
        
        for product in products:
            last_restock = datetime.now() - timedelta(days=random.randint(1, 30))
            supplier = f"مورد {random.choice(['الأجهزة الذكية', 'التكنولوجيا المتقدمة', 'الإلكترونيات الحديثة'])}"
            
            inventory.append({
                'name': product['name'],
                'current_stock': product['stock'],
                'min_stock': random.randint(5, 10),
                'max_stock': random.randint(50, 100),
                'last_restock': last_restock.strftime("%Y-%m-%d"),
                'supplier': supplier
            })
            
        return inventory
        
    def get_sample_customers(self):
        """Generate sample customers data"""
        customers = []
        for i, name in enumerate(self.arabic_names):
            total_purchases = random.randint(500, 15000)
            last_visit = datetime.now() - timedelta(days=random.randint(1, 90))
            
            customers.append({
                'id': f"C{1000 + i}",
                'name': name,
                'phone': f"01{random.randint(100000000, 999999999)}",
                'email': f"customer{i+1}@email.com",
                'address': f"شارع {random.randint(1, 50)}، {random.choice(self.cities)}",
                'total_purchases': total_purchases,
                'last_visit': last_visit.strftime("%Y-%m-%d"),
                'status': random.choice(["نشط", "غير نشط"])
            })
            
        return customers
        
    def get_customer_names(self):
        """Get list of customer names for comboboxes"""
        return self.arabic_names
        
    def get_customer_history(self):
        """Generate customer purchase history"""
        history = []
        for i in range(20):
            date = datetime.now() - timedelta(days=random.randint(1, 365))
            invoice_no = f"INV{2024}{random.randint(1000, 9999)}"
            items_count = random.randint(1, 5)
            total = random.randint(100, 5000)
            
            history.append({
                'date': date.strftime("%Y-%m-%d"),
                'invoice_no': invoice_no,
                'items': f"{items_count} منتج",
                'total': total,
                'payment_method': random.choice(["نقداً", "فيزا", "فودافون كاش"]),
                'status': random.choice(["مدفوع", "آجل", "مدفوع جزئياً"])
            })
            
        return history
        
    def get_sample_suppliers(self):
        """Generate sample suppliers data"""
        suppliers = []
        supplier_names = [
            "شركة الأجهزة الذكية", "مؤسسة التكنولوجيا المتقدمة", "شركة الإلكترونيات الحديثة",
            "مورد الموبايلات المتخصص", "شركة الاتصالات والتقنية", "مؤسسة الأجهزة المحمولة"
        ]
        
        for i, company in enumerate(supplier_names):
            total_purchases = random.randint(50000, 500000)
            outstanding = random.randint(0, 50000)
            
            suppliers.append({
                'id': f"S{100 + i}",
                'name': company,
                'contact_person': random.choice(self.arabic_names),
                'phone': f"02{random.randint(10000000, 99999999)}",
                'address': f"شارع {random.randint(1, 100)}، {random.choice(self.cities)}",
                'total_purchases': total_purchases,
                'outstanding_balance': outstanding,
                'status': "نشط" if outstanding < 30000 else "متأخر"
            })
            
        return suppliers
        
    def get_supplier_invoices(self):
        """Generate supplier invoices data"""
        invoices = []
        for i in range(30):
            date = datetime.now() - timedelta(days=random.randint(1, 180))
            due_date = date + timedelta(days=random.randint(15, 60))
            total = random.randint(5000, 50000)
            paid = random.randint(0, total)
            remaining = total - paid
            
            if remaining == 0:
                status = "مدفوعة"
            elif due_date < datetime.now():
                status = "متأخرة"
            else:
                status = "آجلة"
                
            invoices.append({
                'invoice_no': f"SUP{2024}{1000 + i}",
                'supplier': f"مورد {random.randint(1, 6)}",
                'date': date.strftime("%Y-%m-%d"),
                'due_date': due_date.strftime("%Y-%m-%d"),
                'total': total,
                'paid': paid,
                'remaining': remaining,
                'status': status
            })
            
        return invoices
        
    def get_inventory_report_data(self):
        """Generate inventory report data"""
        report_data = []
        products = self.get_sample_products()[:30]
        
        for product in products:
            unit_cost = product['buy_price']
            total_value = unit_cost * product['stock']
            last_update = datetime.now() - timedelta(days=random.randint(1, 30))
            
            report_data.append({
                'product_name': product['name'],
                'category': product['category'],
                'current_stock': product['stock'],
                'min_stock': random.randint(5, 10),
                'unit_cost': unit_cost,
                'total_value': total_value,
                'last_update': last_update.strftime("%Y-%m-%d"),
                'status': product['status']
            })
            
        return report_data
        
    def get_financial_report_data(self):
        """Generate financial report data"""
        financial_data = []
        months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"]
        
        for month in months:
            revenue = random.randint(40000, 80000)
            costs = revenue * random.uniform(0.6, 0.8)
            profit = revenue - costs
            margin = (profit / revenue) * 100
            expenses = random.randint(5000, 15000)
            net_profit = profit - expenses
            
            financial_data.append({
                'period': month,
                'revenue': int(revenue),
                'costs': int(costs),
                'profit': int(profit),
                'margin': round(margin, 1),
                'expenses': expenses,
                'net_profit': int(net_profit)
            })
            
        return financial_data
        
    def get_saved_reports(self):
        """Generate saved reports data"""
        reports = [
            {
                'name': "تقرير المبيعات الشهرية",
                'type': "مبيعات",
                'created_date': "2024-01-01",
                'last_run': "2024-01-15",
                'description': "تقرير شامل للمبيعات الشهرية"
            },
            {
                'name': "تقرير المخزون المنخفض",
                'type': "مخزون",
                'created_date': "2024-01-05",
                'last_run': "2024-01-14",
                'description': "المنتجات التي تحتاج إعادة تموين"
            },
            {
                'name': "تقرير أداء الموردين",
                'type': "موردين",
                'created_date': "2024-01-10",
                'last_run': "2024-01-13",
                'description': "تقييم أداء الموردين والمدفوعات"
            }
        ]
        return reports
        
    def get_recent_balance_transactions(self):
        """Generate recent balance service transactions"""
        transactions = []
        services = ["فودافون كاش", "أورانج موني", "إتصالات كاش", "فوري"]
        
        for i in range(20):
            time = datetime.now() - timedelta(hours=random.randint(1, 48))
            service = random.choice(services)
            customer = random.choice(self.arabic_names)
            amount = random.randint(50, 1000)
            commission = amount * 0.02  # 2% commission
            
            transactions.append({
                'time': time.strftime("%H:%M"),
                'service': service,
                'customer': customer,
                'amount': amount,
                'commission': round(commission, 2),
                'status': random.choice(["مكتملة", "معلقة", "فاشلة"])
            })
            
        return transactions
        
    def get_recharge_history(self):
        """Generate mobile recharge history"""
        history = []
        for i in range(25):
            date = datetime.now() - timedelta(days=random.randint(1, 30))
            phone = f"01{random.randint(100000000, 999999999)}"
            operator = random.choice(self.phone_operators)
            amount = random.choice([5, 10, 15, 20, 25, 50, 100])
            commission = random.uniform(0.5, 2.0)
            
            history.append({
                'date': date.strftime("%Y-%m-%d"),
                'phone': phone,
                'operator': operator,
                'amount': amount,
                'commission': round(commission, 2),
                'customer': random.choice(self.arabic_names),
                'status': random.choice(["مكتملة", "فاشلة"])
            })
            
        return history
        
    def get_payment_history(self):
        """Generate bill payment history"""
        history = []
        services = ["كهرباء", "مياه", "تليفون", "انترنت", "غاز"]
        
        for i in range(30):
            date = datetime.now() - timedelta(days=random.randint(1, 60))
            service = random.choice(services)
            account = f"{random.randint(100000, 999999)}"
            amount = random.randint(100, 2000)
            commission = random.uniform(5, 20)
            
            history.append({
                'date': date.strftime("%Y-%m-%d"),
                'service': service,
                'account': account,
                'amount': amount,
                'commission': round(commission, 2),
                'customer': random.choice(self.arabic_names),
                'status': random.choice(["مدفوعة", "فاشلة", "معلقة"])
            })
            
        return history
        
    def get_services_breakdown(self):
        """Generate services breakdown for reports"""
        services = [
            "فودافون كاش", "أورانج موني", "إتصالات كاش", "شحن رصيد",
            "فواتير الكهرباء", "فواتير المياه", "فواتير التليفون"
        ]
        
        breakdown = []
        total_transactions = 0
        total_amount = 0
        
        for service in services:
            transactions = random.randint(50, 200)
            amount = random.randint(10000, 50000)
            commission = amount * random.uniform(0.02, 0.05)
            avg_commission = commission / transactions
            
            total_transactions += transactions
            total_amount += amount
            
            breakdown.append({
                'service': service,
                'transactions': transactions,
                'total_amount': amount,
                'total_commission': round(commission, 2),
                'avg_commission': round(avg_commission, 2),
                'percentage': 0  # Will be calculated after all services
            })
            
        # Calculate percentages
        for item in breakdown:
            item['percentage'] = round((item['total_amount'] / total_amount) * 100, 1)
            
        return breakdown
