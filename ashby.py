"""
Ashby Material Selector - Interactive Plotting & Selection Engine
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# Import the custom scripts
from database import MaterialDatabase
from plotting import (
    PROPERTIES, PALETTES, SUBCLASS_CYCLE_COLORS, ASHBY_PRESETS, VALID_INDEX_GUIDES,
    compute_property_value, render_ashby_chart, derive_subclass_color
)

# User settings stored in selector_settings.json
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "selector_settings.json")

# Symbols below are used for the selection of class/subclass in the tree view.
SYM_CHECKED = "✔"
SYM_UNCHECKED = "◻"
SYM_PARTIAL = "▣"

# Symbols below are enable/disable class/material tags.
SYM_STAR_OFF = "☆"
SYM_STAR_ON = "★"

DEFAULT_SETTINGS = {
    "app_dark_mode": False,
    "chart_dark_bg": False,
    "glow_effect": False,
    "active_palette": "CES Classic",
    "grouping_level": "class",
    "preset": "Modulus - Density (E vs ρ)",
    "x_prop": "Density ρ (g/cm³)",
    "y_prop": "Young's Modulus E (GPa)",
    "x_scale": "log",
    "y_scale": "log",
    "show_envelopes": True,
    "show_points": False,
    "show_cat_labels": True,
    "show_guideline": False,
    "guideline_slope": "",
    "active_materials": [],
    "tagged_materials": [],
    "tagged_classes": [],
    "tagged_subclasses": [],
    "manual_positions": {}
}

# Groups used for color scheme theme from main menu.
PALETTE_GROUPS = {
    "Engineering & Academic": [
        "CES Classic", "High Contrast Vibrant", "FEA Stress Spectrum", "Cambridge Blue", "Academic Paper Mono"
    ],
    "Industrial & Technical": [
        "Yanmar Industrial Red", "ANSI Machinery Safety", "Copper & Patina", "Blueprint Drafting", "Aerospace Mil-Spec", "CNC Toolroom"
    ],
    "Natural & Environmental": [
        "Camo Earth", "Botanical Garden", "Desert Dune", "Deep Ocean Trench", "Arctic Glacier", "Forest Canopy", "Autumn Foliage"
    ],
    "Modern Data & Scientific": [
        "Colorblind Safe (Wong)", "Viridis Categorical", "Plasma Accent", "Turbo Spectrum", "Solarized Light", "Solarized Dark"
    ],
    "Retro & Stylized": [
        "Synthwave 84", "Cyberpunk Neon", "Bauhaus Primary", "1980s Terminal Green", "Nordic Frost", "Sunset Horizon"
    ]
}

# Color themes for app window.
THEMES = {
    "Light": {
        "app_bg": "#ECE9D8", "panel_bg": "#ECE9D8", "control_bg": "#E1E1E1",
        "active_bg": "#D0D0D0", "entry_bg": "#FFFFFF", "entry_fg": "#000000",
        "fg_primary": "#000000", "fg_secondary": "#333333", "border": "#B0B0B0",
        "tree_bg": "#1E222B", "tree_fg": "#E6EDF3", "tree_selected": "#2D333B",
        "accent": "#0067C0"
    },
    "Dark": {
        "app_bg": "#202020", "panel_bg": "#2B2B2B", "control_bg": "#323232",
        "active_bg": "#3E3E3E", "entry_bg": "#1F1F1F", "entry_fg": "#FFFFFF",
        "fg_primary": "#FFFFFF", "fg_secondary": "#CCCCCC", "border": "#3F3F3F",
        "tree_bg": "#161B22", "tree_fg": "#E0E0E0", "tree_selected": "#094771",
        "accent": "#0078D4"
    }
}

def adjust_color_for_contrast(hex_color, bg_is_dark=True):
    """
    Adjusts the luminance of a hex color to maintain readability against dark/light backgrounds.

    Algorithm: Perceptual Luminance Adjustment
    1. Parse the RGB channels from the hexadecimal color string.
    2. Compute perceptual luminance using ITU-R BT.601 coefficients:
       L = 0.299 * R + 0.587 * G + 0.114 * B (accounting for human eye sensitivity to green).
    3. Apply threshold clamping and scaling:
       - On light backgrounds: If luminance > 140, attenuate RGB channels by (140 / L) to darken.
       - On dark backgrounds: If luminance < 70, boost RGB channels proportionally to ensure readability.
    4. Re-clamp channels to [0, 255] and return the new hex string.
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        return "#" + hex_color
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
    except ValueError:
        return "#" + hex_color

    lum = 0.299 * r + 0.587 * g + 0.114 * b

    if not bg_is_dark and lum > 140:
        factor = 140.0 / lum
        r = int(r * factor)
        g = int(g * factor)
        b = int(b * factor)
        if g > r and b < 100:
            r = min(200, int(r * 1.15))
    elif bg_is_dark and lum < 70:
        boost = 85.0 - lum
        r = min(255, int(r + boost * 1.2))
        g = min(255, int(g + boost * 1.2))
        b = min(255, int(b + boost * 1.5))

    return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"


