# Backend Setup Guide

## Virtual Environment Setup

First, create a Python virtual environment:
```bash
python -m venv .venv
```

Activate the virtual environment:

For Linux/MacOS:
```bash
source .venv/bin/activate
```

For Windows:
```bash
.venv\Scripts\activate
```

## Installation

Install required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI development server:
```bash
fastapi dev app/main.py
```