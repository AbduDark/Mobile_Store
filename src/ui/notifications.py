#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notification Manager - PyQt6 Notification System
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsOpacityEffect, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPaintEvent

class NotificationWidget(QFrame):
    closed = pyqtSignal()
    
    def __init__(self, title: str, message: str, notification_type: str = 'info'):
        super().__init__()
        self.notification_type = notification_type
        self.setup_ui(title, message)
        self.setup_animation()
        
    def setup_ui(self, title: str, message: str):
        """Setup notification UI"""
        self.setFixedWidth(350)
        self.setMaximumHeight(120)
        self.setObjectName(f"notification_{self.notification_type}")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Header with title and close button
        header_layout = QHBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-weight: bold;
                color: #666;
            }
            QPushButton:hover {
                color: #333;
            }
        """)
        close_btn.clicked.connect(self.close_notification)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        
        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: #555; font-size: 10pt;")
        
        layout.addLayout(header_layout)
        layout.addWidget(message_label)
        layout.addStretch()
        
        # Set window flags for overlay
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def setup_animation(self):
        """Setup show/hide animations"""
        # Opacity effect
        self.opacity_effect = QGraphicsOpacityEffect()
        self.setGraphicsEffect(self.opacity_effect)
        
        # Fade in animation
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Fade out animation
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        self.fade_out.finished.connect(self.close)
        
        # Auto-hide timer
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.close_notification)
        
    def show_notification(self, duration: int = 5000):
        """Show notification with fade in"""
        self.show()
        self.fade_in.start()
        if duration > 0:
            self.hide_timer.start(duration)
            
    def close_notification(self):
        """Close notification with fade out"""
        self.hide_timer.stop()
        self.fade_out.start()
        self.closed.emit()

class NotificationManager:
    def __init__(self, parent):
        self.parent = parent
        self.notifications = []
        self.position_offset = 0
        
    def show_notification(self, title: str, message: str, notification_type: str = 'info', duration: int = 5000):
        """Show a notification"""
        # Create notification widget
        notification = NotificationWidget(title, message, notification_type)
        notification.closed.connect(lambda: self.remove_notification(notification))
        
        # Position notification
        self.position_notification(notification)
        
        # Add to list and show
        self.notifications.append(notification)
        notification.show_notification(duration)
        
    def position_notification(self, notification):
        """Position notification on screen"""
        parent_geometry = self.parent.geometry()
        
        # Calculate position (top-right corner with offset)
        x = parent_geometry.right() - notification.width() - 20
        y = parent_geometry.top() + 50 + self.position_offset
        
        notification.move(x, y)
        self.position_offset += notification.height() + 10
        
    def remove_notification(self, notification):
        """Remove notification and reposition others"""
        if notification in self.notifications:
            self.notifications.remove(notification)
            notification.deleteLater()
            
            # Reposition remaining notifications
            self.position_offset = 0
            for notif in self.notifications:
                self.position_notification(notif)
                
    def show_success(self, title: str, message: str, duration: int = 4000):
        """Show success notification"""
        self.show_notification(title, message, 'success', duration)
        
    def show_warning(self, title: str, message: str, duration: int = 6000):
        """Show warning notification"""
        self.show_notification(title, message, 'warning', duration)
        
    def show_error(self, title: str, message: str, duration: int = 8000):
        """Show error notification"""
        self.show_notification(title, message, 'error', duration)
        
    def show_info(self, title: str, message: str, duration: int = 5000):
        """Show info notification"""
        self.show_notification(title, message, 'info', duration)
        
    def clear_all(self):
        """Clear all notifications"""
        for notification in self.notifications[:]:
            notification.close_notification()

# Dialog-based notifications for important messages
class DialogManager:
    @staticmethod
    def show_success(title: str, message: str, parent=None):
        """Show success dialog"""
        QMessageBox.information(parent, title, message)
        
    @staticmethod
    def show_warning(title: str, message: str, parent=None):
        """Show warning dialog"""
        QMessageBox.warning(parent, title, message)
        
    @staticmethod
    def show_error(title: str, message: str, parent=None):
        """Show error dialog"""
        QMessageBox.critical(parent, title, message)
        
    @staticmethod
    def show_question(title: str, message: str, parent=None) -> bool:
        """Show question dialog"""
        reply = QMessageBox.question(
            parent, title, message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
        
    @staticmethod
    def show_confirmation(title: str, message: str, parent=None) -> bool:
        """Show confirmation dialog"""
        reply = QMessageBox.question(
            parent, title, message,
            QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        )
        return reply == QMessageBox.StandardButton.Ok