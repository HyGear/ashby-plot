import numpy as np
import matplotlib as mpl
import colorsys
from scipy.spatial import ConvexHull
from scipy import interpolate
from matplotlib.path import Path as MplPath

mpl.rcParams['mathtext.fontset'] = 'dejavusans'

# Dictionary mapping descriptive UI labels to database column names or computed keys
PROPERTIES = {
    "Density ρ (g/cm³)": "density",
    "Young's Modulus E (GPa)": "youngs_modulus",
    "Yield / Elastic Limit σy (MPa)": "yield_strength",
    "Tensile Strength σu (MPa)": "tensile_strength",
    "Fracture Toughness K1c (MPa·m^0.5)": "fracture_toughness",
    "Loss Coefficient η (Damping)": "loss_coefficient",
    "Thermal Conductivity λ (W/m·K)": "thermal_conductivity",
    "Specific Heat Cp (J/kg·K)": "specific_heat",
    "Thermal Diffusivity a (m²/s)": "diffusivity",
    "Thermal Expansion Coeff α (10^-6/K)": "thermal_expansion",
    "Max Service Temperature Tmax (°C)": "max_service_temp",
    "Cost per kg Cm ($/kg)": "cost_per_kg",
    "Volumetric Cost Cv ($/m³)": "vol_cost",
    "Specific Stiffness E/ρ (GPa/(g/cm³))": "specific_stiffness",
    "Specific Strength σy/ρ (MPa/(g/cm³))": "specific_strength"
}

# LaTeX formatted labels for plot axes
AXIS_MATH_LABELS = {
    "Density ρ (g/cm³)": r"Density $\rho$ (g/cm$^3$)",
    "Young's Modulus E (GPa)": r"Young's Modulus $E$ (GPa)",
    "Yield / Elastic Limit σy (MPa)": r"Yield / Elastic Limit $\sigma_y$ (MPa)",
    "Tensile Strength σu (MPa)": r"Tensile Strength $\sigma_u$ (MPa)",
    "Fracture Toughness K1c (MPa·m^0.5)": r"Fracture Toughness $K_{1c}$ (MPa$\cdot$m$^{0.5}$)",
    "Loss Coefficient η (Damping)": r"Loss Coefficient $\eta$ (Damping)",
    "Thermal Conductivity λ (W/m·K)": r"Thermal Conductivity $\lambda$ (W/m$\cdot$K)",
    "Specific Heat Cp (J/kg·K)": r"Specific Heat $C_p$ (J/kg$\cdot$K)",
    "Thermal Diffusivity a (m²/s)": r"Thermal Diffusivity $a$ (m$^2$/s)",
    "Thermal Expansion Coeff α (10^-6/K)": r"Thermal Expansion Coeff $\alpha$ ($10^{-6}$/K)",
    "Max Service Temperature Tmax (°C)": r"Max Service Temperature $T_{\mathrm{max}}$ (°C)",
    "Cost per kg Cm ($/kg)": r"Cost per kg $C_m$ (\$/kg)",
    "Volumetric Cost Cv ($/m³)": r"Volumetric Cost $C_v$ (\$/m$^3$)",
    "Specific Stiffness E/ρ (GPa/(g/cm³))": r"Specific Stiffness $E/\rho$ (GPa/(g/cm$^3$))",
    "Specific Strength σy/ρ (MPa/(g/cm³))": r"Specific Strength $\sigma_y/\rho$ (MPa/(g/cm$^3$))"
}

