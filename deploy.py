#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deployment Script for Mobile Shop Management System
Handles testing, packaging, and deployment preparation
"""

import os
import sys
import subprocess
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

class MobileShopDeployment:
    def __init__(self):
        self.version = "2.0.0"
        self.app_name = "MobileShopSystem"
        self.build_dir = "dist"
        self.package_dir = "packages"
        
    def run_tests(self):
        """Run application tests"""
        print("🧪 Running tests...")
        
        # Basic import tests
        try:
            sys.path.insert(0, 'src')
            from database.db_manager import DatabaseManager
            from utils.settings_manager import SettingsManager
            from ui.theme_manager import ThemeManager
            
            print("✅ Core modules import successfully")
            
            # Test database initialization
            db = DatabaseManager(db_path="test.db")
            db.initialize_database()
            print("✅ Database initialization test passed")
            
            # Clean up test database
            if os.path.exists("test.db"):
                os.remove("test.db")
                
            return True
            
        except Exception as e:
            print(f"❌ Tests failed: {e}")
            return False
    
    def check_dependencies(self):
        """Check if all dependencies are available"""
        print("📋 Checking dependencies...")
        
        required_packages = [
            'PyQt6', 'pyqtgraph', 'matplotlib', 
            'requests', 'schedule', 'pyinstaller'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.lower().replace('-', '_'))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} - Missing")
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("Install them with: pip install " + " ".join(missing_packages))
            return False
            
        return True
    
    def build_application(self):
        """Build the application"""
        print("🔨 Building application...")
        
        try:
            # Run build script
            result = subprocess.run([sys.executable, "build_script.py"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Build completed successfully")
                return True
            else:
                print("❌ Build failed:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    def create_portable_package(self):
        """Create portable package"""
        print("📦 Creating portable package...")
        
        if not os.path.exists(self.build_dir):
            print(f"❌ Build directory {self.build_dir} not found")
            return False
        
        # Create packages directory
        os.makedirs(self.package_dir, exist_ok=True)
        
        # Create portable folder
        portable_dir = os.path.join(self.package_dir, f"{self.app_name}_Portable_v{self.version}")
        
        if os.path.exists(portable_dir):
            shutil.rmtree(portable_dir)
        
        os.makedirs(portable_dir)
        
        try:
            # Copy executable
            exe_file = os.path.join(self.build_dir, f"{self.app_name}.exe")
            if os.path.exists(exe_file):
                shutil.copy2(exe_file, portable_dir)
            else:
                print(f"❌ Executable not found: {exe_file}")
                return False
            
            # Copy assets if they exist
            if os.path.exists("assets"):
                shutil.copytree("assets", os.path.join(portable_dir, "assets"))
            
            # Copy documentation
            docs = ["README.txt", "LICENSE.txt"]
            for doc in docs:
                if os.path.exists(doc):
                    shutil.copy2(doc, portable_dir)
            
            # Create run script
            run_script = f'''@echo off
cd /d "%~dp0"
start "" "{self.app_name}.exe"
'''
            with open(os.path.join(portable_dir, "Run.bat"), 'w') as f:
                f.write(run_script)
            
            print(f"✅ Portable package created: {portable_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create portable package: {e}")
            return False
    
    def create_zip_archive(self):
        """Create ZIP archive of portable package"""
        print("🗜️  Creating ZIP archive...")
        
        portable_dir = os.path.join(self.package_dir, f"{self.app_name}_Portable_v{self.version}")
        
        if not os.path.exists(portable_dir):
            print("❌ Portable package not found")
            return False
        
        try:
            zip_filename = f"{self.app_name}_Portable_v{self.version}.zip"
            zip_path = os.path.join(self.package_dir, zip_filename)
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(portable_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.package_dir)
                        zipf.write(file_path, arcname)
            
            print(f"✅ ZIP archive created: {zip_path}")
            
            # Show file size
            size_mb = os.path.getsize(zip_path) / (1024 * 1024)
            print(f"📏 Archive size: {size_mb:.1f} MB")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to create ZIP archive: {e}")
            return False
    
    def generate_deployment_report(self):
        """Generate deployment report"""
        print("📄 Generating deployment report...")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
نظام إدارة محل الموبايل - تقرير النشر
=====================================

معلومات النشر:
• الإصدار: {self.version}
• تاريخ البناء: {timestamp}
• اسم التطبيق: {self.app_name}

الملفات المُنشأة:
"""
        
        # Check what files were created
        files_created = []
        
        exe_file = os.path.join(self.build_dir, f"{self.app_name}.exe")
        if os.path.exists(exe_file):
            size_mb = os.path.getsize(exe_file) / (1024 * 1024)
            files_created.append(f"• {exe_file} ({size_mb:.1f} MB)")
        
        portable_dir = os.path.join(self.package_dir, f"{self.app_name}_Portable_v{self.version}")
        if os.path.exists(portable_dir):
            files_created.append(f"• {portable_dir}/")
        
        zip_file = os.path.join(self.package_dir, f"{self.app_name}_Portable_v{self.version}.zip")
        if os.path.exists(zip_file):
            size_mb = os.path.getsize(zip_file) / (1024 * 1024)
            files_created.append(f"• {zip_file} ({size_mb:.1f} MB)")
        
        if os.path.exists("installer_script.iss"):
            files_created.append("• installer_script.iss")
        
        report += "\n".join(files_created)
        
        report += f"""

خطوات النشر التالية:
1. اختبار التطبيق على أنظمة ويندوز مختلفة
2. إنشاء المثبت باستخدام Inno Setup
3. اختبار المثبت على آلة نظيفة
4. توزيع الملفات للعملاء

المتطلبات النهائية:
• Windows 10 أو أحدث
• 4 جيجابايت رام
• 500 ميجابايت مساحة فارغة
• دعم اللغة العربية في النظام

ملاحظات النشر:
• التطبيق محزم كملف تنفيذي واحد
• يتضمن جميع المكتبات المطلوبة
• يدعم تشغيل محمول بدون تثبيت
• واجهة عربية كاملة مع دعم RTL

تم إنشاء التقرير في: {timestamp}
"""
        
        report_file = os.path.join(self.package_dir, "deployment_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Deployment report created: {report_file}")
    
    def deploy(self):
        """Main deployment process"""
        print("🚀 Starting Mobile Shop System Deployment")
        print("=" * 60)
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed. Please install missing packages.")
            return False
        
        # Step 2: Run tests
        if not self.run_tests():
            print("❌ Tests failed. Please fix issues before deploying.")
            return False
        
        # Step 3: Build application
        if not self.build_application():
            print("❌ Build failed. Please check build errors.")
            return False
        
        # Step 4: Create portable package
        if not self.create_portable_package():
            print("❌ Failed to create portable package.")
            return False
        
        # Step 5: Create ZIP archive
        if not self.create_zip_archive():
            print("❌ Failed to create ZIP archive.")
            return False
        
        # Step 6: Generate deployment report
        self.generate_deployment_report()
        
        print("\n✅ Deployment completed successfully!")
        print("\nDeployment artifacts:")
        print(f"• Executable: {self.build_dir}/{self.app_name}.exe")
        print(f"• Portable package: {self.package_dir}/{self.app_name}_Portable_v{self.version}/")
        print(f"• ZIP archive: {self.package_dir}/{self.app_name}_Portable_v{self.version}.zip")
        print(f"• Installer script: installer_script.iss")
        print(f"• Deployment report: {self.package_dir}/deployment_report.txt")
        
        print("\nReady for distribution! 🎉")
        
        return True

def main():
    deployment = MobileShopDeployment()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "test":
            deployment.run_tests()
        elif command == "build":
            deployment.build_application()
        elif command == "package":
            deployment.create_portable_package()
            deployment.create_zip_archive()
        elif command == "report":
            deployment.generate_deployment_report()
        else:
            print("Unknown command. Available commands: test, build, package, report")
    else:
        # Run full deployment
        deployment.deploy()

if __name__ == "__main__":
    main()