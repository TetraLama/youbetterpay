from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import os

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

###
# Models
###
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    date_fin_recurrence = db.Column(db.DateTime, nullable=True)
    recurrent = db.Column(db.Boolean, nullable=False)
    recurrence_type = db.Column(db.String(80), nullable=True)
    recurrence_nombre_occurence = db.Column(db.Integer, nullable=True)
    reccurence_delta_temps = db.Column(db.Integer, nullable=True)
    compte = db.relationship('Comptes', backref='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.name}>'

class Comptes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)

    def __repr__(self):
        return f'<Compte {self.name}>'

###
# ROUTES
###
@app.route('/', methods=['GET'])
def index():
    users = User.query.all()
    return render_template('index.html.j2', users=users)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=True)