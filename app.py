"""
Windows Optimizer Pro v5.0 - Modular Dashboard Edition
Ứng dụng tối ưu hóa Windows với kiến trúc module hóa
"""
import tkinter as tk
from tkinter import ttk
import sys
import ctypes

# Import modules
from modules.theme import ThemeManager
from modules.ui_components import ModernUI, ModernButton, Card, ScrollableFrame
from modules.system_module import SystemModule
from modules.optimization_module import OptimizationModule
from modules.software_module import SoftwareModule
from modules.network_module import NetworkModule
from modules.security_module import SecurityModule
from modules.files_module import FilesModule
from modules.resources_module import ResourcesModule
from modules.startup_module import StartupModule
from modules.services_module import ServicesModule
from modules.privacy_module import PrivacyModule
from modules.health_module import HealthModule


class ModuleCard(tk.Canvas):
    """Card hiển thị module trên dashboard"""

    def __init__(self, parent, module_info, command, **kwargs):
        self.colors = ThemeManager.get_theme()
        super().__init__(
            parent,
            width=230,
            height=130,
            bg=parent['bg'],
            highlightthickness=0,
            cursor='hand2'
        )

        self.module_info = module_info
        self.command = command
        self.is_hovered = False

        self.draw_card()

        # Bind events
        self.bind('<Button-1>', lambda e: self.on_click())
        self.bind('<Enter>', lambda e: self.on_hover(True))
        self.bind('<Leave>', lambda e: self.on_hover(False))

    def draw_card(self, hovered=False):
        """Vẽ card"""
        self.delete('all')

        w, h = 230, 130
        r = ModernUI.RADIUS['md']
        bg = self.colors['bg_card_hover'] if hovered else self.colors['bg_card']

        # Background with rounded corners
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=bg, outline='')
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=bg, outline='')
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=bg, outline='')
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=bg, outline='')
        self.create_rectangle(r, 0, w-r, h, fill=bg, outline='')
        self.create_rectangle(0, r, w, h-r, fill=bg, outline='')

        # Border
        border_color = self.colors['primary'] if hovered else self.colors['border']
        self.create_rectangle(1, 1, w-1, h-1, outline=border_color, width=2 if hovered else 1)

        # Icon
        self.create_text(
            w//2, 42,
            text=self.module_info['icon'],
            font=('Segoe UI', 32),
            fill=self.colors['text_primary']
        )

        # Module name
        self.create_text(
            w//2, 82,
            text=self.module_info['name'],
            font=('Segoe UI', 12, 'bold'),
            fill=self.colors['text_primary']
        )

        # Description
        self.create_text(
            w//2, 105,
            text=self.module_info['description'],
            font=('Segoe UI', 8),
            fill=self.colors['text_secondary'],
            width=210
        )

    def on_hover(self, hovered):
        """Xử lý hover effect"""
        self.is_hovered = hovered
        self.draw_card(hovered)

    def on_click(self):
        """Xử lý click"""
        if self.command:
            self.command()


class WindowsOptimizerApp:
    """Main Application với Dashboard"""

    def __init__(self, root):
        self.root = root
        self.root.title("Windows Optimizer Pro v6.0 - Ultimate Edition")
        self.root.geometry("1200x800")

        # Set icon nếu có
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Theme
        self.colors = ThemeManager.get_theme()
        self.root.configure(bg=self.colors['bg_main'])

        # Module instances
        self.modules = {}
        self.current_module = None

        # Create UI
        self.create_ui()

        # Show dashboard by default
        self.show_dashboard()

    def create_ui(self):
        """Tạo UI chính"""
        # Header bar
        self.create_header()

        # Main content area
        self.content_area = tk.Frame(self.root, bg=self.colors['bg_main'])
        self.content_area.pack(fill='both', expand=True)

    def create_header(self):
        """Tạo header bar"""
        header = tk.Frame(self.root, bg=self.colors['primary'], height=70)
        header.pack(fill='x')
        header.pack_propagate(False)

        # App title
        tk.Label(
            header,
            text="⚡ Windows Optimizer Pro v6.0 - Ultimate Edition",
            bg=self.colors['primary'],
            fg=self.colors['text_white'],
            font=('Segoe UI', 18, 'bold')
        ).pack(side='left', padx=20)

        # Buttons
        btn_frame = tk.Frame(header, bg=self.colors['primary'])
        btn_frame.pack(side='right', padx=20)

        # Home button
        ModernButton(
            btn_frame,
            text="Dashboard",
            command=self.show_dashboard,
            icon="🏠",
            style='secondary',
            width=140,
            height=36
        ).pack(side='left', padx=5)

        # Theme toggle
        ModernButton(
            btn_frame,
            text="Theme",
            command=self.toggle_theme,
            icon="🌓",
            style='info',
            width=120,
            height=36
        ).pack(side='left', padx=5)

    def show_dashboard(self):
        """Hiển thị dashboard với grid các module cards"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Dashboard container
        dashboard = tk.Frame(self.content_area, bg=self.colors['bg_main'])
        dashboard.pack(fill='both', expand=True, padx=25, pady=15)

        # Title
        tk.Label(
            dashboard,
            text="📊 Dashboard - Chọn module để bắt đầu",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(anchor='w', pady=(0, 12))

        # Scrollable frame for modules
        scroll_frame = ScrollableFrame(dashboard)
        scroll_frame.pack(fill='both', expand=True)

        # Module grid container - Centered
        grid_outer = tk.Frame(scroll_frame.scrollable_frame, bg=self.colors['bg_main'])
        grid_outer.pack(fill='both', expand=True)

        grid_container = tk.Frame(grid_outer, bg=self.colors['bg_main'])
        grid_container.pack(anchor='n', pady=5)

        # Define modules
        module_classes = [
            SystemModule,
            HealthModule,
            OptimizationModule,
            StartupModule,
            ServicesModule,
            PrivacyModule,
            SoftwareModule,
            NetworkModule,
            SecurityModule,
            FilesModule,
            ResourcesModule
        ]

        # Create module cards in grid (4 columns for compact layout)
        row, col = 0, 0
        for ModuleClass in module_classes:
            # Create temporary instance to get info
            temp_module = ModuleClass(self.content_area)
            info = temp_module.get_module_info()

            # Create card
            card = ModuleCard(
                grid_container,
                info,
                command=lambda mc=ModuleClass: self.open_module(mc)
            )
            card.grid(row=row, column=col, padx=6, pady=6)

            col += 1
            if col >= 4:  # 4 columns
                col = 0
                row += 1

    def open_module(self, ModuleClass):
        """Mở một module"""
        # Clear content
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Create module if not exists
        module_key = ModuleClass.__name__
        if module_key not in self.modules:
            self.modules[module_key] = ModuleClass(self.content_area)

        # Show module
        module = self.modules[module_key]
        module.show()
        self.current_module = module

    def toggle_theme(self):
        """Đổi theme Light/Dark"""
        ThemeManager.toggle_theme()
        self.colors = ThemeManager.get_theme()

        # Refresh entire UI
        self.root.configure(bg=self.colors['bg_main'])

        # Recreate UI
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_ui()
        self.show_dashboard()


def main():
    """Entry point"""
    # Check admin rights
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        is_admin = False

    # Don't print warning for now to avoid encoding issues
    # if not is_admin:
    #     print("Warning: Application should run with Administrator rights")

    # Create app
    root = tk.Tk()
    app = WindowsOptimizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
