from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myapp:mypass@postgres:5432/mydb'
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<Note %r>' % self.id


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "POST":
        note_content = request.form["content"]
        new_note = Note(content=note_content)
        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return "something went wrong with adding note"

    else:
        notes = Note.query.order_by(Note.date_created).all()
        return render_template('index.html', notes=notes)


@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Note.query.get_or_404(id)
    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "something went wrong with deleting note"

@app.route('/update/<int:id>', methods=["POST", "GET"])
def update(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        note.content = request.form["content"]
        try:
            db.session.commit()
            return redirect('/')
        except:
            "something went wrong with updatind note"
    else:
        return render_template("update.html", note=note)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