# Color palettes for material classes
PALETTES = {
    "CES Classic": {
        "Ferrous Metals": "#3B6998", "Non-Ferrous Metals": "#C49A2C", "Polymers": "#2E8B57",
        "Ceramics & Glasses": "#A52A2A", "Composites": "#6A3D9A", "Elastomers": "#D95F02",
        "Natural & Biological": "#8C564B", "Gaskets & Seals": "#E377C2", "Cellular Solids": "#7F7F7F",
        "Bearing & Friction": "#BCBD22", "Specialty Non-Metallic": "#17BECF"
    },
    "High Contrast Vibrant": {
        "Ferrous Metals": "#0072B2", "Non-Ferrous Metals": "#E69F00", "Polymers": "#009E73",
        "Ceramics & Glasses": "#D55E00", "Composites": "#CC79A7", "Elastomers": "#56B4E9",
        "Natural & Biological": "#882255", "Gaskets & Seals": "#AA4499", "Cellular Solids": "#999933",
        "Bearing & Friction": "#332288", "Specialty Non-Metallic": "#117733"
    },
    "FEA Stress Spectrum": {
        "Ferrous Metals": "#1F4E79", "Non-Ferrous Metals": "#2CA02C", "Polymers": "#BCBD22",
        "Ceramics & Glasses": "#D62728", "Composites": "#9467BD", "Elastomers": "#FF7F0E",
        "Natural & Biological": "#8C564B", "Gaskets & Seals": "#E377C2", "Cellular Solids": "#7F7F7F",
        "Bearing & Friction": "#17BECF", "Specialty Non-Metallic": "#AEC7E8"
    },
    "Cambridge Blue": {
        "Ferrous Metals": "#0047AB", "Non-Ferrous Metals": "#008080", "Polymers": "#2E8B57",
        "Ceramics & Glasses": "#800020", "Composites": "#4B0082", "Elastomers": "#DAA520",
        "Natural & Biological": "#5C4033", "Gaskets & Seals": "#B8860B", "Cellular Solids": "#708090",
        "Bearing & Friction": "#2F4F4F", "Specialty Non-Metallic": "#4682B4"
    },
    "Academic Paper Mono": {
        "Ferrous Metals": "#1A1A1A", "Non-Ferrous Metals": "#4D4D4D", "Polymers": "#737373",
        "Ceramics & Glasses": "#2B2B2B", "Composites": "#8C8C8C", "Elastomers": "#A6A6A6",
        "Natural & Biological": "#333333", "Gaskets & Seals": "#555555", "Cellular Solids": "#B3B3B3",
        "Bearing & Friction": "#666666", "Specialty Non-Metallic": "#999999"
    },
    "Industrial Red": {
        "Ferrous Metals": "#444444", "Non-Ferrous Metals": "#B0B0B0", "Polymers": "#E60012",
        "Ceramics & Glasses": "#8B0000", "Composites": "#666666", "Elastomers": "#FF4D4D",
        "Natural & Biological": "#7A5230", "Gaskets & Seals": "#C77B58", "Cellular Solids": "#999999",
        "Bearing & Friction": "#CC3333", "Specialty Non-Metallic": "#FF8080"
    },
    "ANSI Machinery Safety": {
        "Ferrous Metals": "#004B87", "Non-Ferrous Metals": "#F1A800", "Polymers": "#00843D",
        "Ceramics & Glasses": "#DA291C", "Composites": "#662483", "Elastomers": "#E87722",
        "Natural & Biological": "#8C531B", "Gaskets & Seals": "#D9381E", "Cellular Solids": "#6C7A89",
        "Bearing & Friction": "#F7A800", "Specialty Non-Metallic": "#0099FF"
    },
    "Copper & Patina": {
        "Ferrous Metals": "#5C4033", "Non-Ferrous Metals": "#B87333", "Polymers": "#4E796B",
        "Ceramics & Glasses": "#8A3324", "Composites": "#2E4F4F", "Elastomers": "#5F9EA0",
        "Natural & Biological": "#8B5A2B", "Gaskets & Seals": "#A0522D", "Cellular Solids": "#778899",
        "Bearing & Friction": "#CD853F", "Specialty Non-Metallic": "#20B2AA"
    },
    "Blueprint Drafting": {
        "Ferrous Metals": "#004B87", "Non-Ferrous Metals": "#60A3BC", "Polymers": "#78E08F",
        "Ceramics & Glasses": "#E55039", "Composites": "#4A69BD", "Elastomers": "#F6B93B",
        "Natural & Biological": "#BADC58", "Gaskets & Seals": "#E77F67", "Cellular Solids": "#778CA3",
        "Bearing & Friction": "#CF6A87", "Specialty Non-Metallic": "#3DC1D3"
    },
    "Aerospace Mil-Spec": {
        "Ferrous Metals": "#34495E", "Non-Ferrous Metals": "#7F8C8D", "Polymers": "#27AE60",
        "Ceramics & Glasses": "#C0392B", "Composites": "#2C3E50", "Elastomers": "#D35400",
        "Natural & Biological": "#8E44AD", "Gaskets & Seals": "#16A085", "Cellular Solids": "#BDC3C7",
        "Bearing & Friction": "#F39C12", "Specialty Non-Metallic": "#2980B9"
    },
    "CNC Toolroom": {
        "Ferrous Metals": "#2B3A42", "Non-Ferrous Metals": "#FFD200", "Polymers": "#4F6D7A",
        "Ceramics & Glasses": "#E63946", "Composites": "#C0D6DF", "Elastomers": "#F4A261",
        "Natural & Biological": "#A8DADC", "Gaskets & Seals": "#E76F51", "Cellular Solids": "#95A5A6",
        "Bearing & Friction": "#2A9D8F", "Specialty Non-Metallic": "#457B9D"
    },
    "Camo Earth": {
        "Ferrous Metals": "#4D5D53", "Non-Ferrous Metals": "#C2B280", "Polymers": "#556B2F",
        "Ceramics & Glasses": "#8B4513", "Composites": "#2F4F4F", "Elastomers": "#D27D2D",
        "Natural & Biological": "#6B8E23", "Gaskets & Seals": "#BDB76B", "Cellular Solids": "#A9A9A9",
        "Bearing & Friction": "#8FBC8F", "Specialty Non-Metallic": "#5F9EA0"
    },
    "Botanical Garden": {
        "Ferrous Metals": "#1B4D3E", "Non-Ferrous Metals": "#A4C639", "Polymers": "#2E8B57",
        "Ceramics & Glasses": "#8B0000", "Composites": "#355E3B", "Elastomers": "#DDA0DD",
        "Natural & Biological": "#228B22", "Gaskets & Seals": "#FF69B4", "Cellular Solids": "#98FB98",
        "Bearing & Friction": "#D2B48C", "Specialty Non-Metallic": "#66CDAA"
    },
    "Desert Dune": {
        "Ferrous Metals": "#4B382A", "Non-Ferrous Metals": "#C29B38", "Polymers": "#A0522D",
        "Ceramics & Glasses": "#8B2500", "Composites": "#D2B48C", "Elastomers": "#DEB887",
        "Natural & Biological": "#CD853F", "Gaskets & Seals": "#F4A460", "Cellular Solids": "#EEE8AA",
        "Bearing & Friction": "#B8860B", "Specialty Non-Metallic": "#DAA520"
    },
    "Deep Ocean Trench": {
        "Ferrous Metals": "#0B1D3A", "Non-Ferrous Metals": "#006994", "Polymers": "#009688",
        "Ceramics & Glasses": "#1A5276", "Composites": "#4A235A", "Elastomers": "#20B2AA",
        "Natural & Biological": "#2E4053", "Gaskets & Seals": "#5D6D7E", "Cellular Solids": "#85929E",
        "Bearing & Friction": "#117864", "Specialty Non-Metallic": "#5499C7"
    },
    "Arctic Glacier": {
        "Ferrous Metals": "#1C3144", "Non-Ferrous Metals": "#007E8A", "Polymers": "#3F88C5",
        "Ceramics & Glasses": "#A5C4D4", "Composites": "#5B6C5D", "Elastomers": "#88B04B",
        "Natural & Biological": "#4682B4", "Gaskets & Seals": "#B0E0E6", "Cellular Solids": "#E0FFFF",
        "Bearing & Friction": "#5F9EA0", "Specialty Non-Metallic": "#87CEEB"
    },
    "Forest Canopy": {
        "Ferrous Metals": "#19381F", "Non-Ferrous Metals": "#EAC435", "Polymers": "#2D6A4F",
        "Ceramics & Glasses": "#78290F", "Composites": "#1B4332", "Elastomers": "#D4A373",
        "Natural & Biological": "#52796F", "Gaskets & Seals": "#84A98C", "Cellular Solids": "#CAD2C5",
        "Bearing & Friction": "#9A8C98", "Specialty Non-Metallic": "#C9ADA7"
    },
    "Autumn Foliage": {
        "Ferrous Metals": "#5E3023", "Non-Ferrous Metals": "#E76F51", "Polymers": "#2A9D8F",
        "Ceramics & Glasses": "#9B2226", "Composites": "#895737", "Elastomers": "#F4A261",
        "Natural & Biological": "#BB3E03", "Gaskets & Seals": "#CA6702", "Cellular Solids": "#E9D8A6",
        "Bearing & Friction": "#AE2012", "Specialty Non-Metallic": "#0A9396"
    },
    "Colorblind Safe (Wong)": {
        "Ferrous Metals": "#0072B2", "Non-Ferrous Metals": "#E69F00", "Polymers": "#009E73",
        "Ceramics & Glasses": "#D55E00", "Composites": "#CC79A7", "Elastomers": "#F0E442",
        "Natural & Biological": "#56B4E9", "Gaskets & Seals": "#999999", "Cellular Solids": "#E69F00",
        "Bearing & Friction": "#0072B2", "Specialty Non-Metallic": "#009E73"
    },
    "Viridis Categorical": {
        "Ferrous Metals": "#440154", "Non-Ferrous Metals": "#21918C", "Polymers": "#5EC962",
        "Ceramics & Glasses": "#3B528B", "Composites": "#FDE725", "Elastomers": "#287D8E",
        "Natural & Biological": "#482878", "Gaskets & Seals": "#31688E", "Cellular Solids": "#1F9E89",
        "Bearing & Friction": "#35B779", "Specialty Non-Metallic": "#B5DE2B"
    },
    "Plasma Accent": {
        "Ferrous Metals": "#0D0887", "Non-Ferrous Metals": "#CC4778", "Polymers": "#F89540",
        "Ceramics & Glasses": "#6A00A8", "Composites": "#B12A90", "Elastomers": "#F0F921",
        "Natural & Biological": "#47039F", "Gaskets & Seals": "#8B0AA5", "Cellular Solids": "#CB4679",
        "Bearing & Friction": "#E56B5D", "Specialty Non-Metallic": "#F8873E"
    },
    "Turbo Spectrum": {
        "Ferrous Metals": "#30123B", "Non-Ferrous Metals": "#1AE4B6", "Polymers": "#A4FC3C",
        "Ceramics & Glasses": "#D82632", "Composites": "#466BE3", "Elastomers": "#FABA39",
        "Natural & Biological": "#3E4989", "Gaskets & Seals": "#22A884", "Cellular Solids": "#7AD151",
        "Bearing & Friction": "#FDE725", "Specialty Non-Metallic": "#FA7629"
    },
    "Solarized Light": {
        "Ferrous Metals": "#268BD2", "Non-Ferrous Metals": "#B58900", "Polymers": "#859900",
        "Ceramics & Glasses": "#DC322F", "Composites": "#6C71C4", "Elastomers": "#CB4B16",
        "Natural & Biological": "#2AA198", "Gaskets & Seals": "#D33682", "Cellular Solids": "#93A1A1",
        "Bearing & Friction": "#586E75", "Specialty Non-Metallic": "#657B83"
    },
    "Solarized Dark": {
        "Ferrous Metals": "#2AA198", "Non-Ferrous Metals": "#B58900", "Polymers": "#859900",
        "Ceramics & Glasses": "#D33682", "Composites": "#6C71C4", "Elastomers": "#CB4B16",
        "Natural & Biological": "#268BD2", "Gaskets & Seals": "#DC322F", "Cellular Solids": "#839496",
        "Bearing & Friction": "#93A1A1", "Specialty Non-Metallic": "#EEE8D5"
    },
    "Synthwave 84": {
        "Ferrous Metals": "#00E5FF", "Non-Ferrous Metals": "#FFE600", "Polymers": "#05FFA1",
        "Ceramics & Glasses": "#FF007F", "Composites": "#B967FF", "Elastomers": "#FF6C00",
        "Natural & Biological": "#FF1493", "Gaskets & Seals": "#7B1FA2", "Cellular Solids": "#38EF7D",
        "Bearing & Friction": "#F107A3", "Specialty Non-Metallic": "#11998E"
    },
    "Cyberpunk Neon": {
        "Ferrous Metals": "#00F0FF", "Non-Ferrous Metals": "#FAED26", "Polymers": "#00FF66",
        "Ceramics & Glasses": "#FF0055", "Composites": "#7B00FF", "Elastomers": "#FF9900",
        "Natural & Biological": "#E056FD", "Gaskets & Seals": "#FF3838", "Cellular Solids": "#3AE374",
        "Bearing & Friction": "#67E6DC", "Specialty Non-Metallic": "#FFFA65"
    },
    "Bauhaus Primary": {
        "Ferrous Metals": "#104E8B", "Non-Ferrous Metals": "#FFD700", "Polymers": "#2E8B57",
        "Ceramics & Glasses": "#CD2626", "Composites": "#262626", "Elastomers": "#FF8C00",
        "Natural & Biological": "#4682B4", "Gaskets & Seals": "#A52A2A", "Cellular Solids": "#808080",
        "Bearing & Friction": "#B8860B", "Specialty Non-Metallic": "#008B8B"
    },
    "1980s Terminal Green": {
        "Ferrous Metals": "#004700", "Non-Ferrous Metals": "#00FF66", "Polymers": "#008F11",
        "Ceramics & Glasses": "#00FF41", "Composites": "#005C00", "Elastomers": "#55FF55",
        "Natural & Biological": "#003300", "Gaskets & Seals": "#00AA00", "Cellular Solids": "#00CC44",
        "Bearing & Friction": "#228822", "Specialty Non-Metallic": "#66FF66"
    },
    "Nordic Frost": {
        "Ferrous Metals": "#5C768D", "Non-Ferrous Metals": "#B8D5E5", "Polymers": "#8EAF9D",
        "Ceramics & Glasses": "#D98880", "Composites": "#4B586E", "Elastomers": "#F2D7D5",
        "Natural & Biological": "#98AFC7", "Gaskets & Seals": "#C2D4D8", "Cellular Solids": "#E1E8EB",
        "Bearing & Friction": "#7E909A", "Specialty Non-Metallic": "#A2B5BF"
    },
    "Sunset Horizon": {
        "Ferrous Metals": "#2C3E50", "Non-Ferrous Metals": "#F39C12", "Polymers": "#16A085",
        "Ceramics & Glasses": "#C0392B", "Composites": "#8E44AD", "Elastomers": "#E67E22",
        "Natural & Biological": "#D35400", "Gaskets & Seals": "#9B59B6", "Cellular Solids": "#BDC3C7",
        "Bearing & Friction": "#E74C3C", "Specialty Non-Metallic": "#1ABC9C"
    }
}

