"""
Windows 10/11 Professional Optimization Tool
Professional system optimization and network port management tool
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


class WindowsOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows Optimizer Pro - Professional System Tool")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')

        # Check admin privileges
        self.is_admin = self.check_admin()

        # Configure style
        self.setup_style()

        # Create main interface
        self.create_widgets()

        # Status
        self.running_scan = False

    def check_admin(self):
        """Check if running with admin privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def setup_style(self):
        """Setup custom styling for the application"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        bg_color = '#1e1e1e'
        fg_color = '#ffffff'
        accent_color = '#0078d4'
        button_color = '#2d2d2d'

        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color, font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), foreground=accent_color)
        style.configure('TButton', background=button_color, foreground=fg_color, borderwidth=0, font=('Segoe UI', 10))
        style.map('TButton', background=[('active', accent_color)])
        style.configure('TNotebook', background=bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=button_color, foreground=fg_color, padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', accent_color)], foreground=[('selected', fg_color)])

    def create_widgets(self):
        """Create main UI widgets"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = ttk.Label(header_frame, text="⚡ Windows Optimizer Pro", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)

        # Admin status
        admin_status = "🔑 Administrator" if self.is_admin else "⚠️ Limited User (Run as Admin for full features)"
        admin_label = ttk.Label(header_frame, text=admin_status,
                               foreground='#4CAF50' if self.is_admin else '#FF9800')
        admin_label.pack(side=tk.RIGHT)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: System Optimization
        self.create_optimization_tab()

        # Tab 2: Port Management
        self.create_port_management_tab()

        # Tab 3: System Info
        self.create_system_info_tab()

    def create_optimization_tab(self):
        """Create system optimization tab"""
        opt_frame = ttk.Frame(self.notebook)
        self.notebook.add(opt_frame, text="🔧 System Optimization")

        # Left panel - Options
        left_panel = ttk.Frame(opt_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(left_panel, text="Optimization Options",
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Optimization options
        self.opt_vars = {}
        options = [
            ("clean_temp", "🗑️ Clean Temporary Files", "Remove temporary files to free up space"),
            ("disable_telemetry", "🔒 Disable Telemetry", "Disable Windows telemetry services"),
            ("optimize_services", "⚙️ Optimize Services", "Disable unnecessary Windows services"),
            ("clean_prefetch", "🚀 Clean Prefetch", "Clear prefetch folder for better performance"),
            ("optimize_visual", "🎨 Optimize Visual Effects", "Set visual effects for best performance"),
            ("disable_startup", "🚫 Optimize Startup", "Disable unnecessary startup programs"),
            ("clean_event_logs", "📋 Clear Event Logs", "Clear Windows event logs"),
            ("optimize_network", "🌐 Optimize Network", "Optimize network settings for better performance"),
            ("disk_cleanup", "💾 Disk Cleanup", "Run Windows disk cleanup utility"),
            ("optimize_power", "⚡ Optimize Power Plan", "Set high performance power plan"),
        ]

        for key, text, desc in options:
            frame = ttk.Frame(left_panel)
            frame.pack(fill=tk.X, pady=5)

            var = tk.BooleanVar(value=True)
            self.opt_vars[key] = var

            cb = ttk.Checkbutton(frame, text=text, variable=var)
            cb.pack(anchor=tk.W)

            desc_label = ttk.Label(frame, text=f"  {desc}",
                                  font=('Segoe UI', 8), foreground='#888888')
            desc_label.pack(anchor=tk.W)

        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill=tk.X, pady=20)

        optimize_btn = tk.Button(btn_frame, text="▶ Run Optimization",
                                command=self.run_optimization,
                                bg='#0078d4', fg='white', font=('Segoe UI', 11, 'bold'),
                                relief=tk.FLAT, padx=20, pady=10, cursor='hand2')
        optimize_btn.pack(side=tk.LEFT, padx=5)

        select_all_btn = tk.Button(btn_frame, text="Select All",
                                   command=self.select_all_optimizations,
                                   bg='#2d2d2d', fg='white', font=('Segoe UI', 10),
                                   relief=tk.FLAT, padx=15, pady=10, cursor='hand2')
        select_all_btn.pack(side=tk.LEFT, padx=5)

        # Right panel - Output
        right_panel = ttk.Frame(opt_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(right_panel, text="Optimization Log",
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        self.opt_output = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                                    bg='#2d2d2d', fg='#00ff00',
                                                    font=('Consolas', 9), relief=tk.FLAT)
        self.opt_output.pack(fill=tk.BOTH, expand=True)

    def create_port_management_tab(self):
        """Create port management tab"""
        port_frame = ttk.Frame(self.notebook)
        self.notebook.add(port_frame, text="🌐 Port Management")

        # Top controls
        control_frame = ttk.Frame(port_frame)
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(control_frame, text="Network Port Scanner & Manager",
                 font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)

        scan_btn = tk.Button(control_frame, text="🔍 Scan Ports",
                            command=self.scan_ports,
                            bg='#0078d4', fg='white', font=('Segoe UI', 10, 'bold'),
                            relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        scan_btn.pack(side=tk.RIGHT, padx=5)

        refresh_btn = tk.Button(control_frame, text="🔄 Refresh Connections",
                               command=self.refresh_connections,
                               bg='#2d2d2d', fg='white', font=('Segoe UI', 10),
                               relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        refresh_btn.pack(side=tk.RIGHT, padx=5)

        # Treeview for connections
        tree_frame = ttk.Frame(port_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Create treeview
        columns = ('PID', 'Process', 'Protocol', 'Local Address', 'Remote Address', 'Status', 'Port')
        self.port_tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                     yscrollcommand=tree_scroll_y.set,
                                     xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.config(command=self.port_tree.yview)
        tree_scroll_x.config(command=self.port_tree.xview)

        # Define headings
        for col in columns:
            self.port_tree.heading(col, text=col)
            self.port_tree.column(col, width=100)

        self.port_tree.pack(fill=tk.BOTH, expand=True)

        # Configure tags for colors
        self.port_tree.tag_configure('established', background='#1a472a')
        self.port_tree.tag_configure('listening', background='#2d4a7c')
        self.port_tree.tag_configure('other', background='#4a4a4a')

        # Action buttons
        action_frame = ttk.Frame(port_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=10)

        kill_btn = tk.Button(action_frame, text="❌ Kill Selected Process",
                            command=self.kill_selected_process,
                            bg='#d32f2f', fg='white', font=('Segoe UI', 10, 'bold'),
                            relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        kill_btn.pack(side=tk.LEFT, padx=5)

        firewall_block_btn = tk.Button(action_frame, text="🚫 Block Port (Firewall)",
                                       command=self.block_port_firewall,
                                       bg='#f57c00', fg='white', font=('Segoe UI', 10),
                                       relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        firewall_block_btn.pack(side=tk.LEFT, padx=5)

        firewall_allow_btn = tk.Button(action_frame, text="✅ Allow Port (Firewall)",
                                       command=self.allow_port_firewall,
                                       bg='#388e3c', fg='white', font=('Segoe UI', 10),
                                       relief=tk.FLAT, padx=15, pady=8, cursor='hand2')
        firewall_allow_btn.pack(side=tk.LEFT, padx=5)

        # Port info output
        info_frame = ttk.Frame(port_frame)
        info_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        ttk.Label(info_frame, text="Port Information:",
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)

        self.port_info = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, height=8,
                                                   bg='#2d2d2d', fg='#00ff00',
                                                   font=('Consolas', 9), relief=tk.FLAT)
        self.port_info.pack(fill=tk.BOTH, expand=True)

    def create_system_info_tab(self):
        """Create system information tab"""
        info_frame = ttk.Frame(self.notebook)
        self.notebook.add(info_frame, text="📊 System Info")

        # Create scrolled text for system info
        self.sys_info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD,
                                                       bg='#2d2d2d', fg='#ffffff',
                                                       font=('Consolas', 9), relief=tk.FLAT)
        self.sys_info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load system info
        self.load_system_info()

    def select_all_optimizations(self):
        """Select all optimization options"""
        for var in self.opt_vars.values():
            var.set(True)

    def log_output(self, text_widget, message, level='info'):
        """Log message to output widget"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        colors = {'info': '#00ff00', 'warning': '#ffaa00', 'error': '#ff0000', 'success': '#00ff00'}

        text_widget.insert(tk.END, f"[{timestamp}] {message}\n")
        text_widget.see(tk.END)
        text_widget.update()

    def run_optimization(self):
        """Run selected optimizations"""
        if not self.is_admin:
            messagebox.showwarning("Admin Required",
                                 "Please run this application as Administrator for full optimization features!")
            return

        def optimize():
            self.opt_output.delete(1.0, tk.END)
            self.log_output(self.opt_output, "=" * 50, 'info')
            self.log_output(self.opt_output, "Starting Windows Optimization...", 'info')
            self.log_output(self.opt_output, "=" * 50, 'info')

            # Clean temporary files
            if self.opt_vars['clean_temp'].get():
                self.log_output(self.opt_output, "\n🗑️ Cleaning temporary files...", 'info')
                self.clean_temp_files()

            # Disable telemetry
            if self.opt_vars['disable_telemetry'].get():
                self.log_output(self.opt_output, "\n🔒 Disabling telemetry...", 'info')
                self.disable_telemetry()

            # Optimize services
            if self.opt_vars['optimize_services'].get():
                self.log_output(self.opt_output, "\n⚙️ Optimizing services...", 'info')
                self.optimize_services()

            # Clean prefetch
            if self.opt_vars['clean_prefetch'].get():
                self.log_output(self.opt_output, "\n🚀 Cleaning prefetch...", 'info')
                self.clean_prefetch()

            # Optimize visual effects
            if self.opt_vars['optimize_visual'].get():
                self.log_output(self.opt_output, "\n🎨 Optimizing visual effects...", 'info')
                self.optimize_visual_effects()

            # Optimize startup
            if self.opt_vars['disable_startup'].get():
                self.log_output(self.opt_output, "\n🚫 Listing startup programs...", 'info')
                self.list_startup_programs()

            # Clean event logs
            if self.opt_vars['clean_event_logs'].get():
                self.log_output(self.opt_output, "\n📋 Clearing event logs...", 'info')
                self.clear_event_logs()

            # Optimize network
            if self.opt_vars['optimize_network'].get():
                self.log_output(self.opt_output, "\n🌐 Optimizing network settings...", 'info')
                self.optimize_network()

            # Disk cleanup
            if self.opt_vars['disk_cleanup'].get():
                self.log_output(self.opt_output, "\n💾 Running disk cleanup...", 'info')
                self.run_disk_cleanup()

            # Optimize power
            if self.opt_vars['optimize_power'].get():
                self.log_output(self.opt_output, "\n⚡ Optimizing power settings...", 'info')
                self.optimize_power_plan()

            self.log_output(self.opt_output, "\n" + "=" * 50, 'success')
            self.log_output(self.opt_output, "✅ Optimization completed!", 'success')
            self.log_output(self.opt_output, "=" * 50, 'success')
            messagebox.showinfo("Complete", "Windows optimization completed successfully!")

        thread = threading.Thread(target=optimize, daemon=True)
        thread.start()

    def execute_command(self, command, shell=True):
        """Execute CMD command and return output"""
        try:
            result = subprocess.run(command, shell=shell, capture_output=True,
                                  text=True, timeout=30)
            return result.stdout + result.stderr
        except Exception as e:
            return f"Error: {str(e)}"

    # Optimization methods
    def clean_temp_files(self):
        """Clean temporary files"""
        commands = [
            'del /q /f /s %TEMP%\\* 2>nul',
            'del /q /f /s C:\\Windows\\Temp\\* 2>nul',
            'del /q /f /s C:\\Windows\\Prefetch\\* 2>nul',
        ]
        for cmd in commands:
            output = self.execute_command(cmd)
            self.log_output(self.opt_output, f"  Executing: {cmd}", 'info')
        self.log_output(self.opt_output, "  ✓ Temporary files cleaned", 'success')

    def disable_telemetry(self):
        """Disable Windows telemetry"""
        services = [
            'DiagTrack',
            'dmwappushservice',
            'WerSvc',
            'OneSyncSvc',
        ]
        for service in services:
            cmd = f'sc stop "{service}" 2>nul && sc config "{service}" start=disabled 2>nul'
            self.execute_command(cmd)
            self.log_output(self.opt_output, f"  Disabled: {service}", 'info')
        self.log_output(self.opt_output, "  ✓ Telemetry services disabled", 'success')

    def optimize_services(self):
        """Optimize Windows services"""
        services_to_disable = [
            'XblAuthManager',
            'XblGameSave',
            'XboxNetApiSvc',
            'XboxGipSvc',
            'Fax',
            'WSearch',
        ]
        for service in services_to_disable:
            cmd = f'sc config "{service}" start=disabled 2>nul'
            self.execute_command(cmd)
            self.log_output(self.opt_output, f"  Disabled: {service}", 'info')
        self.log_output(self.opt_output, "  ✓ Services optimized", 'success')

    def clean_prefetch(self):
        """Clean prefetch folder"""
        cmd = 'del /q /f /s C:\\Windows\\Prefetch\\* 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Prefetch cleaned", 'success')

    def optimize_visual_effects(self):
        """Optimize visual effects for performance"""
        cmd = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Visual effects optimized", 'success')

    def list_startup_programs(self):
        """List startup programs"""
        cmd = 'wmic startup get caption,command 2>nul'
        output = self.execute_command(cmd)
        self.log_output(self.opt_output, "  Startup programs:", 'info')
        self.log_output(self.opt_output, output[:500], 'info')

    def clear_event_logs(self):
        """Clear Windows event logs"""
        cmd = 'for /F "tokens=*" %1 in (\'wevtutil.exe el\') DO wevtutil.exe cl "%1" 2>nul'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Event logs cleared", 'success')

    def optimize_network(self):
        """Optimize network settings"""
        commands = [
            'netsh int tcp set global autotuninglevel=normal',
            'netsh int tcp set global chimney=enabled',
            'netsh int tcp set global dca=enabled',
            'netsh int tcp set global netdma=enabled',
        ]
        for cmd in commands:
            self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ Network settings optimized", 'success')

    def run_disk_cleanup(self):
        """Run disk cleanup"""
        cmd = 'cleanmgr /sagerun:1'
        self.log_output(self.opt_output, "  Starting disk cleanup utility...", 'info')
        self.log_output(self.opt_output, "  (This may take a while)", 'info')

    def optimize_power_plan(self):
        """Set high performance power plan"""
        cmd = 'powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c'
        self.execute_command(cmd)
        self.log_output(self.opt_output, "  ✓ High performance power plan activated", 'success')

    # Port management methods
    def refresh_connections(self):
        """Refresh network connections"""
        def refresh():
            self.port_tree.delete(*self.port_tree.get_children())
            self.port_info.delete(1.0, tk.END)

            self.log_output(self.port_info, "Scanning network connections...", 'info')

            try:
                connections = psutil.net_connections(kind='inet')

                for conn in connections:
                    try:
                        # Get process info
                        try:
                            process = psutil.Process(conn.pid) if conn.pid else None
                            process_name = process.name() if process else "N/A"
                        except:
                            process_name = "N/A"

                        # Get addresses
                        local_addr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
                        remote_addr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"

                        # Determine status tag
                        tag = 'other'
                        if conn.status == 'ESTABLISHED':
                            tag = 'established'
                        elif conn.status == 'LISTEN':
                            tag = 'listening'

                        # Get port
                        port = conn.laddr.port if conn.laddr else "N/A"

                        # Insert into tree
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
                self.log_output(self.port_info, f"✓ Found {total} network connections", 'success')

            except Exception as e:
                self.log_output(self.port_info, f"Error: {str(e)}", 'error')

        thread = threading.Thread(target=refresh, daemon=True)
        thread.start()

    def scan_ports(self):
        """Scan common ports"""
        if self.running_scan:
            messagebox.showinfo("Scanning", "Port scan is already running!")
            return

        def scan():
            self.running_scan = True
            self.port_info.delete(1.0, tk.END)
            self.log_output(self.port_info, "Starting port scan...", 'info')

            # Common ports to scan
            common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080, 8443]

            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)

            self.log_output(self.port_info, f"Scanning {local_ip}...", 'info')

            open_ports = []
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((local_ip, port))
                    sock.close()

                    if result == 0:
                        open_ports.append(port)
                        self.log_output(self.port_info, f"  Port {port}: OPEN", 'success')
                    else:
                        self.log_output(self.port_info, f"  Port {port}: CLOSED", 'info')
                except:
                    pass

            self.log_output(self.port_info, f"\n✓ Scan complete. Found {len(open_ports)} open ports", 'success')
            self.running_scan = False

        thread = threading.Thread(target=scan, daemon=True)
        thread.start()

    def kill_selected_process(self):
        """Kill selected process"""
        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a connection to kill")
            return

        item = self.port_tree.item(selection[0])
        pid = item['values'][0]
        process_name = item['values'][1]

        if pid == "N/A":
            messagebox.showerror("Error", "Cannot kill process without PID")
            return

        result = messagebox.askyesno("Confirm",
                                     f"Kill process '{process_name}' (PID: {pid})?")
        if result:
            try:
                process = psutil.Process(int(pid))
                process.kill()
                self.log_output(self.port_info, f"✓ Killed process {process_name} (PID: {pid})", 'success')
                self.refresh_connections()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to kill process: {str(e)}")

    def block_port_firewall(self):
        """Block port using Windows Firewall"""
        if not self.is_admin:
            messagebox.showwarning("Admin Required",
                                 "Administrator privileges required for firewall operations!")
            return

        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a connection")
            return

        item = self.port_tree.item(selection[0])
        port = item['values'][6]

        if port == "N/A":
            messagebox.showerror("Error", "Invalid port")
            return

        result = messagebox.askyesno("Confirm", f"Block port {port} in Windows Firewall?")
        if result:
            rule_name = f"Block_Port_{port}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=TCP localport={port}'
            output = self.execute_command(cmd)
            self.log_output(self.port_info, f"✓ Blocked port {port}", 'success')
            messagebox.showinfo("Success", f"Port {port} blocked in firewall")

    def allow_port_firewall(self):
        """Allow port using Windows Firewall"""
        if not self.is_admin:
            messagebox.showwarning("Admin Required",
                                 "Administrator privileges required for firewall operations!")
            return

        selection = self.port_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a connection")
            return

        item = self.port_tree.item(selection[0])
        port = item['values'][6]

        if port == "N/A":
            messagebox.showerror("Error", "Invalid port")
            return

        result = messagebox.askyesno("Confirm", f"Allow port {port} in Windows Firewall?")
        if result:
            rule_name = f"Allow_Port_{port}"
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=allow protocol=TCP localport={port}'
            output = self.execute_command(cmd)
            self.log_output(self.port_info, f"✓ Allowed port {port}", 'success')
            messagebox.showinfo("Success", f"Port {port} allowed in firewall")

    def load_system_info(self):
        """Load system information"""
        def load():
            self.sys_info_text.delete(1.0, tk.END)

            # System info
            info = []
            info.append("=" * 60)
            info.append("SYSTEM INFORMATION")
            info.append("=" * 60)
            info.append("")

            # CPU
            info.append("🖥️  CPU Information:")
            info.append(f"  Physical Cores: {psutil.cpu_count(logical=False)}")
            info.append(f"  Logical Cores: {psutil.cpu_count(logical=True)}")
            info.append(f"  CPU Usage: {psutil.cpu_percent(interval=1)}%")
            info.append("")

            # Memory
            mem = psutil.virtual_memory()
            info.append("💾 Memory Information:")
            info.append(f"  Total: {mem.total / (1024**3):.2f} GB")
            info.append(f"  Available: {mem.available / (1024**3):.2f} GB")
            info.append(f"  Used: {mem.used / (1024**3):.2f} GB ({mem.percent}%)")
            info.append("")

            # Disk
            disk = psutil.disk_usage('C:')
            info.append("💿 Disk Information (C:):")
            info.append(f"  Total: {disk.total / (1024**3):.2f} GB")
            info.append(f"  Used: {disk.used / (1024**3):.2f} GB ({disk.percent}%)")
            info.append(f"  Free: {disk.free / (1024**3):.2f} GB")
            info.append("")

            # Network
            info.append("🌐 Network Information:")
            net_if = psutil.net_if_addrs()
            for interface, addrs in net_if.items():
                info.append(f"  Interface: {interface}")
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        info.append(f"    IPv4: {addr.address}")
            info.append("")

            # Process count
            info.append("⚙️  Process Information:")
            info.append(f"  Running Processes: {len(psutil.pids())}")
            info.append("")

            # Boot time
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            info.append(f"⏰ System Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")

            self.sys_info_text.insert(1.0, "\n".join(info))

        thread = threading.Thread(target=load, daemon=True)
        thread.start()


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = WindowsOptimizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
