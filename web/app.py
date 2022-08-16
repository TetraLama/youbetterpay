from flask import Flask, render_template, url_for, redirect, abort, json, flash, request
from dotenv import dotenv_values
import requests
from werkzeug.exceptions import HTTPException
import os

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/accounts', methods=["GET", "POST"])
def accout_list_all():
    if request.method == "GET":
        url = "http://api/v1/accounts/"
        response = requests.request(method="GET", url=url)
        list_accounts = response.json()
        app.logger.debug(list_accounts["data"][0])
        return render_template('accounts.html', accounts=list_accounts["data"][0])
        
    if request.method == "POST":
        url = "http://api/v1/accounts/"
        account_name = request.form.get('account_name')
        if not account_name:
            flash(f'You MUST specify a name', 'error')
        else:
            data = {"name": account_name}
            response = requests.request(method="POST", url=url, json=data)
            if response.status_code != 200:
                flash(f'Something went wrong while adding {account_name}', 'error')
        return redirect(url_for('accout_list_all'))

@app.route('/accounts/<account_id>', methods=["GET"])
def account_detail(account_id):
    url = f"http://api/v1/accounts/{account_id}"
    response = requests.request(method="GET", url=url)
    if response.status_code == 500:
        app.logger.critical(f'Something went wrong while getting {account_id}', 'error')
        flash(f'Something went wrong while getting {account_id}', 'error')
    app.logger.debug(response)
    account = response.json()
    return render_template('account_detail.html', account=account["data"][0])

@app.route('/accounts/delete/<account_id>', methods=["GET"])
def account_delete(account_id):
    url = f"http://api/v1/accounts/{account_id}"
    response = requests.request(method="DELETE", url=url)
    if response.status_code == 500:
        flash(f'Something went wrong while removing {account_id}', 'error')
    return redirect(url_for('accout_list_all'))
    