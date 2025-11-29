"""
Services Manager Module - Quản lý Windows Services
Module quản lý và tối ưu các dịch vụ Windows
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import psutil
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class ServicesModule(BaseModule):
    """Module quản lý Windows Services"""

    def __init__(self, parent):
        super().__init__(parent)
        # Services recommended to disable for optimization
        self.recommended_disable = {
            'DiagTrack': 'Connected User Experiences and Telemetry',
            'dmwappushservice': 'WAP Push Message Routing Service',
            'lfsvc': 'Geolocation Service',
            'MapsBroker': 'Downloaded Maps Manager',
            'NetTcpPortSharing': 'Net.Tcp Port Sharing Service',
            'RemoteAccess': 'Routing and Remote Access',
            'RemoteRegistry': 'Remote Registry',
            'RetailDemo': 'Retail Demo Service',
            'WMPNetworkSvc': 'Windows Media Player Network Sharing Service',
            'WSearch': 'Windows Search (if not used)',
            'XblAuthManager': 'Xbox Live Auth Manager',
            'XblGameSave': 'Xbox Live Game Save',
            'XboxGipSvc': 'Xbox Accessory Management',
            'XboxNetApiSvc': 'Xbox Live Networking Service'
        }

    def get_module_info(self):
        return {
            'icon': '⚙️',
            'name': 'Services Manager',
            'description': 'Quản lý dịch vụ Windows',
            'category': 'system'
        }

    def create_ui(self):
        """Tạo UI cho Services Manager"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="⚙️ Services Manager - Quản lý dịch vụ Windows",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Action buttons
        btn_frame = tk.Frame(header, bg=self.colors['bg_main'])
        btn_frame.pack(side='right')

        ModernButton(
            btn_frame, "Làm mới",
            command=self.load_services,
            icon="🔄", style='primary', width=120, height=36
        ).pack(side='left', padx=5)

        ModernButton(
            btn_frame, "Tối ưu tự động",
            command=self.auto_optimize,
            icon="🚀", style='success', width=150, height=36
        ).pack(side='left', padx=5)

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Filter Card
        filter_card = Card(content.scrollable_frame, title="🔍 Bộ lọc")
        filter_card.pack(fill='x', pady=(0, 16))

        filter_frame = tk.Frame(filter_card.content_frame, bg=self.colors['bg_card'])
        filter_frame.pack(fill='x', pady=8)

        tk.Label(
            filter_frame,
            text="Tìm kiếm:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=(0, 8))

        self.search_entry = tk.Entry(
            filter_frame,
            width=30,
            font=ModernUI.FONTS['body'],
            bg=self.colors['bg_input'],
            fg=self.colors['text_primary']
        )
        self.search_entry.pack(side='left', padx=4)
        self.search_entry.bind('<KeyRelease>', lambda e: self.filter_services())

        # Status filter
        tk.Label(
            filter_frame,
            text="Trạng thái:",
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body_bold']
        ).pack(side='left', padx=(20, 8))

        self.status_var = tk.StringVar(value='all')

        tk.Radiobutton(
            filter_frame, text="Tất cả",
            variable=self.status_var, value='all',
            command=self.filter_services,
            bg=self.colors['bg_card'], fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'], selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=2)

        tk.Radiobutton(
            filter_frame, text="Running",
            variable=self.status_var, value='running',
            command=self.filter_services,
            bg=self.colors['bg_card'], fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'], selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=2)

        tk.Radiobutton(
            filter_frame, text="Stopped",
            variable=self.status_var, value='stopped',
            command=self.filter_services,
            bg=self.colors['bg_card'], fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'], selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=2)

        tk.Radiobutton(
            filter_frame, text="Recommended",
            variable=self.status_var, value='recommended',
            command=self.filter_services,
            bg=self.colors['bg_card'], fg=self.colors['text_primary'],
            font=ModernUI.FONTS['body'], selectcolor=self.colors['bg_input']
        ).pack(side='left', padx=2)

        # Services TreeView Card
        services_card = Card(content.scrollable_frame, title="📋 Danh sách dịch vụ")
        services_card.pack(fill='both', expand=True, pady=(0, 16))

        # TreeView
        tree_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        tree_frame.pack(fill='both', expand=True, pady=(8, 12))

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        tree_scroll_y.pack(side='right', fill='y')

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_x.pack(side='bottom', fill='x')

        # TreeView
        columns = ('name', 'display_name', 'status', 'startup_type', 'description')
        self.services_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',
            height=14,
            yscrollcommand=tree_scroll_y.set,
            xscrollcommand=tree_scroll_x.set
        )

        tree_scroll_y.config(command=self.services_tree.yview)
        tree_scroll_x.config(command=self.services_tree.xview)

        # Column headings
        self.services_tree.heading('name', text='Tên dịch vụ')
        self.services_tree.heading('display_name', text='Tên hiển thị')
        self.services_tree.heading('status', text='Trạng thái')
        self.services_tree.heading('startup_type', text='Startup Type')
        self.services_tree.heading('description', text='Mô tả')

        # Column widths
        self.services_tree.column('name', width=150)
        self.services_tree.column('display_name', width=200)
        self.services_tree.column('status', width=100)
        self.services_tree.column('startup_type', width=120)
        self.services_tree.column('description', width=300)

        self.services_tree.pack(fill='both', expand=True)

        # Action buttons
        action_frame = tk.Frame(services_card.content_frame, bg=self.colors['bg_card'])
        action_frame.pack(fill='x', pady=8)

        ModernButton(
            action_frame, "▶️ Start",
            command=self.start_service,
            style='success', width=100, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "■ Stop",
            command=self.stop_service,
            style='danger', width=100, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "🔄 Restart",
            command=self.restart_service,
            style='warning', width=100, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "⚙️ Auto",
            command=lambda: self.set_startup_type('auto'),
            style='info', width=100, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "✋ Manual",
            command=lambda: self.set_startup_type('demand'),
            style='info', width=100, height=36
        ).pack(side='left', padx=4)

        ModernButton(
            action_frame, "⛔ Disabled",
            command=lambda: self.set_startup_type('disabled'),
            style='warning', width=100, height=36
        ).pack(side='left', padx=4)

        # Info Card
        info_card = Card(content.scrollable_frame, title="ℹ️ Thông tin")
        info_card.pack(fill='x', pady=(0, 0))

        tk.Label(
            info_card.content_frame,
            text="⚠️ CHÚ Ý: Chỉ tắt các dịch vụ nếu bạn hiểu rõ chức năng của chúng.\n"
                 "Tắt dịch vụ quan trọng có thể khiến Windows hoạt động không ổn định.\n\n"
                 "💡 Sử dụng 'Tối ưu tự động' để tắt các dịch vụ không cần thiết một cách an toàn.",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            justify='left'
        ).pack(anchor='w', pady=4)

        # Console
        self.create_console(main)
        self.log("Module Services Manager đã sẵn sàng", "success")

        # Store services
        self.all_services = []

        # Load services
        self.load_services()

        return main

    def load_services(self):
        """Load all Windows services"""
        self.log("🔄 Đang tải danh sách services...", "info")

        def load():
            try:
                self.all_services = []

                # Get services using sc query
                result = subprocess.run(
                    'sc query state= all',
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='ignore'
                )

                # Parse output
                current_service = {}
                for line in result.stdout.split('\n'):
                    line = line.strip()
                    if line.startswith('SERVICE_NAME:'):
                        if current_service:
                            self.all_services.append(current_service)
                        current_service = {'name': line.split(':', 1)[1].strip()}
                    elif line.startswith('DISPLAY_NAME:'):
                        current_service['display_name'] = line.split(':', 1)[1].strip()
                    elif 'STATE' in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            current_service['status'] = parts[3]

                if current_service:
                    self.all_services.append(current_service)

                # Get additional info for each service
                for service in self.all_services:
                    try:
                        result = subprocess.run(
                            f'sc qc "{service["name"]}"',
                            shell=True,
                            capture_output=True,
                            text=True,
                            encoding='utf-8',
                            errors='ignore',
                            timeout=2
                        )

                        for line in result.stdout.split('\n'):
                            if 'START_TYPE' in line:
                                parts = line.split()
                                if len(parts) >= 3:
                                    service['startup_type'] = parts[3]
                            elif 'DISPLAY_NAME' in line:
                                display = line.split(':', 1)[1].strip()
                                service['display_name'] = display

                        # Check if recommended to disable
                        if service['name'] in self.recommended_disable:
                            service['recommended'] = True
                            service['description'] = self.recommended_disable[service['name']]
                        else:
                            service['recommended'] = False
                            service['description'] = ''

                    except:
                        service['startup_type'] = 'UNKNOWN'
                        service['recommended'] = False
                        service['description'] = ''

                self.log(f"✅ Đã tải {len(self.all_services)} services", "success")
                self.filter_services()

            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=load, daemon=True).start()

    def filter_services(self):
        """Filter and display services"""
        # Clear tree
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)

        search_text = self.search_entry.get().lower()
        status_filter = self.status_var.get()

        # Filter
        filtered = []
        for service in self.all_services:
            # Status filter
            if status_filter == 'running' and service.get('status', '').upper() != 'RUNNING':
                continue
            if status_filter == 'stopped' and service.get('status', '').upper() == 'RUNNING':
                continue
            if status_filter == 'recommended' and not service.get('recommended', False):
                continue

            # Search filter
            if search_text:
                if (search_text not in service.get('name', '').lower() and
                    search_text not in service.get('display_name', '').lower() and
                    search_text not in service.get('description', '').lower()):
                    continue

            filtered.append(service)

        # Sort by name
        filtered.sort(key=lambda x: x.get('name', '').lower())

        # Display
        for service in filtered:
            # Color code by status
            status = service.get('status', '').upper()
            tag = 'running' if status == 'RUNNING' else 'stopped'

            self.services_tree.insert('', 'end', values=(
                service.get('name', ''),
                service.get('display_name', ''),
                service.get('status', ''),
                service.get('startup_type', ''),
                service.get('description', '')[:60] + '...' if len(service.get('description', '')) > 60 else service.get('description', '')
            ), tags=(tag,))

        # Configure tags
        self.services_tree.tag_configure('running', foreground=self.colors['success'])
        self.services_tree.tag_configure('stopped', foreground=self.colors['text_muted'])

        self.log(f"📊 Hiển thị {len(filtered)}/{len(self.all_services)} services", "info")

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

        self.log(f"▶️ Đang start service: {service_name}", "info")

        def start():
            try:
                subprocess.run(f'sc start "{service_name}"', shell=True, check=True, capture_output=True)
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

        if not self.confirm("Xác nhận", f"Stop service: {service_name}?"):
            return

        self.log(f"■ Đang stop service: {service_name}", "warning")

        def stop():
            try:
                subprocess.run(f'sc stop "{service_name}"', shell=True, check=True, capture_output=True)
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

        self.log(f"🔄 Đang restart service: {service_name}", "info")

        def restart():
            try:
                subprocess.run(f'sc stop "{service_name}"', shell=True, capture_output=True)
                subprocess.run(f'sc start "{service_name}"', shell=True, check=True, capture_output=True)
                self.log(f"✅ Đã restart service: {service_name}", "success")
                self.load_services()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=restart, daemon=True).start()

    def set_startup_type(self, startup_type):
        """Set startup type for selected service"""
        service_name = self.get_selected_service()
        if not service_name:
            return

        type_names = {'auto': 'Automatic', 'demand': 'Manual', 'disabled': 'Disabled'}
        type_name = type_names.get(startup_type, startup_type)

        if not self.confirm("Xác nhận", f"Đặt startup type của '{service_name}' thành '{type_name}'?"):
            return

        self.log(f"⚙️ Đang thay đổi startup type: {service_name} -> {type_name}", "info")

        def set_type():
            try:
                subprocess.run(
                    f'sc config "{service_name}" start= {startup_type}',
                    shell=True,
                    check=True,
                    capture_output=True
                )
                self.log(f"✅ Đã thay đổi startup type: {service_name}", "success")
                self.load_services()
            except Exception as e:
                self.log(f"❌ Lỗi: {str(e)}", "error")

        threading.Thread(target=set_type, daemon=True).start()

    def auto_optimize(self):
        """Auto optimize services"""
        if not self.confirm("Xác nhận",
                           "Tối ưu tự động sẽ:\n\n"
                           "1. Tắt các dịch vụ không cần thiết (telemetry, Xbox, ...)\n"
                           "2. Chuyển một số dịch vụ sang Manual\n\n"
                           "Tiếp tục?"):
            return

        self.log("🚀 Đang tối ưu services tự động...", "info")

        def optimize():
            count = 0
            for service_name in self.recommended_disable.keys():
                try:
                    # Set to disabled
                    subprocess.run(
                        f'sc config "{service_name}" start= disabled',
                        shell=True,
                        capture_output=True
                    )
                    # Try to stop
                    subprocess.run(
                        f'sc stop "{service_name}"',
                        shell=True,
                        capture_output=True
                    )
                    count += 1
                    self.log(f"⛔ Đã tắt: {service_name}", "info")
                except:
                    pass

            self.log(f"✅ Đã tối ưu {count} services!", "success")
            self.load_services()

        threading.Thread(target=optimize, daemon=True).start()
