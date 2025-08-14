#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Services Management Module (Balance/Payment Services)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from widgets import DataTable, FormField, StatsCard, RTLButton, RTLLabel
from arabic_data import ArabicData

class ServicesModule:
    def __init__(self, parent, theme_manager):
        self.parent = parent
        self.theme_manager = theme_manager
        self.arabic_data = ArabicData()
        self.main_frame = None
        self.setup_module()
        
    def setup_module(self):
        """Setup the services management interface"""
        self.main_frame = tk.Frame(self.parent)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_balance_services_tab()
        self.create_mobile_recharge_tab()
        self.create_payment_services_tab()
        self.create_services_reports_tab()
        
    def create_balance_services_tab(self):
        """Create balance services tab"""
        balance_frame = tk.Frame(self.notebook)
        self.notebook.add(balance_frame, text="خدمات الرصيد")
        
        # Services stats
        stats_frame = tk.Frame(balance_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        balance_stats = [
            ("إجمالي خدمات الرصيد", "25,780 ج.م", "💳", "#4CAF50"),
            ("فودافون كاش", "12,450 ج.م", "📱", "#E91E63"),
            ("أورانج موني", "8,330 ج.م", "🍊", "#FF5722"),
            ("إيتصالات كاش", "5,000 ج.م", "💰", "#2196F3")
        ]
        
        for title, value, icon, color in balance_stats:
            card = StatsCard(stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Quick service buttons
        quick_frame = tk.LabelFrame(balance_frame, text="الخدمات السريعة", font=("Tahoma", 12, "bold"))
        quick_frame.pack(fill=tk.X, pady=(0, 20))
        
        services_grid = tk.Frame(quick_frame)
        services_grid.pack(fill=tk.X, padx=20, pady=20)
        
        # Service buttons in grid
        services = [
            ("💳 فودافون كاش", "#E91E63", self.vodafone_cash),
            ("🍊 أورانج موني", "#FF5722", self.orange_money),
            ("📱 إتصالات كاش", "#2196F3", self.etisalat_cash),
            ("💰 فوري", "#4CAF50", self.fawry_service),
            ("🏦 ماستركارد", "#FF9800", self.mastercard_service),
            ("💸 ويسترن يونيون", "#9C27B0", self.western_union)
        ]
        
        for i, (text, color, command) in enumerate(services):
            row = i // 3
            col = i % 3
            
            btn = RTLButton(
                services_grid,
                text=text,
                font=("Tahoma", 11, "bold"),
                bg=color,
                fg="white",
                command=command,
                width=20,
                height=2
            )
            btn.grid(row=row, column=2-col, padx=10, pady=10, sticky="ew")
            
        # Configure grid weights
        for i in range(3):
            services_grid.columnconfigure(i, weight=1)
            
        # Recent transactions table
        transactions_frame = tk.LabelFrame(balance_frame, text="العمليات الأخيرة", font=("Tahoma", 12, "bold"))
        transactions_frame.pack(fill=tk.BOTH, expand=True)
        
        transactions_columns = {
            'time': 'الوقت',
            'service': 'الخدمة',
            'customer': 'العميل',
            'amount': 'المبلغ',
            'commission': 'العمولة',
            'status': 'الحالة'
        }
        
        self.transactions_table = DataTable(transactions_frame, transactions_columns, self.theme_manager)
        self.transactions_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load recent transactions
        self.load_recent_transactions()
        
    def create_mobile_recharge_tab(self):
        """Create mobile recharge tab"""
        recharge_frame = tk.Frame(self.notebook)
        self.notebook.add(recharge_frame, text="شحن الخطوط")
        
        # Recharge form
        form_frame = tk.LabelFrame(recharge_frame, text="شحن رصيد", font=("Tahoma", 12, "bold"))
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        form_content = tk.Frame(form_frame)
        form_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Two column layout for form
        left_form = tk.Frame(form_content)
        left_form.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        right_form = tk.Frame(form_content)
        right_form.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        # Form fields
        self.recharge_fields = {}
        
        # Right side fields
        self.recharge_fields['phone'] = FormField(right_form, "رقم الهاتف *:")
        self.recharge_fields['phone'].pack(fill=tk.X, pady=5)
        
        self.recharge_fields['operator'] = FormField(
            right_form, 
            "الشبكة *:", 
            'combobox',
            values=["فودافون", "أورانج", "إتصالات", "WE"]
        )
        self.recharge_fields['operator'].pack(fill=tk.X, pady=5)
        
        self.recharge_fields['amount'] = FormField(
            right_form,
            "مبلغ الشحن *:",
            'combobox',
            values=["5", "10", "15", "20", "25", "50", "100"]
        )
        self.recharge_fields['amount'].pack(fill=tk.X, pady=5)
        
        # Left side fields
        self.recharge_fields['customer_name'] = FormField(left_form, "اسم العميل:")
        self.recharge_fields['customer_name'].pack(fill=tk.X, pady=5)
        
        self.recharge_fields['payment_method'] = FormField(
            left_form,
            "طريقة الدفع:",
            'combobox',
            values=["نقداً", "فيزا", "فودافون كاش", "أورانج موني"]
        )
        self.recharge_fields['payment_method'].pack(fill=tk.X, pady=5)
        
        self.recharge_fields['notes'] = FormField(left_form, "ملاحظات:", 'text')
        self.recharge_fields['notes'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Action buttons
        buttons_frame = tk.Frame(form_content)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        recharge_btn = RTLButton(
            buttons_frame,
            text="📱 تنفيذ الشحن",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.process_recharge
        )
        recharge_btn.pack(side=tk.RIGHT, padx=5)
        
        clear_btn = RTLButton(
            buttons_frame,
            text="🔄 مسح البيانات",
            font=("Tahoma", 11),
            command=self.clear_recharge_form
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        # Recharge history
        history_frame = tk.LabelFrame(recharge_frame, text="تاريخ عمليات الشحن", font=("Tahoma", 12, "bold"))
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        recharge_columns = {
            'date': 'التاريخ',
            'phone': 'رقم الهاتف',
            'operator': 'الشبكة',
            'amount': 'المبلغ',
            'commission': 'العمولة',
            'customer': 'العميل',
            'status': 'الحالة'
        }
        
        self.recharge_table = DataTable(history_frame, recharge_columns, self.theme_manager)
        self.recharge_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load recharge history
        self.load_recharge_history()
        
    def create_payment_services_tab(self):
        """Create payment services tab"""
        payment_frame = tk.Frame(self.notebook)
        self.notebook.add(payment_frame, text="خدمات الدفع")
        
        # Payment services grid
        services_frame = tk.LabelFrame(payment_frame, text="خدمات الدفع المتاحة", font=("Tahoma", 12, "bold"))
        services_frame.pack(fill=tk.X, pady=(0, 20))
        
        payment_grid = tk.Frame(services_frame)
        payment_grid.pack(fill=tk.X, padx=20, pady=20)
        
        # Payment services
        payment_services = [
            ("💡 دفع فاتورة الكهرباء", self.pay_electricity),
            ("💧 دفع فاتورة المياه", self.pay_water),
            ("📞 دفع فاتورة التليفون", self.pay_phone),
            ("📺 دفع الانترنت والكيبل", self.pay_internet),
            ("⛽ دفع فاتورة الغاز", self.pay_gas),
            ("🏛️ الخدمات الحكومية", self.gov_services)
        ]
        
        for i, (text, command) in enumerate(payment_services):
            row = i // 2
            col = i % 2
            
            btn = RTLButton(
                payment_grid,
                text=text,
                font=("Tahoma", 11),
                command=command,
                width=30,
                height=2
            )
            btn.grid(row=row, column=1-col, padx=10, pady=10, sticky="ew")
            
        # Configure grid weights
        for i in range(2):
            payment_grid.columnconfigure(i, weight=1)
            
        # Payment form
        payment_form_frame = tk.LabelFrame(payment_frame, text="تفاصيل الدفع", font=("Tahoma", 12, "bold"))
        payment_form_frame.pack(fill=tk.X, pady=(0, 20))
        
        payment_form_content = tk.Frame(payment_form_frame)
        payment_form_content.pack(fill=tk.X, padx=20, pady=20)
        
        # Payment form fields
        self.payment_fields = {}
        
        form_right = tk.Frame(payment_form_content)
        form_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        form_left = tk.Frame(payment_form_content)
        form_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Right side
        self.payment_fields['service_type'] = FormField(
            form_right,
            "نوع الخدمة:",
            'combobox',
            values=["كهرباء", "مياه", "تليفون", "انترنت", "غاز", "خدمات حكومية"]
        )
        self.payment_fields['service_type'].pack(fill=tk.X, pady=5)
        
        self.payment_fields['account_number'] = FormField(form_right, "رقم الحساب/الكود:")
        self.payment_fields['account_number'].pack(fill=tk.X, pady=5)
        
        self.payment_fields['customer_name'] = FormField(form_right, "اسم العميل:")
        self.payment_fields['customer_name'].pack(fill=tk.X, pady=5)
        
        # Left side
        self.payment_fields['amount'] = FormField(form_left, "المبلغ:")
        self.payment_fields['amount'].pack(fill=tk.X, pady=5)
        
        self.payment_fields['commission'] = FormField(form_left, "العمولة:")
        self.payment_fields['commission'].pack(fill=tk.X, pady=5)
        
        self.payment_fields['payment_notes'] = FormField(form_left, "ملاحظات:", 'text')
        self.payment_fields['payment_notes'].pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Payment buttons
        payment_buttons_frame = tk.Frame(payment_form_content)
        payment_buttons_frame.pack(fill=tk.X, pady=10)
        
        process_payment_btn = RTLButton(
            payment_buttons_frame,
            text="💳 تنفيذ الدفع",
            font=("Tahoma", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.process_payment
        )
        process_payment_btn.pack(side=tk.RIGHT, padx=5)
        
        # Payment history
        payment_history_frame = tk.LabelFrame(payment_frame, text="سجل المدفوعات", font=("Tahoma", 12, "bold"))
        payment_history_frame.pack(fill=tk.BOTH, expand=True)
        
        payment_columns = {
            'date': 'التاريخ',
            'service': 'الخدمة',
            'account': 'رقم الحساب',
            'amount': 'المبلغ',
            'commission': 'العمولة',
            'customer': 'العميل',
            'status': 'الحالة'
        }
        
        self.payment_table = DataTable(payment_history_frame, payment_columns, self.theme_manager)
        self.payment_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load payment history
        self.load_payment_history()
        
    def create_services_reports_tab(self):
        """Create services reports tab"""
        reports_frame = tk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="تقارير الخدمات")
        
        # Services stats
        services_stats_frame = tk.Frame(reports_frame)
        services_stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        services_stats = [
            ("إجمالي العمولات", "3,250 ج.م", "💰", "#4CAF50"),
            ("عدد العمليات", "847", "📊", "#2196F3"),
            ("متوسط العمولة", "3.8 ج.م", "📈", "#FF9800"),
            ("أعلى خدمة ربحاً", "فودافون كاش", "🏆", "#9C27B0")
        ]
        
        for title, value, icon, color in services_stats:
            card = StatsCard(services_stats_frame, title, value, icon, color)
            card.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
            
        # Report controls
        controls_frame = tk.Frame(reports_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Date range
        RTLLabel(controls_frame, text="من تاريخ:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        from_date = tk.Entry(controls_frame, font=("Tahoma", 10), width=12, justify='right')
        from_date.pack(side=tk.RIGHT, padx=5)
        from_date.insert(0, "2024-01-01")
        
        RTLLabel(controls_frame, text="إلى تاريخ:", font=("Tahoma", 10)).pack(side=tk.RIGHT, padx=5)
        to_date = tk.Entry(controls_frame, font=("Tahoma", 10), width=12, justify='right')
        to_date.pack(side=tk.RIGHT, padx=5)
        to_date.insert(0, "2024-12-31")
        
        RTLButton(
            controls_frame,
            text="📊 إنشاء تقرير",
            font=("Tahoma", 10),
            command=self.generate_services_report
        ).pack(side=tk.RIGHT, padx=10)
        
        # Services breakdown
        breakdown_frame = tk.LabelFrame(reports_frame, text="تفصيل الخدمات", font=("Tahoma", 12, "bold"))
        breakdown_frame.pack(fill=tk.BOTH, expand=True)
        
        breakdown_columns = {
            'service': 'الخدمة',
            'transactions': 'عدد العمليات',
            'total_amount': 'إجمالي المبالغ',
            'total_commission': 'إجمالي العمولات',
            'avg_commission': 'متوسط العمولة',
            'percentage': 'النسبة من الإجمالي'
        }
        
        self.services_breakdown_table = DataTable(breakdown_frame, breakdown_columns, self.theme_manager)
        self.services_breakdown_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load services breakdown
        self.load_services_breakdown()
        
    def load_recent_transactions(self):
        """Load recent transactions"""
        transactions = self.arabic_data.get_recent_balance_transactions()
        
        for transaction in transactions:
            self.transactions_table.add_row([
                transaction['time'],
                transaction['service'],
                transaction['customer'],
                f"{transaction['amount']} ج.م",
                f"{transaction['commission']} ج.م",
                transaction['status']
            ])
            
    def load_recharge_history(self):
        """Load recharge history"""
        history = self.arabic_data.get_recharge_history()
        
        for record in history:
            self.recharge_table.add_row([
                record['date'],
                record['phone'],
                record['operator'],
                f"{record['amount']} ج.م",
                f"{record['commission']} ج.م",
                record['customer'],
                record['status']
            ])
            
    def load_payment_history(self):
        """Load payment history"""
        history = self.arabic_data.get_payment_history()
        
        for record in history:
            self.payment_table.add_row([
                record['date'],
                record['service'],
                record['account'],
                f"{record['amount']} ج.م",
                f"{record['commission']} ج.م",
                record['customer'],
                record['status']
            ])
            
    def load_services_breakdown(self):
        """Load services breakdown"""
        breakdown = self.arabic_data.get_services_breakdown()
        
        for service in breakdown:
            self.services_breakdown_table.add_row([
                service['service'],
                service['transactions'],
                f"{service['total_amount']} ج.م",
                f"{service['total_commission']} ج.م",
                f"{service['avg_commission']} ج.م",
                f"{service['percentage']}%"
            ])
    
    # Service action methods
    def vodafone_cash(self):
        messagebox.showinfo("فودافون كاش", "فتح خدمة فودافون كاش")
        
    def orange_money(self):
        messagebox.showinfo("أورانج موني", "فتح خدمة أورانج موني")
        
    def etisalat_cash(self):
        messagebox.showinfo("إتصالات كاش", "فتح خدمة إتصالات كاش")
        
    def fawry_service(self):
        messagebox.showinfo("فوري", "فتح خدمة فوري")
        
    def mastercard_service(self):
        messagebox.showinfo("ماستركارد", "فتح خدمة ماستركارد")
        
    def western_union(self):
        messagebox.showinfo("ويسترن يونيون", "فتح خدمة ويسترن يونيون")
        
    def process_recharge(self):
        """Process mobile recharge"""
        phone = self.recharge_fields['phone'].get_value()
        amount = self.recharge_fields['amount'].get_value()
        
        if not phone or not amount:
            messagebox.showerror("خطأ", "يجب إدخال رقم الهاتف ومبلغ الشحن")
            return
            
        messagebox.showinfo("نجح الشحن", f"تم شحن رقم {phone} بمبلغ {amount} جنيه بنجاح")
        self.clear_recharge_form()
        
    def clear_recharge_form(self):
        """Clear recharge form"""
        for field in self.recharge_fields.values():
            field.set_value("")
            
    def pay_electricity(self):
        self.payment_fields['service_type'].set_value("كهرباء")
        
    def pay_water(self):
        self.payment_fields['service_type'].set_value("مياه")
        
    def pay_phone(self):
        self.payment_fields['service_type'].set_value("تليفون")
        
    def pay_internet(self):
        self.payment_fields['service_type'].set_value("انترنت")
        
    def pay_gas(self):
        self.payment_fields['service_type'].set_value("غاز")
        
    def gov_services(self):
        self.payment_fields['service_type'].set_value("خدمات حكومية")
        
    def process_payment(self):
        """Process bill payment"""
        service = self.payment_fields['service_type'].get_value()
        account = self.payment_fields['account_number'].get_value()
        amount = self.payment_fields['amount'].get_value()
        
        if not service or not account or not amount:
            messagebox.showerror("خطأ", "يجب إدخال جميع البيانات المطلوبة")
            return
            
        messagebox.showinfo("نجح الدفع", f"تم دفع فاتورة {service} لحساب {account} بمبلغ {amount} جنيه")
        
    def generate_services_report(self):
        """Generate services report"""
        messagebox.showinfo("تقرير الخدمات", "تم إنشاء تقرير الخدمات بنجاح")
    
    def show(self):
        """Show the module"""
        if self.main_frame:
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
    def hide(self):
        """Hide the module"""
        if self.main_frame:
            self.main_frame.pack_forget()
            
    def update_theme(self):
        """Update module theme"""
        if self.theme_manager and self.main_frame:
            colors = self.theme_manager.get_colors()
            self.main_frame.config(bg=colors['bg'])
