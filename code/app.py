from flask import Flask, request, render_template, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
###
# Models
###
class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), unique=True, nullable=False)
    montant = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
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
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=True)

    def __repr__(self):
        return f'<Compte {self.name}>'
    


###
# ROUTES
###
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@app.route('/comptes', methods=['GET'])
def home_comptes():
    list_comptes = Comptes.query.all()
    return render_template('home_comptes.html.j2', list_comptes=list_comptes)

@app.route('/comptes/create', methods=('GET', 'POST'))
def ajouter_compte():
    if request.method == 'POST':
        nom = request.form['nom_compte']
        error = None

        if not nom:
            error = 'Nom est recquis.'

        if error is not None:
            flash(error)
        else:
            nouveau_compte = Comptes(nom=nom)
            db.session.add(nouveau_compte)
            db.session.commit()
            return redirect(url_for('home_comptes'))

    return render_template('ajout_compte.html.j2')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    app.run(debug=True)