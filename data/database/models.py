"""
Database schema definitions.

This module contains the SQL statements used to create
the relational database schema.
"""


CREATE_CLIENT_TABLE = """
CREATE TABLE IF NOT EXISTS client (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_prenom VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""