class MaterialSelectorApp(tk.Tk):
    """
    Main Tkinter desktop application managing material selection, filtering,
    hierarchy navigation, and interactive Matplotlib Ashby plot rendering.
    """
    def __init__(self):
        """Initializes the main window, database connections, application state, and UI layout."""
        super().__init__()
        self.title("Material Selector - Material Property Charting Engine")
        self.geometry("1480x940")
        self.minsize(1150, 720)

        self.db = MaterialDatabase()
        self.settings = self.load_settings()

        self.style = ttk.Style(self)
        try:
            self.style.theme_use('clam')
        except Exception:
            pass

        self.active_palette = self.settings.get("active_palette", "CES Classic")
        
        # Reactive UI state variables
        self.app_dark_mode_var = tk.BooleanVar(value=self.settings.get("app_dark_mode", False))
        self.chart_dark_bg_var = tk.BooleanVar(value=self.settings.get("chart_dark_bg", False))
        self.glow_effect_var = tk.BooleanVar(value=self.settings.get("glow_effect", False))
        self.grouping_level_var = tk.StringVar(value=self.settings.get("grouping_level", "class"))

        self.x_scale_var = tk.StringVar(value=self.settings.get("x_scale", "log"))
        self.y_scale_var = tk.StringVar(value=self.settings.get("y_scale", "log"))

        self.show_envelopes = tk.BooleanVar(value=self.settings.get("show_envelopes", True))
        self.show_points = tk.BooleanVar(value=self.settings.get("show_points", False))
        self.show_cat_labels = tk.BooleanVar(value=self.settings.get("show_cat_labels", True))
        self.show_guideline = tk.BooleanVar(value=self.settings.get("show_guideline", False))
        self.guideline_slope = tk.StringVar(value=self.settings.get("guideline_slope", ""))

        # Pre-populate active and tagged item sets from DB or persisted config
        raw_all_records = self.db.fetch_records()
        raw_all_materials = [r["material_name"] for r in raw_all_records]
        raw_all_classes = list(set(r["category"] for r in raw_all_records))
        raw_all_subclasses = list(set(r.get("subclass", "General") for r in raw_all_records))

        saved_active = self.settings.get("active_materials", [])
        self.active_materials = set(saved_active) if saved_active else set(raw_all_materials)
        self.tagged_materials = set(self.settings.get("tagged_materials", []))

        saved_tagged_classes = self.settings.get("tagged_classes", None)
        self.tagged_classes = set(saved_tagged_classes) if saved_tagged_classes is not None else set(raw_all_classes)

        saved_tagged_subclasses = self.settings.get("tagged_subclasses", None)
        self.tagged_subclasses = set(saved_tagged_subclasses) if saved_tagged_subclasses is not None else set(raw_all_subclasses)

        self.user_expanded_iids = set()

        # Canvas interaction tracking state
        self.plotted_coords = {}
        self.manual_positions = self.settings.get("manual_positions", {})
        self.active_drag_ann = None
        self.drag_start_pos = None

        self.disp_chk_widgets = []
        self.scale_radio_widgets = []

        self.setup_menu()
        self.setup_ui()
        self.apply_theme()
        self.populate_treeview(initial_build=True)
        self.plot_graph()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_settings(self):
        """Loads persistent user configuration from JSON file or falls back to defaults."""
        settings = dict(DEFAULT_SETTINGS)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    settings.update(saved)
            except Exception:
                pass
        return settings

    def save_settings(self):
        """Dumps current application states, axis selections, and manual coordinates to JSON."""
        self.settings.update({
            "app_dark_mode": self.app_dark_mode_var.get(),
            "chart_dark_bg": self.chart_dark_bg_var.get(),
            "glow_effect": self.glow_effect_var.get(),
            "active_palette": self.active_palette,
            "grouping_level": self.grouping_level_var.get(),
            "preset": self.preset_cb.get() if hasattr(self, "preset_cb") else self.settings.get("preset", ""),
            "x_prop": self.x_axis_cb.get() if hasattr(self, "x_axis_cb") else self.settings.get("x_prop", ""),
            "y_prop": self.y_axis_cb.get() if hasattr(self, "y_axis_cb") else self.settings.get("y_prop", ""),
            "x_scale": self.x_scale_var.get(),
            "y_scale": self.y_scale_var.get(),
            "show_envelopes": self.show_envelopes.get(),
            "show_points": self.show_points.get(),
            "show_cat_labels": self.show_cat_labels.get(),
            "show_guideline": self.show_guideline.get(),
            "guideline_slope": self.guideline_slope.get(),
            "active_materials": list(self.active_materials),
            "tagged_materials": list(self.tagged_materials),
            "tagged_classes": list(self.tagged_classes),
            "tagged_subclasses": list(self.tagged_subclasses),
            "manual_positions": self.manual_positions
        })

        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def on_close(self):
        """Handles application shutdown by persisting preferences and destroying window."""
        self.save_settings()
        self.destroy()

    def setup_menu(self):
        """Constructs top-level native window menus (View, Plot, Theme palettes, and axis scales)."""
        self.menubar = tk.Menu(self)

        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_checkbutton(
            label="App Dark Theme",
            variable=self.app_dark_mode_var,
            command=self.on_app_theme_toggle
        )
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Expand All Tree Branches",
            command=self.expand_all_tree_nodes
        )
        self.view_menu.add_command(
            label="Collapse All Tree Branches",
            command=self.collapse_all_tree_nodes
        )
        self.view_menu.add_separator()
        self.view_menu.add_command(
            label="Inspect Material Data Sources...",
            command=self.show_source_inspector_dialog
        )
        self.view_menu.add_command(
            label="Reset Label Adjustments",
            command=self.reset_label_positions
        )
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        self.plot_menu = tk.Menu(self.menubar, tearoff=0)
        
        grp_submenu = tk.Menu(self.plot_menu, tearoff=0)
        grp_submenu.add_radiobutton(label="Group Envelopes: Class Only", variable=self.grouping_level_var, value="class", command=self.on_grouping_changed)
        grp_submenu.add_radiobutton(label="Group Envelopes: Subclass Only", variable=self.grouping_level_var, value="subclass", command=self.on_grouping_changed)
        grp_submenu.add_radiobutton(label="Group Envelopes: Both (Class & Subclass)", variable=self.grouping_level_var, value="both", command=self.on_grouping_changed)
        self.plot_menu.add_cascade(label="Envelope Grouping Level", menu=grp_submenu)
        self.plot_menu.add_separator()

        self.plot_menu.add_checkbutton(
            label="Show Material Points",
            variable=self.show_points,
            command=self.on_plot_option_changed
        )
        self.plot_menu.add_checkbutton(
            label="Dark Chart Background",
            variable=self.chart_dark_bg_var,
            command=self.on_plot_option_changed
        )
        self.plot_menu.add_checkbutton(
            label="Neon Glow Effect",
            variable=self.glow_effect_var,
            command=self.on_plot_option_changed
        )
        self.plot_menu.add_separator()

        scale_submenu = tk.Menu(self.plot_menu, tearoff=0)
        scale_submenu.add_radiobutton(label="X-Axis: Logarithmic", variable=self.x_scale_var, value="log", command=self.on_scale_changed)
        scale_submenu.add_radiobutton(label="X-Axis: Linear", variable=self.x_scale_var, value="linear", command=self.on_scale_changed)
        scale_submenu.add_separator()
        scale_submenu.add_radiobutton(label="Y-Axis: Logarithmic", variable=self.y_scale_var, value="log", command=self.on_scale_changed)
        scale_submenu.add_radiobutton(label="Y-Axis: Linear", variable=self.y_scale_var, value="linear", command=self.on_scale_changed)
        self.plot_menu.add_cascade(label="Axis Scaling (Log / Linear)", menu=scale_submenu)
        self.plot_menu.add_separator()

        self.palette_var = tk.StringVar(value=self.active_palette)
        for group_name, group_palettes in PALETTE_GROUPS.items():
            grp_menu = tk.Menu(self.plot_menu, tearoff=0)
            for p_name in group_palettes:
                grp_menu.add_radiobutton(
                    label=p_name,
                    variable=self.palette_var,
                    value=p_name,
                    command=self.on_palette_changed
                )
            self.plot_menu.add_cascade(label=group_name, menu=grp_menu)

        self.menubar.add_cascade(label="Plot", menu=self.plot_menu)
        self.config(menu=self.menubar)

    def on_grouping_changed(self):
        """Callback triggered when changing envelope granularity (Class, Subclass, or Both)."""
        self.save_settings()
        self.configure_tree_tags()
        self.populate_treeview()
        self.plot_graph()

    def on_plot_option_changed(self):
        """Callback triggered when toggling plot appearance settings (bubbles, points, dark mode)."""
        self.save_settings()
        self.plot_graph()

    def reset_label_positions(self):
        """Clears user manual dragging offsets for labels and resets them to algorithmic positions."""
        self.manual_positions.clear()
        self.settings["manual_positions"] = {}
        self.save_settings()
        self.plot_graph()

    def on_scale_changed(self):
        """Callback for log/linear toggle changes on axes."""
        self.save_settings()
        self.plot_graph()

    def on_app_theme_toggle(self):
        """Callback when switching between dark and light desktop UI themes."""
        self.apply_theme()
        self.save_settings()
        self.configure_tree_tags()

    def on_palette_changed(self):
        """Callback when selecting a different color palette for material families."""
        self.active_palette = self.palette_var.get()
        self.save_settings()
        self.configure_tree_tags()
        self.plot_graph()

    def apply_theme(self):
        """Updates styling and background/foreground colors across all Tkinter widgets."""
        theme = THEMES["Dark"] if self.app_dark_mode_var.get() else THEMES["Light"]
        self.configure(bg=theme["app_bg"])

        self.style.configure(".",
            background=theme["panel_bg"],
            foreground=theme["fg_primary"],
            font=("Segoe UI", 9)
        )
        self.style.configure("TFrame", background=theme["panel_bg"])
        self.style.configure("TLabelframe",
            background=theme["panel_bg"],
            foreground=theme["fg_primary"],
            bordercolor=theme["border"]
        )
        self.style.configure("TLabelframe.Label",
            background=theme["panel_bg"],
            foreground=theme["fg_primary"],
            font=("Segoe UI", 9, "bold")
        )
        self.style.configure("TLabel",
            background=theme["panel_bg"],
            foreground=theme["fg_primary"]
        )
        self.style.configure("TButton",
            background=theme["control_bg"],
            foreground=theme["fg_primary"],
            bordercolor=theme["border"],
            font=("Segoe UI", 9, "bold")
        )
        self.style.map("TButton",
            background=[("active", theme["active_bg"])],
            foreground=[("active", theme["fg_primary"])]
        )
        self.style.configure("TCombobox",
            fieldbackground=theme["entry_bg"],
            background=theme["control_bg"],
            foreground=theme["fg_primary"],
            arrowcolor=theme["fg_primary"]
        )
        self.style.map("TCombobox",
            fieldbackground=[("readonly", theme["entry_bg"])],
            foreground=[("readonly", theme["fg_primary"])]
        )

        self.style.configure("Treeview",
            background=theme["tree_bg"],
            foreground=theme["tree_fg"],
            fieldbackground=theme["tree_bg"],
            font=("Segoe UI", 9),
            rowheight=24
        )
        self.style.map("Treeview",
            background=[("selected", theme["tree_selected"])],
            foreground=[("selected", "#FFFFFF")]
        )
        self.style.configure("Treeview.Heading",
            background=theme["control_bg"],
            foreground=theme["fg_primary"],
            font=("Segoe UI", 9, "bold")
        )

        if hasattr(self, "search_entry"):
            self.search_entry.configure(
                bg=theme["entry_bg"],
                fg=theme["entry_fg"],
                insertbackground=theme["fg_primary"],
                highlightbackground=theme["border"],
                highlightcolor=theme["accent"],
                relief="flat"
            )

        for chk in self.disp_chk_widgets:
            chk.configure(
                bg=theme["panel_bg"],
                fg=theme["fg_primary"],
                activebackground=theme["panel_bg"],
                activeforeground=theme["fg_primary"],
                selectcolor=theme["control_bg"],
                font=("Segoe UI", 9)
            )

        for rb in self.scale_radio_widgets:
            rb.configure(
                bg=theme["panel_bg"],
                fg=theme["fg_primary"],
                activebackground=theme["panel_bg"],
                activeforeground=theme["fg_primary"],
                selectcolor=theme["control_bg"],
                font=("Segoe UI", 8, "bold")
            )

        if hasattr(self, "tree"):
            self.configure_tree_tags()

    def configure_tree_tags(self):
        """Sets text colors on Treeview category nodes matching the active color palette."""
        palette = PALETTES.get(self.active_palette, PALETTES["CES Classic"])
        theme = THEMES["Dark"] if self.app_dark_mode_var.get() else THEMES["Light"]
        tree_bg_hex = theme["tree_bg"].lstrip('#')
        bg_is_dark = (0.299 * int(tree_bg_hex[0:2], 16) + 0.587 * int(tree_bg_hex[2:4], 16) + 0.114 * int(tree_bg_hex[4:6], 16)) < 128

        for cat, color in palette.items():
            tag_name = f"tag_cat_{cat}"
            adapted_color = adjust_color_for_contrast(color, bg_is_dark=bg_is_dark)
            self.tree.tag_configure(
                tag_name,
                foreground=adapted_color,
                font=("Segoe UI", 9, "bold")
            )

        all_records = self.db.fetch_records()
        cat_to_subs = {}
        for r in all_records:
            cat = r["category"]
            sub = r.get("subclass", "General")
            if cat not in cat_to_subs:
                cat_to_subs[cat] = []
            if sub not in cat_to_subs[cat]:
                cat_to_subs[cat].append(sub)

        for cat, subs in cat_to_subs.items():
            subs_sorted = sorted(subs)
            base_c = palette.get(cat, "#888888")
            for idx, sub in enumerate(subs_sorted):
                derived_c = derive_subclass_color(base_c, idx, len(subs_sorted))
                adapted_sub_color = adjust_color_for_contrast(derived_c, bg_is_dark=bg_is_dark)
                tag_name = f"tag_sub_{sub}"
                self.tree.tag_configure(
                    tag_name,
                    foreground=adapted_sub_color,
                    font=("Segoe UI", 8, "bold")
                )

        self.tree.tag_configure("tag_mat", font=("Segoe UI", 8), foreground=theme["tree_fg"])

    def setup_ui(self):
        """Constructs GUI layout: left control sidebar and embedded Matplotlib canvas."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        left_panel = ttk.Frame(self, padding=6, relief="flat", width=450)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
        left_panel.grid_propagate(False)

        # 1. Presets & Axes
        axis_box = ttk.LabelFrame(left_panel, text="Chart Stages & Ashby Presets", padding=6)
        axis_box.pack(fill="x", pady=2)

        ttk.Label(axis_box, text="Preset:").grid(row=0, column=0, sticky="w", pady=1)
        self.preset_cb = ttk.Combobox(axis_box, values=list(ASHBY_PRESETS.keys()), state="readonly")
        saved_preset = self.settings.get("preset", "Modulus - Density (E vs ρ)")
        self.preset_cb.set(saved_preset if saved_preset in ASHBY_PRESETS else "Modulus - Density (E vs ρ)")
        self.preset_cb.grid(row=0, column=1, columnspan=2, sticky="ew", pady=1)
        self.preset_cb.bind("<<ComboboxSelected>>", self.apply_preset)

        ttk.Label(axis_box, text="Y-Axis:").grid(row=1, column=0, sticky="w", pady=1)
        self.y_axis_cb = ttk.Combobox(axis_box, values=list(PROPERTIES.keys()), state="readonly")
        saved_y = self.settings.get("y_prop", "Young's Modulus E (GPa)")
        self.y_axis_cb.set(saved_y if saved_y in PROPERTIES else "Young's Modulus E (GPa)")
        self.y_axis_cb.grid(row=1, column=1, columnspan=2, sticky="ew", pady=1)
        self.y_axis_cb.bind("<<ComboboxSelected>>", lambda e: self.on_axis_changed())

        y_scale_frame = ttk.Frame(axis_box)
        y_scale_frame.grid(row=2, column=1, columnspan=2, sticky="w", pady=(0, 2))
        rb_y_log = tk.Radiobutton(y_scale_frame, text="Y Log", variable=self.y_scale_var, value="log", command=self.on_scale_changed)
        rb_y_lin = tk.Radiobutton(y_scale_frame, text="Y Linear", variable=self.y_scale_var, value="linear", command=self.on_scale_changed)
        rb_y_log.pack(side="left", padx=(0, 6))
        rb_y_lin.pack(side="left")
        self.scale_radio_widgets.extend([rb_y_log, rb_y_lin])

        ttk.Label(axis_box, text="X-Axis:").grid(row=3, column=0, sticky="w", pady=1)
        self.x_axis_cb = ttk.Combobox(axis_box, values=list(PROPERTIES.keys()), state="readonly")
        saved_x = self.settings.get("x_prop", "Density ρ (g/cm³)")
        self.x_axis_cb.set(saved_x if saved_x in PROPERTIES else "Density ρ (g/cm³)")
        self.x_axis_cb.grid(row=3, column=1, columnspan=2, sticky="ew", pady=1)
        self.x_axis_cb.bind("<<ComboboxSelected>>", lambda e: self.on_axis_changed())

        x_scale_frame = ttk.Frame(axis_box)
        x_scale_frame.grid(row=4, column=1, columnspan=2, sticky="w", pady=(0, 2))
        rb_x_log = tk.Radiobutton(x_scale_frame, text="X Log", variable=self.x_scale_var, value="log", command=self.on_scale_changed)
        rb_x_lin = tk.Radiobutton(x_scale_frame, text="X Linear", variable=self.x_scale_var, value="linear", command=self.on_scale_changed)
        rb_x_log.pack(side="left", padx=(0, 6))
        rb_x_lin.pack(side="left")
        self.scale_radio_widgets.extend([rb_x_log, rb_x_lin])

        axis_box.columnconfigure(1, weight=1)

        # 2. Material Hierarchy Treeview
        tree_box = ttk.LabelFrame(left_panel, text="Material Hierarchy (Class > Subclass > Grade)", padding=6)
        tree_box.pack(fill="both", expand=True, pady=3)

        grp_row = ttk.Frame(tree_box)
        grp_row.pack(fill="x", pady=(0, 3))
        ttk.Label(grp_row, text="Group Envelopes:").pack(side="left")
        rb_grp_cls = tk.Radiobutton(grp_row, text="Class", variable=self.grouping_level_var, value="class", command=self.on_grouping_changed)
        rb_grp_sub = tk.Radiobutton(grp_row, text="Subclass", variable=self.grouping_level_var, value="subclass", command=self.on_grouping_changed)
        rb_grp_both = tk.Radiobutton(grp_row, text="Both", variable=self.grouping_level_var, value="both", command=self.on_grouping_changed)
        rb_grp_cls.pack(side="left", padx=2)
        rb_grp_sub.pack(side="left", padx=2)
        rb_grp_both.pack(side="left", padx=2)
        self.scale_radio_widgets.extend([rb_grp_cls, rb_grp_sub, rb_grp_both])

        filter_row = ttk.Frame(tree_box)
        filter_row.pack(fill="x", pady=(2, 4))
        ttk.Label(filter_row, text="Filter:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.on_search_filter_changed())
        self.search_entry = tk.Entry(filter_row, textvariable=self.search_var, relief="flat", highlightthickness=1)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=4)

        tree_container = ttk.Frame(tree_box)
        tree_container.pack(fill="both", expand=True)

        cols = ("plot_status", "tag_status")
        self.tree = ttk.Treeview(tree_container, columns=cols, selectmode="browse", show="tree headings")
        self.tree.heading("#0", text="Hierarchy", anchor="w")
        self.tree.heading("plot_status", text="Active", anchor="center")
        self.tree.heading("tag_status", text="Tag", anchor="center")

        self.tree.column("#0", width=265, stretch=True)
        self.tree.column("plot_status", width=55, stretch=False, anchor="center")
        self.tree.column("tag_status", width=50, stretch=False, anchor="center")

        tree_vscroll = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_vscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_vscroll.pack(side="right", fill="y")

        self.tree.bind("<Button-1>", self.on_tree_click)
        self.tree.bind("<<TreeviewOpen>>", self.on_tree_node_opened)
        self.tree.bind("<<TreeviewClose>>", self.on_tree_node_closed)

        tree_actions = ttk.Frame(tree_box)
        tree_actions.pack(fill="x", pady=(3, 0))
        ttk.Button(tree_actions, text="Select All", command=self.select_all_materials).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(tree_actions, text="Clear All", command=self.clear_all_materials).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(tree_actions, text="Select All Tags", command=self.select_all_tags).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(tree_actions, text="Clear Tags", command=self.clear_all_tags).pack(side="left", expand=True, fill="x", padx=1)

        # 3. Display Options
        disp_box = ttk.LabelFrame(left_panel, text="Ashby Display & Envelopes", padding=6)
        disp_box.pack(fill="x", pady=3)

        chk_f = ttk.Frame(disp_box)
        chk_f.pack(fill="x")
        self.disp_chk_widgets = []
        chk1 = tk.Checkbutton(chk_f, text="Group Bubbles", variable=self.show_envelopes, command=self.on_plot_option_changed)
        chk1.grid(row=0, column=0, sticky="w")
        chk2 = tk.Checkbutton(chk_f, text="Material Points", variable=self.show_points, command=self.on_plot_option_changed)
        chk2.grid(row=0, column=1, sticky="w")
        chk3 = tk.Checkbutton(chk_f, text="Group Names", variable=self.show_cat_labels, command=self.on_plot_option_changed)
        chk3.grid(row=1, column=0, sticky="w")
        self.guide_chk = tk.Checkbutton(chk_f, text="Index Guide Line", variable=self.show_guideline, command=self.on_plot_option_changed)
        self.guide_chk.grid(row=1, column=1, sticky="w")
        self.disp_chk_widgets.extend([chk1, chk2, chk3, self.guide_chk])

        guide_f = ttk.Frame(disp_box)
        guide_f.pack(fill="x", pady=(2, 0))
        ttk.Label(guide_f, text="Index Guide:").pack(side="left")
        self.guide_cb = ttk.Combobox(guide_f, textvariable=self.guideline_slope, state="readonly")
        self.guide_cb.pack(side="left", fill="x", expand=True, padx=2)
        self.guide_cb.bind("<<ComboboxSelected>>", lambda e: self.on_plot_option_changed())

        db_row = ttk.Frame(left_panel)
        db_row.pack(fill="x", pady=3)
        ttk.Button(db_row, text="Import CSV...", command=self.import_csv_dialog).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(db_row, text="Verify Sources", command=self.show_source_inspector_dialog).pack(side="left", expand=True, fill="x", padx=1)
        ttk.Button(db_row, text="Reset Tags", command=self.reset_label_positions).pack(side="left", expand=True, fill="x", padx=1)

        # 4. Matplotlib Canvas
        plot_frame = ttk.Frame(self, relief="flat")
        plot_frame.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
        plot_frame.grid_rowconfigure(0, weight=1)
        plot_frame.grid_columnconfigure(0, weight=1)

        self.fig = Figure(figsize=(9, 8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="top", fill="both", expand=True)

        self.canvas.mpl_connect("pick_event", self.on_annotation_pick)
        self.canvas.mpl_connect("motion_notify_event", self.on_annotation_drag)
        self.canvas.mpl_connect("button_release_event", self.on_annotation_release)
        self.canvas.mpl_connect("button_press_event", self.on_plot_click)

        toolbar_frame = ttk.Frame(plot_frame)
        toolbar_frame.pack(side="bottom", fill="x")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

    def on_tree_node_opened(self, event):
        """Records expanded treeview node ID to preserve user state during re-population."""
        item = self.tree.focus()
        if item:
            self.user_expanded_iids.add(item)

    def on_tree_node_closed(self, event):
        """Removes collapsed node ID from tracking state."""
        item = self.tree.focus()
        if item and item in self.user_expanded_iids:
            self.user_expanded_iids.remove(item)

    def expand_all_tree_nodes(self):
        """Recursively opens all nodes in the hierarchy tree."""
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            self.user_expanded_iids.add(item)
            for sub in self.tree.get_children(item):
                self.tree.item(sub, open=True)
                self.user_expanded_iids.add(sub)

    def collapse_all_tree_nodes(self):
        """Collapses all parent and subclass branches in the hierarchy tree."""
        for item in self.tree.get_children():
            self.tree.item(item, open=False)
            for sub in self.tree.get_children(item):
                self.tree.item(sub, open=False)
        self.user_expanded_iids.clear()

    def populate_treeview(self, initial_build=False):
        """
        Reconstructs the 3-level Material Treeview (Category -> Subclass -> Material).
        Filters nodes based on the search entry and computes tri-state checkbox icons (✔, ▣, ◻)
        for parent selection states.
        """
        query = self.search_var.get().lower().strip()

        if not initial_build and hasattr(self, "tree"):
            for item in self.tree.get_children():
                if self.tree.item(item, "open"):
                    self.user_expanded_iids.add(item)
                for sub in self.tree.get_children(item):
                    if self.tree.item(sub, "open"):
                        self.user_expanded_iids.add(sub)

        self.tree.delete(*self.tree.get_children())

        records = self.db.fetch_records()
        hierarchy = {}
        for r in records:
            cat = r["category"]
            sub = r.get("subclass", "General")
            name = r["material_name"]
            hierarchy.setdefault(cat, {}).setdefault(sub, []).append(name)

        self.tree_item_meta = {}

        for cat, sub_dict in hierarchy.items():
            cat_id = f"cat_{cat}"
            cat_matches = (query in cat.lower())

            has_matching_children = False
            for sub, mats in sub_dict.items():
                if query in sub.lower() or any(query in m.lower() for m in mats):
                    has_matching_children = True
                    break

            if query and not cat_matches and not has_matching_children:
                continue

            # Tri-state checkbox logic for categories
            cat_active_count = sum(1 for sub in sub_dict.values() for m in sub if m in self.active_materials)
            cat_total_count = sum(len(sub) for sub in sub_dict.values())
            cat_status = SYM_CHECKED if cat_active_count == cat_total_count else (SYM_PARTIAL if cat_active_count > 0 else SYM_UNCHECKED)
            is_open = bool(query) or (cat_id in self.user_expanded_iids)

            cat_tag_status = SYM_STAR_ON if cat in self.tagged_classes else SYM_STAR_OFF

            self.tree.insert(
                "", "end", iid=cat_id, text=f"  {cat}",
                values=(cat_status, cat_tag_status),
                open=is_open,
                tags=(f"tag_cat_{cat}",)
            )
            self.tree_item_meta[cat_id] = {"type": "class", "name": cat, "subclasses": sub_dict}

            for sub, mats in sub_dict.items():
                sub_id = f"sub_{cat}_{sub}"
                sub_matches = (query in sub.lower()) or (query in cat.lower())
                mats_matching = [m for m in mats if (query in m.lower()) or sub_matches]

                if query and not mats_matching:
                    continue

                # Tri-state checkbox logic for subclasses
                sub_active_count = sum(1 for m in mats if m in self.active_materials)
                sub_status = SYM_CHECKED if sub_active_count == len(mats) else (SYM_PARTIAL if sub_active_count > 0 else SYM_UNCHECKED)
                is_sub_open = bool(query) or (sub_id in self.user_expanded_iids)

                sub_tag_status = SYM_STAR_ON if sub in self.tagged_subclasses else SYM_STAR_OFF

                self.tree.insert(
                    cat_id, "end", iid=sub_id, text=f"    ↳ {sub}",
                    values=(sub_status, sub_tag_status),
                    open=is_sub_open,
                    tags=(f"tag_sub_{sub}",)
                )
                self.tree_item_meta[sub_id] = {"type": "subclass", "name": sub, "category": cat, "materials": mats}

                for m in mats:
                    if query and not (query in m.lower() or query in sub.lower() or query in cat.lower()):
                        continue
                    mat_id = f"mat_{m}"
                    mat_status = SYM_CHECKED if m in self.active_materials else SYM_UNCHECKED
                    mat_tag_status = SYM_STAR_ON if m in self.tagged_materials else SYM_STAR_OFF

                    self.tree.insert(
                        sub_id, "end", iid=mat_id, text=f"        • {m}",
                        values=(mat_status, mat_tag_status),
                        tags=("tag_mat",)
                    )
                    self.tree_item_meta[mat_id] = {"type": "material", "name": m, "subclass": sub, "category": cat}

        self.configure_tree_tags()

    def on_tree_click(self, event):
        """
        Handles mouse clicks on the Treeview widget columns:
        - Column #1 (Active): Toggles active plot visibility for an item or cascading hierarchy.
        - Column #2 (Tag): Toggles label tag callouts on the chart.
        """
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        if not item_id or item_id not in self.tree_item_meta:
            return

        meta = self.tree_item_meta[item_id]
        item_type = meta["type"]

        if column == "#1":
            if item_type == "material":
                mat_name = meta["name"]
                if mat_name in self.active_materials:
                    self.active_materials.remove(mat_name)
                else:
                    self.active_materials.add(mat_name)

            elif item_type == "subclass":
                sub_mats = meta["materials"]
                all_active = all(m in self.active_materials for m in sub_mats)
                if all_active:
                    for m in sub_mats:
                        self.active_materials.discard(m)
                else:
                    for m in sub_mats:
                        self.active_materials.add(m)

            elif item_type == "class":
                cat_mats = [m for sub in meta["subclasses"].values() for m in sub]
                all_active = all(m in self.active_materials for m in cat_mats)
                if all_active:
                    for m in cat_mats:
                        self.active_materials.discard(m)
                else:
                    for m in cat_mats:
                        self.active_materials.add(m)

            self.populate_treeview()
            self.save_settings()
            self.plot_graph()

        elif column == "#2":
            if item_type == "material":
                mat_name = meta["name"]
                if mat_name in self.tagged_materials:
                    self.tagged_materials.remove(mat_name)
                else:
                    self.tagged_materials.add(mat_name)

            elif item_type == "subclass":
                sub_name = meta["name"]
                if sub_name in self.tagged_subclasses:
                    self.tagged_subclasses.remove(sub_name)
                else:
                    self.tagged_subclasses.add(sub_name)

            elif item_type == "class":
                cat_name = meta["name"]
                if cat_name in self.tagged_classes:
                    self.tagged_classes.remove(cat_name)
                else:
                    self.tagged_classes.add(cat_name)

            self.populate_treeview()
            self.save_settings()
            self.plot_graph()

    def on_search_filter_changed(self):
        """Filters the material hierarchy treeview dynamically on search input change."""
        self.populate_treeview()

    def select_all_materials(self):
        """Marks all database materials as active and updates the chart."""
        records = self.db.fetch_records()
        self.active_materials = {r["material_name"] for r in records}
        self.populate_treeview()
        self.save_settings()
        self.plot_graph()

    def clear_all_materials(self):
        """Clears all material selections and clears the chart."""
        self.active_materials.clear()
        self.populate_treeview()
        self.save_settings()
        self.plot_graph()

    def select_all_tags(self):
        """Enables label tagging for all material classes and subclasses."""
        records = self.db.fetch_records()
        self.tagged_classes = {r["category"] for r in records}
        self.tagged_subclasses = {r.get("subclass", "General") for r in records}
        self.populate_treeview()
        self.save_settings()
        self.plot_graph()

    def clear_all_tags(self):
        """Clears all active material and category label tags."""
        self.tagged_materials.clear()
        self.tagged_classes.clear()
        self.tagged_subclasses.clear()
        self.populate_treeview()
        self.save_settings()
        self.plot_graph()

    def on_annotation_pick(self, event):
        """
        Initiates mouse dragging for chart annotations.
        Holding Ctrl sets the drag mode to 'anchor' (re-pointing the arrow),
        while a standard click sets 'text' drag mode (moving the callout box).
        """
        if event.mouseevent.button == 1 and hasattr(event.artist, 'tag_id'):
            self.active_drag_ann = event.artist
            
            is_ctrl = False
            me = event.mouseevent
            if getattr(me, 'key', None) in ('control', 'ctrl'):
                is_ctrl = True
            elif hasattr(me, 'guiEvent') and me.guiEvent is not None:
                if getattr(me.guiEvent, 'state', 0) & 0x0004:
                    is_ctrl = True

            self.drag_mode = 'anchor' if is_ctrl else 'text'
            self.drag_start_pos = (me.xdata, me.ydata)

    def on_annotation_drag(self, event):
        """
        Updates annotation coordinates continuously during a mouse drag motion.

        Algorithm:
        - If dragging in 'anchor' mode and the annotation has envelope vertices (`space_verts`),
          the pointer position is projected into log-space (if log scale is on) and snapped to the
          nearest vertex on the envelope polygon via Euclidean distance minimization.
        - If dragging in 'text' mode, moves the text bubble `xyann` directly with the cursor.
        """
        if self.active_drag_ann is not None and event.inaxes == self.ax and event.xdata and event.ydata:
            ann = self.active_drag_ann
            x_is_log = (self.x_scale_var.get() == "log")
            y_is_log = (self.y_scale_var.get() == "log")

            if getattr(self, 'drag_mode', 'text') == 'anchor':
                space_verts = getattr(ann, 'space_verts', None)
                if space_verts:
                    # Convert cursor data into linearized log space for distance measurement
                    sp_x = np.log10(max(event.xdata, 1e-12)) if x_is_log else event.xdata
                    sp_y = np.log10(max(event.ydata, 1e-12)) if y_is_log else event.ydata
                    # Find closest envelope vertex
                    best_v = min(space_verts, key=lambda v: (v[0] - sp_x)**2 + (v[1] - sp_y)**2)
                    snap_x = (10.0**best_v[0]) if x_is_log else best_v[0]
                    snap_y = (10.0**best_v[1]) if y_is_log else best_v[1]
                    ann.xy = (snap_x, snap_y)
                else:
                    ann.xy = (event.xdata, event.ydata)
            else:
                ann.xyann = (event.xdata, event.ydata)

            self.canvas.draw_idle()

    def on_annotation_release(self, event):
        """Saves dragged annotation text/anchor positions to settings and redraws."""
        if self.active_drag_ann is not None:
            ann = self.active_drag_ann
            tag_id = getattr(ann, 'tag_id', None)
            if tag_id:
                tx, ty = ann.xyann
                ax0, ay0 = ann.xy
                self.manual_positions[tag_id] = {
                    "text": [float(tx), float(ty)],
                    "anchor": [float(ax0), float(ay0)]
                }
                self.save_settings()
            self.active_drag_ann = None
            self.drag_start_pos = None
            self.drag_mode = None
            self.plot_graph()

    def update_guideline_ui_state(self):
        """Enables/disables and populates the performance index slope combobox based on the active axis pair."""
        y_prop = self.y_axis_cb.get()
        x_prop = self.x_axis_cb.get()
        pair = (y_prop, x_prop)

        if pair in VALID_INDEX_GUIDES:
            options = VALID_INDEX_GUIDES[pair]
            labels = [opt[0] for opt in options]

            self.guide_chk.configure(state="normal")
            self.guide_cb.configure(values=labels)
            
            if self.guideline_slope.get() not in labels:
                self.guideline_slope.set(labels[0])
            
            if self.show_guideline.get():
                self.guide_cb.configure(state="readonly")
            else:
                self.guide_cb.configure(state="disabled")
        else:
            self.show_guideline.set(False)
            self.guide_chk.configure(state="disabled")
            self.guide_cb.configure(values=["N/A for Current Axes"], state="disabled")
            self.guideline_slope.set("N/A for Current Axes")

    def on_axis_changed(self):
        """Callback triggered when the user alters either the X or Y axis property."""
        self.update_guideline_ui_state()
        self.save_settings()
        self.plot_graph()

    def apply_preset(self, event=None):
        """Configures X and Y axes and sets log-log scaling according to selected Ashby preset."""
        preset = self.preset_cb.get()
        if preset in ASHBY_PRESETS:
            y, x = ASHBY_PRESETS[preset]
            self.y_axis_cb.set(y)
            self.x_axis_cb.set(x)
            self.x_scale_var.set("log")
            self.y_scale_var.set("log")
            self.update_guideline_ui_state()
            self.save_settings()
            self.plot_graph()

    def show_source_inspector_dialog(self):
        """Opens a modal dialog window listing database records alongside reference standards."""
        dlg = tk.Toplevel(self)
        dlg.title("Material Source & Verification Registry")
        dlg.geometry("920x520")

        theme = THEMES["Dark"] if self.app_dark_mode_var.get() else THEMES["Light"]
        dlg.configure(bg=theme["app_bg"])

        frame = ttk.Frame(dlg, padding=8)
        frame.pack(fill="both", expand=True)

        cols = ("Grade / Name", "Class", "Subclass", "Source Reference Standard")
        tree = ttk.Treeview(frame, columns=cols, show="headings")
        tree.heading("Grade / Name", text="Specific Grade / Name")
        tree.heading("Class", text="Class")
        tree.heading("Subclass", text="Subclass")
        tree.heading("Source Reference Standard", text="Source Reference Standard")

        tree.column("Grade / Name", width=250)
        tree.column("Class", width=140)
        tree.column("Subclass", width=170)
        tree.column("Source Reference Standard", width=330)

        sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        all_records = self.db.fetch_records()
        for r in all_records:
            tree.insert("", "end", values=(r["material_name"], r["category"], r.get("subclass", ""), r.get("source", "Standard Reference")))

    def import_csv_dialog(self):
        """Prompts user to select a CSV file and loads new material entries into SQLite."""
        path = filedialog.askopenfilename(
            title="Import Material Records",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if not path:
            return
        try:
            count = self.db.import_csv(path)
            messagebox.showinfo("Import Successful", f"Imported {count} material records into database.")
            self.populate_treeview()
            self.save_settings()
            self.plot_graph()
        except Exception as ex:
            messagebox.showerror("Import Error", f"Failed to import CSV:\n{str(ex)}")

    def on_plot_click(self, event):
        """
        Handles mouse clicks on the canvas for interactive tag selection and anchor dragging.

        Algorithm: Nearest-Neighbor Search in Log/Linear Space
        1. Convert the mouse click coordinates into linearized scale space (log10 if log axis).
        2. Check proximity against annotation anchor points to initiate anchor repositioning.
        3. If no anchor was hit, compute Euclidean distance in scale space to all plotted materials:
           dist = sqrt((x_click - x_mat)^2 + (y_click - y_mat)^2)
        4. If the closest material lies within the threshold, toggle its tagged callout state.
        """
        if self.active_drag_ann is not None:
            return
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None or event.button != 1:
            return

        x_is_log = (self.x_scale_var.get() == "log")
        y_is_log = (self.y_scale_var.get() == "log")

        click_sp_x = np.log10(max(event.xdata, 1e-12)) if x_is_log else event.xdata
        click_sp_y = np.log10(max(event.ydata, 1e-12)) if y_is_log else event.ydata

        # 1. Proximity hit-test against existing callout anchors
        anchor_hit = None
        min_anchor_dist = float("inf")
        if hasattr(self, 'annotation_artists') and self.annotation_artists:
            for ann in self.annotation_artists:
                ax_pt, ay_pt = ann.xy
                sp_ax = np.log10(max(ax_pt, 1e-12)) if x_is_log else ax_pt
                sp_ay = np.log10(max(ay_pt, 1e-12)) if y_is_log else ay_pt
                d = np.hypot(sp_ax - click_sp_x, sp_ay - click_sp_y)
                if d < min_anchor_dist:
                    min_anchor_dist = d
                    anchor_hit = ann

        thresh = 0.04 if (x_is_log and y_is_log) else 4.0
        if min_anchor_dist < thresh and anchor_hit is not None:
            self.active_drag_ann = anchor_hit
            self.drag_mode = 'anchor'
            self.drag_start_pos = (event.xdata, event.ydata)
            return

        # 2. Nearest-neighbor hit-test against plotted material data points
        min_dist = float("inf")
        closest_name = None
        for (px, py), name in self.plotted_coords.items():
            sp_px = np.log10(max(px, 1e-12)) if x_is_log else px
            sp_py = np.log10(max(py, 1e-12)) if y_is_log else py

            dist = np.hypot(sp_px - click_sp_x, sp_py - click_sp_y)
            if dist < min_dist:
                min_dist = dist
                closest_name = name

        dist_thresh = 0.08 if (x_is_log and y_is_log) else 10.0
        if min_dist < dist_thresh and closest_name:
            if closest_name in self.tagged_materials:
                self.tagged_materials.remove(closest_name)
            else:
                self.tagged_materials.add(closest_name)
            self.populate_treeview()
            self.save_settings()
            self.plot_graph()

    def plot_graph(self):
        """
        Gathers selected materials, computes property values, packages hierarchy structures,
        and delegates rendering to `render_ashby_chart`.
        """
        self.update_guideline_ui_state()

        x_prop = self.x_axis_cb.get()
        y_prop = self.y_axis_cb.get()
        grouping_level = self.grouping_level_var.get()

        raw_records = self.db.fetch_records(list(self.active_materials))

        class_dict = {}
        subclass_dict = {}
        hierarchy_map = {}

        for r in raw_records:
            cat = r["category"]
            sub = r.get("subclass", "General")
            xv = compute_property_value(x_prop, r)
            yv = compute_property_value(y_prop, r)
            if xv is not None and yv is not None and xv > 0 and yv > 0:
                if cat not in class_dict:
                    class_dict[cat] = []
                class_dict[cat].append((r["material_name"], xv, yv))

                if sub not in subclass_dict:
                    subclass_dict[sub] = []
                subclass_dict[sub].append((r["material_name"], xv, yv))

                if cat not in hierarchy_map:
                    hierarchy_map[cat] = []
                if sub not in hierarchy_map[cat]:
                    hierarchy_map[cat].append(sub)

        slope_val = None
        pair = (y_prop, x_prop)
        if pair in VALID_INDEX_GUIDES and self.show_guideline.get():
            selected_label = self.guideline_slope.get()
            for label, val in VALID_INDEX_GUIDES[pair]:
                if label == selected_label:
                    slope_val = val
                    break

        if grouping_level == "both":
            active_tagged_groups = self.tagged_classes.union(self.tagged_subclasses)
        elif grouping_level == "subclass":
            active_tagged_groups = self.tagged_subclasses
        else:
            active_tagged_groups = self.tagged_classes

        # Package data structures for the plotting engine
        data_bundle = {
            "classes": class_dict,
            "subclasses": subclass_dict,
            "hierarchy": hierarchy_map
        }

        options = {
            "x_prop": x_prop,
            "y_prop": y_prop,
            "x_scale": self.x_scale_var.get(),
            "y_scale": self.y_scale_var.get(),
            "grouping_level": grouping_level,
            "show_points": self.show_points.get(),
            "show_envelopes": self.show_envelopes.get(),
            "show_cat_labels": self.show_cat_labels.get(),
            "tagged_groups": list(active_tagged_groups),
            "show_guideline": self.show_guideline.get(),
            "guideline_slope_val": slope_val,
            "palette": self.active_palette,
            "dark_bg": self.chart_dark_bg_var.get(),
            "glow_effect": self.glow_effect_var.get()
        }

        self.plotted_coords, self.annotation_artists = render_ashby_chart(
            self.ax, data_bundle, self.tagged_materials, options, self.manual_positions
        )
        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = MaterialSelectorApp()
    app.mainloop()