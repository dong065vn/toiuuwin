"""
Network Module - FULL FEATURES
Module giám sát mạng và network tools
"""
import tkinter as tk
from tkinter import messagebox
import socket
import psutil
import subprocess
import threading
import re
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class NetworkModule(BaseModule):
    """Module giám sát mạng - Full Features"""

    def get_module_info(self):
        return {
            'icon': '🌐',
            'name': 'Mạng',
            'description': 'Giám sát kết nối và network tools',
            'category': 'network'
        }

    def create_ui(self):
        """Tạo UI - Full Network Tools"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🌐 Công cụ mạng",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Quick Actions Card
        quick_card = Card(content.scrollable_frame, title="⚡ Lệnh nhanh")
        quick_card.pack(fill='x', pady=(0, 16))

        quick_btns = tk.Frame(quick_card.content_frame, bg=self.colors['bg_card'])
        quick_btns.pack(fill='x', pady=4)

        ModernButton(
            quick_btns, "Flush DNS",
            command=lambda: self.run_cmd('ipconfig /flushdns'),
            width=120, height=32, style='info'
        ).pack(side='left', padx=4)

        ModernButton(
            quick_btns, "Release IP",
            command=lambda: self.run_cmd('ipconfig /release'),
            width=120, height=32, style='warning'
        ).pack(side='left', padx=4)

        ModernButton(
            quick_btns, "Renew IP",
            command=lambda: self.run_cmd('ipconfig /renew'),
            width=120, height=32, style='success'
        ).pack(side='left', padx=4)

        ModernButton(
            quick_btns, "Reset Winsock",
            command=lambda: self.run_cmd('netsh winsock reset'),
            width=130, height=32, style='danger'
        ).pack(side='left', padx=4)

        # Diagnostics Card
        diag_card = Card(content.scrollable_frame, title="🔍 Network Diagnostics")
        diag_card.pack(fill='x', pady=(0, 16))

        # Host input
        input_frame = tk.Frame(diag_card.content_frame, bg=self.colors['bg_card'])
        input_frame.pack(fill='x', pady=8)

        tk.Label(
            input_frame,
            text="Host/IP:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=4)

        self.host_entry = tk.Entry(
            input_frame,
            width=25,
            font=ModernUI.FONTS['body'],
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary']
        )
        self.host_entry.pack(side='left', padx=4)
        self.host_entry.insert(0, "8.8.8.8")

        # Diagnostic buttons
        diag_btns = tk.Frame(diag_card.content_frame, bg=self.colors['bg_card'])
        diag_btns.pack(fill='x', pady=4)

        ModernButton(
            diag_btns, "Ping",
            command=self.run_ping,
            width=80, height=32, style='primary'
        ).pack(side='left', padx=4)

        ModernButton(
            diag_btns, "Tracert",
            command=self.run_tracert,
            width=80, height=32, style='secondary'
        ).pack(side='left', padx=4)

        ModernButton(
            diag_btns, "NSLookup",
            command=self.run_nslookup,
            width=90, height=32, style='info'
        ).pack(side='left', padx=4)

        # Network Info Card
        info_card = Card(content.scrollable_frame, title="📊 Thông tin mạng")
        info_card.pack(fill='x', pady=(0, 16))

        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)

            self._create_info_row(info_card.content_frame, "Tên máy", hostname)
            self._create_info_row(info_card.content_frame, "Địa chỉ IP", ip)

            # Network interfaces
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        self._create_info_row(info_card.content_frame, interface, addr.address)
        except:
            pass

        # Console
        self.create_console(main)
        self.log("Module Mạng đã sẵn sàng - Sử dụng các công cụ network bên trên", "success")

        return main

    def run_ping(self):
        """Run ping command với validation"""
        host = self.host_entry.get().strip()
        if not self._validate_host(host):
            return
        self.run_cmd(f'ping -n 4 {host}')

    def run_tracert(self):
        """Run tracert command với validation"""
        host = self.host_entry.get().strip()
        if not self._validate_host(host):
            return
        self.run_cmd(f'tracert {host}')

    def run_nslookup(self):
        """Run nslookup command với validation"""
        host = self.host_entry.get().strip()
        if not self._validate_host(host):
            return
        self.run_cmd(f'nslookup {host}')

    def _validate_host(self, host):
        """Validate host/IP để prevent command injection"""
        if not host:
            self.show_error("Lỗi", "Vui lòng nhập Host/IP!")
            return False

        # Chỉ cho phép alphanumeric, dots, hyphens, colons (IPv6)
        if not re.match(r'^[a-zA-Z0-9.\-:]+$', host):
            self.show_error("Lỗi", "Host/IP không hợp lệ! Chỉ cho phép chữ, số, dấu chấm, gạch ngang.")
            return False

        # Prevent command injection
        dangerous_chars = ['&', '|', ';', '$', '`', '(', ')', '<', '>', '"', "'"]
        if any(char in host for char in dangerous_chars):
            self.show_error("Lỗi", "Host/IP chứa ký tự nguy hiểm!")
            return False

        return True

    def run_cmd(self, command):
        """Execute network command in background"""
        self.log(f"🚀 Đang chạy: {command}", "info")

        def execute():
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    encoding='cp1252'  # Windows encoding
                )

                output = result.stdout if result.stdout else result.stderr

                # Log từng dòng
                for line in output.split('\n'):
                    if line.strip():
                        self.log(line, "info")

                self.log("✅ Hoàn thành!", "success")

            except subprocess.TimeoutExpired:
                self.log("⏱️ Timeout - Lệnh chạy quá lâu!", "warning")
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=execute, daemon=True).start()

    def _create_info_row(self, parent, label, value):
        """Tạo hàng thông tin"""
        row = tk.Frame(parent, bg=self.colors['bg_card'])
        row.pack(fill='x', pady=4)

        tk.Label(
            row,
            text=label + ":",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            width=20,
            anchor='w'
        ).pack(side='left')

        tk.Label(
            row,
            text=value,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left')
