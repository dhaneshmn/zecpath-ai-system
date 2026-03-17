# Zecpath AI Hiring Platform

## Overview
The Zecpath AI Recruitment System is an intelligent hiring platform designed to automate the recruitment workflow using Artificial Intelligence. The system processes resumes, analyzes candidate qualifications, matches candidates with job descriptions, and supports recruiters in making efficient hiring decisions. The project is designed using a modular AI architecture, where different AI engines handle specific parts of the recruitment pipeline.

## Project Objectives
- Automate resume processing and candidate screening
- Convert unstructured resumes into structured AI-ready data
- Match candidate profiles with job requirements
- Improve recruitment efficiency through AI-assisted decision making
- Build a scalable architecture for future AI modules


This repository houses the **AI microservices** that power resume parsing, ATS scoring, voice screening, video interviews, technical assessments, and final offer generation. The system is designed for high availability, horizontal scalability, and seamless integration with the Zecpath backend.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development Progress (Days 1–5)](#development-progress-days-15)
  - [Day 1: PRD & AI Blueprint](#day-1-prd--ai-blueprint)
  - [Day 2: Microservices Architecture](#day-2-microservices-architecture)
  - [Day 3: Environment & Repository Setup](#day-3-environment--repository-setup)
  - [Day 4: Data Modelling & JSON Schemas](#day-4-data-modelling--json-schemas)
  - [Day 5: Resume Text Extraction Engine](#day-5-resume-text-extraction-engine)
- [Usage](#usage)
- [Testing](#testing)
- [Logging & Monitoring](#logging--monitoring)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## System Architecture

Zecpath AI follows a **microservices** pattern, where each AI capability is isolated into its own service. Services communicate via REST APIs for synchronous requests (e.g., resume upload → ATS scoring) and a message broker (RabbitMQ/AWS SQS) for asynchronous, long‑running tasks (e.g., outbound voice calls, interview scheduling). All services are stateless, allowing independent deployment and scaling.

![Architecture Diagram](docs/architecture.png)  
*(A Mermaid version is available in `docs/architecture.md`)*

**Key services:**
- **ATS AI** – Resume parsing, skill extraction, candidate scoring.
- **Voice AI** – Outbound calls, conversational screening, multilingual TTS/STT.
- **Interview Intelligence** – HR and technical interviews with dynamic questioning.
- **Behavior Analysis** – Facial expression, gaze tracking, malpractice detection.
- **Decision Engine** – Multi‑round score aggregation and final recommendation.
- **Offer Management** – Automated offer letter generation and acceptance tracking.

---

## Tech Stack

- **Languages:** Python 3.10+ (primary), Node.js (ancillary services)
- **AI/ML:** spaCy, Hugging Face Transformers, OpenAI API, custom PyTorch models
- **Voice:** Twilio, AWS Connect, Google TTS/STT
- **Video:** WebRTC (Daily.co / Twilio Video), OpenCV (face detection)
- **Data Storage:** PostgreSQL (relational), MongoDB (flexible profiles), Redis (cache)
- **Message Broker:** RabbitMQ / AWS SQS
- **Containerisation:** Docker, Kubernetes (for orchestration)
- **CI/CD:** GitHub Actions, ArgoCD
- **Monitoring:** Prometheus, Grafana, ELK stack

---

## Project Structure
 
```
zecpath-ai/
├── .github/                    # GitHub workflows
├── docs/                       # Architecture diagrams, design docs
├── data/
│   ├── raw_resumes/            # Original resumes (PDF/DOCX) for testing
│   └── extracted/              # Cleaned text + metadata from pipeline
├── parsers/                    # Text extraction modules
│   ├── __init__.py
│   ├── pdf_parser.py           # PDF text extractor (pdfplumber)
│   ├── docx_parser.py          # DOCX text extractor (python-docx)
│   └── extraction_pipeline.py  # End-to-end extraction pipeline
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Centralised logging setup
│   └── text_cleaner.py         # Unicode normalisation, bullet replacement, whitespace cleanup
├── tests/
│   ├── __init__.py
│   └── test_extractors.py      # Unit tests for extractors & pipeline
├── logs/                       # Runtime logs
├── scripts/                    # Utility scripts (e.g., run_extraction.py)
├── .gitignore
├── .pre-commit-config.yaml     # Pre-commit hooks (black, flake8)
├── pyproject.toml              # Black configuration
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies (pytest, black, etc.)
└── README.md                   # This file
```
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.10 or higher
- Git
- (Optional) Docker
 
### Installation
 
1. **Clone the repository**
   ```bash
   git clone https://github.com/zecpath/zecpath-ai.git
   cd zecpath-ai
   ```
 
2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
 
3. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```
 
4. **Set up pre-commit hooks** *(optional but recommended)*
   ```bash
   pre-commit install
   ```
 
5. **Add sample resumes**  
   Place at least one PDF and one DOCX file in `data/raw_resumes/`.  
   *(Avoid temporary Word files like `~$...` – they will be ignored.)*
 
---
 
## Development Progress (Days 1–5)
 
### Day 1: PRD & AI Blueprint
 
- Thoroughly analysed the 100-phase PRD.
- Mapped the entire hiring lifecycle: job posting → ATS → voice screening → HR interview → technical interview → machine test → salary negotiation → offer.
- Identified 18+ distinct AI engines and their responsibilities.
- Produced a **Hiring Lifecycle Flowchart** and an **AI Responsibilities Overview** document.
 
### Day 2: Microservices Architecture
 
- Designed a decoupled, event-driven architecture with dedicated AI services.
- Defined input/output contracts for each engine (see `docs/io_specs.md`).
- Chose communication patterns:
  - **REST** for synchronous, low-latency operations (e.g., resume upload → ATS).
  - **Message queues** for asynchronous tasks (e.g., triggering voice calls, batch scoring).
- Created architecture and data flow diagrams (Mermaid) to visualise system interactions.
 
### Day 3: Environment & Repository Setup
 
- Initialised Git repository with a comprehensive `.gitignore`.
- Set up Python virtual environment and installed core libraries (`pdfplumber`, `python-docx`, `pytest`).
- Designed a modular folder structure (`parsers`, `utils`, `tests`, `data`).
- Implemented a centralised logging module (`utils/logger.py`) that writes to both console and file.
- Integrated `pytest` with a placeholder test.
- Wrote a detailed `README.md` to document setup and conventions.
 
### Day 4: Data Modelling & JSON Schemas
 
- Analysed 10+ resumes from diverse domains (tech, sales, HR, fresher, experienced).
- Identified common fields: personal info, skills, work experience, education, certifications, projects.
- Defined standardised data entities:
  - `CandidateProfile`
  - `JobProfile`
  - `Skill` (with aliases for normalisation)
- Designed JSON schemas (draft-07) for both resume and job description data — used for validation and as the interchange format between services.
- Documented schemas and field mappings in `docs/data_entity_design.md`.
 
### Day 5: Resume Text Extraction Engine
 
- Implemented a robust **PDF extractor** (`parsers/pdf_parser.py`) using `pdfplumber` — handles multi-page PDFs and logs pages with no text.
- Implemented a **DOCX extractor** (`parsers/docx_parser.py`) using `python-docx` — extracts paragraphs and table cells.
- Built a **text cleaner** (`utils/text_cleaner.py`) that:
  - Normalises Unicode (NFKC) to fix smart quotes and em dashes.
  - Replaces common bullet characters (`•`, `▪`, `→`) with a standard dash `-`.
  - Collapses multiple spaces and newlines while preserving paragraph breaks.
- Created an **extraction pipeline** (`parsers/extraction_pipeline.py`) that:
  - Detects file type by extension.
  - Calls the appropriate extractor.
  - Cleans the raw text.
  - Saves cleaned text as `.txt` and metadata (word count, length, etc.) as `.json` in `data/extracted/`.
- Wrote comprehensive **unit tests** (`tests/test_extractors.py`) covering:
  - PDF extraction on all PDFs in `data/raw_resumes/`.
  - DOCX extraction on all DOCX files.
  - Full pipeline execution (including saving files).
- Verified that logs are written to `logs/ai_activities.log`.
