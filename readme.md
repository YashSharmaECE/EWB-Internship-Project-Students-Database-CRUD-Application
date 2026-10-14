# EWB Internship Project: Students Database CRUD Application

This repository contains the backend source code for the Students Database CRUD Application, developed as part of the EWB Edu Tech Pvt. Ltd. Internship Program. The application is built using Python, FastAPI, and SQLite for persistent data storage. It also features an optional local AI integration using Ollama.

## Features
* **Full CRUD Operations:** Create, Read (List/View), Update, and Delete student records.
* **Persistent Storage:** Data is securely saved using a local SQLite database (`students.db`).
* **Input Validation:** Ensured via Pydantic models.
* **AI Extension (Bonus):** Natural language querying of database records using a local Ollama model (llama3.2:1b).

## Prerequisites
Before running this project, ensure you have the following installed on your system:
* Python 3.8+
* `pip` (Python package installer)
* [Ollama](https://ollama.com/) (Only required for the optional AI feature)

## Installation & Setup

1. **Clone the repository** (if applicable) or download the project folder.
2. **Create a virtual environment:**

## Screenshots
<img width="1920" height="1080" alt="Screenshot (129)" src="https://github.com/user-attachments/assets/a6a157b5-0860-4fbf-b736-8dcc963417db" />

   ```bash
   python -m venv venv
