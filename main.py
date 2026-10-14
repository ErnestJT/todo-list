from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey, select
from forms import CategoryAddForm, FlaskForm, TaskAddForm, CategoryDeleteForm, TaskEditForm
from flask import session as session_data
import random

app = Flask(__name__)
app.secret_key = '239cf47561cc2db27067aeedc99d880cac52'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_list.db'

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Category(db.Model):
    __tablename__ = "categories"
    
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    tasks: Mapped[list["Task"]] = relationship()

    def __init__(self, category_name, tasks) -> None:
        self.category_name = category_name
        self.tasks = tasks

class Task(db.Model):
    __tablename__ = "tasks"
    
    task_id: Mapped[int] = mapped_column(Integer,primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), nullable=False)
    task_description: Mapped[str] = mapped_column(String(500), nullable=False)
    due_date: Mapped[str] = mapped_column(String(100), nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    color: Mapped[str] = mapped_column(String(50), nullable=False)
    is_highlighted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    
    def __init__(self, category_id, task_description, due_date, is_completed,
                 color, is_highlighted) -> None:
        self.category_id = category_id
        self.task_description = task_description
        self.due_date = due_date
        self.is_completed = is_completed
        self.color = color
        self.is_highlighted = is_highlighted
    
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'task_description': self.task_description,
            'due_date': self.due_date,
            'is_completed': self.is_completed,
            'color': self.color,
            'is_highlighted': self.is_highlighted
        }

with app.app_context():
    db.create_all()
        

@app.route('/', methods=['GET','POST'])
def todo_list():
    select_form = FlaskForm()
    category_add_form = CategoryAddForm()
    category_delete_form = CategoryDeleteForm()
    task_add_form = TaskAddForm()
    task_edit_form = TaskEditForm()
    
    category_list = db.session.execute(select(Category)).scalars().all()
    category_id = session_data.get('category_id', '')
    
    
    if not category_id:
        task_list = []
    else:
        task_list = db.session.execute(select(Task).where(Task.category_id == category_id)).scalars().all()
    
    if request.method == 'POST':
        category_id = request.form.get('category-list')
        session_data['category_id'] = category_id
        
        task_list = db.session.execute(select(Task).where(Task.category_id == category_id)).scalars().all()
        
    
    return render_template('index.html', category_select_form=select_form, 
                           category_add_form=category_add_form, task_add_form=task_add_form,
                           categories=category_list, tasks=task_list,
                           category_delete_form=category_delete_form,
                           task_edit_form=task_edit_form)

@app.route('/create-category', methods=['POST'])
def create_category():
    
    category_name = request.form['category_add_field']
    
    new_category = Category(category_name=category_name, tasks=[])
    db.session.add(new_category)
    db.session.commit()

    return redirect('/')

@app.route('/delete-category', methods=['POST'])
def delete_category():
    category_id = session_data['category_id']
    if not category_id:
        return redirect('/')
    
    selected_category = db.session.execute(select(Category).where(Category.category_id == category_id)).scalars().all()[0]
    for task in selected_category.tasks:
        db.session.delete(task)
    db.session.delete(selected_category)
    db.session.commit()
    return redirect('/')

@app.route('/get-task/<int:task_id>', methods=['POST'])
def get_task(task_id):
    selected_task = db.session.execute(select(Task).where(Task.task_id == task_id)).scalar_one()
    
    return jsonify(selected_task.to_dict())
    
@app.route('/add-task', methods=['POST'])
def add_task():
    category_id = session_data.get('category_id')

    new_task = Task(category_id=category_id,
                    task_description= request.form['task_add_field'],
                    due_date='N/A', is_completed=False, 
                    color=f"#{random.randint(0, 0xFFFFFF):06x}" , 
                    is_highlighted=False)
    db.session.add(new_task)
    
    selected_category = db.session.execute(select(Category).where(Category.category_id == category_id)).scalars().all()[0]
    selected_category.tasks.append(new_task)
    
    db.session.commit()
    return redirect('/')

@app.route('/change-state/<int:task_id>', methods=['POST'])
def change_task_state(task_id):
    task = db.session.execute(select(Task).where(Task.task_id == task_id)).scalars().all()[0]
    if task.is_completed:
        task.is_completed = False
    else:
        task.is_completed = True
    db.session.commit()
    return redirect('/')

@app.route('/edit-task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    selected_task = db.session.execute(select(Task).where(Task.task_id == task_id)).scalar_one()
    
    selected_task.color = request.form['color_field']
    selected_task.task_description = request.form['name_field']
    selected_task.due_date = request.form['date_field']

    db.session.commit()
    return redirect('/')
    
@app.route('/highlight-task/<int:task_id>')
def highlight_task(task_id):
    task = db.session.execute(select(Task).where(Task.task_id == task_id)).scalar_one()
    if task.is_highlighted:
        task.is_highlighted = False
    else:
        task.is_highlighted = True
    db.session.commit()
    return redirect('/')

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    selected_task = db.session.execute(select(Task).where(Task.task_id == task_id)).scalar()
    db.session.delete(selected_task)
    db.session.commit()
    
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)