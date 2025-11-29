"""
Base Module Class
Lớp cơ sở cho tất cả các module trong ứng dụng
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
from abc import ABC, abstractmethod
import datetime
from .theme import ThemeManager
from .ui_components import ModernUI, Card, ScrollableFrame


class BaseModule(ABC):
    """
    Base class cho tất cả các module
    Mỗi module sẽ kế thừa class này và implement các method riêng
    """

    def __init__(self, parent):
        """
        Khởi tạo module

        Args:
            parent: Widget cha (thường là main window hoặc frame)
        """
        self.parent = parent
        self.colors = ThemeManager.get_theme()
        self.main_frame = None
        self.console = None
        self.console_frame = None
        self.console_visible = True  # Console hiển thị mặc định

    @abstractmethod
    def get_module_info(self):
        """
        Trả về thông tin module (icon, tên, mô tả)

        Returns:
            dict: {'icon': str, 'name': str, 'description': str, 'category': str}
        """
        pass

    @abstractmethod
    def create_ui(self):
        """
        Tạo giao diện cho module
        Method này phải được implement bởi các module con

        Returns:
            tk.Frame: Frame chứa UI của module
        """
        pass

    def show(self):
        """Hiển thị module"""
        if self.main_frame is None:
            self.main_frame = self.create_ui()

        if self.main_frame:
            self.main_frame.pack(fill='both', expand=True)

    def hide(self):
        """Ẩn module"""
        if self.main_frame:
            self.main_frame.pack_forget()

    def destroy(self):
        """Hủy module"""
        if self.main_frame:
            self.main_frame.destroy()
            self.main_frame = None

    def refresh_theme(self):
        """Refresh theme khi đổi light/dark mode"""
        self.colors = ThemeManager.get_theme()
        if self.main_frame:
            self._refresh_all_widgets(self.main_frame)

    def _refresh_all_widgets(self, widget):
        """Recursively refresh all widgets"""
        if hasattr(widget, 'refresh_theme'):
            widget.refresh_theme()

        for child in widget.winfo_children():
            self._refresh_all_widgets(child)

    def log(self, message, level='info'):
        """
        Log message to console

        Args:
            message: Message to log
            level: 'info', 'success', 'warning', 'error'
        """
        if self.console:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            colors = ThemeManager.get_theme()

            color_map = {
                'info': colors['console_info'],
                'success': colors['console_success'],
                'warning': colors['console_warning'],
                'error': colors['console_error']
            }

            self.console.insert(tk.END, f"[{timestamp}] {message}\n")
            self.console.see(tk.END)

    def create_console(self, parent):
        """
        Tạo console output cho module với nút toggle ẩn/hiện

        Args:
            parent: Widget cha

        Returns:
            scrolledtext.ScrolledText: Console widget
        """
        # Container chính - chỉ chiếm không gian tối thiểu khi ẩn
        self.console_outer = tk.Frame(parent, bg=self.colors['bg_main'])
        self.console_outer.pack(fill='x', padx=16, pady=(0, 16))

        # Toggle bar - luôn hiển thị, compact
        self.toggle_bar = tk.Frame(self.console_outer, bg=self.colors['bg_card'], height=32)
        self.toggle_bar.pack(fill='x')
        self.toggle_bar.pack_propagate(False)

        # Toggle button với icon và text
        toggle_btn_frame = tk.Frame(self.toggle_bar, bg=self.colors['bg_card'])
        toggle_btn_frame.pack(fill='both', expand=True, padx=8, pady=4)

        self.toggle_icon = tk.Label(
            toggle_btn_frame,
            text="▼",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 10),
            cursor='hand2'
        )
        self.toggle_icon.pack(side='left', padx=(0, 8))

        self.toggle_label = tk.Label(
            toggle_btn_frame,
            text="📋 Console Output",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=('Segoe UI', 10, 'bold'),
            cursor='hand2'
        )
        self.toggle_label.pack(side='left')

        # Bind click events
        self.toggle_bar.bind('<Button-1>', lambda e: self.toggle_console())
        toggle_btn_frame.bind('<Button-1>', lambda e: self.toggle_console())
        self.toggle_icon.bind('<Button-1>', lambda e: self.toggle_console())
        self.toggle_label.bind('<Button-1>', lambda e: self.toggle_console())

        # Console container - có thể ẩn/hiện
        self.console_frame = tk.Frame(self.console_outer, bg=self.colors['bg_card'])
        self.console_frame.pack(fill='both', expand=True, pady=(4, 0))

        # Console text area
        self.console = scrolledtext.ScrolledText(
            self.console_frame,
            bg=self.colors['console_bg'],
            fg=self.colors['console_text'],
            font=ModernUI.FONTS['console'],
            height=8,
            wrap=tk.WORD,
            relief='flat',
            borderwidth=1
        )
        self.console.pack(fill='both', expand=True, padx=4, pady=4)

        return self.console

    def toggle_console(self):
        """Toggle hiện/ẩn console - tiết kiệm không gian tối đa"""
        if self.console_visible:
            # Ẩn console - chỉ giữ lại toggle bar
            self.console_frame.pack_forget()
            self.console_outer.config(height=32)
            self.toggle_icon.config(text="▶")
            self.toggle_label.config(text="📋 Console (Click để hiện)")
            self.console_visible = False
        else:
            # Hiện console - mở rộng full
            self.console_outer.config(height=0)  # Reset height
            self.console_frame.pack(fill='both', expand=True, pady=(4, 0))
            self.toggle_icon.config(text="▼")
            self.toggle_label.config(text="📋 Console Output")
            self.console_visible = True

    def create_action_buttons(self, parent, actions):
        """
        Tạo action buttons

        Args:
            parent: Widget cha
            actions: List of tuples (text, command, style)
        """
        from .ui_components import ModernButton

        button_frame = tk.Frame(parent, bg=self.colors['bg_card'])
        button_frame.pack(fill='x', padx=16, pady=8)

        for text, command, style in actions:
            btn = ModernButton(
                button_frame,
                text=text,
                command=command,
                style=style,
                width=120,
                height=36
            )
            btn.pack(side='left', padx=(0, 8))

    def show_error(self, title, message):
        """Show error dialog"""
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        """Show info dialog"""
        messagebox.showinfo(title, message)

    def show_warning(self, title, message):
        """Show warning dialog"""
        messagebox.showwarning(title, message)

    def confirm(self, title, message):
        """Show confirmation dialog"""
        return messagebox.askyesno(title, message)
