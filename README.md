# 📖 Overview

Intelligent Credit File Analysis System is an AI-powered Intelligent Document Processing (IDP) platform developed to automate the analysis of banking credit files.

The system transforms scanned banking documents into structured digital information through an end-to-end pipeline combining computer vision, Optical Character Recognition (OCR), Large Language Models (LLMs), data validation, normalization, and database integration.

Current capabilities include:

- PDF preprocessing
- OCR using PaddleOCR
- OCR correction using Groq LLM
- Automatic extraction of key banking fields
- Field validation
- Data normalization
- Automatic storage in a relational SQLite database

The project is being developed during an AI Engineering internship at Banque Populaire Morocco and will later evolve into a Retrieval-Augmented Generation (RAG) assistant for intelligent document querying.

# 🎯 Objectives

The project aims to:

- Automate the processing of banking credit documents.
- Improve OCR accuracy using image preprocessing.
- Correct OCR errors using a Large Language Model.
- Extract critical banking information automatically.
- Validate extracted information.
- Normalize banking data.
- Store both structured data and complete OCR text.
- Build an intelligent RAG assistant for banking document search and question answering.

app/
│
├── main.py
├── pipeline.py
│
├── preprocessing/
│   ├── loader.py
│   ├── pdf_converter.py
│   ├── grayscale.py
│   ├── deskew.py
│   ├── denoise.py
│   ├── contrast.py
│   └── resize.py
│
├── ocr/
│   └── paddle_ocr.py
│
├── postprocessing/
│   ├── ocr_postprocessor.py
│   └── text_reconstructor.py
│
├── llm/
│   ├── groq_client.py
│   └── field_extractor.py
│
├── validation/
│   └── validator.py
│
├── normalization/
│   └── normalizer.py
│
data/
│
├── database/
│   ├── connection.py
│   ├── database_manager.py
│   └── models.py
│
├── input/
└── processed/

PDF Documents
      │
      ▼
Document Validation
      │
      ▼
PDF → Images
      │
      ▼
Grayscale
      │
      ▼
Deskew
      │
      ▼
Noise Removal
      │
      ▼
Contrast Enhancement
      │
      ▼
Resize
      │
      ▼
PaddleOCR
      │
      ▼
OCR Confidence Filtering
      │
      ▼
Reading Order Reconstruction
      │
      ▼
LLM OCR Correction
      │
      ▼
Field Extraction
      │
      ▼
Validation
      │
      ▼
Normalization
      │
      ▼
SQLite Database
      │
      ▼
Future RAG Assistant

# 🗄️ Database

The project stores all processed information inside a relational SQLite database.

Current schema:

- client
- dossier_credit
- document
- document_page
- ocr_results
- extracted_fields
- validation_results

Each processed PDF automatically populates the database.

# 🔎 OCR

OCR is performed using PaddleOCR.

The OCR pipeline includes:

- Text detection
- Text recognition
- Confidence filtering
- Reading-order reconstruction
- OCR correction using Groq LLM

Both raw OCR output and corrected text are stored in the database.

# 🤖 Large Language Model

The project uses Groq API to:

- Correct OCR mistakes
- Extract structured banking information

Future versions will also use the LLM as part of the RAG system.

## Core

- Python 3.10
- OpenCV
- NumPy
- pdf2image
- SQLite

## OCR

- PaddleOCR
- PaddlePaddle

## AI

- Groq API
- LLM Prompt Engineering

## Future

- LangChain
- FAISS
- SentenceTransformers

# ▶️ Running the Project

Place one or more PDF files inside:

data/input/

Run:

python -m app.main

Each PDF will automatically:

- be preprocessed
- undergo OCR
- have key fields extracted
- be validated
- be normalized
- be stored in the SQLite database

# 📈 Current Progress

- [x] Project architecture
- [x] PDF preprocessing
- [x] OCR integration (PaddleOCR)
- [x] OCR post-processing
- [x] OCR correction using LLM
- [x] Banking field extraction
- [x] Field validation
- [x] Field normalization
- [x] SQLite database integration
- [x] Batch processing of multiple PDF documents
- [ ] Search interface
- [ ] Retrieval-Augmented Generation (RAG)

## ✅ Phase 1 — Document Preprocessing

Completed.

## ✅ Phase 2 — OCR

Completed.

## ✅ Phase 3 — Information Extraction

Completed.

Currently extracting:

- Full Name
- Account Number
- Credit Type
- Credit Amount
- Production Date
- Archive Date

## ✅ Phase 4 — Validation & Normalization

Completed.

## ✅ Phase 5 — Database

Completed.

## 🔄 Phase 6 — Search Interface

Search client dossiers by:

- Client name
- (Future) National ID (CIN)

## 🚀 Phase 7 — Retrieval-Augmented Generation (RAG)

Allow users to ask natural-language questions about processed banking documents using the stored OCR text.

