from flask import Flask, render_template, url_for, redirect, json, flash, request
import requests
from werkzeug.exceptions import HTTPException
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

API_URL = "http://api:8082"
API_URL_ACCOUNT = f"{API_URL}/api/v1/accounts"
API_URL_TYPE = f"{API_URL}/api/v1/types"
API_URL_TRANSACTION = f"{API_URL}/api/v1/transactions"
API_URL_CATEGORY = f"{API_URL}/api/v1/categories"


def get_all_accounts() -> list:
    response = requests.request(method="GET", url=API_URL_ACCOUNT)
    return response.json()


def get_all_categories() -> list:
    response = requests.request(method="GET", url=API_URL_CATEGORY)
    return response.json()


def get_all_transactions() -> list:
    response = requests.request(method="GET", url=API_URL_TRANSACTION)
    return response.json()


def get_all_types() -> list:
    response = requests.request(method="GET", url=API_URL_TYPE)
    return response.json()


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/accounts", methods=["GET", "POST"])
def list_all_accounts():
    if request.method == "GET":
        list_accounts = get_all_accounts()
        app.logger.debug(list_accounts["data"][0])
        return render_template("accounts.html", accounts=list_accounts["data"][0])

    if request.method == "POST":
        account_name = request.form.get("account_name")
        if not account_name:
            flash("You MUST specify a name", "error")
        else:
            data = {"name": account_name}
            response = requests.request(method="POST", url=API_URL_ACCOUNT, json=data)
            if response.status_code != 200:
                flash(f"Something went wrong while adding {account_name}", "error")
        return redirect(url_for("list_all_accounts"))


@app.route("/accounts/<account_id>", methods=["GET"])
def account_detail(account_id):
    url = f"{API_URL_ACCOUNT}/{account_id}"
    response = requests.request(method="GET", url=url)
    if response.status_code == 500:
        app.logger.critical(f"Something went wrong while getting {account_id}", "error")
        flash(f"Something went wrong while getting {account_id}", "error")
    app.logger.debug(response)
    account = response.json()
    return render_template("account_detail.html", account=account["data"][0])


@app.route("/accounts/delete/<account_id>", methods=["GET"])
def account_delete(account_id):
    url = f"{API_URL_ACCOUNT}/{account_id}"
    response = requests.request(method="DELETE", url=url)
    if response.status_code == 500:
        flash(f"Something went wrong while removing {account_id}", "error")
    return redirect(url_for("list_all_accounts"))


###
# TYPES
###
@app.route("/types", methods=["GET", "POST"])
def list_all_types():
    if request.method == "GET":
        list_types = get_all_types()
        app.logger.debug(list_types["data"][0])
        return render_template("types.html", types=list_types["data"][0])

    if request.method == "POST":
        type_name = request.form.get("type_name")
        if not type_name:
            flash("You MUST specify a name", "error")
        else:
            data = {"name": type_name}
            response = requests.request(method="POST", url=API_URL_TYPE, json=data)
            if response.status_code != 200:
                flash(f"Something went wrong while adding {type_name}", "error")
        return redirect(url_for("list_all_types"))


@app.route("/types/<type_id>", methods=["GET"])
def type_detail(type_id):
    url = f"{API_URL_TYPE}/{type_id}"
    response = requests.request(method="GET", url=url)
    if response.status_code == 500:
        app.logger.critical(f"Something went wrong while getting {type_id}", "error")
        flash(f"Something went wrong while getting {type_id}", "error")
    app.logger.debug(response)
    type = response.json()
    return render_template("type_detail.html", type=type["data"][0])


@app.route("/types/delete/<type_id>", methods=["GET"])
def type_delete(type_id):
    url = f"{API_URL_TYPE}/{type_id}"
    response = requests.request(method="DELETE", url=url)
    if response.status_code == 500:
        flash(f"Something went wrong while removing {type_id}", "error")
    return redirect(url_for("list_all_types"))


###
# CATEGORIES
###
@app.route("/categories", methods=["GET", "POST"])
def list_all_categories():
    if request.method == "GET":
        list_categories = get_all_categories()
        app.logger.debug(list_categories["data"][0])
        return render_template("categories.html", categories=list_categories["data"][0])

    if request.method == "POST":
        category_name = request.form.get("category_name")
        if not category_name:
            flash("You MUST specify a name", "error")
        else:
            data = {"name": category_name}
            response = requests.request(method="POST", url=API_URL_CATEGORY, json=data)
            if response.status_code != 200:
                flash(f"Something went wrong while adding {category_name}", "error")
        return redirect(url_for("list_all_categories"))


