"""
Comprehensive Global Engineering Material Dataset.
Includes regional designations:
  - North America: AISI, ASTM, SAE, AMS
  - Europe: EN, DIN Werkstoff-Nr., ISO
  - Japan: JIS
  - China: GB/T
  - Korea: KS

Format:
(
    material_name, category, subclass, source,
    density [g/cm³], youngs_modulus [GPa], yield_strength [MPa],
    tensile_strength [MPa], fracture_toughness [MPa·m^0.5], loss_coefficient [η],
    thermal_conductivity [W/m·K], specific_heat [J/kg·K], thermal_expansion [10^-6/K],
    max_service_temp [°C], cost_per_kg [$/kg]
)
"""

DEFAULT_MATERIALS = [
    # =========================================================================
    # 1. FERROUS METALS
    # =========================================================================
    # Subclass: Low Carbon Steel
    ("AISI 1006 Low Carbon Steel", "Ferrous Metals", "Low Carbon Steel", "ASM Handbook Vol 1: Carbon Steels", 7.87, 205.0, 170.0, 330.0, 120.0, 0.0003, 52.0, 480.0, 12.0, 400.0, 0.85),
    ("AISI 1018 Cold Drawn", "Ferrous Metals", "Low Carbon Steel", "ASTM A108 / MatWeb", 7.87, 205.0, 370.0, 440.0, 80.0, 0.0003, 51.9, 486.0, 11.9, 400.0, 0.90),
    ("ASTM A36 Structural Plate", "Ferrous Metals", "Low Carbon Steel", "ASTM A36 / AISC Manual", 7.85, 200.0, 250.0, 400.0, 90.0, 0.0004, 51.0, 480.0, 12.0, 400.0, 0.80),
    ("EN S235JR (1.0038) Structural", "Ferrous Metals", "Low Carbon Steel", "EN 10025-2 / DIN 1.0038", 7.85, 210.0, 235.0, 360.0, 95.0, 0.0004, 52.0, 475.0, 12.0, 400.0, 0.82),
    ("EN S355J2 (1.0577) Heavy Plate", "Ferrous Metals", "Low Carbon Steel", "EN 10025-2 / DIN 1.0577", 7.85, 210.0, 355.0, 510.0, 85.0, 0.0003, 50.0, 475.0, 12.0, 420.0, 0.92),
    ("EN DC01 (1.0330) Cold Rolled", "Ferrous Metals", "Low Carbon Steel", "EN 10130 / DIN 1.0330 Sheet", 7.85, 205.0, 240.0, 370.0, 110.0, 0.0003, 53.0, 480.0, 11.9, 380.0, 0.90),
    ("JIS SS400 General Structural", "Ferrous Metals", "Low Carbon Steel", "JIS G 3101 Standard Spec", 7.85, 200.0, 245.0, 400.0, 90.0, 0.0004, 51.0, 480.0, 12.0, 400.0, 0.82),
    ("JIS SPCC Commercial Cold Rolled", "Ferrous Metals", "Low Carbon Steel", "JIS G 3141 Steel Sheet", 7.86, 205.0, 220.0, 340.0, 105.0, 0.0003, 52.5, 480.0, 12.0, 380.0, 0.88),
    ("GB/T Q235B Standard Structural", "Ferrous Metals", "Low Carbon Steel", "GB/T 700-2006 Standard", 7.85, 200.0, 235.0, 370.0, 95.0, 0.0004, 51.0, 480.0, 12.0, 400.0, 0.78),
    ("GB/T Q195 Stamping Strip", "Ferrous Metals", "Low Carbon Steel", "GB/T 700-2006 Standard", 7.86, 205.0, 195.0, 315.0, 120.0, 0.0003, 53.0, 480.0, 12.0, 380.0, 0.75),
    ("KS SS275 Structural Grade", "Ferrous Metals", "Low Carbon Steel", "KS D 3503 Structural Spec", 7.85, 205.0, 275.0, 410.0, 90.0, 0.0004, 51.0, 480.0, 12.0, 400.0, 0.84),

    # Subclass: Medium Carbon Steel
    ("AISI 1045 Normalized", "Ferrous Metals", "Medium Carbon Steel", "ASM Handbook Vol 1", 7.85, 206.0, 380.0, 625.0, 60.0, 0.0004, 49.8, 486.0, 11.5, 450.0, 0.95),
    ("EN C45E (1.1191) Engineering", "Ferrous Metals", "Medium Carbon Steel", "EN 10083-2 / DIN 1.1191", 7.85, 210.0, 430.0, 650.0, 58.0, 0.0004, 49.0, 480.0, 11.6, 450.0, 0.98),
    ("JIS S45C Machinery Carbon", "Ferrous Metals", "Medium Carbon Steel", "JIS G 4051 Carbon Steel", 7.85, 206.0, 390.0, 640.0, 60.0, 0.0004, 49.5, 485.0, 11.5, 450.0, 0.96),
    ("GB/T 45# High Quality Carbon", "Ferrous Metals", "Medium Carbon Steel", "GB/T 699-2015 Machinery", 7.85, 206.0, 355.0, 600.0, 62.0, 0.0004, 49.8, 486.0, 11.5, 450.0, 0.88),
    ("KS SM45C Machinery Shaft", "Ferrous Metals", "Medium Carbon Steel", "KS D 3752 Carbon Steel", 7.85, 206.0, 390.0, 640.0, 60.0, 0.0004, 49.5, 485.0, 11.5, 450.0, 0.95),

    # Subclass: High Carbon & Spring Steel
    ("AISI 1095 High Carbon Spring", "Ferrous Metals", "High Carbon & Spring Steel", "ASTM A684 / MatWeb", 7.84, 205.0, 520.0, 830.0, 25.0, 0.0004, 47.0, 460.0, 10.8, 400.0, 1.20),
    ("EN 51CrV4 (1.8159) Spring Steel", "Ferrous Metals", "High Carbon & Spring Steel", "EN 10089 / DIN 1.8159 Spec", 7.85, 210.0, 1100.0, 1350.0, 38.0, 0.0003, 44.0, 470.0, 11.5, 420.0, 1.85),
    ("JIS SUP9 Laminated Spring Steel", "Ferrous Metals", "High Carbon & Spring Steel", "JIS G 4801 Spring Steel", 7.85, 208.0, 1080.0, 1250.0, 36.0, 0.0003, 45.0, 470.0, 11.5, 400.0, 1.70),
    ("JIS SK85 (SK5) Carbon Tool/Spring", "Ferrous Metals", "High Carbon & Spring Steel", "JIS G 4401 Tool Steel", 7.84, 205.0, 490.0, 800.0, 32.0, 0.0004, 48.0, 470.0, 11.0, 400.0, 1.35),
    ("GB/T 65Mn Spring Steel Strip", "Ferrous Metals", "High Carbon & Spring Steel", "GB/T 1222 Spring Steels", 7.85, 205.0, 785.0, 980.0, 35.0, 0.0003, 46.0, 470.0, 11.2, 400.0, 1.25),

    # Subclass: Alloy Steel
    ("AISI 4140 Q&T 300HB", "Ferrous Metals", "Alloy Steel", "ASTM A29 / ASM Specialty", 7.85, 210.0, 655.0, 1020.0, 65.0, 0.0003, 42.6, 473.0, 12.3, 500.0, 1.95),
    ("EN 42CrMo4 (1.7225) Engineering", "Ferrous Metals", "Alloy Steel", "EN 10083-3 / DIN 1.7225", 7.85, 210.0, 750.0, 1000.0, 65.0, 0.0003, 42.0, 475.0, 12.2, 500.0, 2.10),
    ("EN 34CrNiMo6 (1.6582) Heavy Duty", "Ferrous Metals", "Alloy Steel", "EN 10083-3 / DIN 1.6582", 7.85, 210.0, 800.0, 1100.0, 70.0, 0.0003, 38.0, 475.0, 12.0, 520.0, 2.80),
    ("EN 100Cr6 (1.3505) Bearing Steel", "Ferrous Metals", "Alloy Steel", "EN ISO 683-17 / DIN 1.3505", 7.81, 210.0, 1700.0, 2100.0, 18.0, 0.0002, 46.0, 475.0, 11.9, 200.0, 2.45),
    ("JIS SCM440 Chromium Molybdenum", "Ferrous Metals", "Alloy Steel", "JIS G 4053 Cr-Mo Steel", 7.85, 210.0, 700.0, 1000.0, 65.0, 0.0003, 42.5, 475.0, 12.2, 500.0, 1.95),
    ("JIS SUJ2 High Carbon Bearing", "Ferrous Metals", "Alloy Steel", "JIS G 4805 Bearing Steel", 7.81, 210.0, 1700.0, 2100.0, 18.0, 0.0002, 46.5, 475.0, 11.9, 200.0, 2.35),
    ("GB/T 42CrMo Heavy Machinery", "Ferrous Metals", "Alloy Steel", "GB/T 3077 Alloy Steel", 7.85, 210.0, 700.0, 980.0, 65.0, 0.0003, 42.0, 475.0, 12.2, 500.0, 1.80),
    ("GB/T 20CrMnTi Carburized Gear", "Ferrous Metals", "Alloy Steel", "GB/T 3077 Gear Steel", 7.85, 205.0, 835.0, 1080.0, 68.0, 0.0003, 44.0, 470.0, 12.1, 480.0, 1.75),
    ("GB/T GCr15 Standard Bearing", "Ferrous Metals", "Alloy Steel", "GB/T 18254 Bearing Spec", 7.81, 210.0, 1680.0, 2050.0, 18.0, 0.0002, 46.2, 475.0, 11.9, 200.0, 2.10),
    ("KS SCM440 Structural Shaft", "Ferrous Metals", "Alloy Steel", "KS D 3711 Cr-Mo Steel", 7.85, 210.0, 700.0, 1000.0, 65.0, 0.0003, 42.5, 475.0, 12.2, 500.0, 1.95),

    # Subclass: Ultra-High Strength Steel (UHSS & AHSS)
    ("Maraging 300 (Vascomax 300)", "Ferrous Metals", "Ultra-High Strength Steel", "MIL-HDBK-5J / Teledyne Vasco", 8.00, 190.0, 2000.0, 2060.0, 45.0, 0.0002, 25.5, 450.0, 10.1, 450.0, 35.00),
    ("AerMet 100 Ultra-High Toughness", "Ferrous Metals", "Ultra-High Strength Steel", "Carpenter Technology Specs", 7.89, 194.0, 1720.0, 1965.0, 115.0, 0.0002, 28.0, 460.0, 10.8, 425.0, 45.00),
    ("300M Modified 4340 Aircraft", "Ferrous Metals", "Ultra-High Strength Steel", "MIL-S-8844 / AMS 6419", 7.85, 205.0, 1680.0, 2000.0, 55.0, 0.0003, 38.0, 470.0, 11.7, 450.0, 8.50),
    ("Hardox 500 Extreme Wear Plate", "Ferrous Metals", "Ultra-High Strength Steel", "SSAB Hardox Product Sheet", 7.85, 210.0, 1250.0, 1550.0, 35.0, 0.0003, 44.0, 480.0, 11.5, 250.0, 3.20),
    ("EN S890QL (1.8983) High Yield", "Ferrous Metals", "Ultra-High Strength Steel", "EN 10025-6 Structural Quenched", 7.85, 210.0, 890.0, 980.0, 60.0, 0.0003, 40.0, 470.0, 11.8, 450.0, 3.40),
    ("POSCO DP780 Dual Phase Auto", "Ferrous Metals", "Ultra-High Strength Steel", "POSCO Automotive Steel Guide", 7.85, 210.0, 480.0, 800.0, 55.0, 0.0004, 46.0, 480.0, 12.0, 350.0, 1.45),
    ("Baosteel MS1180 Martensitic Auto", "Ferrous Metals", "Ultra-High Strength Steel", "Baosteel Auto Sheet Manual", 7.85, 205.0, 950.0, 1200.0, 38.0, 0.0003, 43.0, 475.0, 11.8, 300.0, 1.65),

    # Subclass: Tool Steel
    ("Tool Steel D2 Wear Resistant", "Ferrous Metals", "Tool Steel", "ASTM A681 / Bohler D2", 7.70, 210.0, 1600.0, 2200.0, 18.0, 0.0002, 20.0, 460.0, 10.4, 450.0, 6.00),
    ("Tool Steel M2 High Speed", "Ferrous Metals", "Tool Steel", "ASTM A600 High Speed Steel", 8.16, 220.0, 2200.0, 3250.0, 16.0, 0.0002, 24.0, 440.0, 10.0, 550.0, 8.50),
    ("Tool Steel H13 Hot Work", "Ferrous Metals", "Tool Steel", "NADCA 207 Die Casting Spec", 7.80, 210.0, 1650.0, 1990.0, 28.0, 0.0003, 28.6, 460.0, 10.4, 600.0, 6.20),
    ("Tool Steel S7 Shock Resistant", "Ferrous Metals", "Tool Steel", "ASTM A681 / Finkl S7", 7.83, 207.0, 1520.0, 1900.0, 35.0, 0.0003, 28.0, 460.0, 11.2, 500.0, 5.80),
    ("Tool Steel W1 Water Hardening", "Ferrous Metals", "Tool Steel", "ASTM A681 Carbon Tool Steel", 7.85, 210.0, 650.0, 820.0, 20.0, 0.0003, 44.0, 470.0, 11.5, 300.0, 3.80),
    ("Tool Steel CPM 3V Powder Metal", "Ferrous Metals", "Tool Steel", "Crucible Industries CPM 3V", 7.80, 220.0, 1860.0, 2100.0, 42.0, 0.0002, 23.0, 460.0, 11.0, 550.0, 14.50),
    ("Tool Steel M42 Cobalt High-Speed", "Ferrous Metals", "Tool Steel", "ASTM A600 Cobalt HSS", 8.15, 225.0, 2400.0, 3400.0, 14.0, 0.0002, 22.0, 430.0, 10.2, 580.0, 16.00),
    ("EN 1.2379 (X153CrMoV12) Cold Work", "Ferrous Metals", "Tool Steel", "EN ISO 4957 / DIN 1.2379", 7.70, 210.0, 1650.0, 2200.0, 18.0, 0.0002, 20.5, 460.0, 10.5, 450.0, 6.20),
    ("EN 1.2344 (X40CrMoV5-1) Hot Die", "Ferrous Metals", "Tool Steel", "EN ISO 4957 / DIN 1.2344", 7.80, 210.0, 1650.0, 1990.0, 28.0, 0.0003, 28.5, 460.0, 10.5, 600.0, 6.40),
    ("JIS SKD11 Cold Work Die Steel", "Ferrous Metals", "Tool Steel", "JIS G 4404 Alloy Tool Steel", 7.70, 210.0, 1600.0, 2200.0, 18.0, 0.0002, 20.0, 460.0, 10.4, 450.0, 5.80),
    ("JIS SKD61 Hot Work Die Steel", "Ferrous Metals", "Tool Steel", "JIS G 4404 Alloy Tool Steel", 7.80, 210.0, 1600.0, 1980.0, 28.0, 0.0003, 28.0, 460.0, 10.4, 600.0, 6.10),
    ("GB/T Cr12MoV Cold Work Die", "Ferrous Metals", "Tool Steel", "GB/T 1299 Tool Steels", 7.70, 210.0, 1580.0, 2150.0, 18.0, 0.0002, 20.0, 460.0, 10.4, 450.0, 4.90),

    # Subclass: Stainless Steel
    ("Stainless 304 Annealed Sheet", "Ferrous Metals", "Stainless Steel", "ASTM A240 / ASM Stainless", 7.93, 193.0, 215.0, 505.0, 150.0, 0.0005, 16.2, 500.0, 17.3, 800.0, 3.80),
    ("Stainless 17-4 PH H900 Aged", "Ferrous Metals", "Stainless Steel", "AMS 5643 / Armco 17-4PH", 7.78, 196.0, 1170.0, 1310.0, 75.0, 0.0003, 17.8, 460.0, 10.8, 350.0, 7.50),
    ("EN 1.4301 (X5CrNi18-10) 304", "Ferrous Metals", "Stainless Steel", "EN 10088-2 / DIN 1.4301", 7.93, 200.0, 230.0, 540.0, 150.0, 0.0005, 15.0, 500.0, 16.0, 800.0, 3.90),
    ("EN 1.4404 (X2CrNiMo17-12-2) 316L", "Ferrous Metals", "Stainless Steel", "EN 10088-2 / DIN 1.4404", 8.00, 200.0, 240.0, 560.0, 140.0, 0.0005, 15.0, 500.0, 16.0, 800.0, 5.30),
    ("EN 1.4462 (X2CrNiMoN22-5-3) 2205", "Ferrous Metals", "Stainless Steel", "EN 10088-2 Duplex Stainless", 7.80, 200.0, 480.0, 700.0, 100.0, 0.0004, 19.0, 480.0, 13.0, 300.0, 6.20),
    ("JIS SUS304 Standard Austenitic", "Ferrous Metals", "Stainless Steel", "JIS G 4303 Stainless Bar", 7.93, 193.0, 205.0, 520.0, 150.0, 0.0005, 16.3, 500.0, 17.3, 800.0, 3.85),
    ("JIS SUS316 Marine Corrosion", "Ferrous Metals", "Stainless Steel", "JIS G 4303 Stainless Steel", 8.00, 193.0, 240.0, 550.0, 140.0, 0.0005, 16.3, 500.0, 16.0, 800.0, 5.25),
    ("GB/T 06Cr19Ni10 Standard 304", "Ferrous Metals", "Stainless Steel", "GB/T 20878-2007 Stainless", 7.93, 193.0, 205.0, 520.0, 150.0, 0.0005, 16.2, 500.0, 17.3, 800.0, 3.40),
    ("GB/T 022Cr17Ni12Mo2 Low-C 316L", "Ferrous Metals", "Stainless Steel", "GB/T 20878-2007 Stainless", 8.00, 193.0, 220.0, 530.0, 140.0, 0.0005, 16.0, 500.0, 16.0, 800.0, 4.80),
    ("KS STS304 Austenitic Sheet", "Ferrous Metals", "Stainless Steel", "KS D 3705 Stainless Steel", 7.93, 193.0, 205.0, 520.0, 150.0, 0.0005, 16.3, 500.0, 17.3, 800.0, 3.80),

    # Subclass: Cast Iron
    ("Gray Cast Iron Class 30", "Ferrous Metals", "Cast Iron", "ASTM A48 / AFS Handbook", 7.22, 110.0, 190.0, 214.0, 14.0, 0.0025, 50.0, 485.0, 10.8, 450.0, 0.78),
    ("Ductile Iron 65-45-12 Annealed", "Ferrous Metals", "Cast Iron", "ASTM A536 / Ductile Iron Soc", 7.10, 169.0, 310.0, 448.0, 38.0, 0.0009, 36.0, 500.0, 11.5, 500.0, 1.15),
    ("ADI Austempered Ductile Iron Gr 1", "Ferrous Metals", "Cast Iron", "ASTM A897 Standards", 7.10, 170.0, 850.0, 1200.0, 50.0, 0.0006, 30.0, 510.0, 12.0, 350.0, 1.90),
    ("EN-GJL-250 (GG-25) Gray Iron", "Ferrous Metals", "Cast Iron", "EN 1561 / DIN 1691 Flake Iron", 7.20, 115.0, 180.0, 250.0, 15.0, 0.0025, 48.0, 490.0, 11.0, 450.0, 0.85),
    ("EN-GJS-400-15 (GGG-40) Ductile", "Ferrous Metals", "Cast Iron", "EN 1563 / DIN 1693 Spheroidal", 7.10, 169.0, 250.0, 400.0, 42.0, 0.0009, 36.0, 500.0, 12.0, 500.0, 1.25),
    ("JIS FC250 Machinery Gray Cast", "Ferrous Metals", "Cast Iron", "JIS G 5501 Gray Iron Castings", 7.20, 115.0, 180.0, 250.0, 15.0, 0.0025, 48.0, 490.0, 11.0, 450.0, 0.82),
    ("JIS FCD500-7 Ductile Cast Iron", "Ferrous Metals", "Cast Iron", "JIS G 5502 Spheroidal Iron", 7.10, 168.0, 320.0, 500.0, 36.0, 0.0008, 35.0, 500.0, 11.8, 500.0, 1.20),
    ("GB/T HT250 Gray Iron Casting", "Ferrous Metals", "Cast Iron", "GB/T 9439 Gray Iron Standards", 7.20, 115.0, 175.0, 250.0, 15.0, 0.0025, 48.0, 490.0, 11.0, 450.0, 0.72),
    ("GB/T QT500-7 Nodular Ductile", "Ferrous Metals", "Cast Iron", "GB/T 1348 Spheroidal Iron", 7.10, 168.0, 320.0, 500.0, 36.0, 0.0008, 35.0, 500.0, 11.8, 500.0, 1.10),

    # =========================================================================
    # 2. NON-FERROUS METALS
    # =========================================================================
    # Subclass: Aluminum Alloy
    ("Aluminum 6061-T6 Extrusion", "Non-Ferrous Metals", "Aluminum Alloy", "ASTM B221 / AA Standards", 2.70, 68.9, 276.0, 310.0, 29.0, 0.0002, 167.0, 896.0, 23.4, 150.0, 3.40),
    ("Aluminum 7075-T6 High Strength", "Non-Ferrous Metals", "Aluminum Alloy", "AMS 4045 / Kaiser Aluminum", 2.81, 71.7, 503.0, 572.0, 26.0, 0.0002, 130.0, 960.0, 23.6, 120.0, 7.20),
    ("Aluminum 2024-T3 Aerospace", "Non-Ferrous Metals", "Aluminum Alloy", "MIL-HDBK-5J / Alcoa Data", 2.78, 73.1, 345.0, 483.0, 36.0, 0.0002, 121.0, 875.0, 23.2, 130.0, 5.40),
    ("EN AW-6082-T6 Structural Marine", "Non-Ferrous Metals", "Aluminum Alloy", "EN 573-3 / DIN 3.2315", 2.70, 70.0, 260.0, 310.0, 30.0, 0.0002, 170.0, 890.0, 23.1, 150.0, 3.60),
    ("EN AW-5083-H111 Ship Plate", "Non-Ferrous Metals", "Aluminum Alloy", "EN 573-3 / DIN 3.3547 Marine", 2.66, 71.0, 145.0, 290.0, 34.0, 0.0002, 120.0, 900.0, 24.2, 130.0, 3.90),
    ("JIS A5052-H32 Sheet Wrought", "Non-Ferrous Metals", "Aluminum Alloy", "JIS H 4000 Aluminum Sheet", 2.68, 70.0, 195.0, 240.0, 32.0, 0.0002, 138.0, 880.0, 23.8, 160.0, 3.50),
    ("JIS A7075-T6 Aircraft Duralumin", "Non-Ferrous Metals", "Aluminum Alloy", "JIS H 4000 High Strength", 2.81, 71.7, 500.0, 570.0, 26.0, 0.0002, 130.0, 960.0, 23.6, 120.0, 7.40),
    ("GB/T 6061-T6 Extruded Profile", "Non-Ferrous Metals", "Aluminum Alloy", "GB/T 3190 Aluminum Standard", 2.70, 68.9, 275.0, 310.0, 29.0, 0.0002, 167.0, 896.0, 23.4, 150.0, 3.10),
    ("GB/T 2A12-T4 Aircraft Duralumin", "Non-Ferrous Metals", "Aluminum Alloy", "GB/T 3190 / Former LY12", 2.78, 72.0, 325.0, 470.0, 34.0, 0.0002, 120.0, 880.0, 23.2, 130.0, 5.10),

    # Subclass: Copper & Brass
    ("Copper C11000 Electrolytic Tough", "Non-Ferrous Metals", "Copper & Brass", "CDA Standards / ASTM B152", 8.94, 115.0, 69.0, 220.0, 75.0, 0.0001, 388.0, 385.0, 17.0, 200.0, 9.80),
    ("Copper C17200 Beryllium Aged", "Non-Ferrous Metals", "Copper & Brass", "Materion Alloy 25 Specs", 8.25, 131.0, 1100.0, 1280.0, 30.0, 0.0002, 105.0, 420.0, 17.5, 200.0, 38.00),
    ("EN CW614N (CuZn39Pb3) Brass", "Non-Ferrous Metals", "Copper & Brass", "EN 12164 / DIN 2.0401 Brass", 8.44, 96.0, 250.0, 430.0, 45.0, 0.0003, 113.0, 380.0, 20.2, 150.0, 7.60),
    ("EN CW004A (Cu-ETP) Pure", "Non-Ferrous Metals", "Copper & Brass", "EN 13601 Copper Rod/Bar", 8.94, 118.0, 100.0, 250.0, 75.0, 0.0001, 390.0, 385.0, 16.8, 200.0, 9.90),
    ("JIS C3604 Free Cutting Brass", "Non-Ferrous Metals", "Copper & Brass", "JIS H 3250 Brass Bar", 8.50, 97.0, 300.0, 410.0, 48.0, 0.0003, 115.0, 380.0, 20.5, 150.0, 7.50),
    ("JIS C1100 Pure Tough Pitch", "Non-Ferrous Metals", "Copper & Brass", "JIS H 3100 Copper Sheet", 8.94, 115.0, 70.0, 225.0, 75.0, 0.0001, 390.0, 385.0, 17.0, 200.0, 9.70),
    ("GB/T H62 Structural Brass Plate", "Non-Ferrous Metals", "Copper & Brass", "GB/T 5231 Copper Alloys", 8.43, 105.0, 160.0, 390.0, 55.0, 0.0002, 120.0, 385.0, 19.9, 160.0, 7.10),
    ("GB/T HPb59-1 Leaded Machining", "Non-Ferrous Metals", "Copper & Brass", "GB/T 5231 Lead Brass", 8.45, 98.0, 280.0, 420.0, 46.0, 0.0003, 115.0, 380.0, 20.0, 150.0, 7.20),
    ("Phosphor Bronze C51000 Spring Grade", "Non-Ferrous Metals", "Copper & Brass", "ASTM B103 Phosphor Bronze", 8.86, 110.0, 480.0, 580.0, 45.0, 0.0002, 70.0, 380.0, 17.8, 150.0, 11.50),
    ("Aluminum Bronze C95400 Gear Cast", "Non-Ferrous Metals", "Copper & Brass", "ASTM B148 Al-Bronze Specs", 7.45, 110.0, 220.0, 585.0, 38.0, 0.0004, 38.0, 420.0, 16.2, 260.0, 12.00),
    ("Silicon Bronze C65500 Sheet", "Non-Ferrous Metals", "Copper & Brass", "ASTM B98 Silicon Bronze", 8.53, 105.0, 260.0, 480.0, 60.0, 0.0003, 36.0, 380.0, 18.0, 180.0, 10.80),
    ("Nickel Al Bronze C95800 Propeller", "Non-Ferrous Metals", "Copper & Brass", "MIL-B-24480 / ASTM B148", 7.64, 117.0, 280.0, 655.0, 42.0, 0.0003, 42.0, 440.0, 16.0, 260.0, 14.50),

    # Subclass: Titanium Alloy
    ("Titanium Ti-6Al-4V Grade 5", "Non-Ferrous Metals", "Titanium Alloy", "MIL-HDBK-5J / ASTM B265", 4.43, 114.0, 880.0, 950.0, 75.0, 0.0003, 6.7, 526.0, 8.6, 400.0, 34.00),
    ("Titanium Grade 2 Unalloyed", "Non-Ferrous Metals", "Titanium Alloy", "ASTM B348 / TIMET Grade 2", 4.51, 103.0, 275.0, 345.0, 75.0, 0.0004, 16.4, 523.0, 8.6, 315.0, 22.00),
    ("Titanium Ti-6Al-2Sn-4Zr-2Mo (Ti-6242)", "Non-Ferrous Metals", "Titanium Alloy", "TIMET / AMS 4919 High-Temp", 4.54, 114.0, 990.0, 1030.0, 60.0, 0.0003, 7.0, 520.0, 8.8, 540.0, 42.00),
    ("Titanium Ti-3Al-2.5V (Grade 9)", "Non-Ferrous Metals", "Titanium Alloy", "ASTM B338 Aircraft Tubing", 4.48, 105.0, 585.0, 690.0, 80.0, 0.0003, 8.3, 525.0, 8.8, 380.0, 36.00),
    ("Titanium Ti-5Al-2.5Sn (Grade 6)", "Non-Ferrous Metals", "Titanium Alloy", "ASTM B265 Cryogenic Spec", 4.48, 110.0, 780.0, 830.0, 75.0, 0.0003, 7.8, 525.0, 8.7, 480.0, 40.00),
    ("Titanium Ti-10V-2Fe-3Al Near-Beta", "Non-Ferrous Metals", "Titanium Alloy", "AMS 4983 Gear Forging", 4.65, 110.0, 1190.0, 1260.0, 48.0, 0.0003, 7.5, 515.0, 9.0, 315.0, 52.00),
    ("EN 3.7164 (Ti-6Al-4V) Aerospace", "Non-Ferrous Metals", "Titanium Alloy", "EN 3.7164 / ISO 5832-3", 4.43, 114.0, 890.0, 960.0, 75.0, 0.0003, 6.7, 525.0, 8.6, 400.0, 36.00),
    ("JIS Class 60 (Ti-6Al-4V) Bar", "Non-Ferrous Metals", "Titanium Alloy", "JIS H 4600 Titanium Bar", 4.43, 114.0, 880.0, 950.0, 75.0, 0.0003, 6.7, 526.0, 8.6, 400.0, 35.00),
    ("GB/T TC4 (Ti-6Al-4V) Aerospace", "Non-Ferrous Metals", "Titanium Alloy", "GB/T 2965 Titanium Alloys", 4.43, 114.0, 860.0, 940.0, 75.0, 0.0003, 6.7, 526.0, 8.6, 400.0, 30.00),
    ("GB/T TA2 Commercial Pure Ti", "Non-Ferrous Metals", "Titanium Alloy", "GB/T 3621 Pure Titanium", 4.51, 103.0, 275.0, 370.0, 80.0, 0.0004, 16.0, 523.0, 8.6, 315.0, 20.00),

    # Subclass: Nickel Superalloy
    ("Inconel 718 Turbine Disc Grade", "Non-Ferrous Metals", "Nickel Superalloy", "AMS 5662 / Special Metals", 8.19, 211.0, 1100.0, 1375.0, 90.0, 0.0003, 11.4, 435.0, 13.0, 650.0, 36.00),
    ("Inconel 625 Marine Exhaust Alloy", "Non-Ferrous Metals", "Nickel Superalloy", "Special Metals INCONEL 625", 8.44, 208.0, 517.0, 930.0, 95.0, 0.0003, 9.8, 410.0, 12.8, 980.0, 32.00),
    ("Incoloy 800H Petrochemical Alloy", "Non-Ferrous Metals", "Nickel Superalloy", "Special Metals Incoloy 800H", 7.94, 196.0, 205.0, 520.0, 130.0, 0.0003, 11.5, 460.0, 14.4, 800.0, 26.00),
    ("Inconel X-750 Aged Spring Alloy", "Non-Ferrous Metals", "Nickel Superalloy", "Special Metals Inconel X-750", 8.28, 214.0, 860.0, 1240.0, 70.0, 0.0003, 12.0, 430.0, 12.6, 700.0, 34.00),
    ("Waspaloy Aero-Turbine Disc", "Non-Ferrous Metals", "Nickel Superalloy", "AMS 5708 / Haynes Waspaloy", 8.19, 213.0, 795.0, 1210.0, 80.0, 0.0003, 11.0, 440.0, 12.2, 760.0, 46.00),
    ("Haynes 230 Combustion Chamber", "Non-Ferrous Metals", "Nickel Superalloy", "Haynes International 230", 8.97, 211.0, 390.0, 860.0, 110.0, 0.0003, 8.9, 397.0, 12.7, 980.0, 44.00),
    ("Monel 400 Seawater Alloy", "Non-Ferrous Metals", "Nickel Superalloy", "Special Metals Monel 400", 8.80, 179.0, 240.0, 550.0, 150.0, 0.0003, 21.8, 427.0, 13.9, 480.0, 22.00),
    ("Hastelloy C-276 Severe Corrosion", "Non-Ferrous Metals", "Nickel Superalloy", "Haynes International C-276", 8.89, 205.0, 355.0, 790.0, 120.0, 0.0003, 10.2, 427.0, 11.2, 1000.0, 42.00),
    ("EN 2.4668 (NiCr19Fe19Nb5Mo3) 718", "Non-Ferrous Metals", "Nickel Superalloy", "DIN EN 10095 / W.Nr 2.4668", 8.19, 210.0, 1120.0, 1380.0, 90.0, 0.0003, 11.4, 435.0, 13.0, 650.0, 38.00),
    ("GB/T GH4169 Turbine Alloy (718)", "Non-Ferrous Metals", "Nickel Superalloy", "GB/T 14992 Superalloys", 8.19, 210.0, 1080.0, 1360.0, 90.0, 0.0003, 11.4, 435.0, 13.0, 650.0, 32.00),

    # Subclass: Magnesium Alloy
    ("Magnesium AZ31B Wrought Sheet", "Non-Ferrous Metals", "Magnesium Alloy", "ASTM B90 Standards", 1.77, 45.0, 200.0, 260.0, 22.0, 0.0015, 96.0, 1020.0, 26.0, 150.0, 4.20),
    ("Magnesium AZ91D Die Cast Housing", "Non-Ferrous Metals", "Magnesium Alloy", "ASTM B94 Die Cast Specs", 1.81, 45.0, 150.0, 230.0, 16.0, 0.0020, 72.0, 1050.0, 26.0, 120.0, 3.80),
    ("Magnesium WE43 High Temp Aero", "Non-Ferrous Metals", "Magnesium Alloy", "Magnesium Elektron WE43 Data", 1.84, 44.0, 165.0, 250.0, 18.0, 0.0018, 51.0, 960.0, 26.0, 250.0, 12.50),

    # Subclass: Refractory Metal
    ("Tungsten Pure Sintered Rod", "Non-Ferrous Metals", "Refractory Metal", "Plansee Tungsten Tech Guide", 19.25, 410.0, 750.0, 980.0, 5.0, 0.0001, 173.0, 134.0, 4.5, 1700.0, 45.00),
    ("Molybdenum Pure Sintered Sheet", "Non-Ferrous Metals", "Refractory Metal", "ASTM B386 / Plansee Moly", 10.22, 320.0, 500.0, 650.0, 25.0, 0.0002, 138.0, 250.0, 4.8, 1200.0, 48.00),
    ("Tantalum Pure Capacitor Grade", "Non-Ferrous Metals", "Refractory Metal", "ASTM B365 / Cabot Tantalum", 16.65, 186.0, 170.0, 240.0, 110.0, 0.0002, 57.5, 140.0, 6.5, 1400.0, 180.00),
    ("Niobium C-103 Rocket Nozzle Alloy", "Non-Ferrous Metals", "Refractory Metal", "ASTM B655 / Wah Chang C-103", 8.85, 105.0, 345.0, 480.0, 65.0, 0.0003, 42.0, 270.0, 7.2, 1350.0, 140.00),

    # =========================================================================
    # 3. POLYMERS
    # =========================================================================
    # Subclass: Commodity Thermoplastic
    ("ABS Standard Injection Grade", "Polymers", "Commodity Thermoplastic", "Sabic Cycolac Tech Sheets", 1.04, 2.2, 42.0, 45.0, 2.2, 0.03, 0.17, 1400.0, 90.0, 85.0, 2.30),
    ("HDPE High Density Blow Molded", "Polymers", "Commodity Thermoplastic", "Dow Chemical HDPE Specs", 0.95, 1.1, 26.0, 32.0, 2.4, 0.08, 0.48, 1900.0, 120.0, 80.0, 1.50),
    ("PP Polypropylene Homopolymer", "Polymers", "Commodity Thermoplastic", "LyondellBasell Profax", 0.90, 1.5, 33.0, 35.0, 2.2, 0.05, 0.22, 1800.0, 150.0, 100.0, 1.60),
    ("PVC Rigid Schedule 80 Pipe", "Polymers", "Commodity Thermoplastic", "Harvel Plastics PVC Guide", 1.40, 3.0, 45.0, 52.0, 2.1, 0.03, 0.16, 1050.0, 70.0, 60.0, 1.30),
    ("Polystyrene GPPS Transparent", "Polymers", "Commodity Thermoplastic", "Total Petrochemicals GPPS", 1.05, 3.2, 40.0, 45.0, 1.0, 0.02, 0.13, 1300.0, 70.0, 70.0, 1.50),

    # Subclass: Engineering Thermoplastic
    ("Polycarbonate Optical Clear", "Polymers", "Engineering Thermoplastic", "Covestro Makrolon 2805", 1.20, 2.3, 62.0, 70.0, 3.2, 0.02, 0.20, 1250.0, 65.0, 130.0, 3.80),
    ("Nylon 6/6 Industrial Bar", "Polymers", "Engineering Thermoplastic", "DuPont Zytel 101L Spec", 1.14, 3.0, 82.0, 85.0, 2.8, 0.04, 0.25, 1670.0, 80.0, 105.0, 3.60),
    ("POM Acetal Homopolymer Delrin", "Polymers", "Engineering Thermoplastic", "DuPont Delrin Design Guide", 1.42, 3.1, 69.0, 72.0, 2.7, 0.03, 0.37, 1500.0, 100.0, 90.0, 3.40),
    ("BASF Ultramid B3 (PA6) Europe", "Polymers", "Engineering Thermoplastic", "BASF Ultramid Technical Guide", 1.13, 2.8, 75.0, 80.0, 3.0, 0.04, 0.28, 1650.0, 85.0, 110.0, 3.50),
    ("Celanese Hostaform C9021 (POM-C)", "Polymers", "Engineering Thermoplastic", "Celanese Hostaform POM Manual", 1.41, 2.8, 65.0, 68.0, 2.8, 0.03, 0.31, 1500.0, 110.0, 100.0, 3.30),
    ("PMMA Acrylic Cast Sheet Clear", "Polymers", "Engineering Thermoplastic", "Rohm Plexiglas GS Specs", 1.18, 3.2, 65.0, 75.0, 1.6, 0.03, 0.19, 1450.0, 75.0, 85.0, 2.90),

    # Subclass: High Performance Polymer
    ("PTFE Virgin Teflon Fluoropolymer", "Polymers", "High Performance Polymer", "Chemours Teflon PTFE Data", 2.18, 0.50, 20.0, 30.0, 3.0, 0.08, 0.25, 1050.0, 120.0, 260.0, 14.50),
    ("PEEK Virgin Engineering Grade", "Polymers", "High Performance Polymer", "Victrex PEEK 450G Specs", 1.30, 3.8, 100.0, 105.0, 4.0, 0.01, 0.25, 1340.0, 45.0, 250.0, 75.00),
    ("Evonik VESTAKEEP PEEK Europe", "Polymers", "High Performance Polymer", "Evonik Vestakeep Design Specs", 1.30, 4.0, 105.0, 110.0, 4.2, 0.01, 0.26, 1350.0, 45.0, 250.0, 80.00),
    ("PEI Polyetherimide Ultem 1000", "Polymers", "High Performance Polymer", "SABIC Ultem 1000 Manual", 1.28, 3.2, 105.0, 110.0, 3.3, 0.02, 0.22, 1250.0, 55.0, 170.0, 28.00),
    ("PAI Torlon 4203 Bearing Resin", "Polymers", "High Performance Polymer", "Solvay Torlon Design Guide", 1.41, 4.5, 150.0, 175.0, 3.5, 0.01, 0.26, 1200.0, 30.0, 260.0, 95.00),
    ("PVDF Chemical Lining Resin", "Polymers", "High Performance Polymer", "Arkema Kynar 740 Tech Spec", 1.78, 2.1, 50.0, 55.0, 2.4, 0.05, 0.19, 1300.0, 120.0, 150.0, 18.00),

    # Subclass: 3D Printing / FDM Thermoplastic
    ("PLA Standard 3D Filament", "Polymers", "3D Printing Thermoplastic", "NatureWorks Ingeo 4043D Data", 1.24, 3.5, 50.0, 65.0, 2.0, 0.03, 0.13, 1800.0, 68.0, 55.0, 2.20),
    ("Tough PLA Impact Modified", "Polymers", "3D Printing Thermoplastic", "MatterHackers Tough PLA Specs", 1.25, 2.8, 42.0, 52.0, 3.2, 0.04, 0.14, 1850.0, 75.0, 60.0, 2.80),
    ("PETG 3D Printing Copolymer", "Polymers", "3D Printing Thermoplastic", "Eastman Chemical PETG Specs", 1.27, 2.1, 45.0, 50.0, 2.5, 0.03, 0.20, 1300.0, 60.0, 75.0, 2.50),
    ("ASA UV-Weatherable Filament", "Polymers", "3D Printing Thermoplastic", "BASF Forward AM Ultrafuse ASA", 1.07, 2.3, 45.0, 48.0, 2.4, 0.03, 0.18, 1400.0, 85.0, 95.0, 3.50),
    ("TPU 95A Flexible 3D Filament", "Polymers", "3D Printing Thermoplastic", "Ultimaker TPU 95A Data Sheet", 1.21, 0.035, 15.0, 38.0, 12.0, 0.15, 0.22, 1700.0, 150.0, 85.0, 4.50),
    ("PA-CF Carbon Fiber Nylon FDM", "Polymers", "3D Printing Thermoplastic", "Polymaker PolyMide PA-CF Data", 1.18, 7.5, 95.0, 110.0, 4.2, 0.02, 0.38, 1500.0, 35.0, 150.0, 8.50),

    # Subclass: Thermoset Resin & Epoxy
    ("Epoxy Structural Infusion Resin", "Polymers", "Thermoset Resin & Epoxy", "Hexion Epikote 828 Specs", 1.18, 3.4, 70.0, 85.0, 1.6, 0.02, 0.21, 1200.0, 55.0, 130.0, 5.50),
    ("Epoxy Tooling / Casting Resin", "Polymers", "Thermoset Resin & Epoxy", "Huntsman RenCast Technical", 1.22, 3.8, 80.0, 90.0, 1.4, 0.015, 0.23, 1150.0, 50.0, 150.0, 6.20),
    ("Vinyl Ester Chemical Resin", "Polymers", "Thermoset Resin & Epoxy", "Ashland Derakane 411 Guide", 1.15, 3.5, 65.0, 78.0, 1.3, 0.02, 0.20, 1250.0, 60.0, 125.0, 4.80),
    ("Polyester Unsaturated Resin", "Polymers", "Thermoset Resin & Epoxy", "Reichhold Polylite Marine Resin", 1.20, 3.2, 50.0, 60.0, 1.0, 0.025, 0.19, 1300.0, 70.0, 90.0, 3.00),
    ("Phenolic Bakelite Unfilled", "Polymers", "Thermoset Resin & Epoxy", "Bakelite Thermoset Handb.", 1.40, 6.5, 70.0, 75.0, 1.2, 0.01, 0.25, 1400.0, 40.0, 150.0, 2.50),
    ("Bismaleimide (BMI) High-Temp", "Polymers", "Thermoset Resin & Epoxy", "Cytec 5250-4 BMI Manual", 1.28, 4.2, 90.0, 105.0, 1.2, 0.012, 0.24, 1200.0, 42.0, 250.0, 35.00),

    # =========================================================================
    # 4. CERAMICS & GLASSES
    # =========================================================================
    # Subclass: Oxide Ceramic
    ("Alumina 96% Substrate Grade", "Ceramics & Glasses", "Oxide Ceramic", "CoorsTek AD-96 Property Data", 3.75, 330.0, 2200.0, 250.0, 3.8, 0.0001, 25.0, 880.0, 7.2, 1500.0, 11.00),
    ("Alumina 99.5% High Purity", "Ceramics & Glasses", "Oxide Ceramic", "Kyocera A-479 Specs", 3.90, 375.0, 2600.0, 310.0, 4.2, 0.0001, 35.0, 880.0, 7.0, 1600.0, 18.00),
    ("Zirconia Y-TZP 3mol% Bio/Wear", "Ceramics & Glasses", "Oxide Ceramic", "Tosoh TZ-3Y Technical Data", 6.05, 210.0, 2100.0, 1200.0, 8.5, 0.0002, 2.2, 450.0, 10.3, 1000.0, 45.00),
    ("Beryllia (BeO) High Conduction", "Ceramics & Glasses", "Oxide Ceramic", "Materion Thermalox Beryllia", 2.85, 345.0, 2100.0, 230.0, 3.0, 0.0001, 260.0, 1050.0, 7.5, 1800.0, 95.00),

    # Subclass: Non-Oxide Carbide & Nitride
    ("Silicon Carbide Sintered SSiC", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "Saint-Gobain Hexoloy SA", 3.15, 410.0, 3900.0, 420.0, 4.0, 0.0001, 120.0, 670.0, 4.0, 1600.0, 38.00),
    ("Silicon Nitride Gas Pressure", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "Ceradyne Ceralloy 147", 3.20, 310.0, 3000.0, 750.0, 6.5, 0.0001, 30.0, 710.0, 3.2, 1200.0, 55.00),
    ("Boron Carbide Ballistic Armor B4C", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "3M Technical Ceramics Data", 2.52, 450.0, 3500.0, 350.0, 3.2, 0.0001, 35.0, 950.0, 5.0, 1200.0, 65.00),
    ("Titanium Diboride TiB2 Extreme", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "Momentive TiB2 Technical Data", 4.52, 530.0, 3500.0, 450.0, 4.5, 0.0001, 64.0, 630.0, 7.0, 1600.0, 75.00),
    ("Aluminum Nitride AlN Electronic", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "Tokuyama Shapal AlN Data", 3.26, 310.0, 2000.0, 280.0, 3.0, 0.0001, 170.0, 740.0, 4.5, 1200.0, 55.00),
    ("Tungsten Carbide 6% Co Micrograin", "Ceramics & Glasses", "Non-Oxide Carbide & Nitride", "Sandvik Coromant Grade H10F", 14.95, 630.0, 4500.0, 1800.0, 10.0, 0.0002, 100.0, 220.0, 5.2, 800.0, 45.00),

    # Subclass: Minerals & Semiconductors
    ("Diamond Single Crystal CVD", "Ceramics & Glasses", "Minerals & Semiconductors", "Element Six Synthetic Diamond", 3.52, 1050.0, 10000.0, 2000.0, 4.0, 0.00005, 2000.0, 510.0, 1.0, 700.0, 2500.00),
    ("Silicon Single Crystal Wafer", "Ceramics & Glasses", "Minerals & Semiconductors", "MEMC Electronic Materials Spec", 2.33, 160.0, 1000.0, 120.0, 1.0, 0.0001, 149.0, 710.0, 2.6, 600.0, 35.00),
    ("Germanium Single Crystal", "Ceramics & Glasses", "Minerals & Semiconductors", "Umicore Optical Germanium Data", 5.32, 103.0, 800.0, 90.0, 0.8, 0.0001, 60.0, 320.0, 5.8, 450.0, 220.00),
    ("Gallium Arsenide (GaAs) Wafer", "Ceramics & Glasses", "Minerals & Semiconductors", "Freiberger Compound Materials", 5.32, 85.0, 600.0, 80.0, 0.5, 0.0001, 55.0, 350.0, 5.7, 400.0, 350.00),
    ("Silicon Carbide 4H-SiC Electronic", "Ceramics & Glasses", "Minerals & Semiconductors", "Wolfspeed 4H-SiC Substrates", 3.21, 450.0, 3200.0, 380.0, 3.5, 0.0001, 370.0, 690.0, 4.0, 1000.0, 450.00),
    ("Quartz Crystal Single SiO2", "Ceramics & Glasses", "Minerals & Semiconductors", "Sawyer Quartz Technical Guide", 2.65, 95.0, 1500.0, 110.0, 1.2, 0.0001, 6.8, 730.0, 7.5, 550.0, 45.00),
    ("Sapphire Single Crystal Al2O3", "Ceramics & Glasses", "Minerals & Semiconductors", "Saint-Gobain Sapphire Optics", 3.98, 400.0, 3000.0, 400.0, 4.5, 0.0001, 35.0, 760.0, 5.5, 1700.0, 65.00),

    # Subclass: Technical Glass & Glass-Ceramic
    ("Borosilicate Glass Pyrex 7740", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Corning Pyrex 7740 Data Sheet", 2.23, 64.0, 1000.0, 45.0, 0.7, 0.0003, 1.2, 750.0, 3.3, 450.0, 5.00),
    ("Schott Borofloat 33 Float Glass", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Schott Borofloat 33 Spec", 2.20, 63.0, 1000.0, 45.0, 0.7, 0.0003, 1.2, 800.0, 3.25, 450.0, 6.20),
    ("Soda Lime Float Window Glass", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Pilkington Float Glass Spec", 2.50, 70.0, 1000.0, 40.0, 0.7, 0.0004, 1.0, 840.0, 9.0, 400.0, 1.50),
    ("Fused Silica Quartz Optical", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Heraeus Suprasil Fused Silica", 2.20, 73.0, 1100.0, 50.0, 0.8, 0.0002, 1.4, 740.0, 0.5, 1000.0, 18.00),
    ("Zerodur Zero-Expansion Ceramic", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Schott Zerodur Optical Sheet", 2.53, 90.0, 900.0, 50.0, 1.1, 0.0002, 1.46, 820.0, 0.05, 600.0, 85.00),
    ("Macor Machinable Glass Ceramic", "Ceramics & Glasses", "Technical Glass & Glass-Ceramic", "Corning Macor Technical Guide", 2.52, 67.0, 350.0, 94.0, 1.5, 0.0003, 1.46, 790.0, 9.3, 800.0, 68.00),

    # Subclass: Concrete & Cementitious
    ("Plain Unreinforced Concrete C30/37", "Ceramics & Glasses", "Concrete & Cementitious", "Eurocode 2 / ACI 318 Standard", 2.35, 32.0, 30.0, 3.5, 0.7, 0.020, 1.4, 900.0, 10.0, 300.0, 0.08),
    ("High-Strength Concrete C80/95", "Ceramics & Glasses", "Concrete & Cementitious", "ACI 363R High Strength Report", 2.45, 42.0, 80.0, 5.5, 0.9, 0.015, 1.6, 920.0, 10.5, 300.0, 0.14),
    ("Ultra-High Performance UHPC", "Ceramics & Glasses", "Concrete & Cementitious", "FHWA Ductal UHPC Benchmark", 2.55, 55.0, 150.0, 12.0, 2.2, 0.010, 1.8, 950.0, 11.0, 350.0, 0.45),
    ("Lightweight Concrete (LWAC)", "Ceramics & Glasses", "Concrete & Cementitious", "ACI 213R Lightweight Mix", 1.80, 18.0, 25.0, 2.4, 0.5, 0.025, 0.8, 950.0, 9.0, 250.0, 0.12),
    ("Fly Ash Geopolymer Concrete", "Ceramics & Glasses", "Concrete & Cementitious", "RILEM TC 247-DTA Geopolymer", 2.30, 28.0, 45.0, 4.2, 0.8, 0.018, 1.2, 920.0, 10.2, 400.0, 0.10),
    ("Engineered Cementitious (ECC)", "Ceramics & Glasses", "Concrete & Cementitious", "Li: Engineered Cementitious", 2.10, 20.0, 35.0, 4.8, 1.8, 0.022, 1.1, 930.0, 10.5, 250.0, 0.38),

    # =========================================================================
    # 5. COMPOSITES
    # =========================================================================
    # Subclass: Polymer Matrix Composite - Carbon
    ("CFRP UD Carbon Epoxy Std Modulus", "Composites", "PMC - Carbon Fiber", "Torayca T700/Epoxy Data", 1.55, 135.0, 1200.0, 1500.0, 40.0, 0.0015, 4.5, 1000.0, 0.1, 140.0, 35.00),
    ("CFRP Woven Twill Prepreg Quasi-Iso", "Composites", "PMC - Carbon Fiber", "Hexcel HexPly M21 2x2 Twill", 1.50, 70.0, 650.0, 800.0, 35.0, 0.0020, 3.8, 1050.0, 2.5, 130.0, 38.00),
    ("CFRP Carbon PEEK Aerospace Tape", "Composites", "PMC - Carbon Fiber", "Cytec APC-2/AS4 Tape", 1.58, 130.0, 1350.0, 1600.0, 45.0, 0.0010, 4.8, 1150.0, 0.8, 250.0, 110.00),
    ("CFRP High Modulus M40J UD Tape", "Composites", "PMC - Carbon Fiber", "Torayca M40J Space Grade Tape", 1.60, 230.0, 1400.0, 1800.0, 35.0, 0.0012, 6.5, 950.0, -0.5, 140.0, 85.00),

    # Subclass: Polymer Matrix Composite - Glass & Aramid
    ("GFRP E-Glass Epoxy UD Prepreg", "Composites", "PMC - Glass & Aramid", "Owens Corning E-Glass Spec", 1.95, 45.0, 850.0, 1050.0, 35.0, 0.0030, 0.7, 1100.0, 7.0, 130.0, 12.00),
    ("GFRP E-Glass Vinyl Ester Marine", "Composites", "PMC - Glass & Aramid", "Ashland Derakane 411 Guide", 1.75, 20.0, 210.0, 280.0, 28.0, 0.0050, 0.4, 1200.0, 16.0, 105.0, 6.50),
    ("GFRP S-2 Glass Aerospace Prepreg", "Composites", "PMC - Glass & Aramid", "AGY S-2 Glass Technical Book", 1.98, 55.0, 1100.0, 1450.0, 40.0, 0.0025, 0.8, 1050.0, 5.5, 150.0, 22.00),
    ("AFRP Aramid Kevlar 49 Epoxy", "Composites", "PMC - Glass & Aramid", "DuPont Kevlar Composites Book", 1.38, 75.0, 950.0, 1350.0, 45.0, 0.0030, 0.5, 1200.0, -2.0, 140.0, 28.00),
    ("AFRP Kevlar 29 Ballistic Fabric", "Composites", "PMC - Glass & Aramid", "DuPont Kevlar Ballistics Manual", 1.40, 45.0, 750.0, 1050.0, 50.0, 0.0040, 0.45, 1250.0, -1.5, 150.0, 32.00),

    # Subclass: Reinforced Concrete
    ("Steel-Reinforced Concrete (2% Rebar)", "Composites", "Reinforced Concrete", "ACI 318 / Eurocode 2 Standard", 2.45, 35.0, 55.0, 45.0, 12.0, 0.015, 1.7, 880.0, 11.0, 300.0, 0.18),
    ("Steel-Reinforced Concrete (4% Rebar)", "Composites", "Reinforced Concrete", "AASHTO LRFD Bridge Specs", 2.55, 40.0, 95.0, 85.0, 20.0, 0.012, 2.1, 860.0, 11.5, 300.0, 0.28),
    ("Glass Fiber Reinf Concrete GFRC", "Composites", "Reinforced Concrete", "PCI GFRC Architectural Manual", 2.15, 28.0, 40.0, 22.0, 4.5, 0.020, 1.2, 920.0, 10.0, 250.0, 0.40),
    ("Steel Fiber Reinf Concrete SFRC 1%", "Composites", "Reinforced Concrete", "Bekaert Dramix SFRC Technical", 2.42, 36.0, 50.0, 16.0, 8.5, 0.018, 1.8, 890.0, 10.5, 300.0, 0.35),

    # Subclass: Ceramic & Carbon Matrix Composite
    ("Carbon-Carbon 2D Brake Disc", "Composites", "Ceramic & Carbon Matrix Composite", "Brembo Racing Carbon Data", 1.75, 95.0, 250.0, 310.0, 25.0, 0.0020, 60.0, 800.0, 1.5, 1200.0, 160.00),
    ("Ceramic Matrix SiC/SiC Turbine Vane", "Composites", "Ceramic & Carbon Matrix Composite", "GE Aviation CFM-LEAP CMCs", 2.60, 230.0, 320.0, 380.0, 25.0, 0.0005, 18.0, 900.0, 4.0, 1250.0, 280.00),
    ("Ceramic Matrix C/SiC High Temp Brake", "Composites", "Ceramic & Carbon Matrix Composite", "SGL Carbon Brembo C/SiC Data", 2.30, 180.0, 280.0, 330.0, 22.0, 0.0006, 24.0, 950.0, 3.5, 1150.0, 190.00),

    # Subclass: Laminated & Structural Sandwich
    ("G10/FR4 PCB Glass Epoxy Sheet", "Composites", "Laminated & Structural Sandwich", "NEMA LI-1 Industrial Standard", 1.85, 24.0, 280.0, 340.0, 25.0, 0.0050, 0.3, 1100.0, 14.0, 130.0, 8.50),
    ("Micarta Phenolic Canvas Grade C", "Composites", "Laminated & Structural Sandwich", "Norplex-Micarta Industrial Guide", 1.36, 7.5, 65.0, 85.0, 9.0, 0.0200, 0.25, 1400.0, 35.0, 115.0, 7.20),
    ("Rohacell 51 PMI Foam Core", "Composites", "Laminated & Structural Sandwich", "Evonik Rohacell Design Book", 0.05, 0.07, 1.4, 1.6, 0.3, 0.0800, 0.03, 1500.0, 35.0, 160.0, 35.00),
    ("Nomex Aerospace Honeycomb Core", "Composites", "Laminated & Structural Sandwich", "Euro-Composites ECA Core Spec", 0.048, 0.13, 2.4, 3.1, 0.6, 0.0400, 0.04, 1250.0, 30.0, 180.0, 65.00),
    ("Divinycell H80 Marine Core Foam", "Composites", "Laminated & Structural Sandwich", "Diab Divinycell Technical Data", 0.08, 0.09, 1.8, 2.5, 0.4, 0.0900, 0.03, 1400.0, 40.0, 80.0, 14.00),

    # Subclass: Metal Matrix Composite
    ("Aluminum 6061 Matrix SiC 20%", "Composites", "Metal Matrix Composite", "DWA Aluminum Composites Data", 2.80, 105.0, 420.0, 520.0, 18.0, 0.0003, 140.0, 850.0, 15.5, 200.0, 18.00),
    ("Aluminum Matrix B4C MMC Armor", "Composites", "Metal Matrix Composite", "Materion MMC Defense Data", 2.65, 110.0, 410.0, 490.0, 20.0, 0.0003, 130.0, 880.0, 15.0, 250.0, 28.00),
    ("Copper Matrix Diamond Heat Sink", "Composites", "Metal Matrix Composite", "Plansee Thermal MMC Guide", 6.20, 250.0, 250.0, 320.0, 12.0, 0.0002, 550.0, 420.0, 6.0, 300.0, 140.00),

    # =========================================================================
    # 6. ELASTOMERS
    # =========================================================================
    # Subclass: Industrial Rubber
    ("Natural Rubber Pure Gum 40 ShA", "Elastomers", "Industrial Rubber", "Vanderbilt Rubber Handbook", 0.93, 0.0015, 2.0, 25.0, 12.0, 0.05, 0.15, 1900.0, 220.0, 70.0, 2.20),
    ("Natural Rubber Carbon Black 60 ShA", "Elastomers", "Industrial Rubber", "Bridgestone Tire Tech Spec", 1.10, 0.0040, 3.5, 22.0, 10.0, 0.10, 0.18, 1800.0, 200.0, 75.0, 2.50),
    ("Styrene Butadiene SBR 65 ShA", "Elastomers", "Industrial Rubber", "ASTM D2000 Automotive Spec", 1.18, 0.0060, 4.2, 19.0, 7.0, 0.16, 0.22, 1800.0, 190.0, 85.0, 2.30),
    ("Nitrile Rubber NBR 60 ShA", "Elastomers", "Industrial Rubber", "Parker O-Ring Handbook ORD 5700", 1.00, 0.0038, 3.2, 17.0, 6.2, 0.22, 0.24, 1900.0, 210.0, 95.0, 3.50),
    ("Neoprene CR 60 ShA Standard", "Elastomers", "Industrial Rubber", "DuPont Neoprene Design Handb.", 1.30, 0.0050, 3.8, 18.0, 6.8, 0.16, 0.20, 1680.0, 190.0, 100.0, 4.40),
    ("EPDM Rubber Dense Radiator 70 ShA", "Elastomers", "Industrial Rubber", "Lanxess Keltan EPDM Manual", 1.15, 0.0065, 4.5, 14.0, 5.5, 0.15, 0.25, 1900.0, 190.0, 130.0, 3.10),
    ("Butyl Rubber IIR Tire Tube 50 ShA", "Elastomers", "Industrial Rubber", "ExxonMobil Butyl Handbook", 0.92, 0.0028, 2.2, 14.0, 5.0, 0.35, 0.13, 1950.0, 210.0, 110.0, 3.20),

    # Subclass: Specialty & Thermoplastic Elastomer
    ("Silicone VMQ O-Ring 50 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Dow Corning Silastic Tech Data", 1.18, 0.0028, 2.0, 9.5, 4.2, 0.08, 0.22, 1300.0, 280.0, 220.0, 13.50),
    ("Silicone VMQ High Temp 70 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Wacker Elastosil Tech Spec", 1.25, 0.0055, 3.2, 8.5, 3.8, 0.09, 0.25, 1300.0, 260.0, 260.0, 14.00),
    ("Fluorosilicone FVMQ Fuel Seal", "Elastomers", "Specialty & Thermoplastic Elastomer", "Parker Fluorosilicone L1120", 1.40, 0.0035, 2.5, 8.0, 3.0, 0.12, 0.23, 1250.0, 250.0, 190.0, 42.00),
    ("Viton FKM Fluoroelastomer 75 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Chemours Viton Genuine Sheet", 1.85, 0.0080, 5.0, 13.0, 3.5, 0.20, 0.20, 1400.0, 160.0, 210.0, 32.00),
    ("Kalrez FFKM Chemical Extreme 7075", "Elastomers", "Specialty & Thermoplastic Elastomer", "DuPont Kalrez 7075 Spec", 2.01, 0.0110, 6.5, 16.0, 3.8, 0.25, 0.18, 1300.0, 160.0, 315.0, 380.00),
    ("Cast Polyurethane MDI Ether 80 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Gallagher Corp Cast Urethane", 1.18, 0.0120, 5.5, 35.0, 14.0, 0.10, 0.22, 1750.0, 170.0, 80.0, 6.50),
    ("TPU Polyester Estane 85 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Lubrizol Estane 58887 Spec", 1.20, 0.0220, 7.5, 40.0, 15.0, 0.12, 0.21, 1700.0, 160.0, 95.0, 5.20),
    ("TPO Polyolefin Santoprene 64 ShA", "Elastomers", "Specialty & Thermoplastic Elastomer", "Celanese Santoprene 101-64", 0.96, 0.0070, 3.0, 8.0, 5.5, 0.15, 0.18, 1900.0, 210.0, 115.0, 3.95),

    # =========================================================================
    # 7. NATURAL & BIOLOGICAL MATERIALS
    # =========================================================================
    # Subclass: Structural Wood & Timber
    ("White Oak (Quercus alba, Dry)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.75, 12.3, 48.0, 105.0, 4.2, 0.035, 0.17, 1700.0, 5.0, 100.0, 1.80),
    ("Hard Sugar Maple (Acer saccharum)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.72, 12.6, 52.0, 110.0, 4.0, 0.030, 0.16, 1700.0, 4.8, 100.0, 2.10),
    ("Black Walnut (Juglans nigra)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.61, 11.6, 45.0, 100.0, 3.8, 0.032, 0.14, 1750.0, 4.5, 100.0, 3.50),
    ("Hickory / Pecan (Carya ovata)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.83, 15.0, 60.0, 130.0, 4.8, 0.028, 0.19, 1650.0, 5.2, 100.0, 2.40),
    ("Douglas Fir (Pseudotsuga menziesii)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.53, 13.4, 45.0, 85.0, 3.2, 0.035, 0.13, 1700.0, 4.0, 100.0, 0.95),
    ("Southern Yellow Pine (Pinus taeda)", "Natural & Biological", "Structural Wood & Timber", "USDA Wood Handbook FPL-GTR-190", 0.59, 12.4, 40.0, 88.0, 3.0, 0.038, 0.14, 1700.0, 4.2, 100.0, 0.85),
    ("European Beech (Fagus sylvatica)", "Natural & Biological", "Structural Wood & Timber", "DIN 68364 / EN 338 Timber Specs", 0.71, 14.0, 55.0, 115.0, 4.1, 0.030, 0.16, 1700.0, 4.8, 100.0, 1.95),
    ("Balsa Wood (Ochroma pyramidale)", "Natural & Biological", "Structural Wood & Timber", "Ashby CES Materials Selector Data", 0.16, 3.4, 12.0, 20.0, 0.8, 0.060, 0.05, 1800.0, 2.5, 90.0, 4.50),

    # Subclass: Bamboo & Bone
    ("Moso Bamboo Outer Culm P. edulis", "Natural & Biological", "Bamboo & Bone", "ISO 22157 Bamboo Physical Standards", 0.85, 18.5, 75.0, 160.0, 5.5, 0.025, 0.22, 1600.0, 4.5, 90.0, 1.20),
    ("Guadua Bamboo Culm G. angustifolia", "Natural & Biological", "Bamboo & Bone", "INBAR Guadua Tech Spec / ISO 22157", 0.78, 16.0, 65.0, 140.0, 5.0, 0.028, 0.20, 1650.0, 4.2, 90.0, 1.10),
    ("Laminated Bamboo Lumber (LBL)", "Natural & Biological", "Bamboo & Bone", "ASTM D5456 / Bamboo Composite", 0.70, 11.5, 50.0, 95.0, 4.2, 0.035, 0.18, 1700.0, 5.0, 90.0, 1.80),
    ("Cortical Bone Longitudinal Femur", "Natural & Biological", "Bamboo & Bone", "Cowin Bone Mechanics / Currey Data", 1.90, 18.0, 110.0, 140.0, 4.5, 0.040, 0.55, 1300.0, 15.0, 45.0, 250.00),
    ("Cortical Bone Transverse Femur", "Natural & Biological", "Bamboo & Bone", "Cowin Bone Mechanics / Currey Data", 1.90, 11.5, 55.0, 65.0, 2.8, 0.050, 0.50, 1300.0, 18.0, 45.0, 250.00),
    ("Bovine Haversian Cortical Bone", "Natural & Biological", "Bamboo & Bone", "Currey: Bones Structure and Mechanics", 1.95, 20.0, 125.0, 155.0, 5.2, 0.035, 0.58, 1280.0, 14.0, 45.0, 120.00),
    ("Cancellous Trabecular Vertebral", "Natural & Biological", "Bamboo & Bone", "Gibson & Ashby: Cellular Solids", 0.35, 0.8, 4.5, 6.0, 0.4, 0.120, 0.15, 1500.0, 25.0, 45.0, 200.00),

    # =========================================================================
    # 8. GASKETS & SEALS
    # =========================================================================
    # Subclass: Gasket & Flange Sheet
    ("Vegetable Fiber Gasket Paper (N-8092)", "Gaskets & Seals", "Gasket & Flange Sheet", "ASTM F104 / Fel-Pro Tech Data", 0.88, 1.10, 14.0, 22.0, 0.8, 0.080, 0.16, 1400.0, 24.0, 120.0, 4.50),
    ("Compressed Non-Asbestos Sheet (CNAF)", "Gaskets & Seals", "Gasket & Flange Sheet", "DIN 28091 / Klinger C-4400 Spec", 1.75, 3.80, 22.0, 32.0, 1.2, 0.060, 0.42, 1150.0, 18.0, 250.0, 8.50),
    ("Rubber-Bonded Cork Sheet (NC-711)", "Gaskets & Seals", "Gasket & Flange Sheet", "ASTM F104 / Armstrong Cork Data", 0.68, 0.09, 2.8, 4.5, 0.4, 0.220, 0.09, 1800.0, 65.0, 125.0, 6.20),
    ("Flexible Exfoliated Graphite Sheet", "Gaskets & Seals", "Gasket & Flange Sheet", "GrafTech Grafoil GTB Datasheet", 1.12, 1.40, 4.8, 6.5, 0.5, 0.140, 120.0, 710.0, 1.2, 450.0, 24.00),

    # =========================================================================
    # 9. CELLULAR SOLIDS
    # =========================================================================
    # Subclass: Polymer & Metal Foams
    ("Rigid Polyurethane Foam (6 lb/cu ft)", "Cellular Solids", "Polymer & Metal Foams", "General Plastics Last-A-Foam FR-3706", 0.096, 0.085, 2.2, 2.6, 0.25, 0.070, 0.028, 1500.0, 55.0, 110.0, 5.20),
    ("Flexible Polyurethane Seating Foam", "Cellular Solids", "Polymer & Metal Foams", "Dow Voranol Molded Foam Data", 0.042, 0.0009, 0.09, 0.16, 0.05, 0.350, 0.038, 1800.0, 120.0, 85.0, 3.80),
    ("Extruded Polystyrene Foam (XPS)", "Cellular Solids", "Polymer & Metal Foams", "Owens Corning Foamular Tech Data", 0.035, 0.026, 0.38, 0.52, 0.10, 0.080, 0.030, 1300.0, 70.0, 75.0, 3.10),
    ("Open-Cell Aluminum Foam (Duocel 8%)", "Cellular Solids", "Polymer & Metal Foams", "ERG Aerospace Duocel Al 6101 Data", 0.220, 1.85, 5.8, 7.2, 1.6, 0.015, 8.5, 900.0, 23.0, 300.0, 48.00),

    # =========================================================================
    # 10. BEARING & FRICTION
    # =========================================================================
    # Subclass: Porous Bushing & Bearing Metal
    ("Sintered Bronze SAE 841 (Oilite)", "Bearing & Friction", "Porous Bushing & Bearing Metal", "ASTM B438 / Beemer Precision", 6.60, 60.0, 75.0, 125.0, 14.0, 0.003, 45.0, 380.0, 18.0, 150.0, 14.00),
    ("Sintered Iron-Copper SAE 863", "Bearing & Friction", "Porous Bushing & Bearing Metal", "ASTM B439 / Keystone Powder Metal", 6.00, 95.0, 275.0, 345.0, 16.0, 0.002, 38.0, 460.0, 12.5, 150.0, 9.50),
    ("DU Steel-Bronze-PTFE Bushing Liner", "Bearing & Friction", "Porous Bushing & Bearing Metal", "GGB Bearing Technology DU Manual", 4.80, 48.0, 140.0, 180.0, 12.0, 0.040, 52.0, 420.0, 15.0, 280.0, 24.00),

    # Subclass: Friction & Brake Lining
    ("Semi-Metallic Brake Friction Pad", "Bearing & Friction", "Friction & Brake Lining", "SAE J661 Brake Lining Standards", 2.80, 8.5, 35.0, 45.0, 2.5, 0.080, 2.2, 850.0, 16.0, 400.0, 8.50),
    ("Sintered Metallic Clutch Friction Pad", "Bearing & Friction", "Friction & Brake Lining", "Wellman Friction Products Manual", 5.40, 35.0, 120.0, 160.0, 6.5, 0.020, 28.0, 450.0, 14.0, 550.0, 28.00),
    ("Non-Asbestos Organic (NAO) Brake Pad", "Bearing & Friction", "Friction & Brake Lining", "SAE J661 / Federal-Mogul Data", 2.10, 5.2, 25.0, 32.0, 1.8, 0.120, 1.1, 1050.0, 22.0, 320.0, 6.80),

    # =========================================================================
    # 11. SPECIALTY NON-METALLIC
    # =========================================================================
    # Subclass: Electrical Barrier & Film
    ("Muscovite Mica Plate Laminate", "Specialty Non-Metallic", "Electrical Barrier & Film", "ISO 60371 / Cogebi Mica Data", 2.20, 35.0, 110.0, 150.0, 1.5, 0.005, 0.55, 880.0, 10.0, 500.0, 18.00),
    ("Vulcanized Electrical Fiber (Fishpaper)", "Specialty Non-Metallic", "Electrical Barrier & Film", "ASTM D710 / Spaulding Armite Data", 1.25, 6.5, 45.0, 75.0, 2.2, 0.035, 0.24, 1450.0, 25.0, 115.0, 7.50),
    ("Polyimide Film (DuPont Kapton HN)", "Specialty Non-Metallic", "Electrical Barrier & Film", "DuPont Kapton Summary of Properties", 1.42, 2.5, 69.0, 165.0, 3.2, 0.015, 0.12, 1090.0, 20.0, 400.0, 85.00),
]