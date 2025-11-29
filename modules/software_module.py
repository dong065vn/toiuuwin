"""
Software Module - FULL FEATURES
Module quản lý phần mềm và Windows Services
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import win32serviceutil
import win32service
import wmi
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class SoftwareModule(BaseModule):
    """Module quản lý phần mềm và Services - Full Features"""

    def get_module_info(self):
        return {
            'icon': '📦',
            'name': 'Phần mềm',
            'description': 'Quản lý ứng dụng và Windows Services',
            'category': 'software'
        }

    def create_ui(self):
        """Tạo UI - Software & Services Management"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="📦 Quản lý phần mềm & Services",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Services Management Card
        services_card = Card(content.scrollable_frame, title="⚙️ Quản lý Windows Services")
        services_card.pack(fill='both', expand=True, pady=(0, 16))

        # Search/Filter
        search_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        search_frame.pack(fill='x', pady=(8, 12))

        tk.Label(
            search_frame,
            text="🔍 Tìm kiếm:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=(0, 8))

        self.search_entry = tk.Entry(
            search_frame,
            width=30,
            font=ModernUI.FONTS['body'],
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary']
        )
        self.search_entry.pack(side='left', padx=4)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_services())

        ModernButton(
            search_frame, "Làm mới",
            command=self.load_services,
            icon="🔄", style='primary', width=100, height=32
        ).pack(side='left', padx=8)

        # Filter buttons
        filter_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        filter_frame.pack(fill='x', pady=(0, 8))

        self.filter_var = tk.StringVar(value='all')

        tk.Radiobutton(
            filter_frame,
            text="Tất cả",
            variable=self.filter_var,
            value='all',
            command=self.filter_services,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=8)

        tk.Radiobutton(
            filter_frame,
            text="Running",
            variable=self.filter_var,
            value='running',
            command=self.filter_services,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=8)

        tk.Radiobutton(
            filter_frame,
            text="Stopped",
            variable=self.filter_var,
            value='stopped',
            command=self.filter_services,
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'],
            selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=8)

        # Services TreeView
        tree_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(0, 12))

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')

        # TreeView
        columns = ('name', 'display_name', 'status', 'startup_type')
        self.services_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=12,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.services_tree.yview)
        tree_scroll_x.config(command=self.services_tree.xview)

        # Column headings
        self.services_tree.heading('name', text='Tên Service')
        self.services_tree.heading('display_name', text='Tên hiển thị')
        self.services_tree.heading('status', text='Trạng thái')
        self.services_tree.heading('startup_type', text='Startup Type')

        # Column widths
        self.services_tree.column('name', width=200)
        self.services_tree.column('display_name', width=250)
        self.services_tree.column('status', width=100)
        self.services_tree.column('startup_type', width=120)

        self.services_tree.pack(fill='both', expand=True)

        # Action buttons
        action_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        action_frame.pack(fill='x', pady=8)

        ModernButton(
            action_frame, "▶ Start",
            command=self.start_service,
            style='success', width=90, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "■ Stop",
            command=self.stop_service,
            style='danger', width=90, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "🔄 Restart",
            command=self.restart_service,
            style='warning', width=100, height=36
        ).pack(side='left', padx=4)

        tk.Frame(action_frame, bg=self.colors['bg_card'], width=20).pack(side='left')

        ModernButton(
            action_frame, "Auto",
            command=lambda: self.set_startup_type('Auto'),
            style='primary', width=80, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "Manual",
            command=lambda: self.set_startup_type('Manual'),
            style='secondary', width=90, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "Disabled",
            command=lambda: self.set_startup_type('Disabled'),
            style='danger', width=100, height=36
        ).pack(side='left', padx=4)

        # Startup Programs Card
        startup_card = Card(content.scrollable_frame, title="🚀 Startup Programs")
        startup_card.pack(fill='x', pady=(0, 16))

        startup_btns = tk.Frame(startup_card.content_frame, bg=self.colors['bg_card'])
        startup_btns.pack(fill='x', pady=8)

        ModernButton(
            startup_btns, "Mở Task Manager → Startup",
            command=self.open_startup_manager,
            icon="🚀", style='info', width=220, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            startup_btns, "Mở msconfig",
            command=self.open_msconfig,
            icon="⚙️", style='secondary', width=140, height=36
        ).pack(side='left', padx=4)

        # Console
        self.create_console(main)
        self.log("Module Phần mềm đã sẵn sàng", "success")

        # Store all services for filtering
        self.all_services = []

        # Load services
        self.load_services()

        return main

    def load_services(self):
        """Load Windows Services"""
        self.log("🔄 Đang tải danh sách Windows Services...", "info")

        def load():
            try:
                # Clear tree
                for item in self.services_tree.get_children():
                    self.services_tree.delete(item)

                self.all_services = []

                # Try WMI first
                try:
                    c = wmi.WMI()
                    services = c.Win32_Service()

                    for service in services:
                        name = service.Name
                        display_name = service.DisplayName
                        status = service.State  # Running, Stopped, etc.
                        startup_type = service.StartMode  # Auto, Manual, Disabled

                        self.all_services.append({
                            'name': name,
                            'display_name': display_name,
                            'status': status,
                            'startup_type': startup_type
                        })

                    self.log(f"✅ Đã tải {len(self.all_services)} services qua WMI", "success")

                except Exception as wmi_error:
                    self.log(f"⚠️ WMI failed, using sc query: {str(wmi_error)}", "warning")

                    # Fallback to sc query
                    result = subprocess.run(
                        'sc query type= service state= all',
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )

                    lines = result.stdout.split('\n')
                    current_service = {}

                    for line in lines:
                        line = line.strip()
                        if line.startswith('SERVICE_NAME:'):
                            if current_service:
                                self.all_services.append(current_service)
                            current_service = {'name': line.split(':', 1)[1].strip()}
                        elif line.startswith('DISPLAY_NAME:'):
                            current_service['display_name'] = line.split(':', 1)[1].strip()
                        elif line.startswith('STATE'):
                            parts = line.split()
                            if len(parts) >= 3:
                                current_service['status'] = parts[3]
                        elif line.startswith('START_TYPE'):
                            parts = line.split()
                            if len(parts) >= 3:
                                current_service['startup_type'] = parts[3]

                    if current_service:
                        self.all_services.append(current_service)

                    self.log(f"✅ Đã tải {len(self.all_services)} services qua sc query", "success")

                # Display services
                self.filter_services()

            except Exception as e:
                self.log(f"❌ Lỗi khi tải services: {str(e)}", "error")

        threading.Thread(target=load, daemon=True).start()

    def filter_services(self):
        """Filter services based on search and filter"""
        # Clear tree
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)

        search_text = self.search_entry.get().lower()
        filter_type = self.filter_var.get()

        count = 0
        for service in self.all_services:
            # Search filter
            if search_text:
                if (search_text not in service.get('name', '').lower() and
                    search_text not in service.get('display_name', '').lower()):
                    continue

            # Status filter
            status = service.get('status', '').lower()
            if filter_type == 'running' and 'running' not in status:
                continue
            elif filter_type == 'stopped' and 'stopped' not in status:
                continue

            # Insert to tree
            self.services_tree.insert('', 'end', values=(
                service.get('name', 'N/A'),
                service.get('display_name', 'N/A'),
                service.get('status', 'N/A'),
                service.get('startup_type', 'N/A')
            ))
            count += 1

        self.log(f"📊 Hiển thị {count} services", "info")

    def get_selected_service(self):
        """Get selected service name"""
        selection = self.services_tree.selection()
        if not selection:
            self.show_error("Lỗi", "Vui lòng chọn một service!")
            return None

        item = self.services_tree.item(selection[0])
        return item['values'][0]  # Service name

    def start_service(self):
        """Start selected service"""
        service_name = self.get_selected_service()
        if not service_name:
            return

        if not self.confirm("Xác nhận", f"Start service '{service_name}'?"):
            return

        self.log(f"▶ Đang start service: {service_name}...", "info")

        def start():
            try:
                win32serviceutil.StartService(service_name)
                self.log(f"✅ Đã start service: {service_name}", "success")
                self.load_services()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=start, daemon=True).start()

    def stop_service(self):
        """Stop selected service"""
        service_name = self.get_selected_service()
        if not service_name:
            return

        if not self.confirm("Xác nhận", f"Stop service '{service_name}'?"):
            return

        self.log(f"■ Đang stop service: {service_name}...", "info")

        def stop():
            try:
                win32serviceutil.StopService(service_name)
                self.log(f"✅ Đã stop service: {service_name}", "success")
                self.load_services()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=stop, daemon=True).start()

    def restart_service(self):
        """Restart selected service"""
        service_name = self.get_selected_service()
        if not service_name:
            return

        if not self.confirm("Xác nhận", f"Restart service '{service_name}'?"):
            return

        self.log(f"🔄 Đang restart service: {service_name}...", "info")

        def restart():
            try:
                win32serviceutil.RestartService(service_name)
                self.log(f"✅ Đã restart service: {service_name}", "success")
                self.load_services()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=restart, daemon=True).start()

    def set_startup_type(self, startup_type):
        """Set service startup type (Auto/Manual/Disabled)"""
        service_name = self.get_selected_service()
        if not service_name:
            return

        if not self.confirm("Xác nhận", f"Đặt '{service_name}' startup type thành '{startup_type}'?"):
            return

        self.log(f"⚙️ Đang đặt startup type: {service_name} → {startup_type}...", "info")

        def set_type():
            try:
                # Map to sc config values
                sc_type_map = {
                    'Auto': 'auto',
                    'Manual': 'demand',
                    'Disabled': 'disabled'
                }

                sc_type = sc_type_map.get(startup_type, 'demand')

                result = subprocess.run(
                    f'sc config "{service_name}" start= {sc_type}',
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=10
                )

                if result.returncode == 0:
                    self.log(f"✅ Đã đặt startup type: {service_name} → {startup_type}", "success")
                    self.load_services()
                else:
                    self.log(f"❌ Lỗi: {result.stderr}", "error")

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=set_type, daemon=True).start()

    def open_startup_manager(self):
        """Open Task Manager Startup tab"""
        self.log("🚀 Đang mở Task Manager → Startup...", "info")
        try:
            subprocess.Popen('taskmgr.exe /0 /startup', shell=True)
            self.log("✅ Đã mở Task Manager!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")

    def open_msconfig(self):
        """Open System Configuration"""
        self.log("⚙️ Đang mở msconfig...", "info")
        try:
            subprocess.Popen('msconfig', shell=True)
            self.log("✅ Đã mở msconfig!", "success")
        except Exception as e:
            self.log(f"❌ Lỗi: {str(e)}", "error")
