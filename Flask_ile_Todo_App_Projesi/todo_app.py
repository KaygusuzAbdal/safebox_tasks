from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123asd@localhost/TodoAppDb'
db = SQLAlchemy(app)


class Tasks(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(250), nullable=False)
    Status = db.Column(db.Integer)

    def __repr__(self):
        return '<Todo %r>' % self.ID


class Status(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.ID


@app.route("/")
def home():
    todo_list = Tasks.query.order_by(Tasks.Status).all()
    status_list = Status.query.all()
    print(todo_list)
    return render_template("index.html", tasks=todo_list, statuses=status_list)


@app.route("/add", methods=["GET"])
def add_page():
    return render_template("add.html")


@app.route("/add", methods=["POST"])
def add_task():
    todo_name = request.form['Name']
    new_todo = Tasks(Name=todo_name, Status=1)
    try:
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    except:
        return 'Veritabanına eklenirken bir hata oluştu!'


@app.route('/delete/<int:id>', methods=["POST"])
def delete(id):
    todo_to_delete = Tasks.query.get_or_404(id)
    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Veritabanından silinirken bir hata oluştu!'


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Tasks.query.get_or_404(id)
    status_list = Status.query.all()
    if request.method == 'POST':
        todo.Name = request.form['Name']
        todo.Status = request.form['Status']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Veritabanında güncelleme yapılırken bir hata oluştu!'
    else:
        return render_template('edit.html', task=todo, statuses=status_list)


@app.route("/add_stat", methods=["GET", "POST"])
def add_status():
    if request.method == "POST":
        stat_name = request.form['Name']
        new_stat = Status(Name=stat_name)
        try:
            db.session.add(new_stat)
            db.session.commit()
            return redirect('/')
        except:
            return 'Veritabanına eklenirken bir hata oluştu!'
    else:
        return render_template("add_stat.html")


if __name__ == "__main__":
    app.run(debug=True, port=8080)
