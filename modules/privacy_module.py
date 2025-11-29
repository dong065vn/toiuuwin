"""
Privacy Tweaks Module - Bảo mật & Riêng tư
Module tối ưu quyền riêng tư, tắt telemetry, tracking
"""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
from .base import BaseModule
from .ui_components import ModernUI, Card, ModernButton


class PrivacyModule(BaseModule):
    """Module Privacy & Telemetry Tweaks"""

    def get_module_info(self):
        return {
            'icon': '🔒',
            'name': 'Privacy Tweaks',
            'description': 'Bảo vệ quyền riêng tư, tắt tracking',
            'category': 'security'
        }

    def create_ui(self):
        """Tạo UI cho Privacy Module"""
        main = tk.Frame(self.parent, bg=self.colors['bg_main'])

        # Header
        header = tk.Frame(main, bg=self.colors['bg_main'])
        header.pack(fill='x', padx=20, pady=20)

        tk.Label(
            header,
            text="🔒 Privacy Tweaks - Bảo vệ quyền riêng tư",
            bg=self.colors['bg_main'],
            fg=self.colors['text_primary'],
            font=ModernUI.FONTS['heading']
        ).pack(side='left')

        # Content with scrolling
        from .ui_components import ScrollableFrame
        content = ScrollableFrame(main)
        content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        # Info Card
        info_card = Card(content.scrollable_frame, title="ℹ️ Giới thiệu")
        info_card.pack(fill='x', pady=(0, 16))

        tk.Label(
            info_card.content_frame,
            text="Module này giúp bảo vệ quyền riêng tư bằng cách tắt các tính năng thu thập dữ liệu,\n"
                 "telemetry, tracking của Windows và ứng dụng bên thứ ba.",
            bg=self.colors['bg_card'],
            fg=self.colors['text_secondary'],
            font=ModernUI.FONTS['body'],
            justify='left'
        ).pack(anchor='w', pady=4)

        # Privacy options
        self.privacy_vars = {}
        self.create_privacy_options(content.scrollable_frame)

        # Quick Action Buttons
        quick_card = Card(content.scrollable_frame, title="⚡ Hành động nhanh")
        quick_card.pack(fill='x', pady=(16, 0))

        quick_frame = tk.Frame(quick_card.content_frame, bg=self.colors['bg_card'])
        quick_frame.pack(fill='x', pady=8)

        ModernButton(
            quick_frame, "🛡️ Tối đa Privacy",
            command=self.maximum_privacy,
            style='primary', width=160, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            quick_frame, "⚖️ Privacy cân bằng",
            command=self.balanced_privacy,
            style='info', width=160, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            quick_frame, "✅ Áp dụng đã chọn",
            command=self.apply_privacy_tweaks,
            style='success', width=160, height=40
        ).pack(side='left', padx=4)

        ModernButton(
            quick_frame, "↺ Khôi phục mặc định",
            command=self.restore_defaults,
            style='warning', width=160, height=40
        ).pack(side='left', padx=4)

        # Console
        self.create_console(main)
        self.log("Module Privacy Tweaks đã sẵn sàng", "success")

        return main

    def create_privacy_options(self, parent):
        """Tạo các tùy chọn privacy"""

        # 📡 Telemetry & Data Collection
        telemetry_card = Card(parent, title="📡 Telemetry & Thu thập dữ liệu")
        telemetry_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_telemetry'] = tk.BooleanVar()
        self.privacy_vars['disable_diagtrack'] = tk.BooleanVar()
        self.privacy_vars['disable_error_reporting'] = tk.BooleanVar()
        self.privacy_vars['disable_feedback'] = tk.BooleanVar()

        ttk.Checkbutton(telemetry_card.content_frame,
                       text="🛡️ Tắt Windows Telemetry (DiagTrack)",
                       variable=self.privacy_vars['disable_telemetry']).pack(anchor='w', pady=2)
        ttk.Checkbutton(telemetry_card.content_frame,
                       text="🛡️ Tắt Connected User Experiences",
                       variable=self.privacy_vars['disable_diagtrack']).pack(anchor='w', pady=2)
        ttk.Checkbutton(telemetry_card.content_frame,
                       text="🛡️ Tắt Windows Error Reporting",
                       variable=self.privacy_vars['disable_error_reporting']).pack(anchor='w', pady=2)
        ttk.Checkbutton(telemetry_card.content_frame,
                       text="🛡️ Tắt Feedback Notifications",
                       variable=self.privacy_vars['disable_feedback']).pack(anchor='w', pady=2)

        # 🎯 Advertising & Personalization
        ads_card = Card(parent, title="🎯 Quảng cáo & Cá nhân hóa")
        ads_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_advertising_id'] = tk.BooleanVar()
        self.privacy_vars['disable_suggested_content'] = tk.BooleanVar()
        self.privacy_vars['disable_tips'] = tk.BooleanVar()
        self.privacy_vars['disable_tailored_exp'] = tk.BooleanVar()

        ttk.Checkbutton(ads_card.content_frame,
                       text="🎯 Tắt Advertising ID",
                       variable=self.privacy_vars['disable_advertising_id']).pack(anchor='w', pady=2)
        ttk.Checkbutton(ads_card.content_frame,
                       text="🎯 Tắt Suggested Content (Start Menu)",
                       variable=self.privacy_vars['disable_suggested_content']).pack(anchor='w', pady=2)
        ttk.Checkbutton(ads_card.content_frame,
                       text="🎯 Tắt Windows Tips & Suggestions",
                       variable=self.privacy_vars['disable_tips']).pack(anchor='w', pady=2)
        ttk.Checkbutton(ads_card.content_frame,
                       text="🎯 Tắt Tailored Experiences",
                       variable=self.privacy_vars['disable_tailored_exp']).pack(anchor='w', pady=2)

        # 🌐 Network & Location
        network_card = Card(parent, title="🌐 Mạng & Vị trí")
        network_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_location'] = tk.BooleanVar()
        self.privacy_vars['disable_wifi_sense'] = tk.BooleanVar()
        self.privacy_vars['disable_network_discovery'] = tk.BooleanVar()

        ttk.Checkbutton(network_card.content_frame,
                       text="📍 Tắt Location Tracking",
                       variable=self.privacy_vars['disable_location']).pack(anchor='w', pady=2)
        ttk.Checkbutton(network_card.content_frame,
                       text="📡 Tắt WiFi Sense",
                       variable=self.privacy_vars['disable_wifi_sense']).pack(anchor='w', pady=2)
        ttk.Checkbutton(network_card.content_frame,
                       text="🌐 Tắt Network Discovery (nếu không dùng mạng LAN)",
                       variable=self.privacy_vars['disable_network_discovery']).pack(anchor='w', pady=2)

        # 🎤 App Permissions
        permissions_card = Card(parent, title="🎤 Quyền truy cập ứng dụng")
        permissions_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_camera'] = tk.BooleanVar()
        self.privacy_vars['disable_microphone'] = tk.BooleanVar()
        self.privacy_vars['disable_notifications'] = tk.BooleanVar()
        self.privacy_vars['disable_account_info'] = tk.BooleanVar()

        ttk.Checkbutton(permissions_card.content_frame,
                       text="📷 Tắt Camera cho apps",
                       variable=self.privacy_vars['disable_camera']).pack(anchor='w', pady=2)
        ttk.Checkbutton(permissions_card.content_frame,
                       text="🎤 Tắt Microphone cho apps",
                       variable=self.privacy_vars['disable_microphone']).pack(anchor='w', pady=2)
        ttk.Checkbutton(permissions_card.content_frame,
                       text="🔔 Tắt Notifications cho apps",
                       variable=self.privacy_vars['disable_notifications']).pack(anchor='w', pady=2)
        ttk.Checkbutton(permissions_card.content_frame,
                       text="👤 Tắt Account Info cho apps",
                       variable=self.privacy_vars['disable_account_info']).pack(anchor='w', pady=2)

        # 🔍 Cortana & Search
        cortana_card = Card(parent, title="🔍 Cortana & Search")
        cortana_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_cortana'] = tk.BooleanVar()
        self.privacy_vars['disable_web_search'] = tk.BooleanVar()
        self.privacy_vars['disable_bing_search'] = tk.BooleanVar()

        ttk.Checkbutton(cortana_card.content_frame,
                       text="🔍 Tắt Cortana hoàn toàn",
                       variable=self.privacy_vars['disable_cortana']).pack(anchor='w', pady=2)
        ttk.Checkbutton(cortana_card.content_frame,
                       text="🌐 Tắt Web Search trong Start Menu",
                       variable=self.privacy_vars['disable_web_search']).pack(anchor='w', pady=2)
        ttk.Checkbutton(cortana_card.content_frame,
                       text="🔎 Tắt Bing Search trong Start Menu",
                       variable=self.privacy_vars['disable_bing_search']).pack(anchor='w', pady=2)

        # 🎮 Xbox & Gaming
        xbox_card = Card(parent, title="🎮 Xbox & Gaming")
        xbox_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_xbox_features'] = tk.BooleanVar()
        self.privacy_vars['disable_game_dvr'] = tk.BooleanVar()

        ttk.Checkbutton(xbox_card.content_frame,
                       text="🎮 Tắt Xbox Live features",
                       variable=self.privacy_vars['disable_xbox_features']).pack(anchor='w', pady=2)
        ttk.Checkbutton(xbox_card.content_frame,
                       text="🎬 Tắt Game DVR & Game Bar",
                       variable=self.privacy_vars['disable_game_dvr']).pack(anchor='w', pady=2)

        # 🌍 Cloud & Sync
        cloud_card = Card(parent, title="☁️ Cloud & Sync")
        cloud_card.pack(fill='x', pady=(0, 12))

        self.privacy_vars['disable_onedrive'] = tk.BooleanVar()
        self.privacy_vars['disable_sync_settings'] = tk.BooleanVar()

        ttk.Checkbutton(cloud_card.content_frame,
                       text="☁️ Tắt OneDrive sync",
                       variable=self.privacy_vars['disable_onedrive']).pack(anchor='w', pady=2)
        ttk.Checkbutton(cloud_card.content_frame,
                       text="🔄 Tắt Settings Sync",
                       variable=self.privacy_vars['disable_sync_settings']).pack(anchor='w', pady=2)

    def maximum_privacy(self):
        """Chế độ privacy tối đa - tắt tất cả"""
        if not self.confirm("Xác nhận",
                           "Bật TẤT CẢ các tùy chọn privacy?\n\n"
                           "Điều này sẽ tắt nhiều tính năng của Windows."):
            return

        for var in self.privacy_vars.values():
            var.set(True)

        self.log("🛡️ Đã chọn chế độ Privacy tối đa", "success")
        messagebox.showinfo("Thông báo", "Đã chọn tất cả các tùy chọn privacy.\nNhấn 'Áp dụng đã chọn' để thực thi.")

    def balanced_privacy(self):
        """Chế độ privacy cân bằng"""
        # Uncheck all first
        for var in self.privacy_vars.values():
            var.set(False)

        # Select balanced options
        balanced_options = [
            'disable_telemetry',
            'disable_diagtrack',
            'disable_advertising_id',
            'disable_suggested_content',
            'disable_tips',
            'disable_location',
            'disable_cortana',
            'disable_web_search',
            'disable_game_dvr'
        ]

        for option in balanced_options:
            if option in self.privacy_vars:
                self.privacy_vars[option].set(True)

        self.log("⚖️ Đã chọn chế độ Privacy cân bằng", "info")
        messagebox.showinfo("Thông báo", "Đã chọn các tùy chọn privacy cân bằng.\nNhấn 'Áp dụng đã chọn' để thực thi.")

    def apply_privacy_tweaks(self):
        """Áp dụng các privacy tweaks đã chọn"""
        self.log("🔒 Đang áp dụng Privacy Tweaks...", "info")

        def apply():
            count = 0

            # 📡 Telemetry
            if self.privacy_vars['disable_telemetry'].get():
                self.log("📡 Tắt Telemetry...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')
                self._execute('sc stop DiagTrack')
                self._execute('sc config DiagTrack start=disabled')
                count += 1

            if self.privacy_vars['disable_diagtrack'].get():
                self.log("📡 Tắt Connected User Experiences...", "info")
                self._execute('sc stop dmwappushservice')
                self._execute('sc config dmwappushservice start=disabled')
                count += 1

            if self.privacy_vars['disable_error_reporting'].get():
                self.log("📡 Tắt Error Reporting...", "info")
                self._execute('sc stop WerSvc')
                self._execute('sc config WerSvc start=disabled')
                count += 1

            if self.privacy_vars['disable_feedback'].get():
                self.log("📡 Tắt Feedback...", "info")
                self._execute('reg add "HKCU\\SOFTWARE\\Microsoft\\Siuf\\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f')
                count += 1

            # 🎯 Advertising
            if self.privacy_vars['disable_advertising_id'].get():
                self.log("🎯 Tắt Advertising ID...", "info")
                self._execute('reg add "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f')
                count += 1

            if self.privacy_vars['disable_suggested_content'].get():
                self.log("🎯 Tắt Suggested Content...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SilentInstalledAppsEnabled /t REG_DWORD /d 0 /f')
                count += 1

            if self.privacy_vars['disable_tips'].get():
                self.log("🎯 Tắt Tips...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SoftLandingEnabled /t REG_DWORD /d 0 /f')
                count += 1

            if self.privacy_vars['disable_tailored_exp'].get():
                self.log("🎯 Tắt Tailored Experiences...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Privacy" /v TailoredExperiencesWithDiagnosticDataEnabled /t REG_DWORD /d 0 /f')
                count += 1

            # 🌐 Network
            if self.privacy_vars['disable_location'].get():
                self.log("📍 Tắt Location...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location" /v Value /t REG_SZ /d Deny /f')
                count += 1

            if self.privacy_vars['disable_wifi_sense'].get():
                self.log("📡 Tắt WiFi Sense...", "info")
                self._execute('reg add "HKLM\\Software\\Microsoft\\PolicyManager\\default\\WiFi\\AllowWiFiHotSpotReporting" /v Value /t REG_DWORD /d 0 /f')
                count += 1

            # 🎤 App Permissions
            if self.privacy_vars['disable_camera'].get():
                self.log("📷 Tắt Camera...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\webcam" /v Value /t REG_SZ /d Deny /f')
                count += 1

            if self.privacy_vars['disable_microphone'].get():
                self.log("🎤 Tắt Microphone...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\microphone" /v Value /t REG_SZ /d Deny /f')
                count += 1

            # 🔍 Cortana
            if self.privacy_vars['disable_cortana'].get():
                self.log("🔍 Tắt Cortana...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f')
                count += 1

            if self.privacy_vars['disable_web_search'].get():
                self.log("🌐 Tắt Web Search...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v DisableWebSearch /t REG_DWORD /d 1 /f')
                count += 1

            if self.privacy_vars['disable_bing_search'].get():
                self.log("🔎 Tắt Bing Search...", "info")
                self._execute('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Search" /v BingSearchEnabled /t REG_DWORD /d 0 /f')
                count += 1

            # 🎮 Xbox
            if self.privacy_vars['disable_game_dvr'].get():
                self.log("🎬 Tắt Game DVR...", "info")
                self._execute('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f')
                self._execute('reg add "HKLM\\SOFTWARE\\Microsoft\\PolicyManager\\default\\ApplicationManagement\\AllowGameDVR" /v Value /t REG_DWORD /d 0 /f')
                count += 1

            # ☁️ Cloud
            if self.privacy_vars['disable_onedrive'].get():
                self.log("☁️ Tắt OneDrive...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /t REG_DWORD /d 1 /f')
                count += 1

            if self.privacy_vars['disable_sync_settings'].get():
                self.log("🔄 Tắt Settings Sync...", "info")
                self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\SettingSync" /v DisableSettingSync /t REG_DWORD /d 2 /f')
                count += 1

            self.log(f"✅ Hoàn thành! Đã áp dụng {count} privacy tweaks", "success")
            self.log("ℹ️ Một số thay đổi cần khởi động lại để có hiệu lực", "info")

        threading.Thread(target=apply, daemon=True).start()

    def restore_defaults(self):
        """Khôi phục cài đặt mặc định"""
        if not self.confirm("Xác nhận",
                           "Khôi phục tất cả privacy settings về mặc định?"):
            return

        self.log("↺ Đang khôi phục privacy settings...", "warning")

        def restore():
            self.log("🔄 Bật lại Telemetry...", "info")
            self._execute('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 3 /f')
            self._execute('sc config DiagTrack start=auto')

            self.log("🔄 Bật lại các services...", "info")
            self._execute('sc config dmwappushservice start=auto')
            self._execute('sc config WerSvc start=auto')

            self.log("🔄 Bật lại Location...", "info")
            self._execute('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location" /v Value /t REG_SZ /d Allow /f')

            self.log("✅ Đã khôi phục!", "success")

        threading.Thread(target=restore, daemon=True).start()

    def _execute(self, command):
        """Execute command"""
        try:
            subprocess.run(command, shell=True, check=True, capture_output=True, timeout=10)
            return True
        except:
            return False
