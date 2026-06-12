from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = \
'mysql+pymysql://root:root@localhost/cartoon_voting'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Character(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    votes = db.Column(
        db.Integer,
        default=0
    )

with app.app_context():

    db.create_all()

    if Character.query.count() == 0:

        characters = [
            Character(name="Doraemon"),
            Character(name="Shinchan"),
            Character(name="Motu Patlu"),
            Character(name="Chhota Bheem")
        ]

        db.session.add_all(characters)
        db.session.commit()
@app.route("/")
def home():
    characters=Character.query.all()
    winner=Character.query.order_by(Character.votes.desc()).first()
    return render_template("index.html",characters=characters,winner=winner)

@app.route('/vote/<int:id>')
def vote(id):

    character = Character.query.get_or_404(id)

    character.votes += 1

    db.session.commit()

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)