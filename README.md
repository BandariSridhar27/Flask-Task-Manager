# Flask Task Manager

A simple CRUD Task Manager app built with Python Flask and SQLite.

## Features
- Add, edit, delete, and duplicate tasks
- Mark tasks as Done
- Task status tracking: Pending, In Progress, Done
- Bootstrap-styled UI
- Export tasks to CSV
- User login/authentication (optional)
- SQLite database

## Setup & Run Locally

```bash
git clone https://github.com/yourusername/flask-task-manager.git
cd flask-task-manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
