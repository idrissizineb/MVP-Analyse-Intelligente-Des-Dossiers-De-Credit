# 📄 Intelligent Credit File Analysis System

> An AI-powered document processing pipeline for automating the analysis of banking credit files.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

# 📖 Overview

This project aims to automate the analysis of banking credit files by transforming scanned PDF documents into structured digital information.

The system is designed to process various banking documents such as:

- National Identity Cards
- Salary Certificates
- Bank Statements
- Tax Documents
- Employment Certificates
- Credit Application Files

The preprocessing pipeline prepares scanned documents for Optical Character Recognition (OCR), ensuring higher text recognition accuracy before information extraction.

The project is being developed as part of an AI Engineering internship at **Banque Populaire Morocco**.

---

# 🎯 Objectives

The main objectives are:

- Convert PDF documents into high-quality images.
- Improve scanned document quality using image preprocessing.
- Increase OCR accuracy.
- Automatically extract relevant information from banking documents.
- Validate extracted information.
- Store structured data for further processing.
- Build a Retrieval-Augmented Generation (RAG) system for intelligent document querying.

---

# 🏗️ Current Project Architecture

```
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
├── data/
│   ├── raw/
│   └── processed/
│
└── utils/
```

---

# ⚙️ Current Processing Pipeline

```
PDF Document
      │
      ▼
Document Validation
      │
      ▼
PDF → Image Conversion
      │
      ▼
Grayscale Conversion
      │
      ▼
Skew Detection & Correction
      │
      ▼
Noise Removal
      │
      ▼
Contrast Enhancement (CLAHE)
      │
      ▼
Image Resizing
      │
      ▼
Processed Images
```

---

# 📚 Preprocessing Modules

## 1. Document Loader

Responsible for:

- validating the document path
- checking supported file formats
- ensuring the document exists

---

## 2. PDF Converter

Uses **pdf2image** to convert PDF pages into OpenCV images.

Output:

```
PDF

↓

List[np.ndarray]
```

---

## 3. Grayscale Conversion

Converts RGB images into grayscale.

Benefits:

- reduces computational cost
- removes unnecessary color information
- improves OCR preprocessing

---

## 4. Deskew Correction

Automatically detects page rotation using the Hough Transform.

Corrects:

- scanned documents
- slightly rotated pages
- misaligned text

---

## 5. Noise Removal

Uses **Non-Local Means Denoising**.

Advantages:

- preserves text edges
- removes scanner noise
- reduces compression artifacts

---

## 6. Contrast Enhancement

Uses **CLAHE (Contrast Limited Adaptive Histogram Equalization)**.

Advantages:

- improves faint text
- increases OCR readability
- preserves local document details
- avoids over-enhancement

---

## 7. Image Resizing

Upscales low-resolution images while preserving the aspect ratio.

Interpolation:

```
cv2.INTER_LANCZOS4
```

Benefits:

- improves OCR accuracy
- avoids unnecessary resizing
- maintains document proportions

---

# 🛠️ Technologies Used

- Python 3.10+
- OpenCV
- NumPy
- pdf2image
- Poppler
- pathlib

Future technologies:

- PaddleOCR
- PaddlePaddle
- FastAPI
- SQLite / PostgreSQL
- LangChain
- FAISS
- HuggingFace Transformers

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/intelligent-credit-analysis.git

cd intelligent-credit-analysis
```

---

## Create a virtual environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install dependencies

```bash
pip install -r requirements.txt
```

---

## Install Poppler

This project requires **Poppler** for PDF conversion.

Download Poppler for Windows and add the `bin` directory to your system PATH.

---

# ▶️ Running the Project

Place your PDF inside:

```
data/raw/
```

Then execute:

```bash
python -m app.main
```

---

# 📂 Output

During development, intermediate preprocessing results are automatically saved.

Example:

```
data/
│
├── processed/
│   ├── page_1_gray.png
│   ├── page_1_deskew.png
│   ├── page_1_denoised.png
│   ├── page_1_contrast.png
│   └── page_1_resized.png
```

These images allow visual verification of every preprocessing stage.

---

# 🧩 Design Principles

The project follows a modular architecture.

Each module has **one responsibility only**.

Example:

| Module | Responsibility |
|----------|----------------|
| Loader | Validate documents |
| PDF Converter | Convert PDF pages |
| Grayscale | RGB → Grayscale |
| Deskew | Correct rotation |
| Denoiser | Remove scanner noise |
| Contrast | Improve readability |
| Resize | Optimize resolution |

This modular design makes the pipeline:

- scalable
- maintainable
- reusable
- easy to test

---

# 📈 Current Progress

- [x] Project architecture
- [x] Document validation
- [x] PDF conversion
- [x] Grayscale preprocessing
- [x] Automatic deskew correction
- [x] Noise removal
- [x] Contrast enhancement
- [x] Image resizing
- [ ] OCR integration
- [ ] Document classification
- [ ] Information extraction
- [ ] Data validation
- [ ] Database integration
- [ ] RAG system

---

# 🛣️ Roadmap

## Phase 1 — Image Preprocessing ✅

- PDF loading
- Image enhancement
- Document normalization

---

## Phase 2 — OCR

- PaddleOCR integration
- Text detection
- Text recognition

---

## Phase 3 — Information Extraction

Automatic extraction of:

- Full Name
- CIN
- Date of Birth
- Salary
- Employer
- Bank Account
- Address

---

## Phase 4 — Validation

- Required fields
- Format validation
- Missing information detection

---

## Phase 5 — Database

Store extracted information into a structured database.

---

## Phase 6 — Retrieval-Augmented Generation (RAG)

Create an intelligent assistant capable of answering questions such as:

> "Show me all salary certificates submitted after January 2025."

> "What is the monthly salary declared in this file?"

---

# 📊 Future Improvements

- Multi-language OCR
- Signature detection
- Stamp detection
- QR Code extraction
- Barcode recognition
- Handwritten text recognition
- Automatic document classification
- Batch document processing

---

# 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a Pull Request.

---

# 📄 License

This project is released under the MIT License.

---

# 👩‍💻 Author

**Zineb Idrissi**

Master's Student in Artificial Intelligence & IOT

Université Ibn Tofaïl – Morocco

AI Engineering Intern @ Banque Populaire Morocco