@app.route("/categories/<category_id>", methods=["GET"])
def category_detail(category_id):
    url = f"{API_URL_CATEGORY}/{category_id}"
    response = requests.request(method="GET", url=url)
    if response.status_code == 500:
        app.logger.critical(
            f"Something went wrong while getting {category_id}", "error"
        )
        flash(f"Something went wrong while getting {category_id}", "error")
    app.logger.debug(response)
    category = response.json()
    return render_template("category_detail.html", category=category["data"][0])


@app.route("/categories/delete/<category_id>", methods=["GET"])
def category_delete(category_id):
    url = f"{API_URL_CATEGORY}/{category_id}"
    response = requests.request(method="DELETE", url=url)
    if response.status_code == 500:
        flash(f"Something went wrong while removing {category_id}", "error")
    return redirect(url_for("list_all_categories"))


###
# TRANSACTIONS
###
@app.route("/transactions", methods=["GET", "POST"])
def list_all_transactions():
    if request.method == "GET":
        list_transactions = get_all_transactions()
        list_types = get_all_types()
        list_categories = get_all_categories()
        list_accounts = get_all_accounts()

        return render_template(
            "transactions.html",
            transactions=list_transactions["data"][0],
            types=list_types["data"][0],
            categories=list_categories["data"][0],
            accounts=list_accounts["data"][0],
        )

    if request.method == "POST":
        if not request.form.get("description"):
            flash("You MUST specify a description", "error")
        else:
            data = {"description": request.form.get("description")}

            if request.form.get("target_account"):
                data["target_account"] = request.form.get("target_account")

            if (
                request.form.get("dest_account")
                and request.form.get("dest_account") is not None
            ):
                data["dest_account"] = request.form.get("dest_account")

            if request.form.get("ammount"):
                data["ammount"] = request.form.get("ammount")

            if (
                request.form.get("ammount_is_calculated")
                and request.form.get("ammount_is_calculated") is not None
            ):
                data["ammount_is_calculated"] = request.form.get(
                    "ammount_is_calculated"
                )

            if request.form.get("category"):
                data["category"] = request.form.get("category")

            if request.form.get("type"):
                data["type"] = request.form.get("type")

            if request.form.get("date") or request.form.get("date") is not None:
                data["date"] = request.form.get("date")

            if (
                request.form.get("is_reccurent")
                and request.form.get("is_reccurent") is not None
            ):
                data["is_reccurent"] = request.form.get("is_reccurent")

            if (
                request.form.get("frequency_every_number")
                and request.form.get("frequency_every_number") is not None
            ):
                data["frequency_every_number"] = request.form.get(
                    "frequency_every_number"
                )

            if (
                request.form.get("freccurency_every_unit")
                and request.form.get("freccurency_every_unit") is not None
            ):
                data["freccurency_every_unit"] = request.form.get(
                    "freccurency_every_unit"
                )

            if (
                request.form.get("date_end_reccurency")
                and request.form.get("date_end_reccurency") is not None
            ):
                data["date_end_reccurency"] = request.form.get("date_end_reccurency")

            app.logger.critical(json.dumps(data))
            response = requests.request(
                method="POST", url=API_URL_TRANSACTION, json=data
            )
            if response.status_code != 200:
                flash(f"Something went wrong while adding", "error")
        return redirect(url_for("list_all_transactions"))
        # return render_template("transaction_detail.html", transaction=json.dumps(data))


@app.route("/transactions/<transaction_id>", methods=["GET"])
def transaction_detail(transaction_id):
    url = f"{API_URL_TRANSACTION}/{transaction_id}"
    response = requests.request(method="GET", url=url)
    if response.status_code == 500:
        app.logger.critical(
            f"Something went wrong while getting {transaction_id}", "error"
        )
        flash(f"Something went wrong while getting {transaction_id}", "error")
    app.logger.debug(response)
    transaction = response.json()
    return render_template("transaction_detail.html", type=transaction["data"][0])


@app.route("/transactions/delete/<transaction_id>", methods=["GET"])
def transaction_delete(transaction_id):
    url = f"{API_URL_TRANSACTION}/{transaction_id}"
    response = requests.request(method="DELETE", url=url)
    if response.status_code == 500:
        flash(f"Something went wrong while removing {transaction_id}", "error")
    return redirect(url_for("list_all_transactions"))
