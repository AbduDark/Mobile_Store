# Mobile Shop Management System

## Overview

A Windows desktop application for managing mobile phone retail shops, built with Python PyQt6 and featuring a complete Arabic (RTL) user interface. The system provides comprehensive management for products, inventory, customers, suppliers, financial reporting, and mobile/payment services. The application is designed as a professional desktop solution with modern UI components, database integration, charts, notifications, and deployment capabilities.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**December 2024 - PyQt6 Migration Complete**
- Successfully migrated entire application from Tkinter to PyQt6 architecture
- Implemented professional database management with SQLite integration  
- Added advanced UI components including data tables, charts (PyQtGraph/matplotlib), and modern dialogs
- Created comprehensive notification system and enhanced theme management
- Developed modular structure with separate components for products, customers, suppliers, reports, services, and settings
- Integrated build scripts with PyInstaller for professional deployment
- Set up new PyQt6 workflow while maintaining Arabic RTL interface throughout

## System Architecture

### Frontend Architecture
- **Framework**: Python PyQt6 with professional desktop components
- **Layout System**: Modular sidebar navigation with advanced tabbed content areas
- **Theme Management**: Comprehensive theme system with light/dark modes and full styling
- **RTL Support**: Native PyQt6 RTL support for proper Arabic text alignment and layouts
- **Widget System**: Custom PyQt6 widgets extending base components for Arabic support
- **Charts & Visualization**: PyQtGraph and matplotlib integration for data visualization

### UI/UX Design Pattern
- **Navigation**: Sidebar-based navigation with emoji icons and Arabic labels
- **Content Layout**: Tabbed interface within each module for organized functionality
- **Data Presentation**: Custom data tables with RTL alignment, search, and filtering
- **Forms**: Form field components with Arabic labels and RTL input support
- **Statistics**: Card-based statistics display with color-coded metrics

### Module Structure
- **Products Module**: Advanced product management with inventory tracking, stock alerts, and data visualization
- **Customers Module**: Comprehensive customer database, purchase history, loyalty program, and relationship management
- **Suppliers Module**: Supplier management, order tracking, payment processing, and financial management
- **Reports Module**: Advanced reporting with sales analysis, inventory reports, financial summaries, and interactive charts
- **Services Module**: Mobile recharge services, bill payment services, transaction history, and commission tracking
- **Settings Module**: Complete application configuration, theme management, backup settings, and business preferences

### Data Management
- **SQLite Database**: Professional database implementation with full schema
- **Database Manager**: Comprehensive CRUD operations, backup/restore, and data integrity
- **Settings Manager**: QSettings-based configuration management with change notifications
- **Data Models**: Structured database models for all business entities

### Theme System
- **Light Theme**: Clean white background with subtle grays and accent colors
- **Dark Theme**: Dark background with contrasting elements for better visibility
- **Color Palette**: Semantic color system (success, warning, error, accent colors)
- **Font Management**: Arabic-friendly font selection (Tahoma, Cairo, Amiri)

## External Dependencies

### Core Dependencies
- **Python 3.11+**: Runtime environment with modern features
- **PyQt6 6.4.2+**: Professional GUI framework with native widgets
- **PyQtGraph**: High-performance plotting and data visualization
- **matplotlib**: Advanced charting and statistical plotting
- **SQLite3**: Built-in database engine (included with Python)
- **requests**: HTTP client for external service integration
- **schedule**: Task scheduling for automated backups
- **pyinstaller**: Application packaging and deployment

### Font Requirements
- **Tahoma**: Primary Arabic font (usually available on Windows)
- **Cairo**: Modern Arabic font for enhanced readability
- **Amiri**: Traditional Arabic font for formal documents
- **System fonts**: Automatic fallback to system Arabic fonts

### System Requirements
- **Windows Desktop**: Optimized for Windows 10/11 desktop environment
- **Display**: Minimum 1200x800 resolution, optimized for 1920x1080
- **Memory**: 4GB RAM recommended for optimal performance
- **Storage**: 500MB available space for installation
- **Arabic Language Support**: Full Unicode and RTL text rendering support

### Professional Features
- **Database Integration**: Complete SQLite database with advanced queries
- **Backup & Restore**: Automated backup system with cloud sync capabilities  
- **Report Export**: PDF and Excel export functionality for reports
- **Deployment System**: Professional installer and portable deployment options
- **Notification System**: Toast notifications and system integration
- **Multi-tab Interface**: Advanced workspace management with tab support