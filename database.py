import sqlite3
import csv
import os
from default_materials import DEFAULT_MATERIALS

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "material_selector.db")

class MaterialDatabase:
    """
    Manages persistent SQLite storage and querying for material engineering properties,
    categories, subclasses, and source citations.
    """
    def __init__(self, db_path=DB_FILE):
        """Initializes database path and sets up tables."""
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """
        Creates and returns a connection to SQLite with row factory configured to
        allow column access by key name.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """
        Creates the 'materials' schema if it does not exist and inserts default material records
        if the table is empty.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS materials (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    material_name TEXT UNIQUE NOT NULL,
                    category TEXT NOT NULL,
                    subclass TEXT NOT NULL,
                    source TEXT NOT NULL,
                    density REAL,
                    youngs_modulus REAL,
                    yield_strength REAL,
                    tensile_strength REAL,
                    fracture_toughness REAL,
                    loss_coefficient REAL,
                    thermal_conductivity REAL,
                    specific_heat REAL,
                    thermal_expansion REAL,
                    max_service_temp REAL,
                    cost_per_kg REAL
                )
            """)
            cursor.execute("SELECT COUNT(*) FROM materials")
            if cursor.fetchone()[0] == 0:
                self.populate_default_records(cursor)
            conn.commit()

    def populate_default_records(self, cursor):
        """Inserts built-in default material tuples into the database table."""
        query = """
            INSERT OR IGNORE INTO materials (
                material_name, category, subclass, source, density, youngs_modulus,
                yield_strength, tensile_strength, fracture_toughness, loss_coefficient,
                thermal_conductivity, specific_heat, thermal_expansion,
                max_service_temp, cost_per_kg
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.executemany(query, DEFAULT_MATERIALS)

    def get_categories(self):
        """Queries and returns an alphabetically sorted list of unique material categories."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM materials ORDER BY category ASC")
            return [row["category"] for row in cursor.fetchall()]

    def get_subclasses_by_categories(self, categories):
        """
        Queries and returns distinct subclasses belonging to the specified set of categories.
        Uses parameterized placeholders (?, ?) to safely handle dynamic category lists.
        """
        if not categories:
            return []
        placeholders = ",".join(["?"] * len(categories))
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT DISTINCT subclass FROM materials 
                WHERE category IN ({placeholders}) 
                ORDER BY subclass ASC
            """, categories)
            return [row["subclass"] for row in cursor.fetchall()]

    def get_materials_by_hierarchy(self, categories, subclasses):
        """
        Retrieves matching materials filtered by both selected categories and subclasses.
        Returns a list of (material_name, category, subclass, source) tuples.
        """
        if not categories or not subclasses:
            return []
        cat_placeholders = ",".join(["?"] * len(categories))
        sub_placeholders = ",".join(["?"] * len(subclasses))
        params = list(categories) + list(subclasses)
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                SELECT material_name, category, subclass, source FROM materials 
                WHERE category IN ({cat_placeholders}) AND subclass IN ({sub_placeholders})
                ORDER BY category ASC, subclass ASC, material_name ASC
            """, params)
            return [(row["material_name"], row["category"], row["subclass"], row["source"]) for row in cursor.fetchall()]

    def fetch_records(self, material_names=None):
        """
        Fetches full database records as dictionaries.
        If `material_names` is provided, fetches only matching entries; otherwise returns all.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if material_names:
                placeholders = ",".join(["?"] * len(material_names))
                cursor.execute(f"SELECT * FROM materials WHERE material_name IN ({placeholders})", material_names)
            else:
                cursor.execute("SELECT * FROM materials")
            return [dict(row) for row in cursor.fetchall()]

    def get_material_source_info(self, material_name):
        """Retrieves citation and hierarchy metadata for a single material by name."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT material_name, category, subclass, source FROM materials WHERE material_name = ?", (material_name,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def import_csv(self, filepath):
        """
        Parses an external CSV file and batch-inserts or updates material records.
        Converts missing or blank property fields to None (SQL NULL).
        Returns the number of imported/updated records.
        """
        count = 0
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = []
            for row in reader:
                records.append((
                    row["material_name"].strip(),
                    row["category"].strip(),
                    row.get("subclass", "General").strip(),
                    row.get("source", "User CSV Import").strip(),
                    float(row["density"]) if row.get("density") else None,
                    float(row["youngs_modulus"]) if row.get("youngs_modulus") else None,
                    float(row["yield_strength"]) if row.get("yield_strength") else None,
                    float(row["tensile_strength"]) if row.get("tensile_strength") else None,
                    float(row["fracture_toughness"]) if row.get("fracture_toughness") else None,
                    float(row["loss_coefficient"]) if row.get("loss_coefficient") else None,
                    float(row["thermal_conductivity"]) if row.get("thermal_conductivity") else None,
                    float(row["specific_heat"]) if row.get("specific_heat") else None,
                    float(row["thermal_expansion"]) if row.get("thermal_expansion") else None,
                    float(row["max_service_temp"]) if row.get("max_service_temp") else None,
                    float(row["cost_per_kg"]) if row.get("cost_per_kg") else None,
                ))
            with self.get_connection() as conn:
                cursor = conn.cursor()
                query = """
                    INSERT OR REPLACE INTO materials (
                        material_name, category, subclass, source, density, youngs_modulus,
                        yield_strength, tensile_strength, fracture_toughness, loss_coefficient,
                        thermal_conductivity, specific_heat, thermal_expansion,
                        max_service_temp, cost_per_kg
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                cursor.executemany(query, records)
                conn.commit()
                count = len(records)
        return count