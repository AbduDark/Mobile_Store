#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Script for Mobile Shop Management System
Creates a Windows executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build_directories():
    """Clean previous build directories"""
    directories_to_clean = ['build', 'dist', '__pycache__']
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            shutil.rmtree(directory)
            print(f"Cleaned directory: {directory}")
            
def create_pyinstaller_spec():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

a = Analysis(
    ['main_pyqt6.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('src', 'src'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'pyqtgraph',
        'matplotlib',
        'sqlite3',
        'requests',
        'schedule'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MobileShopSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
    version='version_info.txt'
)
'''
    
    with open('MobileShopSystem.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file")

def create_version_info():
    """Create version info file for Windows executable"""
    version_info = '''
# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(2, 0, 0, 0),
    prodvers=(2, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Mobile Shop Solutions'),
        StringStruct(u'FileDescription', u'Mobile Shop Management System'),
        StringStruct(u'FileVersion', u'2.0.0.0'),
        StringStruct(u'InternalName', u'MobileShopSystem'),
        StringStruct(u'LegalCopyright', u'© 2024 Mobile Shop Solutions'),
        StringStruct(u'OriginalFilename', u'MobileShopSystem.exe'),
        StringStruct(u'ProductName', u'نظام إدارة محل الموبايل'),
        StringStruct(u'ProductVersion', u'2.0.0.0')])
    ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("Created version info file")

