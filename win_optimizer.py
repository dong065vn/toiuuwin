"""
Windows 10/11 Professional Optimization Tool
Công cụ tối ưu hóa hệ thống và quản lý cổng mạng chuyên nghiệp
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import psutil
import socket
from datetime import datetime
import ctypes
import sys


class ModernButton(tk.Canvas):
    """Custom modern button with hover effects"""
    def __init__(self, parent, text, command, bg_color='#0078D4', fg_color='white',
                 width=150, height=40, **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg=parent['bg'])

        self.bg_color = bg_color
        self.hover_color = self._adjust_color(bg_color, 1.2)
        self.fg_color = fg_color
        self.command = command
        self.text = text

        self.draw_button()
        self.bind('<Button-1>', lambda e: self.on_click())
        self.bind('<Enter>', lambda e: self.on_hover())
        self.bind('<Leave>', lambda e: self.on_leave())

    def _adjust_color(self, color, factor):
        """Lighten or darken a color"""
        color = color.lstrip('#')
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def draw_button(self, color=None):
        """Draw the button"""
        self.delete('all')
        bg = color if color else self.bg_color
        self.create_rectangle(0, 0, self.winfo_reqwidth(), self.winfo_reqheight(),
                            fill=bg, outline='', tags='bg')
        self.create_text(self.winfo_reqwidth()//2, self.winfo_reqheight()//2,
                        text=self.text, fill=self.fg_color,
                        font=('Segoe UI', 10, 'bold'), tags='text')

    def on_hover(self):
        self.draw_button(self.hover_color)
        self.configure(cursor='hand2')

    def on_leave(self):
        self.draw_button()
        self.configure(cursor='')

    def on_click(self):
        if self.command:
            self.command()


class WindowsOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Optimizer Pro - Công Cụ Tối Ưu Hệ Thống Chuyên Nghiệp")
        self.root.geometry("1400x900")

        # Modern color scheme - easier on eyes
        self.colors = {
            'bg': '#F5F6FA',           # Light gray background
            'primary': '#0078D4',      # Microsoft blue
            'secondary': '#005A9E',    # Darker blue
            'success': '#107C10',      # Green
            'warning': '#FF8C00',      # Orange
            'danger': '#E81123',       # Red
            'dark': '#2B2B2B',        # Dark gray
            'light': '#FFFFFF',        # White
            'text': '#323130',         # Dark text
            'text_secondary': '#605E5C', # Gray text
            'border': '#EDEBE9',       # Light border
            'hover': '#F3F2F1',        # Hover background
            'card': '#FFFFFF',         # Card background
            'console': '#1E1E1E',      # Console background
            'console_text': '#00FF00'  # Console text
        }

        self.root.configure(bg=self.colors['bg'])

        # Check admin privileges
        self.is_admin = self.check_admin()

        # Configure style
        self.setup_style()

        # Create main interface
        self.create_widgets()

        # Status
        self.running_scan = False

    def check_admin(self):
        """Kiểm tra quyền Administrator"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def setup_style(self):
        """Thiết lập style cho ứng dụng"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure frames
        style.configure('Card.TFrame', background=self.colors['card'],
                       relief='flat', borderwidth=1)
        style.configure('TFrame', background=self.colors['bg'])

        # Configure labels
        style.configure('TLabel', background=self.colors['bg'],
                       foreground=self.colors['text'], font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'),
                       foreground=self.colors['primary'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12),
                       foreground=self.colors['text_secondary'])
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'),
                       foreground=self.colors['dark'])

        # Configure notebook
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=self.colors['light'],
                       foreground=self.colors['text'], padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', self.colors['light'])])

        # Configure checkbuttons
        style.configure('TCheckbutton', background=self.colors['card'],
                       foreground=self.colors['text'], font=('Segoe UI', 10))

        # Configure treeview
        style.configure('Treeview', background=self.colors['light'],
                       foreground=self.colors['text'], fieldbackground=self.colors['light'],
                       font=('Segoe UI', 9))
        style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                       background=self.colors['primary'], foreground=self.colors['light'])
        style.map('Treeview', background=[('selected', self.colors['primary'])])

    def create_widgets(self):
        """Tạo giao diện chính"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['card'], height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        # Title container
        title_container = tk.Frame(header_frame, bg=self.colors['card'])
        title_container.pack(side=tk.LEFT, padx=30, pady=20)

        title_label = ttk.Label(title_container, text="⚡ Windows Optimizer Pro",
                               style='Title.TLabel')
        title_label.pack(anchor=tk.W)

        subtitle_label = ttk.Label(title_container,
                                  text="Công Cụ Tối Ưu Windows 10/11 Chuyên Nghiệp",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(anchor=tk.W)

        # Admin status
        status_frame = tk.Frame(header_frame, bg=self.colors['card'])
        status_frame.pack(side=tk.RIGHT, padx=30, pady=20)

        if self.is_admin:
            status_icon = "🔑"
            status_text = "Quyền Quản Trị Viên"
            status_color = self.colors['success']
        else:
            status_icon = "⚠️"
            status_text = "Chế Độ Hạn Chế\n(Chạy với quyền Admin để mở khóa đầy đủ tính năng)"
            status_color = self.colors['warning']

        status_label = tk.Label(status_frame, text=f"{status_icon} {status_text}",
                               bg=self.colors['card'], fg=status_color,
                               font=('Segoe UI', 10, 'bold'), justify=tk.RIGHT)
        status_label.pack()

        # Separator
        separator = tk.Frame(self.root, bg=self.colors['border'], height=2)
        separator.pack(fill=tk.X)

        # Main content area
        content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create tabs
        self.create_optimization_tab()
        self.create_port_management_tab()
        self.create_system_info_tab()

    def create_optimization_tab(self):
        """Tạo tab Tối Ưu Hệ Thống"""
        opt_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(opt_frame, text="🔧 Tối Ưu Hệ Thống")

        # Main container
        main_container = tk.Frame(opt_frame, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel - Options (in a scrollable card)
        left_card = tk.Frame(main_container, bg=self.colors['card'], relief='solid',
                            borderwidth=1)
        left_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Header for left panel
        left_header = tk.Frame(left_card, bg=self.colors['primary'], height=50)
        left_header.pack(fill=tk.X)
        left_header.pack_propagate(False)

        ttk.Label(left_header, text="Tùy Chọn Tối Ưu",
                 font=('Segoe UI', 12, 'bold'),
                 background=self.colors['primary'],
                 foreground=self.colors['light']).pack(side=tk.LEFT, padx=20, pady=15)

        # Scrollable options
        options_canvas = tk.Canvas(left_card, bg=self.colors['card'],
                                  highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_card, orient="vertical",
                                 command=options_canvas.yview)
        scrollable_frame = tk.Frame(options_canvas, bg=self.colors['card'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: options_canvas.configure(scrollregion=options_canvas.bbox("all"))
        )

        options_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        options_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        options_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Optimization options
        self.opt_vars = {}
        options = [
            ("clean_temp", "🗑️ Dọn Dẹp File Tạm",
             "Xóa các file tạm thời không cần thiết để giải phóng dung lượng"),
            ("disable_telemetry", "🔒 Tắt Thu Thập Dữ Liệu",
             "Vô hiệu hóa các dịch vụ thu thập dữ liệu của Windows"),
            ("optimize_services", "⚙️ Tối Ưu Dịch Vụ",
             "Tắt các dịch vụ Windows không cần thiết"),
            ("clean_prefetch", "🚀 Dọn Dẹp Prefetch",
             "Xóa cache prefetch để tăng hiệu suất"),
            ("optimize_visual", "🎨 Tối Ưu Hiệu Ứng",
             "Cài đặt hiệu ứng hình ảnh cho hiệu suất tốt nhất"),
            ("disable_startup", "🚫 Tối Ưu Khởi Động",
             "Quản lý các chương trình khởi động cùng hệ thống"),
            ("clear_event_logs", "📋 Xóa Nhật Ký Sự Kiện",
             "Xóa các log sự kiện của Windows"),
            ("optimize_network", "🌐 Tối Ưu Mạng",
             "Tối ưu cài đặt mạng để có hiệu suất tốt hơn"),
            ("disk_cleanup", "💾 Dọn Dẹp Ổ Đĩa",
             "Chạy tiện ích dọn dẹp ổ đĩa của Windows"),
            ("optimize_power", "⚡ Tối Ưu Nguồn Điện",
             "Đặt chế độ hiệu suất cao"),
            ("disable_bitlocker", "🔓 Tắt BitLocker",
             "Vô hiệu hóa mã hóa ổ đĩa BitLocker (cẩn thận!)"),
            ("disable_hibernate", "💤 Tắt Hibernate",
             "Vô hiệu hóa chế độ ngủ đông để tiết kiệm dung lượng"),
            ("clean_windows_old", "📁 Xóa Windows.old",
             "Xóa thư mục cài đặt Windows cũ"),
            ("clear_dns_cache", "🌍 Xóa DNS Cache",
             "Làm mới bộ nhớ cache DNS"),
            ("optimize_ssd", "💿 Tối Ưu SSD",
             "Chạy lệnh TRIM cho ổ SSD"),
            ("disable_windows_defender", "🛡️ Tắt Windows Defender",
             "Tạm thời tắt Windows Defender (không khuyến khích!)"),
        ]

        for key, text, desc in options:
            option_frame = tk.Frame(scrollable_frame, bg=self.colors['card'])
            option_frame.pack(fill=tk.X, pady=8, padx=15)

            var = tk.BooleanVar(value=True if key not in ['disable_bitlocker',
                                                          'disable_windows_defender'] else False)
            self.opt_vars[key] = var

            cb = ttk.Checkbutton(option_frame, text=text, variable=var,
                               style='TCheckbutton')
            cb.pack(anchor=tk.W)

            desc_label = tk.Label(option_frame, text=f"  {desc}",
                                 font=('Segoe UI', 8),
                                 foreground=self.colors['text_secondary'],
                                 bg=self.colors['card'], justify=tk.LEFT)
            desc_label.pack(anchor=tk.W, padx=20)

        # Buttons at bottom of left panel
        btn_frame = tk.Frame(left_card, bg=self.colors['card'])
        btn_frame.pack(fill=tk.X, pady=20, padx=20)

        # Custom buttons
        run_btn = ModernButton(btn_frame, "▶ BẮT ĐẦU TỐI ƯU",
                              self.run_optimization,
                              bg_color=self.colors['success'], width=200, height=45)
        run_btn.pack(side=tk.LEFT, padx=5)

        select_all_btn = ModernButton(btn_frame, "Chọn Tất Cả",
                                      self.select_all_optimizations,
                                      bg_color=self.colors['secondary'], width=150, height=45)
        select_all_btn.pack(side=tk.LEFT, padx=5)

        deselect_all_btn = ModernButton(btn_frame, "Bỏ Chọn Tất Cả",
                                       self.deselect_all_optimizations,
                                       bg_color=self.colors['text_secondary'],
                                       width=150, height=45)
        deselect_all_btn.pack(side=tk.LEFT, padx=5)

        # Right panel - Output
        right_card = tk.Frame(main_container, bg=self.colors['card'],
                             relief='solid', borderwidth=1)
        right_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header for right panel
        right_header = tk.Frame(right_card, bg=self.colors['primary'], height=50)
        right_header.pack(fill=tk.X)
        right_header.pack_propagate(False)

        ttk.Label(right_header, text="📊 Nhật Ký Tối Ưu",
                 font=('Segoe UI', 12, 'bold'),
                 background=self.colors['primary'],
                 foreground=self.colors['light']).pack(side=tk.LEFT, padx=20, pady=15)

        # Output console
        console_frame = tk.Frame(right_card, bg=self.colors['console'])
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.opt_output = scrolledtext.ScrolledText(
            console_frame, wrap=tk.WORD,
            bg=self.colors['console'], fg=self.colors['console_text'],
            font=('Consolas', 9), relief=tk.FLAT, padx=10, pady=10
        )
        self.opt_output.pack(fill=tk.BOTH, expand=True)

    def create_port_management_tab(self):
        """Tạo tab Quản Lý Cổng"""
        port_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(port_frame, text="🌐 Quản Lý Cổng")

        # Control panel
        control_card = tk.Frame(port_frame, bg=self.colors['card'],
                               relief='solid', borderwidth=1)
        control_card.pack(fill=tk.X, padx=10, pady=10)

        control_inner = tk.Frame(control_card, bg=self.colors['card'])
        control_inner.pack(fill=tk.X, padx=20, pady=15)

        ttk.Label(control_inner, text="Quản Lý Kết Nối Mạng và Cổng",
                 style='Header.TLabel').pack(side=tk.LEFT)

        # Buttons
        btn_container = tk.Frame(control_inner, bg=self.colors['card'])
        btn_container.pack(side=tk.RIGHT)

        scan_btn = ModernButton(btn_container, "🔍 Quét Cổng",
                               self.scan_ports, bg_color=self.colors['primary'],
                               width=120, height=35)
        scan_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ModernButton(btn_container, "🔄 Làm Mới",
                                  self.refresh_connections,
                                  bg_color=self.colors['secondary'],
                                  width=120, height=35)
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_card = tk.Frame(port_frame, bg=self.colors['card'],
                            relief='solid', borderwidth=1)
        tree_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        tree_frame = tk.Frame(tree_card, bg=self.colors['light'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Treeview
        columns = ('PID', 'Tiến Trình', 'Giao Thức', 'Địa Chỉ Local',
                  'Địa Chỉ Remote', 'Trạng Thái', 'Cổng')
        self.port_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.config(command=self.port_tree.yview)
        tree_scroll_x.config(command=self.port_tree.xview)

        for col in columns:
            self.port_tree.heading(col, text=col)
            self.port_tree.column(col, width=120)

        self.port_tree.pack(fill=tk.BOTH, expand=True)

        # Color tags
        self.port_tree.tag_configure('established', background='#C8E6C9')
        self.port_tree.tag_configure('listening', background='#BBDEFB')
        self.port_tree.tag_configure('other', background='#F5F5F5')

        # Action buttons
        action_card = tk.Frame(port_frame, bg=self.colors['card'],
                              relief='solid', borderwidth=1)
        action_card.pack(fill=tk.X, padx=10, pady=(0, 10))

        action_inner = tk.Frame(action_card, bg=self.colors['card'])
        action_inner.pack(fill=tk.X, padx=20, pady=15)

        kill_btn = ModernButton(action_inner, "❌ Kết Thúc Tiến Trình",
                               self.kill_selected_process,
                               bg_color=self.colors['danger'], width=180, height=35)
        kill_btn.pack(side=tk.LEFT, padx=5)

        block_btn = ModernButton(action_inner, "🚫 Chặn Cổng",
                                self.block_port_firewall,
                                bg_color=self.colors['warning'], width=130, height=35)
        block_btn.pack(side=tk.LEFT, padx=5)

        allow_btn = ModernButton(action_inner, "✅ Cho Phép Cổng",
                                self.allow_port_firewall,
                                bg_color=self.colors['success'], width=150, height=35)
        allow_btn.pack(side=tk.LEFT, padx=5)

        # Info panel
        info_card = tk.Frame(port_frame, bg=self.colors['card'],
                            relief='solid', borderwidth=1)
        info_card.pack(fill=tk.BOTH, padx=10, pady=(0, 10))

        info_header = tk.Frame(info_card, bg=self.colors['primary'], height=40)
        info_header.pack(fill=tk.X)
        info_header.pack_propagate(False)

        ttk.Label(info_header, text="Thông Tin Cổng",
                 font=('Segoe UI', 11, 'bold'),
                 background=self.colors['primary'],
                 foreground=self.colors['light']).pack(side=tk.LEFT, padx=20, pady=10)

        self.port_info = scrolledtext.ScrolledText(
            info_card, wrap=tk.WORD, height=8,
            bg=self.colors['console'], fg=self.colors['console_text'],
            font=('Consolas', 9), relief=tk.FLAT, padx=10, pady=10
        )
        self.port_info.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_system_info_tab(self):
        """Tạo tab Thông Tin Hệ Thống"""
        info_frame = tk.Frame(self.notebook, bg=self.colors['bg'])
        self.notebook.add(info_frame, text="📊 Thông Tin Hệ Thống")

        # Card container
        info_card = tk.Frame(info_frame, bg=self.colors['card'],
                            relief='solid', borderwidth=1)
        info_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Header
        info_header = tk.Frame(info_card, bg=self.colors['primary'], height=50)
        info_header.pack(fill=tk.X)
        info_header.pack_propagate(False)

        ttk.Label(info_header, text="Thông Tin Chi Tiết Hệ Thống",
                 font=('Segoe UI', 12, 'bold'),
                 background=self.colors['primary'],
                 foreground=self.colors['light']).pack(side=tk.LEFT, padx=20, pady=15)

        refresh_info_btn = ModernButton(info_header, "🔄 Làm Mới",
                                       self.load_system_info,
                                       bg_color=self.colors['secondary'],
                                       width=100, height=30)
        refresh_info_btn.pack(side=tk.RIGHT, padx=20)

        # System info display
        self.sys_info_text = scrolledtext.ScrolledText(
            info_card, wrap=tk.WORD,
            bg=self.colors['light'], fg=self.colors['text'],
            font=('Consolas', 10), relief=tk.FLAT, padx=20, pady=20
        )
        self.sys_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load info
        self.load_system_info()

    def select_all_optimizations(self):
        """Chọn tất cả tùy chọn tối ưu"""
        for var in self.opt_vars.values():
            var.set(True)

    def deselect_all_optimizations(self):
        """Bỏ chọn tất cả tùy chọn tối ưu"""
        for var in self.opt_vars.values():
            var.set(False)

    def log_output(self, text_widget, message, level='info'):
        """Ghi log ra widget"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {
            'info': '#00FF00',
            'warning': '#FFA500',
            'error': '#FF0000',
            'success': '#00FF00'
        }

        text_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        text_widget.see(tk.END)
        text_widget.update()

    def execute_command(self, command, shell=True):
        """Thực thi lệnh CMD và trả về kết quả"""
        try:
            result = subprocess.run(command, shell=shell, capture_output=True,
                                  text=True, timeout=30)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Lỗi: {str(e)}"

    def run_optimization(self):
        """Chạy các tối ưu đã chọn"""
        if not self.is_admin:
            messagebox.showwarning("Cần Quyền Quản Trị",
                                 "Vui lòng chạy ứng dụng với quyền Administrator để sử dụng đầy đủ tính năng!")
            return

        def optimize():
            self.opt_output.delete(1.0, tk.END)
            self.log_output(self.opt_output, "=" * 70, 'info')
            self.log_output(self.opt_output, "BẮT ĐẦU TỐI ƯU HÓA HỆ THỐNG WINDOWS", 'info')
            self.log_output(self.opt_output, "=" * 70, 'info')

            if self.opt_vars['clean_temp'].get():
                self.log_output(self.opt_output, "\n🗑️ Đang dọn dẹp file tạm...", 'info')
                self.clean_temp_files()

            if self.opt_vars['disable_telemetry'].get():
                self.log_output(self.opt_output, "\n🔒 Đang tắt thu thập dữ liệu...", 'info')
                self.disable_telemetry()

            if self.opt_vars['optimize_services'].get():
                self.log_output(self.opt_output, "\n⚙️ Đang tối ưu dịch vụ...", 'info')
                self.optimize_services()

            if self.opt_vars['clean_prefetch'].get():
                self.log_output(self.opt_output, "\n🚀 Đang dọn dẹp prefetch...", 'info')
                self.clean_prefetch()

            if self.opt_vars['optimize_visual'].get():
                self.log_output(self.opt_output, "\n🎨 Đang tối ưu hiệu ứng hình ảnh...", 'info')
                self.optimize_visual_effects()

            if self.opt_vars['disable_startup'].get():
                self.log_output(self.opt_output, "\n🚫 Đang liệt kê chương trình khởi động...", 'info')
                self.list_startup_programs()

            if self.opt_vars['clear_event_logs'].get():
                self.log_output(self.opt_output, "\n📋 Đang xóa nhật ký sự kiện...", 'info')
                self.clear_event_logs()

            if self.opt_vars['optimize_network'].get():
                self.log_output(self.opt_output, "\n🌐 Đang tối ưu cài đặt mạng...", 'info')
                self.optimize_network()

            if self.opt_vars['disk_cleanup'].get():
                self.log_output(self.opt_output, "\n💾 Đang chạy dọn dẹp ổ đĩa...", 'info')
                self.run_disk_cleanup()

            if self.opt_vars['optimize_power'].get():
                self.log_output(self.opt_output, "\n⚡ Đang tối ưu cài đặt nguồn...", 'info')
                self.optimize_power_plan()

            if self.opt_vars['disable_bitlocker'].get():
                self.log_output(self.opt_output, "\n🔓 Đang tắt BitLocker...", 'info')
                self.disable_bitlocker()

            if self.opt_vars['disable_hibernate'].get():
                self.log_output(self.opt_output, "\n💤 Đang tắt chế độ ngủ đông...", 'info')
                self.disable_hibernate()

            if self.opt_vars['clean_windows_old'].get():
                self.log_output(self.opt_output, "\n📁 Đang xóa Windows.old...", 'info')
                self.clean_windows_old()

            if self.opt_vars['clear_dns_cache'].get():
                self.log_output(self.opt_output, "\n🌍 Đang xóa DNS cache...", 'info')
                self.clear_dns_cache()

            if self.opt_vars['optimize_ssd'].get():
                self.log_output(self.opt_output, "\n💿 Đang tối ưu SSD...", 'info')
                self.optimize_ssd()

            if self.opt_vars['disable_windows_defender'].get():
                self.log_output(self.opt_output, "\n🛡️ Đang tắt Windows Defender...", 'info')
                self.disable_windows_defender()

            self.log_output(self.opt_output, "\n" + "=" * 70, 'success')
            self.log_output(self.opt_output, "✅ HOÀN THÀNH TỐI ƯU HÓA!", 'success')
            self.log_output(self.opt_output, "=" * 70, 'success')
            messagebox.showinfo("Hoàn Thành",
                              "Tối ưu hóa Windows đã hoàn thành!\nKhuyến nghị khởi động lại máy.")

        thread = threading.Thread(target=optimize, daemon=True)
        thread.start()

    # Optimization methods
    def clean_temp_files(self):
        """Dọn dẹp file tạm"""
        commands = [
            'del /q /f /s %TEMP%\\* 2>nul',
            'del /q /f /s C:\\Windows\\Temp\\* 2>nul',
        ]
        for cmd in commands:
            self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã dọn dẹp file tạm", 'success')

    def disable_telemetry(self):
        """Tắt thu thập dữ liệu"""
        services = ['DiagTrack', 'dmwappushservice', 'WerSvc', 'OneSyncSvc']
        for service in services:
            cmd = f'sc stop "{service}" 2>nul && sc config "{service}" start=disabled 2>nul'
            self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã tắt các dịch vụ thu thập dữ liệu", 'success')

    def optimize_services(self):
        """Tối ưu dịch vụ Windows"""
        services = ['XblAuthManager', 'XblGameSave', 'XboxNetApiSvc', 'XboxGipSvc',
                   'Fax', 'WSearch']
        for service in services:
            cmd = f'sc config "{service}" start=disabled 2>nul'
            self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã tối ưu dịch vụ", 'success')

    def clean_prefetch(self):
        """Dọn dẹp prefetch"""
        cmd = 'del /q /f /s C:\\Windows\\Prefetch\\* 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã dọn dẹp prefetch", 'success')

    def optimize_visual_effects(self):
        """Tối ưu hiệu ứng hình ảnh"""
        cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã tối ưu hiệu ứng hình ảnh", 'success')

    def list_startup_programs(self):
        """Liệt kê chương trình khởi động"""
        cmd = 'wmic startup get caption,command 2>nul'
        output = self.execute_command(cmd)
        self.log_output(self.opt_output, "  Các chương trình khởi động:", 'info')
        self.log_output(self.opt_output, output[:500] if output else "  Không có dữ liệu", 'info')

    def clear_event_logs(self):
        """Xóa nhật ký sự kiện"""
        cmd = 'wevtutil el | Foreach-Object {wevtutil cl "$_"} 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã xóa nhật ký sự kiện", 'success')

    def optimize_network(self):
        """Tối ưu cài đặt mạng"""
        commands = [
            'netsh int tcp set global autotuninglevel=normal',
            'netsh int tcp set global chimney=enabled',
            'netsh int tcp set global dca=enabled',
            'netsh int tcp set global netdma=enabled',
        ]
        for cmd in commands:
            self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã tối ưu cài đặt mạng", 'success')

    def run_disk_cleanup(self):
        """Chạy dọn dẹp ổ đĩa"""
        self.log_output(self.opt_output, "  Đang khởi động tiện ích dọn dẹp ổ đĩa...", 'info')
        cmd = 'cleanmgr /sagerun:1'
        self.execute_command(cmd)

    def optimize_power_plan(self):
        """Tối ưu cài đặt nguồn"""
        cmd = 'powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã kích hoạt chế độ hiệu suất cao", 'success')

    def disable_bitlocker(self):
        """Tắt BitLocker"""
        result = messagebox.askyesno("Cảnh Báo",
            "Tắt BitLocker sẽ giải mã ổ đĩa của bạn.\n"
            "Điều này có thể mất nhiều thời gian và giảm bảo mật.\n\n"
            "Bạn có chắc chắn muốn tiếp tục?")

        if result:
            cmd = 'manage-bde -off C:'
            output = self.execute_command(cmd)
            self.log_output(self.opt_output, "  ✓ Đã bắt đầu tắt BitLocker", 'success')
            self.log_output(self.opt_output, f"  {output[:200]}", 'info')
        else:
            self.log_output(self.opt_output, "  ⊘ Đã hủy tắt BitLocker", 'warning')

    def disable_hibernate(self):
        """Tắt chế độ ngủ đông"""
        cmd = 'powercfg -h off'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã tắt chế độ ngủ đông", 'success')

    def clean_windows_old(self):
        """Xóa Windows.old"""
        cmd = 'rd /s /q C:\\Windows.old 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã xóa Windows.old (nếu có)", 'success')

    def clear_dns_cache(self):
        """Xóa DNS cache"""
        cmd = 'ipconfig /flushdns'
        output = self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã xóa DNS cache", 'success')

    def optimize_ssd(self):
        """Tối ưu SSD"""
        cmd = 'defrag C: /L /O'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Đã chạy TRIM cho SSD", 'success')

    def disable_windows_defender(self):
        """Tắt Windows Defender"""
        result = messagebox.askyesno("Cảnh Báo Bảo Mật",
            "Tắt Windows Defender sẽ làm giảm bảo mật hệ thống!\n"
            "Chỉ làm điều này nếu bạn có phần mềm bảo mật khác.\n\n"
            "Tiếp tục?")

        if result:
            cmd = 'reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v DisableAntiSpyware /t REG_DWORD /d 1 /f'
            self.execute_command(cmd)
            self.log_output(self.opt_output, "  ⚠ Đã tắt Windows Defender (yêu cầu khởi động lại)", 'warning')
        else:
            self.log_output(self.opt_output, "  ⊘ Đã hủy tắt Windows Defender", 'warning')

    # Port management methods
    def refresh_connections(self):
        """Làm mới kết nối mạng"""
        def refresh():
            self.port_tree.delete(*self.port_tree.get_children())
            self.port_info.delete(1.0, tk.END)

            self.log_output(self.port_info, "Đang quét kết nối mạng...", 'info')

            try:
                connections = psutil.net_connections(kind='inet')

                for conn in connections:
                    try:
                        try:
                            process = psutil.Process(conn.pid) if conn.pid else None
                            process_name = process.name() if process else "N/A"
                        except:
                            process_name = "N/A"

                        local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                        remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"

                        tag = 'other'
                        if conn.status == 'ESTABLISHED':
                            tag = 'established'
                        elif conn.status == 'LISTEN':
                            tag = 'listening'

                        port = conn.laddr.port if conn.laddr else "N/A"

                        self.port_tree.insert('', tk.END, values=(
                            conn.pid or "N/A",
                            process_name,
                            conn.type.name,
                            local_addr,
                            remote_addr,
                            conn.status,
                            port
                        ), tags=(tag,))
                    except:
                        continue

                total = len(self.port_tree.get_children())
                self.log_output(self.port_info, f"✓ Tìm thấy {total} kết nối mạng", 'success')

            except Exception as e:
                self.log_output(self.port_info, f"Lỗi: {str(e)}", 'error')

        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()

    def scan_ports(self):
        """Quét các cổng phổ biến"""
        if self.running_scan:
            messagebox.showinfo("Đang Quét", "Quá trình quét cổng đang chạy!")
            return

        def scan():
            self.running_scan = True
            self.port_info.delete(1.0, tk.END)
            self.log_output(self.port_info, "Bắt đầu quét cổng...", 'info')

            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
                          3306, 3389, 5432, 8080, 8443]

            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            self.log_output(self.port_info, f"Đang quét {local_ip}...", 'info')

            open_ports = []
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((local_ip, port))
                    sock.close()

                    if result == 0:
                        open_ports.append(port)
                        self.log_output(self.port_info, f"  Cổng {port}: MỞ", 'success')
                    else:
                        self.log_output(self.port_info, f"  Cổng {port}: ĐÓNG", 'info')
                except:
                    pass

            self.log_output(self.port_info,
                          f"\n✓ Quét hoàn thành. Tìm thấy {len(open_ports)} cổng mở",
                          'success')
            self.running_scan = False

        thread = threading.Thread(target=scan, daemon=True)
        thread.start()

    def kill_selected_process(self):
        """Kết thúc tiến trình đã chọn"""
        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("Chưa Chọn", "Vui lòng chọn một kết nối để kết thúc")
            return

        item = self.port_tree.item(selection[0])
        pid = item['values'][0]
        process_name = item['values'][1]

        if pid == "N/A":
            messagebox.showerror("Lỗi", "Không thể kết thúc tiến trình không có PID")
            return

        result = messagebox.askyesno("Xác Nhận",
                                     f"Kết thúc tiến trình '{process_name}' (PID: {pid})?")
        if result:
            try:
                process = psutil.Process(int(pid))
                process.kill()
                self.log_output(self.port_info,
                              f"✓ Đã kết thúc tiến trình {process_name} (PID: {pid})",
                              'success')
                self.refresh_connections()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể kết thúc tiến trình: {str(e)}")

    def block_port_firewall(self):
        """Chặn cổng qua Windows Firewall"""
        if not self.is_admin:
            messagebox.showwarning("Cần Quyền Quản Trị",
                                 "Cần quyền Administrator để thao tác với Firewall!")
            return

        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("Chưa Chọn", "Vui lòng chọn một kết nối")
            return

        item = self.port_tree.item(selection[0])
        port = item['values'][6]

        if port == "N/A":
            messagebox.showerror("Lỗi", "Cổng không hợp lệ")
            return

        result = messagebox.askyesno("Xác Nhận",
                                     f"Chặn cổng {port} trong Windows Firewall?")
        if result:
            rule_name = f"Block_Port_{port}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=TCP localport={port}'
            self.execute_command(cmd)
            self.log_output(self.port_info, f"✓ Đã chặn cổng {port}", 'success')
            messagebox.showinfo("Thành Công", f"Cổng {port} đã được chặn trong firewall")

    def allow_port_firewall(self):
        """Cho phép cổng qua Windows Firewall"""
        if not self.is_admin:
            messagebox.showwarning("Cần Quyền Quản Trị",
                                 "Cần quyền Administrator để thao tác với Firewall!")
            return

        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("Chưa Chọn", "Vui lòng chọn một kết nối")
            return

        item = self.port_tree.item(selection[0])
        port = item['values'][6]

        if port == "N/A":
            messagebox.showerror("Lỗi", "Cổng không hợp lệ")
            return

        result = messagebox.askyesno("Xác Nhận",
                                     f"Cho phép cổng {port} qua Windows Firewall?")
        if result:
            rule_name = f"Allow_Port_{port}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'
            self.execute_command(cmd)
            self.log_output(self.port_info, f"✓ Đã cho phép cổng {port}", 'success')
            messagebox.showinfo("Thành Công", f"Cổng {port} đã được cho phép qua firewall")

    def load_system_info(self):
        """Tải thông tin hệ thống"""
        def load():
            self.sys_info_text.delete(1.0, tk.END)

            info = []
            info.append("=" * 80)
            info.append("THÔNG TIN HỆ THỐNG WINDOWS")
            info.append("=" * 80)
            info.append("")

            # CPU
            info.append("🖥️  THÔNG TIN BỘ XỬ LÝ (CPU):")
            info.append(f"  • Số lõi vật lý: {psutil.cpu_count(logical=False)}")
            info.append(f"  • Số lõi logic: {psutil.cpu_count(logical=True)}")
            info.append(f"  • Mức sử dụng CPU: {psutil.cpu_percent(interval=1)}%")
            info.append("")

            # Memory
            mem = psutil.virtual_memory()
            info.append("💾 THÔNG TIN BỘ NHỚ (RAM):")
            info.append(f"  • Tổng dung lượng: {mem.total / (1024**3):.2f} GB")
            info.append(f"  • Đã sử dụng: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
            info.append(f"  • Còn trống: {mem.available / (1024**3):.2f} GB")
            info.append("")

            # Disk
            disk = psutil.disk_usage('C:')
            info.append("💿 THÔNG TIN Ổ ĐĨA (C:):")
            info.append(f"  • Tổng dung lượng: {disk.total / (1024**3):.2f} GB")
            info.append(f"  • Đã sử dụng: {disk.used / (1024**3):.2f} GB ({disk.percent}%)")
            info.append(f"  • Còn trống: {disk.free / (1024**3):.2f} GB")
            info.append("")

            # Network
            info.append("🌐 THÔNG TIN MẠNG:")
            net_if = psutil.net_if_addrs()
            for interface, addrs in net_if.items():
                info.append(f"  • Giao diện: {interface}")
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info.append(f"    - IPv4: {addr.address}")
            info.append("")

            # Process
            info.append("⚙️  THÔNG TIN TIẾN TRÌNH:")
            info.append(f"  • Số tiến trình đang chạy: {len(psutil.pids())}")
            info.append("")

            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            info.append(f"⏰ THỜI GIAN KHỞI ĐỘNG HỆ THỐNG:")
            info.append(f"  • {boot_time.strftime('%d/%m/%Y %H:%M:%S')}")
            info.append("")

            # Battery (if available)
            try:
                battery = psutil.sensors_battery()
                if battery:
                    info.append("🔋 THÔNG TIN PIN:")
                    info.append(f"  • Mức pin: {battery.percent}%")
                    info.append(f"  • Đang sạc: {'Có' if battery.power_plugged else 'Không'}")
                    info.append("")
            except:
                pass

            info.append("=" * 80)

            self.sys_info_text.insert(1.0, "\n".join(info))

        thread = threading.Thread(target=load, daemon=True)
        thread.start()


def main():
    """Hàm chính khởi chạy ứng dụng"""
    root = tk.Tk()

    # Set icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass

    app = WindowsOptimizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