SUBCLASS_CYCLE_COLORS = [
    "#E63946", "#F4A261", "#E76F51", "#2A9D8F", "#264653",
    "#0077B6", "#00B4D8", "#7209B7", "#B5179E", "#4361EE",
    "#4CC9F0", "#38B000", "#70E000", "#9EF01A", "#CC5803",
    "#D90429", "#EF233C", "#8D99AE", "#588157", "#3A5A40"
]

ASHBY_PRESETS = {
    "Modulus - Density (E vs ρ)": ("Young's Modulus E (GPa)", "Density ρ (g/cm³)"),
    "Strength - Density (σy vs ρ)": ("Yield / Elastic Limit σy (MPa)", "Density ρ (g/cm³)"),
    "Fracture Toughness - Strength (K1c vs σy)": ("Fracture Toughness K1c (MPa·m^0.5)", "Yield / Elastic Limit σy (MPa)"),
    "Modulus - Relative Cost (E vs Cv)": ("Young's Modulus E (GPa)", "Volumetric Cost Cv ($/m³)"),
    "Strength - Relative Cost (σy vs Cv)": ("Yield / Elastic Limit σy (MPa)", "Volumetric Cost Cv ($/m³)"),
    "Loss Coeff - Modulus (η vs E)": ("Loss Coefficient η (Damping)", "Young's Modulus E (GPa)"),
    "Conductivity - Diffusivity (λ vs a)": ("Thermal Conductivity λ (W/m·K)", "Thermal Diffusivity a (m²/s)"),
    "Expansion - Modulus (α vs E)": ("Thermal Expansion Coeff α (10^-6/K)", "Young's Modulus E (GPa)"),
    "Max Service Temp - Modulus (Tmax vs E)": ("Max Service Temperature Tmax (°C)", "Young's Modulus E (GPa)")
}

