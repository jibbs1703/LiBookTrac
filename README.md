# LiBookTrac: A Library Management System

![Python Version](https://img.shields.io/badge/python-3.12-blue)
![CI](https://github.com/jibbs1703/LiBookTrac/actions/workflows/CI.yaml/badge.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-v0.116-blue?logo=fastapi&style=flat)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-v16-blue?logo=postgresql&style=flat)
![Docker](https://img.shields.io/badge/Docker-v41-blue?logo=docker&style=flat)
![Nginx](https://img.shields.io/badge/Nginx-v1.28-green?logo=nginx&style=flat)
![pre-commit](https://img.shields.io/badge/precommit-enabled-yellow)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)
![license](https://img.shields.io/github/license/peaceiris/actions-gh-pages.svg)

## Overview

LiBookTrac is an efficient library management system developed to streamline the management and tracking of
library resources. Leveraging the capabilities of **Pydantic** and **FastAPI**, this project offers a robust
and high-performance solution for both library administrators and users.

## Features

- **User Management:** Add, update, and manage library users effortlessly.
- **Book Management:** Comprehensive features for adding, updating, and removing books from the collection.
- **Loan Management:** Efficiently track and manage book borrowings and returns.
- **Search Functionality:** Powerful search capabilities to quickly locate books and users.
- **API Documentation:** Automatically generated and interactive API documentation using FastAPI.

## Technologies Used

- **FastAPI:** A modern web framework for building APIs with Python based on standard Python type hints.
- **Pydantic:** Data validation and settings management using Python type annotations.
- **PostgreSQL:**  A relational database management system for storing library data.

## Getting Started

- **Clone the repository:**
```bash
git clone https://github.com/your-username/LiBookTrac.git
cd LiBookTrac
```

- **Create and Activate Virtual Environment:**
```bash
python -m venv libooktrac
libooktrac\Scripts\activate

```

- **Install Project Requirements:**
```bash
pip install -r requirements.txt
```

- **Run Library Management Application Locally:**
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8008
```

- **Run Library Management Application in Container:**
```bash
docker build -f backend.Dockerfile -t libooktrac:latest .
docker rm -f libooktrac-env || true # Remove existing container if it exists
docker run -it --name libooktrac-env -v .:/workspace -p 8000:8000 libooktrac:latest
docker exec -it libooktrac-env sh
```

- TODO

- use isbn check to input book details (external API exists)
