from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for flash messages

# Create DB table if not exists
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

# Homepage - Show all tasks
@app.route('/')
def index():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Add a task
@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Edit page
@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    conn.close()
    return render_template('edit.html', task=task)

# Update task
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    title = request.form['title']
    description = request.form['description']
    status = request.form['status']
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET title=?, description=?, status=? WHERE id=?", (title, description, status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Delete task
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# Duplicate task
@app.route('/duplicate/<int:id>')
def duplicate(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT title, description, status FROM tasks WHERE id=?", (id,))
    task = c.fetchone()
    c.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", task)
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# **Mark Task as Done**
@app.route('/mark_done/<int:id>', methods=['POST'])
def mark_done(id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("UPDATE tasks SET status='Done' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Task marked as done!", "success")  # Flash message for confirmation
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)