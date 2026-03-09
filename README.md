# Zecpath AI System

## Overview
The Zecpath AI Recruitment System is an intelligent hiring platform designed to automate the recruitment workflow using Artificial Intelligence. The system processes resumes, analyzes candidate qualifications, matches candidates with job descriptions, and supports recruiters in making efficient hiring decisions. The project is designed using a modular AI architecture, where different AI engines handle specific parts of the recruitment pipeline.

## Project Objectives
- Automate resume processing and candidate screening
- Convert unstructured resumes into structured AI-ready data
- Match candidate profiles with job requirements
- Improve recruitment efficiency through AI-assisted decision making
- Build a scalable architecture for future AI modules

## Project Layout
The repository follows a modular folder structure to keep the project organized, scalable, and maintainable.
```text
zecpath-ai-system/
│
├── data/                 # Stores resumes, datasets, and processed files
│
├── parsers/              # Resume parsing and text extraction modules
│
├── ats_engine/           # Candidate-job matching logic (ATS scoring)
│
├── screening_ai/         # AI models used for candidate screening
│
├── interview_ai/         # AI modules for interview analysis
│
├── scoring/              # Candidate ranking and final scoring
│
├── utils/                # Shared utilities (logging, helper functions)
│
├── tests/                # Automated unit tests
│
├── logs/                 # System logs generated during execution
│
├── main.py               # Entry point for the system
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .gitignore
```