def create_default_icon():
    """Create a default icon file if not exists"""
    if not os.path.exists('assets/icon.ico'):
        os.makedirs('assets', exist_ok=True)
        # For now, we'll skip icon creation - in real deployment,
        # you would include a proper .ico file
        print("Note: Create an icon file at assets/icon.ico for better branding")

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        print("Building executable with PyInstaller...")
        
        # Run PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--onefile',
            '--windowed',
            '--name', 'MobileShopSystem',
            '--distpath', 'dist',
            '--workpath', 'build',
            'MobileShopSystem.spec'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            print(f"Output location: {os.path.abspath('dist/MobileShopSystem.exe')}")
        else:
            print("❌ Build failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False
        
    return True

def create_installer_script():
    """Create Inno Setup installer script"""
    installer_script = '''
[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-1234567890AB}}
AppName=نظام إدارة محل الموبايل
AppVersion=2.0.0
AppVerName=نظام إدارة محل الموبايل 2.0.0
AppPublisher=Mobile Shop Solutions
AppPublisherURL=https://mobileshopsolutions.com
AppSupportURL=https://mobileshopsolutions.com/support
AppUpdatesURL=https://mobileshopsolutions.com/updates
DefaultDirName={autopf}\\Mobile Shop System
DefaultGroupName=Mobile Shop System
AllowNoIcons=yes
LicenseFile=LICENSE.txt
InfoBeforeFile=README.txt
OutputDir=installer
OutputBaseFilename=MobileShopSystem_Setup_v2.0.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets\\icon.ico
UninstallDisplayIcon={app}\\MobileShopSystem.exe

[Languages]
Name: "arabic"; MessagesFile: "compiler:Languages\\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\MobileShopSystem.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\\*"; DestDir: "{app}\\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\نظام إدارة محل الموبايل"; Filename: "{app}\\MobileShopSystem.exe"
Name: "{group}\\{cm:ProgramOnTheWeb,Mobile Shop System}"; Filename: "https://mobileshopsolutions.com"
Name: "{group}\\{cm:UninstallProgram,نظام إدارة محل الموبايل}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\نظام إدارة محل الموبايل"; Filename: "{app}\\MobileShopSystem.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\MobileShopSystem.exe"; Description: "{cm:LaunchProgram,نظام إدارة محل الموبايل}"; Flags: nowait postinstall skipifsilent

[Code]
function GetUninstallString(): String;
var
  sUnInstPath: String;
  sUnInstallString: String;
begin
  sUnInstPath := ExpandConstant('Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{#emit SetupSetting("AppId")}_is1');
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade(): Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function UnInstallOldVersion(): Integer;
var
  sUnInstallString: String;
  iResultCode: Integer;
begin
  Result := 0;
  sUnInstallString := GetUninstallString();
  if sUnInstallString <> '' then begin
    sUnInstallString := RemoveQuotes(sUnInstallString);
    if Exec(sUnInstallString, '/SILENT /NORESTART /SUPPRESSMSGBOXES','', SW_HIDE, ewWaitUntilTerminated, iResultCode) then
      Result := 3
    else
      Result := 2;
  end else
    Result := 1;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep=ssInstall) then
  begin
    if (IsUpgrade()) then
    begin
      UnInstallOldVersion();
    end;
  end;
end;
'''
    
    with open('installer_script.iss', 'w', encoding='utf-8') as f:
        f.write(installer_script)
    
    print("Created Inno Setup installer script")

def create_documentation():
    """Create documentation files"""
    # Create README
    readme_content = '''
نظام إدارة محل الموبايل
=====================

نظام شامل لإدارة محلات الهواتف المحمولة واكسسواراتها

المزايا الرئيسية:
• واجهة باللغة العربية مع دعم RTL
• إدارة شاملة للمنتجات والمخزون
• نظام إدارة العملاء مع برنامج الولاء
• إدارة الموردين والطلبات
• تقارير مفصلة ورسوم بيانية
• خدمات شحن الجوال ودفع الفواتير
• نسخ احتياطي تلقائي
• مظهر فاتح وداكن

متطلبات النظام:
• Windows 10 أو أحدث
• 4 جيجابايت رام أو أكثر
• 500 ميجابايت مساحة فارغة
• دعم اللغة العربية

للحصول على الدعم الفني:
support@mobileshopsolutions.com

© 2024 Mobile Shop Solutions
'''
    
    with open('README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Create LICENSE
    license_content = '''
اتفاقية ترخيص برنامج نظام إدارة محل الموبايل

هذا البرنامج محمي بحقوق الطبع والنشر لشركة Mobile Shop Solutions.

شروط الاستخدام:
1. يُسمح باستخدام هذا البرنامج للأغراض التجارية
2. يُمنع نسخ أو توزيع البرنامج بدون إذن مكتوب
3. يُمنع إعادة هندسة أو تفكيك البرنامج
4. الشركة غير مسؤولة عن أي أضرار قد تنتج عن استخدام البرنامج

للحصول على ترخيص تجاري أو مزيد من المعلومات:
contact@mobileshopsolutions.com

© 2024 Mobile Shop Solutions. جميع الحقوق محفوظة.
'''
    
    with open('LICENSE.txt', 'w', encoding='utf-8') as f:
        f.write(license_content)
    
    print("Created documentation files")

def create_requirements_file():
    """Create requirements.txt for development"""
    requirements = '''PyQt6>=6.4.2
PyQt6-tools>=6.4.2.3.3
PyQtGraph>=0.13.7
matplotlib>=3.10.5
pyinstaller>=6.15.0
requests>=2.32.4
schedule>=1.2.2
setuptools>=80.9.0
'''
    
    with open('requirements_dev.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print("Created development requirements file")

def main():
    """Main build process"""
    print("🚀 Starting build process for Mobile Shop Management System")
    print("=" * 60)
    
    # Step 1: Clean previous builds
    print("\n1. Cleaning previous builds...")
    clean_build_directories()
    
    # Step 2: Create necessary files
    print("\n2. Creating build files...")
    create_version_info()
    create_pyinstaller_spec()
    create_default_icon()
    create_documentation()
    create_requirements_file()
    
    # Step 3: Build executable
    print("\n3. Building executable...")
    if not build_executable():
        print("❌ Build failed. Please check the errors above.")
        sys.exit(1)
    
    # Step 4: Create installer script
    print("\n4. Creating installer script...")
    create_installer_script()
    
    print("\n✅ Build process completed successfully!")
    print("\nNext steps:")
    print("1. Test the executable: dist/MobileShopSystem.exe")
    print("2. Install Inno Setup and compile installer_script.iss to create installer")
    print("3. Test the installer on a clean Windows machine")
    
    print("\nFiles created:")
    print("• dist/MobileShopSystem.exe - Main executable")
    print("• installer_script.iss - Inno Setup installer script")
    print("• README.txt - User documentation") 
    print("• LICENSE.txt - License agreement")
    print("• requirements_dev.txt - Development dependencies")

if __name__ == "__main__":
    main()