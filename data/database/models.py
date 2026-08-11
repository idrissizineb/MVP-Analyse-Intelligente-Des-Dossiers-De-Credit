from dataclasses import dataclass
from typing import Optional


# ==========================================================
# PYTHON DATA MODELS
# ==========================================================


@dataclass
class Client:

    id: Optional[int] = None

    cin: Optional[str] = None

    nom_prenom: Optional[str] = None


@dataclass
class CreditDossier:

    id: Optional[int] = None

    client_id: Optional[int] = None

    numero_compte: Optional[str] = None

    nature_credit: Optional[str] = None

    montant_credit: Optional[float] = None

    date_de_decision: Optional[str] = None

    date_archivage: Optional[str] = None

    statut: str = "en_analyse"


@dataclass
class Document:

    id: Optional[int] = None

    dossier_id: Optional[int] = None

    nom_fichier: Optional[str] = None

    type_document: Optional[str] = None

    nombre_pages: Optional[int] = None

    chemin_fichier: Optional[str] = None


@dataclass
class DocumentPage:

    id: Optional[int] = None

    document_id: Optional[int] = None

    numero_page: Optional[int] = None

    chemin_image: Optional[str] = None


@dataclass
class OCRResult:

    id: Optional[int] = None

    page_id: Optional[int] = None

    raw_text: Optional[str] = None

    corrected_text: Optional[str] = None

    raw_ocr_json: Optional[str] = None

    average_confidence: Optional[float] = None

    ocr_engine: str = "PaddleOCR"


@dataclass
class ExtractedField:

    id: Optional[int] = None

    document_id: Optional[int] = None

    field_name: Optional[str] = None

    field_value: Optional[str] = None

    normalized_value: Optional[str] = None

    confidence: Optional[float] = None


@dataclass
class ValidationResult:

    id: Optional[int] = None

    document_id: Optional[int] = None

    field_name: Optional[str] = None

    field_value: Optional[str] = None

    status: Optional[str] = None

    error_message: Optional[str] = None


# ==========================================================
# DATABASE SCHEMA
# ==========================================================


CREATE_CLIENT_TABLE = """

CREATE TABLE IF NOT EXISTS client (

    client_id INTEGER PRIMARY KEY AUTOINCREMENT,

    cin TEXT UNIQUE NOT NULL,

    nom_prenom TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

"""


CREATE_DOSSIER_CREDIT_TABLE = """

CREATE TABLE IF NOT EXISTS dossier_credit (

    dossier_id INTEGER PRIMARY KEY AUTOINCREMENT,

    client_id INTEGER NOT NULL,

    numero_compte TEXT NOT NULL,

    nature_credit TEXT NOT NULL,

    montant_credit REAL NOT NULL,

    date_de_decision TEXT,

    date_archivage TEXT,

    statut TEXT DEFAULT 'en_analyse',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (client_id)

        REFERENCES client(client_id)

        ON DELETE CASCADE

)

"""


CREATE_DOCUMENT_TABLE = """

CREATE TABLE IF NOT EXISTS document (

    document_id INTEGER PRIMARY KEY AUTOINCREMENT,

    dossier_id INTEGER NOT NULL,

    nom_fichier TEXT NOT NULL,

    type_document TEXT,

    nombre_pages INTEGER NOT NULL,

    chemin_fichier TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (dossier_id)

        REFERENCES dossier_credit(dossier_id)

        ON DELETE CASCADE

)

"""


CREATE_DOCUMENT_PAGE_TABLE = """

CREATE TABLE IF NOT EXISTS document_page (

    page_id INTEGER PRIMARY KEY AUTOINCREMENT,

    document_id INTEGER NOT NULL,

    numero_page INTEGER NOT NULL,

    chemin_image TEXT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (document_id)

        REFERENCES document(document_id)

        ON DELETE CASCADE

)

"""