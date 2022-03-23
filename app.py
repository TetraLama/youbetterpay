from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
import os
import click

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY="dev",
    SQLALCHEMY_DATABASE_URI="sqlite:///{}".format(
        os.path.join(app.instance_path, "db.sqlite")
    ),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db = SQLAlchemy(app)


def init_db():
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


app.cli.add_command(init_db_command)


class Bank(db.Model):
    __tablename__ = "bank"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class TransactionType(db.Model):
    __tablename__ = "transaction_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    ammount = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)
    recursive = db.Column(db.Boolean, nullable=False)
    prelevement_day = db.Column(db.Integer, nullable=True)

    transaction_type_id = db.Column(
        db.Integer, db.ForeignKey("transaction_type.id"), nullable=False
    )
    transaction_type = db.relationship(
        "TransactionType", backref=db.backref("transactions", lazy=True)
    )

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    account = db.relationship("Account", backref=db.backref("accounts", lazy=True))

    def __init__(
        self, name, description, monthly, prelevement_day, transaction_type, account
    ):
        self.name = name
        self.description = description
        self.monthly = monthly
        self.prelevement_day = prelevement_day
        self.transaction_type = transaction_type
        self.account = account

    def __repr__(self):
        return "%r" % self.name


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    bank_id = db.Column(db.Integer, db.ForeignKey("bank.id"), nullable=False)
    bank = db.relationship("Bank", backref=db.backref("accounts", lazy=True))

    def __init__(self, name, bank):
        self.name = name
        self.bank = bank

    def __repr__(self):
        return "%r" % self.name


@app.route("/")
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/account")
def dashboard_account():
    return render_template("dashboard_account.html", accounts=Account.query.all())


@app.route("/bank")
def dashboard_bank():
    return render_template(
        "dashboard_bank.html", banks=Bank.query.all(), accounts=Account.query.all()
    )


@app.route("/transaction")
def dashboard_transaction():
    return render_template(
        "dashboard_transaction.html", transactions=Transaction.query.all()
    )


@app.route("/transaction_type")
def dashboard_transaction_type():
    return render_template(
        "dashboard_transaction_type.html",
        transactions_type=TransactionType.query.all(),
    )


@app.route("/bank/add", methods=["GET", "POST"])
def new_bank():
    if request.method == "POST":
        if not request.form["name"]:
            flash("Please enter all the fields", "error")
        else:
            bank = Bank(request.form["name"])

            db.session.add(bank)
            db.session.commit()
            flash("Bank was successfully added", "info")
            return redirect(url_for("dashboard_bank"))
    return render_template("add_edit_bank.html")


@app.route("/bank/del/<int:id>", methods=["GET"])
def delete_bank(id):
    bank = Bank.query.get(id)
    flash("Bank {} deleted".format(bank), "info")
    db.session.delete(bank)
    db.session.commit()
    return redirect(url_for("dashboard_bank"))


@app.route("/bank/edit/<int:id>", methods=["GET", "POST"])
def edit_bank(id):
    bank = Bank.query.get(id)
    if request.method == "POST":
        bank.name = request.form["name"]
        db.session.add(bank)
        db.session.commit()
        flash("Bank {} edited".format(bank), "info")
        return redirect(url_for("dashboard_bank"))
    else:
        return render_template("add_edit_bank.html", bank=bank)


@app.route("/account/add", methods=["GET", "POST"])
def new_account():
    if request.method == "POST":
        if not request.form["name"] or not request.form["bank"]:
            flash("Please enter all the fields", "error")
        else:
            bank = Bank.query.filter_by(name=request.form["bank"]).first_or_404()
            account = Account(request.form["name"], bank)
            db.session.add(account)
            db.session.commit()
            flash("Account was successfully added")
            return redirect(url_for("dashboard_account"))
    return render_template(
        "add_edit_account.html",
        banks=Bank.query.all(),
    )


@app.route("/account/del/<int:id>", methods=["GET"])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    flash("Account {} deleted".format(account), "info")
    return redirect(url_for("accounts"))


@app.route("/account/edit/<int:id>", methods=["GET", "POST"])
def edit_account(id):
    account = Account.query.get(id)
    if request.method == "POST":
        account.name = request.form["name"]
        account.bank = request.form["bank"]
        db.session.add(account)
        db.session.commit()
        flash("Account type {} edited".format(account), "info")
        return redirect(url_for("dashboard_transaction_type"))
    else:
        return render_template(
            "add_edit_account.html", account=account, banks=Bank.query.all()
        )


@app.route("/transaction/add", methods=["GET", "POST"])
def new_transaction():
    if request.method == "POST":
        if (
            not request.form["name"]
            or not request.form["monthly"]
            or not request.form["transaction_type"]
            or not request.form["account"]
        ):
            flash("Please enter all the fields", "error")
        else:
            transaction = Transaction(
                name=request.form["name"],
                description=request.form["description"],
                namonthlyme=request.form["monthly"],
                prelevement_day=request.form["prelevement_day"],
                transaction_type=request.form["transaction_type"],
                account=request.form["account"],
            )
            db.session.add(new_transaction)
            db.session.commit()
            flash("Transaction {} was successfully added".format(transaction.name))
            return redirect(url_for("dashboard_transaction_type"))
    return render_template(
        "add_edit_transaction.html", transactions=Transaction.query.all()
    )


@app.route("/transaction/del/<int:id>", methods=["GET"])
def delete_transaction(id):
    transaction = Transaction.query.get(id)
    db.session.delete(transaction)
    db.session.commit()
    flash("Account type {} deleted".format(transaction), "info")
    return redirect(url_for("dashboard_transaction"))


@app.route("/transaction/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    transaction = Transaction.query.get(id)
    if request.method == "POST":
        transaction.name = request.form["name"]
        transaction.description = (request.form["description"],)
        transaction.namonthlyme = (request.form["monthly"],)
        transaction.prelevement_day = (request.form["prelevement_day"],)
        transaction.transaction_type = (request.form["transaction_type"],)
        transaction.account = (request.form["account"],)
        db.session.add(transaction)
        db.session.commit()
        flash("Transaction {} edited".format(transaction), "info")
        return redirect(url_for("dashboard_transaction_type"))
    else:
        return render_template("add_edit_transaction.html", transaction=transaction)


@app.route("/transaction_type/add", methods=["GET", "POST"])
def new_transaction_type():
    if request.method == "POST":
        if not request.form["name"]:
            flash("Please enter all the fields", "error")
        else:
            transaction_type = TransactionType(request.form["name"])
            db.session.add(transaction_type)
            db.session.commit()
            flash(
                "Transaction type {} was successfully added".format(
                    transaction_type.name
                ),
                "info",
            )
            return redirect(url_for("dashboard_transaction_type"))
    return render_template("add_edit_transaction_type.html")


@app.route("/transaction_type/del/<int:id>", methods=["GET"])
def delete_transaction_type(id):
    transaction_type = TransactionType.query.get(id)
    db.session.delete(transaction_type)
    db.session.commit()
    flash("Account type {} deleted".format(transaction_type), "info")
    return redirect(url_for("dashboard_transaction_type"))


@app.route("/transaction_type/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction_type(id):
    transaction_type = TransactionType.query.get(id)
    if request.method == "POST":
        transaction_type.name = request.form["name"]
        db.session.add(transaction_type)
        db.session.commit()
        flash("Account type {} edited".format(transaction_type), "info")
        return redirect(url_for("dashboard_transaction_type"))
    else:
        return render_template(
            "add_edit_transaction_type.html", transaction_type=transaction_type
        )


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
