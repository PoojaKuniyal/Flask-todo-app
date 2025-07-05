# static and templates - 2 directories in the same folder as app.py and env
# flask sql-alchemy package for creating database

from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(10), default="Pending")  # Done or Pending
    deadline = db.Column(db.String(50), nullable=True)
    priority = db.Column(db.String(10), nullable=True)
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"{self.sno} - {self.title}"
    
@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        deadline = request.form.get('deadline')
        priority = request.form.get('priority')
        
        todo =Todo(title=title, desc=desc, deadline=deadline, priority=priority) # object create
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()

    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        todo.deadline = request.form.get('deadline')
        todo.priority = request.form.get('priority')
        todo.status = request.form.get('status', 'Pending')
        
        db.session.commit()
        return redirect('/')
    
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first() 
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/toggle/<int:sno>', methods=['POST'])
def toggle_status(sno):
    todo = Todo.query.get(sno)
    todo.status = 'Done' if todo.status == 'Pending' else 'Pending'
    db.session.commit()
    return redirect('/')


# if __name__ =='__main__':
#     print("Starting Flask app…")
#     app.run(debug=True) 


# if you are testing db setup and in the powershell 
# from app import db  db.create_all() doesnt work run below code then comment it after creation
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Starting Flask app…")
    app.run(debug=True)