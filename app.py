from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#This is going to tell where our databse is located
#Three forward slashes is a relative path
#the test.db is telling what itll be stored as
db = SQLAlchemy(app)

class Todo(db.Model):
    #The model for our database
    #This can be modified to accomodate our Email database and submission
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #User cannot create a new task
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


#Index Route to browse URL without 404

@app.route('/', methods=['POST', 'GET'])
#After route, adding option called methods 
def index():
    if request.method == 'POST':
        #If the return method is equal to post which itself equals a submit
        #Command was: return 'Hello'
        #Can set this to return a new page that has "submit" which can be useful for the emails

        task_content = request.form['content']
        #task_content is a variable
        #pass in the id of the input, named content. task_content is equal to the content input
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        #New task will: create a new task from our tsk_content, try to commit to database, then redirect back to our '/'
        except:
            return 'There was an issue adding your task'
        #In exception if problem
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        #The above looks at the whole database contents according to date created and grabs all of them
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)