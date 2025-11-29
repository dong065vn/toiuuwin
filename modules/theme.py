"""
Theme Management System
Hệ thống quản lý theme Light/Dark mode
"""


class ThemeManager:
    """Modern Theme System - Professional Grade Design"""

    # Light Theme - Ultra Modern & Clean (2025 Design)
    LIGHT_THEME = {
        # Primary - Modern Gradient Blue System
        'primary': '#2563EB',
        'primary_hover': '#1D4ED8',
        'primary_light': '#DBEAFE',
        'primary_dark': '#1E40AF',
        'gradient_start': '#3B82F6',
        'gradient_end': '#06B6D4',
        'gradient_purple': '#8B5CF6',

        # Secondary - Modern Emerald Green
        'secondary': '#10B981',
        'secondary_hover': '#059669',
        'secondary_light': '#D1FAE5',
        'secondary_dark': '#047857',

        # Status colors
        'success': '#22C55E',
        'success_light': '#DCFCE7',
        'danger': '#EF4444',
        'danger_light': '#FEE2E2',
        'warning': '#F59E0B',
        'warning_light': '#FEF3C7',
        'info': '#3B82F6',
        'info_light': '#DBEAFE',

        # Backgrounds
        'bg_main': '#FFFFFF',
        'bg_secondary': '#F9FAFB',
        'bg_sidebar': '#F9FAFB',
        'bg_card': '#FFFFFF',
        'bg_card_hover': '#F3F4F6',
        'bg_hover': '#F3F4F6',
        'bg_selected': '#DBEAFE',
        'bg_input': '#FFFFFF',

        # Text colors
        'text_primary': '#111827',
        'text_secondary': '#4B5563',
        'text_tertiary': '#6B7280',
        'text_white': '#FFFFFF',
        'text_muted': '#9CA3AF',
        'text_on_primary': '#FFFFFF',

        # Borders
        'border': '#E5E7EB',
        'border_strong': '#D1D5DB',
        'border_focus': '#3B82F6',
        'divider': '#F3F4F6',

        # Shadows
        'shadow_sm': '#F9FAFB',
        'shadow_md': '#F3F4F6',
        'shadow_lg': '#E5E7EB',
        'card_shadow': '#F3F4F6',

        # Console
        'console_bg': '#F9FAFB',
        'console_text': '#111827',
        'console_error': '#EF4444',
        'console_warning': '#F59E0B',
        'console_info': '#3B82F6',
        'console_success': '#22C55E',
    }

    # Dark Theme - Ultra Modern Dark (2025 Design)
    DARK_THEME = {
        # Primary - Vibrant Blue for Dark Mode
        'primary': '#60A5FA',
        'primary_hover': '#3B82F6',
        'primary_light': '#1E3A8A',
        'primary_dark': '#2563EB',
        'gradient_start': '#60A5FA',
        'gradient_end': '#22D3EE',
        'gradient_purple': '#A78BFA',

        # Secondary - Modern Emerald
        'secondary': '#34D399',
        'secondary_hover': '#10B981',
        'secondary_light': '#064E3B',
        'secondary_dark': '#059669',

        # Status colors
        'success': '#4ADE80',
        'success_light': '#064E3B',
        'danger': '#F87171',
        'danger_light': '#7F1D1D',
        'warning': '#FBBF24',
        'warning_light': '#78350F',
        'info': '#60A5FA',
        'info_light': '#1E3A8A',

        # Backgrounds
        'bg_main': '#0F172A',
        'bg_secondary': '#1E293B',
        'bg_sidebar': '#0F172A',
        'bg_card': '#1E293B',
        'bg_card_hover': '#334155',
        'bg_hover': '#334155',
        'bg_selected': '#1E3A8A',
        'bg_input': '#1E293B',

        # Text colors
        'text_primary': '#F8FAFC',
        'text_secondary': '#CBD5E1',
        'text_tertiary': '#94A3B8',
        'text_white': '#FFFFFF',
        'text_muted': '#64748B',
        'text_on_primary': '#FFFFFF',

        # Borders
        'border': '#334155',
        'border_strong': '#475569',
        'border_focus': '#60A5FA',
        'divider': '#1E293B',

        # Shadows
        'shadow_sm': '#0A0F1A',
        'shadow_md': '#050810',
        'shadow_lg': '#000000',
        'card_shadow': '#000000',

        # Console
        'console_bg': '#1E293B',
        'console_text': '#F8FAFC',
        'console_error': '#F87171',
        'console_warning': '#FBBF24',
        'console_info': '#60A5FA',
        'console_success': '#4ADE80',
    }

    _current_theme = 'light'

    @classmethod
    def get_theme(cls):
        """Get current theme colors"""
        return cls.LIGHT_THEME if cls._current_theme == 'light' else cls.DARK_THEME

    @classmethod
    def set_theme(cls, theme_name):
        """Set theme: 'light' or 'dark'"""
        if theme_name in ['light', 'dark']:
            cls._current_theme = theme_name
            return True
        return False

    @classmethod
    def toggle_theme(cls):
        """Toggle between light and dark theme"""
        cls._current_theme = 'dark' if cls._current_theme == 'light' else 'light'
        return cls._current_theme

    @classmethod
    def get_current_theme_name(cls):
        """Get current theme name"""
        return cls._current_theme
