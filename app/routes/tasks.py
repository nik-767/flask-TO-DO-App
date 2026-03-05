from flask import Blueprint , render_template, request , redirect , url_for , session , flash
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks' , __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@tasks_bp.route('/add', methods= ["POST"])
def add_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    
    title = request.form.get('title')
    if title:
        new_tasks = Task(title=title, status='pending')
        db.session.add(new_tasks)
        db.session.commit()
        flash('Task added successfully' , 'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    task = Task.query.get(task_id)
    if task:
        if task.status == 'pending':
            task.status = 'Done'
        else:
            task.status = 'pending'
        db.session.commit()
    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
    return redirect(url_for('tasks.view_tasks'))