# Slopes for Ashby Material Index lines M = y^(1/n) / x => log(y) = n*log(x) + C
VALID_INDEX_GUIDES = {
    ("Young's Modulus E (GPa)", "Density ρ (g/cm³)"): [
        ("Slope 1 (n=1): Tie / Tension (M = E / ρ)", 1.0),
        ("Slope 2 (n=2): Bending Beam (M = E^1/2 / ρ)", 2.0),
        ("Slope 3 (n=3): Flat Panel (M = E^1/3 / ρ)", 3.0),
    ],
    ("Yield / Elastic Limit σy (MPa)", "Density ρ (g/cm³)"): [
        ("Slope 1 (n=1): Tie Yield (M = σy / ρ)", 1.0),
        ("Slope 1.5 (n=1.5): Bending Beam Collapse (M = σy^2/3 / ρ)", 1.5),
        ("Slope 2 (n=2): Flat Panel Collapse (M = σy^1/2 / ρ)", 2.0),
    ],
    ("Young's Modulus E (GPa)", "Volumetric Cost Cv ($/m³)"): [
        ("Slope 1 (n=1): Min Cost Tie (M = E / Cv)", 1.0),
        ("Slope 2 (n=2): Min Cost Beam (M = E^1/2 / Cv)", 2.0),
        ("Slope 3 (n=3): Min Cost Panel (M = E^1/3 / Cv)", 3.0),
    ],
    ("Yield / Elastic Limit σy (MPa)", "Volumetric Cost Cv ($/m³)"): [
        ("Slope 1 (n=1): Min Cost Tie Yield (M = σy / Cv)", 1.0),
        ("Slope 1.5 (n=1.5): Min Cost Beam Collapse (M = σy^2/3 / Cv)", 1.5),
        ("Slope 2 (n=2): Min Cost Panel Collapse (M = σy^1/2 / Cv)", 2.0),
    ],
    ("Fracture Toughness K1c (MPa·m^0.5)", "Yield / Elastic Limit σy (MPa)"): [
        ("Slope 2 (n=2): Constant Flaw Size ac ∝ (K1c / σy)^2", 2.0),
    ],
    ("Fracture Toughness K1c (MPa·m^0.5)", "Young's Modulus E (GPa)"): [
        ("Slope 0.5 (n=0.5): Crack Opening Disp δc ∝ K1c^2 / E", 0.5),
        ("Slope 1.0 (n=1.0): Critical Strain Energy Release G1c", 1.0),
    ],
    ("Thermal Conductivity λ (W/m·K)", "Thermal Diffusivity a (m²/s)"): [
        ("Slope 1 (n=1): Constant Vol Heat Capacity ρCp = λ / a", 1.0),
    ]
}

def derive_subclass_color(base_hex, sub_idx, total_subs):
    """
    Generates a distinct shade of a base class color for each subclass.

    Algorithm: HLS Color Space Luminance Modulating
    1. Converts base RGB hex to HLS (Hue, Lightness, Saturation).
    2. Calculates normalized subclass offset: norm = (sub_idx / (total_subs - 1)) - 0.5 in [-0.5, 0.5].
    3. Modulates lightness L within [0.30, 0.72] based on the offset to produce darker-to-lighter shades.
    4. Slightly boosts saturation S within [0.48, 0.95] to prevent washing out.
    5. Converts HLS back to RGB and formats as hex string.
    """
    if total_subs <= 1:
        return base_hex

    hex_str = base_hex.lstrip('#')
    r = int(hex_str[0:2], 16) / 255.0
    g = int(hex_str[2:4], 16) / 255.0
    b = int(hex_str[4:6], 16) / 255.0

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    norm = (sub_idx / (total_subs - 1.0)) - 0.5
    new_l = max(0.30, min(0.72, l + (norm * 0.24)))
    new_s = max(0.48, min(0.95, s * 1.02))

    new_r, new_g, new_b = colorsys.hls_to_rgb(h, new_l, new_s)
    return f"#{int(new_r * 255):02x}{int(new_g * 255):02x}{int(new_b * 255):02x}"

def to_space(val, is_log):
    """Transforms a coordinate value into linear visual space (log10 if is_log=True)."""
    return np.log10(max(float(val), 1e-12)) if is_log else float(val)

def from_space(val, is_log):
    """Inverts a linear visual space coordinate back to original data space (10^val if is_log=True)."""
    return (10.0**float(val)) if is_log else float(val)

def compute_property_value(prop_key, row):
    """
    Extracts raw or derived material engineering properties from a database record row.

    Handles on-the-fly derivations:
    - Thermal Diffusivity: a = λ / (ρ * Cp)
    - Volumetric Cost: Cv = Cm * ρ
    - Specific Stiffness: E / ρ
    - Specific Strength: σy / ρ
    """
    field = PROPERTIES.get(prop_key)
    if not field:
        return None
    if field == "diffusivity":
        lam = row.get("thermal_conductivity")
        rho = row.get("density")
        cp = row.get("specific_heat")
        if lam and rho and cp:
            return lam / ((rho * 1000.0) * cp)
        return None
    elif field == "vol_cost":
        cm = row.get("cost_per_kg")
        rho = row.get("density")
        if cm and rho:
            return cm * (rho * 1000.0)
        return None
    elif field == "specific_stiffness":
        e = row.get("youngs_modulus")
        rho = row.get("density")
        if e and rho:
            return e / rho
        return None
    elif field == "specific_strength":
        sy = row.get("yield_strength")
        rho = row.get("density")
        if sy and rho:
            return sy / rho
        return None
    return row.get(field)

def generate_envelope_spline(pts, x_log, y_log, scale_x_unit=0.15, scale_y_unit=0.15, space_pts_input=None):
    """
    Generates a smooth, closed boundary envelope (bubble) enclosing a cluster of points.

    Algorithm: Convex Hull with Periodic Parametric B-Spline Interpolation
    1. Space Transformation:
       Converts data coordinates into visual space (log10 if logarithmic scale) so geometric
       distance matches what the user perceives on the screen.
    2. Cluster Size Handling:
       - N >= 4 points:
         Computes the 2D Convex Hull (Quickhull via `scipy.spatial.ConvexHull`) to isolate outer
         boundary vertices. Closes the polygon loop (appending vertex 0 at end) and fits a cubic
         periodic B-spline (scipy.interpolate.splprep with k=3, per=1, s=0.0). Samples 300 points
         via `splev` to produce an organic boundary.
       - N == 3 points:
         Calculates polar angles theta = arctan2(y - cy, x - cx) around centroid (cx, cy),
         sorts points angularly to form a counter-clockwise loop, and fits a quadratic periodic
         spline (k=2, per=1). Samples 200 points.
       - N == 2 points:
         Fits an oriented ellipse centered at the midpoint, aligned along the angle theta = arctan2(dy, dx),
         with semi-major axis proportional to inter-point distance and semi-minor axis scaled to thickness.
       - N == 1 point:
         Generates a circular/ellipsoidal bubble based on chart display units (scale_x_unit, scale_y_unit).
    3. Inversion:
       Transforms interpolated spline points back from visual space to original data scale (10^x).
    """
    if space_pts_input is not None and len(space_pts_input) > 0:
        space_pts = np.array(space_pts_input, dtype=float)
        sx = space_pts[:, 0]
        sy = space_pts[:, 1]
    elif len(pts) > 0:
        sx = np.array([to_space(p[0], x_log) for p in pts])
        sy = np.array([to_space(p[1], y_log) for p in pts])
        space_pts = np.column_stack((sx, sy))
    else:
        return None, None, None, None

    cx = np.mean(sx)
    cy = np.mean(sy)

    try:
        if len(space_pts) >= 4:
            # 2D Convex Hull outer boundary
            hull = ConvexHull(space_pts)
            hx = [sx[i] for i in hull.vertices]
            hy = [sy[i] for i in hull.vertices]
            x_closed = np.r_[hx, hx[0]]
            y_closed = np.r_[hy, hy[0]]

            # Cubic periodic B-spline smoothing
            tck, u = interpolate.splprep([x_closed, y_closed], u=None, s=0.0, per=1, k=3)
            u_new = np.linspace(u.min(), u.max(), num=300)
            x_new_space, y_new_space = interpolate.splev(u_new, tck, der=0)

        elif len(space_pts) == 3:
            # Angular sort around centroid for triangle closure
            angles = np.arctan2(sy - cy, sx - cx)
            sort_idx = np.argsort(angles)
            hx = sx[sort_idx]
            hy = sy[sort_idx]
            x_closed = np.r_[hx, hx[0]]
            y_closed = np.r_[hy, hy[0]]
            tck, u = interpolate.splprep([x_closed, y_closed], u=None, s=0.0, per=1, k=2)
            u_new = np.linspace(u.min(), u.max(), num=200)
            x_new_space, y_new_space = interpolate.splev(u_new, tck, der=0)

        elif len(space_pts) == 2:
            # Oriented bounding ellipse between 2 points
            dx = sx[1] - sx[0]
            dy = sy[1] - sy[0]
            dist = np.hypot(dx, dy)
            theta = np.arctan2(dy, dx)

            mid_x = (sx[0] + sx[1]) / 2.0
            mid_y = (sy[0] + sy[1]) / 2.0

            a = max(dist / 2.0 * 1.08, 0.04)
            b = max(dist * 0.08, 0.022)

            t = np.linspace(0, 2 * np.pi, 120)
            x_local = a * np.cos(t)
            y_local = b * np.sin(t)

            x_new_space = mid_x + x_local * np.cos(theta) - y_local * np.sin(theta)
            y_new_space = mid_y + x_local * np.sin(theta) + y_local * np.cos(theta)

        else:
            # Minimum radius circular bubble around isolated point
            r_x = max(scale_x_unit * 0.18, 0.025) * 1.10
            r_y = max(scale_y_unit * 0.18, 0.025) * 1.10
            theta = np.linspace(0, 2 * np.pi, 80)
            x_new_space = cx + r_x * np.cos(theta)
            y_new_space = cy + r_y * np.sin(theta)

        # Invert from visual coordinates back to data coordinates
        x_new = [from_space(v, x_log) for v in x_new_space]
        y_new = [from_space(v, y_log) for v in y_new_space]
        return np.array(x_new), np.array(y_new), list(zip(x_new_space, y_new_space)), (cx, cy)
    except Exception:
        return None, None, None, None

