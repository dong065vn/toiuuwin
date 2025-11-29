"""
Modern UI Components
Các component UI hiện đại cho ứng dụng
"""
import tkinter as tk
from tkinter import ttk
from .theme import ThemeManager


class ModernUI:
    """Figma-style Modern UI - Professional Design System"""

    SCALE_FACTOR = 1.0

    @classmethod
    def get_colors(cls):
        """Get current theme colors dynamically"""
        return ThemeManager.get_theme()

    @classmethod
    def set_scale_factor(cls, factor):
        """Set responsive scale factor for all UI elements"""
        cls.SCALE_FACTOR = max(0.7, min(1.5, factor))

    @classmethod
    def scaled_font(cls, font_key):
        """Get scaled font based on current scale factor"""
        font = cls.FONTS.get(font_key, cls.FONTS['body'])
        family, size = font[0], font[1]
        scaled_size = int(size * cls.SCALE_FACTOR)
        if len(font) > 2:
            return (family, scaled_size, font[2])
        return (family, scaled_size)

    COLORS = ThemeManager.LIGHT_THEME

    FONTS = {
        'heading': ('Segoe UI', 24, 'bold'),
        'subheading': ('Segoe UI', 18, 'bold'),
        'title': ('Segoe UI', 14, 'bold'),
        'body': ('Segoe UI', 10),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'small': ('Segoe UI', 9),
        'tiny': ('Segoe UI', 8),
        'console': ('Cascadia Code', 9),
        'console_fallback': ('Consolas', 9),
        'button': ('Segoe UI', 10, 'bold'),
        'code': ('Cascadia Code', 10),
        'badge': ('Segoe UI', 8, 'bold'),
    }

    SPACING = {
        'xxs': 4,
        'xs': 8,
        'sm': 12,
        'md': 16,
        'lg': 24,
        'xl': 32,
        'xxl': 48,
        '2xl': 64,
    }

    RADIUS = {
        'none': 0,
        'sm': 6,
        'md': 10,
        'lg': 14,
        'xl': 20,
        'full': 999,
    }


class ModernButton(tk.Canvas):
    """Professional button with gradient and animations"""

    def __init__(self, parent, text, command=None, bg_color=None,
                 width=140, height=36, icon="", style='primary', **kwargs):
        super().__init__(parent, width=width, height=height,
                        highlightthickness=0, bg=parent['bg'])

        self.parent = parent
        self.style = style
        self.command = command
        self.text = text
        self.icon = icon
        self.enabled = True
        self._custom_bg_color = bg_color

        self._update_colors()
        self.draw_button()
        self.bind('<Button-1>', lambda e: self.on_click())

    def _update_colors(self):
        """Update colors based on current theme"""
        colors = ThemeManager.get_theme()

        color_map = {
            'primary': colors['primary'],
            'secondary': colors['secondary'],
            'success': colors['success'],
            'danger': colors['danger'],
            'warning': colors['warning'],
            'info': colors['info'],
        }

        if self._custom_bg_color:
            self.bg_color = self._custom_bg_color
        else:
            self.bg_color = color_map.get(self.style, colors['primary'])

    def refresh_theme(self):
        """Refresh button colors when theme changes"""
        self._update_colors()
        self.draw_button()

    def draw_button(self, color=None):
        self.delete('all')
        colors = ThemeManager.get_theme()
        bg = color if color else self.bg_color
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        r = ModernUI.RADIUS['md']

        if w <= 0 or h <= 0:
            return

        # Rounded rectangle
        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=bg, outline='', width=0)
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=bg, outline='', width=0)
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=bg, outline='', width=0)
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=bg, outline='', width=0)
        self.create_rectangle(r, 0, w-r, h, fill=bg, outline='', width=0)
        self.create_rectangle(0, r, w, h-r, fill=bg, outline='', width=0)

        # Text
        display_text = f"{self.icon}  {self.text}" if self.icon else self.text
        self.create_text(w//2, h//2, text=display_text,
                        fill=colors['text_on_primary'],
                        font=ModernUI.FONTS['button'])

    def on_click(self):
        if self.command and self.enabled:
            self.command()


class Card(tk.Frame):
    """Professional card component"""

    def __init__(self, parent, title="", padding=16, **kwargs):
        colors = ThemeManager.get_theme()
        super().__init__(parent, bg=colors['bg_card'], **kwargs)

        self.colors = colors
        self.padding = padding

        if title:
            title_label = tk.Label(
                self,
                text=title,
                bg=colors['bg_card'],
                fg=colors['text_primary'],
                font=ModernUI.FONTS['title']
            )
            title_label.pack(pady=(padding, padding//2), padx=padding, anchor='w')

        self.content_frame = tk.Frame(self, bg=colors['bg_card'])
        self.content_frame.pack(fill='both', expand=True, padx=padding, pady=(0, padding))

    def refresh_theme(self):
        """Refresh card colors when theme changes"""
        colors = ThemeManager.get_theme()
        self.configure(bg=colors['bg_card'])
        self.content_frame.configure(bg=colors['bg_card'])


class ScrollableFrame(tk.Frame):
    """Scrollable frame container"""

    def __init__(self, parent, **kwargs):
        colors = ThemeManager.get_theme()
        super().__init__(parent, bg=colors['bg_main'], **kwargs)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self, bg=colors['bg_main'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=colors['bg_main'])

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def refresh_theme(self):
        """Refresh scrollable frame colors when theme changes"""
        colors = ThemeManager.get_theme()
        self.configure(bg=colors['bg_main'])
        self.canvas.configure(bg=colors['bg_main'])
        self.scrollable_frame.configure(bg=colors['bg_main'])
