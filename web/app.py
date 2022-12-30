from flask import Flask, render_template, url_for, redirect, json, flash, request
import requests
from werkzeug.exceptions import HTTPException
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

API_URL="http://api:8082"
API_URL_ACCOUNT=f"{API_URL}/v1/accounts"
API_URL_TYPE=f"{API_URL}/v1/types"

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
        response = requests.request(method="GET", url=API_URL_ACCOUNT)
        list_accounts = response.json()
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
        response = requests.request(method="GET", url=API_URL_TYPE)
        list_types = response.json()
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
# TYPES
###
@app.route("/types", methods=["GET", "POST"])
def list_all_types():
    if request.method == "GET":
        response = requests.request(method="GET", url=API_URL_TYPE)
        list_types = response.json()
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