def check_box_collision(cx, cy, half_w, half_h, mpl_polygons):
    """
    Checks if an axis-aligned bounding box collides with any polygon envelopes.

    Algorithm: Multi-Point Point-in-Polygon (PIP) Sampling
    Samples 9 test points on the candidate box (center, 4 corners, and 4 edge midpoints)
    and tests them using `matplotlib.path.Path.contains_point` (Ray-Casting Algorithm)
    against each envelope polygon. Returns True if any point falls inside an envelope.
    """
    pts = [
        (cx, cy),
        (cx - half_w, cy - half_h),
        (cx + half_w, cy - half_h),
        (cx - half_w, cy + half_h),
        (cx + half_w, cy + half_h),
        (cx, cy - half_h),
        (cx, cy + half_h),
        (cx - half_w, cy),
        (cx + half_w, cy)
    ]
    for p in pts:
        for poly in mpl_polygons:
            if poly.contains_point(p):
                return True
    return False

def render_ashby_chart(ax, data_bundle, tagged_materials, options, manual_positions=None):
    """
    Renders the complete Ashby chart on the given Matplotlib axis.

    Advanced Algorithms Included:
    1. Multi-Tier Perimeter Callout Engine (Radial Ray Projection):
       - Computes a global convex hull enclosing all active material envelopes.
       - For each category/subclass label, projects a ray from the cluster center through the envelope
         centroid along an aspect-ratio-corrected angle.
       - Calculates the maximum reach of the global hull along this unit direction vector (ux, uy).
       - Places candidate label positions along outer staggered radial tiers, stepping outward
         until the label box clears all envelope polygon boundaries via `check_box_collision`.
    2. Multi-Body Label Collision Resolution:
       - Iterates up to 60 relaxation passes over all placed label boxes.
       - Detects pairwise AABB overlaps (dx < sep_x and dy < sep_y).
       - Applies a repulsive displacement along the label's radial unit vector to push colliding
         boxes outward until overlap is resolved.
    3. Performance Guide Lines:
       - Evaluates selection criteria: M = y^(1/n) / x => y = C * x^n
       - In log-log space, this forms a line with slope n passing through the geometric midpoint
         of the current data domain.
    """
    ax.clear()

    x_scale_log = (str(options.get("x_scale", "log")).lower() == "log")
    y_scale_log = (str(options.get("y_scale", "log")).lower() == "log")
    grouping_level = options.get("grouping_level", "class")
    tagged_groups = set(options.get("tagged_groups", []))

    ax.set_xscale("log" if x_scale_log else "linear")
    ax.set_yscale("log" if y_scale_log else "linear")

    all_x, all_y = [], []
    plotted_coords = {}
    group_centroids = {}
    tags_to_draw = []
    envelope_data = {}
    all_mpl_polygons = []
    placed_boxes_global = []
    all_label_extents = []
    annotation_objects = []

    palette_name = options.get("palette", "CES Classic")
    palette = PALETTES.get(palette_name, PALETTES["CES Classic"])
    is_dark = options.get("dark_bg", False)
    glow_enabled = options.get("glow_effect", False)

    fig_bg = "#0D1117" if is_dark else "#FFFFFF"
    fg_color = "#E6EDF3" if is_dark else "#1F2328"
    grid_color = "#30363D" if is_dark else "#D0D7DE"
    tag_bg = "#161B22" if is_dark else "#FFFFE0"
    tag_edge = "#8B949E" if is_dark else "#666666"
    class_bg = "#161B22" if is_dark else "#FFFFFF"
    arrow_color = "#8B949E" if is_dark else "#222222"

    ax.figure.patch.set_facecolor(fig_bg)
    ax.set_facecolor(fig_bg)

    class_dict = data_bundle.get("classes", {})
    subclass_dict = data_bundle.get("subclasses", {})
    hierarchy_map = data_bundle.get("hierarchy", {})

    sub_to_class = {}
    class_to_subs = {}
    for cls_k, sub_list in hierarchy_map.items():
        class_to_subs[cls_k] = sub_list
        for s in sub_list:
            sub_to_class[s] = cls_k

    if grouping_level == "class":
        raw_items = [pt for items in class_dict.values() for pt in items]
    else:
        raw_items = [pt for items in subclass_dict.values() for pt in items]

    for pt in raw_items:
        all_x.append(pt[1])
        all_y.append(pt[2])

    if all_x and all_y:
        span_space_x = abs(to_space(max(all_x), x_scale_log) - to_space(min(all_x), x_scale_log))
        span_space_y = abs(to_space(max(all_y), y_scale_log) - to_space(min(all_y), y_scale_log))
        scale_x_unit = max(span_space_x * 0.12, 0.10)
        scale_y_unit = max(span_space_y * 0.12, 0.10)
    else:
        scale_x_unit, scale_y_unit = 0.15, 0.15

    all_cluster_vertices = []
    class_sub_spline_points = {}

    # 1. Render Subclass Envelopes First
    if grouping_level in ("subclass", "both"):
        for sub_name, items in subclass_dict.items():
            if not items:
                continue

            parent_cls = sub_to_class.get(sub_name)
            base_c = palette.get(parent_cls, "#555555") if parent_cls else "#555555"
            siblings = class_to_subs.get(parent_cls, [sub_name])
            total_subs = len(siblings)
            s_idx = siblings.index(sub_name) if sub_name in siblings else 0

            color = derive_subclass_color(base_c, s_idx, total_subs)

            pts = np.array([[pt[1], pt[2]] for pt in items], dtype=float)

            sc_x = np.mean([to_space(p[0], x_scale_log) for p in pts])
            sc_y = np.mean([to_space(p[1], y_scale_log) for p in pts])
            group_centroids[sub_name] = (sc_x, sc_y)

            for pt in items:
                plotted_coords[(pt[1], pt[2])] = (pt[0], sub_name)
                if pt[0] in tagged_materials:
                    tags_to_draw.append((pt[0], sub_name, pt[1], pt[2]))

            if options.get("show_points", False):
                if glow_enabled:
                    for halo_size, halo_alpha in [(80, 0.10), (50, 0.22), (32, 0.38)]:
                        ax.scatter(pts[:, 0], pts[:, 1], color=color, alpha=halo_alpha, s=halo_size, edgecolors="none")
                ax.scatter(pts[:, 0], pts[:, 1], color=color, alpha=0.85 if is_dark else 0.72, s=24, edgecolors="none", label=sub_name)

            if options.get("show_envelopes", True):
                x_new, y_new, space_vertices, center = generate_envelope_spline(
                    pts, x_scale_log, y_scale_log, scale_x_unit, scale_y_unit
                )
                if x_new is not None:
                    scx, scy = center
                    all_cluster_vertices.extend(space_vertices)

                    if parent_cls:
                        class_sub_spline_points.setdefault(parent_cls, []).extend(space_vertices)

                    if grouping_level == "both" and total_subs <= 1:
                        color = base_c
                        fill_alpha = 0.08
                        line_w = 1.3
                        line_alpha = 0.60
                        line_style = "--"
                    elif grouping_level == "both":
                        fill_alpha = 0.18
                        line_w = 1.4
                        line_alpha = 0.88
                        line_style = "-"
                    else:
                        fill_alpha = 0.20 if (glow_enabled or is_dark) else 0.16
                        line_w = 1.6
                        line_alpha = 0.95
                        line_style = "-"

                    if glow_enabled and (grouping_level != "both" or total_subs > 1):
                        for lw, alpha_g in [(5.5, 0.08), (3.5, 0.15)]:
                            ax.plot(x_new, y_new, color=color, linestyle="-", linewidth=lw, alpha=alpha_g)

                    ax.plot(x_new, y_new, color=color, linestyle=line_style, linewidth=line_w, alpha=line_alpha)
                    ax.fill(x_new, y_new, color=color, alpha=fill_alpha)

                    poly_path = MplPath(space_vertices)
                    all_mpl_polygons.append(poly_path)

                    env_obj = {
                        "color": color,
                        "space_vertices": space_vertices,
                        "scx": scx,
                        "scy": scy,
                        "poly_path": poly_path,
                        "level": "subclass"
                    }
                    envelope_data[sub_name] = env_obj

                    if grouping_level == "both" and total_subs <= 1 and parent_cls:
                        envelope_data[parent_cls] = env_obj

    # 2. Render Class Envelopes (Tangential Wrap With Zero Standoff Gap)
    if grouping_level in ("class", "both"):
        for cls_name, items in class_dict.items():
            if not items:
                continue

            siblings = class_to_subs.get(cls_name, [])
            if grouping_level == "both" and len(siblings) <= 1:
                continue

            color = palette.get(cls_name, "#555555")
            pts = np.array([[pt[1], pt[2]] for pt in items], dtype=float)

            sc_x = np.mean([to_space(p[0], x_scale_log) for p in pts])
            sc_y = np.mean([to_space(p[1], y_scale_log) for p in pts])
            group_centroids[cls_name] = (sc_x, sc_y)

            if grouping_level == "class":
                for pt in items:
                    plotted_coords[(pt[1], pt[2])] = (pt[0], cls_name)
                    if pt[0] in tagged_materials:
                        tags_to_draw.append((pt[0], cls_name, pt[1], pt[2]))

            if options.get("show_points", False) and grouping_level == "class":
                if glow_enabled:
                    for halo_size, halo_alpha in [(80, 0.10), (50, 0.22), (32, 0.38)]:
                        ax.scatter(pts[:, 0], pts[:, 1], color=color, alpha=halo_alpha, s=halo_size, edgecolors="none")
                ax.scatter(pts[:, 0], pts[:, 1], color=color, alpha=0.85 if is_dark else 0.70, s=24, edgecolors="none", label=cls_name)

            if options.get("show_envelopes", True):
                if grouping_level == "both" and cls_name in class_sub_spline_points:
                    child_space_pts = np.array(class_sub_spline_points[cls_name])
                    x_new, y_new, space_vertices, center = generate_envelope_spline(
                        [], x_scale_log, y_scale_log, scale_x_unit, scale_y_unit,
                        space_pts_input=child_space_pts
                    )
                else:
                    x_new, y_new, space_vertices, center = generate_envelope_spline(
                        pts, x_scale_log, y_scale_log, scale_x_unit, scale_y_unit
                    )

                if x_new is not None:
                    scx, scy = center
                    all_cluster_vertices.extend(space_vertices)

                    if grouping_level == "both":
                        fill_alpha = 0.08
                        line_w = 1.3
                        line_alpha = 0.60
                        line_style = "--"
                    else:
                        fill_alpha = 0.20 if (glow_enabled or is_dark) else 0.16
                        line_w = 1.6
                        line_alpha = 0.95
                        line_style = "--"

                    if glow_enabled and grouping_level != "both":
                        for lw, alpha_g in [(7.0, 0.08), (4.5, 0.16), (2.8, 0.30)]:
                            ax.plot(x_new, y_new, color=color, linestyle="-", linewidth=lw, alpha=alpha_g)

                    ax.plot(x_new, y_new, color=color, linestyle=line_style, linewidth=line_w, alpha=line_alpha)
                    ax.fill(x_new, y_new, color=color, alpha=fill_alpha)

                    poly_path = MplPath(space_vertices)
                    all_mpl_polygons.append(poly_path)

                    envelope_data[cls_name] = {
                        "color": color,
                        "space_vertices": space_vertices,
                        "scx": scx,
                        "scy": scy,
                        "poly_path": poly_path,
                        "level": "class"
                    }

    # 3. Multi-Tier Staggered Perimeter Ring Engine (Filtered by tagged_groups)
    active_envelope_labels = {
        name: env for name, env in envelope_data.items()
        if options.get("show_cat_labels", True) and (name in tagged_groups)
    }

    if active_envelope_labels:
        all_env_cx = [env["scx"] for env in envelope_data.values()]
        all_env_cy = [env["scy"] for env in envelope_data.values()]
        cluster_cx = np.mean(all_env_cx)
        cluster_cy = np.mean(all_env_cy)

        all_v_arr = np.array(all_cluster_vertices)
        if len(all_v_arr) >= 4:
            global_hull = ConvexHull(all_v_arr)
            global_hull_verts = [all_v_arr[i] for i in global_hull.vertices]
        else:
            global_hull_verts = all_cluster_vertices

        aspect_ratio = (scale_x_unit / max(scale_y_unit, 1e-4))

        # Sort envelopes angularly around the global cluster centroid
        envelope_sort_items = []
        for grp_name, env in active_envelope_labels.items():
            scx, scy = env["scx"], env["scy"]
            ndx = (scx - cluster_cx) / aspect_ratio
            ndy = (scy - cluster_cy)
            ang = np.arctan2(ndy, ndx)
            envelope_sort_items.append((ang, grp_name, env))

        envelope_sort_items.sort(key=lambda it: it[0])

        n_grp = len(envelope_sort_items)
        group_label_requests = []

        nominal_angles = np.linspace(-np.pi * 0.95, np.pi * 0.95, n_grp)
        tier_offsets = [0.55 * scale_y_unit, 1.20 * scale_y_unit, 1.85 * scale_y_unit]

        # Compute initial radial projections
        for idx, (_, grp_name, env) in enumerate(envelope_sort_items):
            scx, scy = env["scx"], env["scy"]
            space_verts = env["space_vertices"]

            display_text = grp_name
            name_len = len(display_text)

            half_w = max(0.24, name_len * 0.018) * scale_x_unit
            half_h = 0.095 * scale_y_unit

            target_angle = nominal_angles[idx]
            ux = np.cos(target_angle) * aspect_ratio
            uy = np.sin(target_angle)
            norm_u = np.hypot(ux, uy)
            ux, uy = ux / norm_u, uy / norm_u

            # Select the envelope vertex furthest along the ray direction as the arrow anchor
            best_anchor = max(space_verts, key=lambda v: (v[0] - scx) * ux + (v[1] - scy) * uy)

            # Project along ray to clear the entire global hull
            max_global_reach = 0.0
            for gv in global_hull_verts:
                reach = (gv[0] - cluster_cx) * ux + (gv[1] - cluster_cy) * uy
                if reach > max_global_reach:
                    max_global_reach = reach

            stagger_tier = tier_offsets[idx % 3]
            base_cand_x = cluster_cx + ux * (max_global_reach + stagger_tier)
            base_cand_y = cluster_cy + uy * (max_global_reach + stagger_tier)

            cand_x = base_cand_x
            cand_y = base_cand_y
            step = 0.08 * scale_y_unit

            # Step outward radially until candidate label box clears all envelope bubbles
            while check_box_collision(cand_x, cand_y, half_w + 0.05 * scale_x_unit, half_h + 0.05 * scale_y_unit, all_mpl_polygons):
                cand_x += ux * step
                cand_y += uy * step

            tag_id = f"GRP_{grp_name}"
            group_label_requests.append({
                "grp_name": grp_name,
                "display_text": display_text,
                "tag_id": tag_id,
                "color": env["color"],
                "scx": scx,
                "scy": scy,
                "cx": cand_x,
                "cy": cand_y,
                "half_w": half_w,
                "half_h": half_h,
                "space_verts": space_verts,
                "anchor": best_anchor,
                "ux": ux,
                "uy": uy
            })

        # Multi-body iterative collision resolution (relaxation passes)
        for _ in range(60):
            moved = False
            for i in range(n_grp):
                for j in range(i + 1, n_grp):
                    a = group_label_requests[i]
                    b = group_label_requests[j]

                    dx = abs(b["cx"] - a["cx"])
                    dy = abs(b["cy"] - a["cy"])
                    min_sep_x = a["half_w"] + b["half_w"] + 0.06 * scale_x_unit
                    min_sep_y = a["half_h"] + b["half_h"] + 0.05 * scale_y_unit

                    if dx < min_sep_x and dy < min_sep_y:
                        moved = True
                        dist_a = np.hypot(a["cx"] - cluster_cx, a["cy"] - cluster_cy)
                        dist_b = np.hypot(b["cx"] - cluster_cx, b["cy"] - cluster_cy)
                        if dist_b >= dist_a:
                            b["cx"] += b["ux"] * 0.20 * scale_y_unit
                            b["cy"] += b["uy"] * 0.20 * scale_y_unit
                        else:
                            a["cx"] += a["ux"] * 0.20 * scale_y_unit
                            a["cy"] += a["uy"] * 0.20 * scale_y_unit
            if not moved:
                break

        # Render group annotations
        for req in group_label_requests:
            grp_name = req["grp_name"]
            display_text = req["display_text"]
            tag_id = req["tag_id"]
            half_w = req["half_w"]
            half_h = req["half_h"]
            space_verts = req["space_verts"]

            custom_text = None
            custom_anchor = None
            if manual_positions and tag_id in manual_positions:
                pos_data = manual_positions[tag_id]
                if isinstance(pos_data, dict):
                    custom_text = pos_data.get("text")
                    custom_anchor = pos_data.get("anchor")
                elif isinstance(pos_data, (list, tuple)):
                    if len(pos_data) >= 2:
                        custom_text = (pos_data[0], pos_data[1])
                    if len(pos_data) == 4:
                        custom_anchor = (pos_data[2], pos_data[3])

            if custom_text:
                final_x = to_space(custom_text[0], x_scale_log)
                final_y = to_space(custom_text[1], y_scale_log)
                tx = custom_text[0]
                ty = custom_text[1]
            else:
                final_x = req["cx"]
                final_y = req["cy"]
                tx = from_space(final_x, x_scale_log)
                ty = from_space(final_y, y_scale_log)

            if custom_anchor:
                ax0 = custom_anchor[0]
                ay0 = custom_anchor[1]
            else:
                vx = final_x - req["scx"]
                vy = final_y - req["scy"]
                norm_v = np.hypot(vx, vy)
                if norm_v > 1e-4:
                    ux, uy = vx / norm_v, vy / norm_v
                    best_anchor = max(space_verts, key=lambda v: (v[0] - req["scx"]) * ux + (v[1] - req["scy"]) * uy)
                else:
                    best_anchor = req["anchor"]

                ax0 = from_space(best_anchor[0], x_scale_log)
                ay0 = from_space(best_anchor[1], y_scale_log)

            placed_boxes_global.append((final_x, final_y, half_w, half_h))

            ann = ax.annotate(
                display_text, xy=(ax0, ay0), xytext=(tx, ty),
                ha="center", va="center",
                weight="bold", fontsize=8.5, color=fg_color,
                bbox=dict(boxstyle="round,pad=0.28", facecolor=class_bg, edgecolor=req["color"], alpha=0.96),
                arrowprops=dict(
                    arrowstyle="->", color=arrow_color, lw=1.1,
                    shrinkA=0.0, shrinkB=0.0
                ),
                picker=True
            )
            ann.tag_id = tag_id
            ann.is_class_tag = True
            ann.space_verts = space_verts
            ann.x_scale_log = x_scale_log
            ann.y_scale_log = y_scale_log
            annotation_objects.append(ann)
            all_label_extents.append((final_x, final_y, half_w, half_h))

    # 4. Individual Material Tags
    tags_by_group = {}
    for item in tags_to_draw:
        tags_by_group.setdefault(item[1], []).append(item)

    for grp_name, m_items in tags_by_group.items():
        scx, scy = group_centroids.get(grp_name, (0.0, 0.0))
        tag_requests = []

        for m_name, _, xv, yv in m_items:
            sp_x = to_space(xv, x_scale_log)
            sp_y = to_space(yv, y_scale_log)

            dx = sp_x - scx
            dy = sp_y - scy
            ang = np.arctan2(dy, dx)

            display_m_text = m_name
            name_len_m = len(display_m_text)
            hw = max(0.20, name_len_m * 0.016) * scale_x_unit
            hh = 0.085 * scale_y_unit

            tag_requests.append({
                'name': m_name,
                'display_text': display_m_text,
                'xv': xv,
                'yv': yv,
                'space_x': sp_x,
                'space_y': sp_y,
                'angle': ang,
                'half_w': hw,
                'half_h': hh
            })

        for st in tag_requests:
            ang = st['angle']
            r_dist = 0.45 * scale_y_unit
            cx_sp = st['space_x'] + np.cos(ang) * r_dist
            cy_sp = st['space_y'] + np.sin(ang) * r_dist

            m_name = st['name']
            tag_id = f"MAT_{m_name}"

            custom_text = None
            custom_anchor = None
            if manual_positions and tag_id in manual_positions:
                pos_data = manual_positions[tag_id]
                if isinstance(pos_data, dict):
                    custom_text = pos_data.get("text")
                    custom_anchor = pos_data.get("anchor")
                elif isinstance(pos_data, (list, tuple)):
                    if len(pos_data) >= 2:
                        custom_text = (pos_data[0], pos_data[1])
                    if len(pos_data) == 4:
                        custom_anchor = (pos_data[2], pos_data[3])

            if custom_text:
                tx, ty = custom_text[0], custom_text[1]
                final_x = to_space(tx, x_scale_log)
                final_y = to_space(ty, y_scale_log)
            else:
                final_x = cx_sp
                final_y = cy_sp
                tx = from_space(final_x, x_scale_log)
                ty = from_space(final_y, y_scale_log)

            if custom_anchor:
                ax0, ay0 = custom_anchor[0], custom_anchor[1]
            else:
                ax0, ay0 = st['xv'], st['yv']

            xv = st['xv']
            yv = st['yv']

            if glow_enabled:
                ax.scatter(xv, yv, color="#FF0055", s=100, alpha=0.25, edgecolors="none", zorder=5)
            ax.scatter(xv, yv, color="#FF2255", s=40, edgecolors="white" if is_dark else "black", zorder=6)

            ann = ax.annotate(
                st['display_text'], xy=(ax0, ay0), xytext=(tx, ty),
                ha="center", va="center",
                fontsize=8.0, weight="bold", color=fg_color, zorder=7,
                bbox=dict(boxstyle="square,pad=0.25", facecolor=tag_bg, edgecolor=tag_edge, alpha=0.96),
                arrowprops=dict(
                    arrowstyle="->", color=arrow_color, lw=0.9,
                    shrinkA=0.0, shrinkB=0.0
                ),
                picker=True
            )
            ann.tag_id = tag_id
            ann.is_class_tag = False
            ann.space_verts = None
            ann.x_scale_log = x_scale_log
            ann.y_scale_log = y_scale_log
            annotation_objects.append(ann)
            all_label_extents.append((final_x, final_y, st['half_w'], st['half_h']))

    # 5. Performance Guide Lines
    if options.get("show_guideline", False) and all_x and all_y:
        n = options.get("guideline_slope_val")
        if n is not None:
            min_x, max_x = min(all_x), max(all_x)
            min_y, max_y = min(all_y), max(all_y)
            # Find geometric midpoint on log-scale or arithmetic midpoint on linear scale
            mid_x = np.sqrt(min_x * max_x) if (x_scale_log and min_x > 0) else (min_x + max_x) / 2.0
            mid_y = np.sqrt(min_y * max_y) if (y_scale_log and min_y > 0) else (min_y + max_y) / 2.0

            # Solve constant C in y = C * x^n
            c_val = mid_y / (max(mid_x, 1e-12) ** n)
            line_x = np.geomspace(min_x, max_x, 150) if (x_scale_log and min_x > 0) else np.linspace(min_x, max_x, 150)
            line_y = c_val * (line_x ** n)
            valid = (line_y >= min_y * 0.1) & (line_y <= max_y * 10)
            if np.any(valid):
                if glow_enabled:
                    ax.plot(line_x[valid], line_y[valid], color=fg_color, linestyle="-", linewidth=4.0, alpha=0.15)
                ax.plot(line_x[valid], line_y[valid], color=fg_color, linestyle="-.", linewidth=1.5,
                        label=f"Guide: Slope {n}")

    # 6. Chart Titles and Axes Labels
    x_label = AXIS_MATH_LABELS.get(options['x_prop'], options['x_prop'])
    y_label = AXIS_MATH_LABELS.get(options['y_prop'], options['y_prop'])

    ax.grid(True, which="both", ls=":", color=grid_color, alpha=0.75)
    title_prefix = "Dual Class + Subclass" if grouping_level == "both" else ("Subclass Grouping" if grouping_level == "subclass" else "Class Grouping")
    ax.set_title(f"Material Selection Chart ({title_prefix}): {y_label} vs. {x_label}", weight="normal", fontsize=11.5, color=fg_color)
    ax.set_xlabel(x_label, weight="normal", fontsize=10.0, color=fg_color)
    ax.set_ylabel(y_label, weight="normal", fontsize=10.0, color=fg_color)
    ax.tick_params(colors=fg_color, which="both")

    for spine in ax.spines.values():
        spine.set_color(grid_color if is_dark else fg_color)

    # 7. Global Viewport Auto-Zoom
    # Expands axis limits to contain all data points and outer callout label bounding boxes
    if all_x and all_y:
        all_space_x = [to_space(x, x_scale_log) for x in all_x]
        all_space_y = [to_space(y, y_scale_log) for y in all_y]

        for scx, scy, hw, hh in all_label_extents:
            all_space_x.extend([scx - hw - 0.18 * scale_x_unit, scx + hw + 0.18 * scale_x_unit])
            all_space_y.extend([scy - hh - 0.18 * scale_y_unit, scy + hh + 0.18 * scale_y_unit])

        min_sx, max_sx = min(all_space_x), max(all_space_x)
        min_sy, max_sy = min(all_space_y), max(all_space_y)

        span_x = max_sx - min_sx
        span_y = max_sy - min_sy

        pad_x = max(span_x * 0.16, 0.32 * scale_x_unit)
        pad_y = max(span_y * 0.16, 0.32 * scale_y_unit)

        target_min_x = from_space(min_sx - pad_x, x_scale_log)
        target_max_x = from_space(max_sx + pad_x, x_scale_log)
        target_min_y = from_space(min_sy - pad_y, y_scale_log)
        target_max_y = from_space(max_sy + pad_y, y_scale_log)

        if x_scale_log:
            target_min_x = max(target_min_x, 1e-12)
        else:
            target_min_x = max(0.0, target_min_x)

        if y_scale_log:
            target_min_y = max(target_min_y, 1e-12)
        else:
            target_min_y = max(0.0, target_min_y)

        ax.set_xlim(target_min_x, target_max_x)
        ax.set_ylim(target_min_y, target_max_y)

    coords_map = {k: v[0] for k, v in plotted_coords.items()}
    return coords_map, annotation_objects
