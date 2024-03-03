from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# sqlite:/// = relative path, sqlite://// = absolute path
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
# Initializing database with app
db = SQLAlchemy(app)

app.app_context().push()

# Creating classes
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Nullable prevents the user from entering a blank text
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Returns a string when completed
    def __repr__(self):
        return f"<Task {self.id}>"

@app.route("/", methods=["POST", "GET"])
def index():

    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error adding your task"

    else:
        # Looks into all database contents ordered by date created. all() returns all
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
