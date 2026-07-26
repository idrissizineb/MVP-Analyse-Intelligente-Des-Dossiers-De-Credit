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

CREATE_DOSSIER_CREDIT_TABLE = """
CREATE TABLE IF NOT EXISTS dossier_credit (
    dossier_id INTEGER PRIMARY KEY AUTOINCREMENT,

    client_id INTEGER NOT NULL,

    numero_compte VARCHAR(50) NOT NULL,

    nature_credit VARCHAR(255) NOT NULL,

    montant_credit DECIMAL(15, 2) NOT NULL,

    date_production DATE,

    date_archivage DATE,

    statut VARCHAR(50) DEFAULT 'en_analyse',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id)
        REFERENCES client(client_id)
);
"""

CREATE_DOCUMENT_TABLE = """
CREATE TABLE IF NOT EXISTS document (
    document_id INTEGER PRIMARY KEY AUTOINCREMENT,

    dossier_id INTEGER NOT NULL,

    nom_fichier VARCHAR(255) NOT NULL,

    type_document VARCHAR(100),

    nombre_pages INTEGER NOT NULL,

    chemin_fichier VARCHAR(500) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (dossier_id)
        REFERENCES dossier_credit(dossier_id)
);
"""

CREATE_DOCUMENT_PAGE_TABLE = """
CREATE TABLE IF NOT EXISTS document_page (
    page_id INTEGER PRIMARY KEY AUTOINCREMENT,

    document_id INTEGER NOT NULL,

    numero_page INTEGER NOT NULL,

    chemin_image VARCHAR(500) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (document_id)
        REFERENCES document(document_id)
);
"""