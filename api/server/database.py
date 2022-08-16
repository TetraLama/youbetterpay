import motor.motor_asyncio
from bson.objectid import ObjectId
import os

###
# DATABASE
###
MONGODB_URL="mongodb://{}:{}@{}/{}?retryWrites=true&w=majority&authSource=admin".format(os.environ["DB_USERNAME"], os.environ["DB_PASSWORD"], os.environ["DB_HOST"], os.environ["DB_NAME"])
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
database = client.youbetterpay
accounts_collection = database.get_collection("accounts")
transactions_collection = database.get_collection("transactions")
categories_collection = database.get_collection("categories")


###
# ACCOUNTS
###
def account_helper(account) -> dict:
    return {
        "id": str(account["_id"]),
        "name": account["name"]
    }

async def retrieve_accounts():
    accounts = []
    async for account in accounts_collection.find():
        accounts.append(account_helper(account))
    return accounts

# Add a new account into to the database
async def add_account(account_data: dict) -> dict:
    account = await accounts_collection.insert_one(account_data)
    new_account = await accounts_collection.find_one({"_id": account.inserted_id})
    return account_helper(new_account)

# Retrieve a account with a matching ID
async def retrieve_account(id: str) -> dict:
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        return account_helper(account)

# Update a account with a matching ID
async def update_account(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        updated_account = await accounts_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_account:
            return True
        return False

# Delete a account from the database
async def delete_account(id: str):
    account = await accounts_collection.find_one({"_id": ObjectId(id)})
    if account:
        await accounts_collection.delete_one({"_id": ObjectId(id)})
        return True

###
# TRANSACTION
###
def transaction_helper(transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "description": transaction["description"],
        "ammount": transaction["description"],
        "target_account": transaction["target_account"],
        "source_account": transaction["source_account"]
    }

async def retrieve_transactions() -> list:
    transactions = []
    async for transaction in transactions_collection.find():
        transactions.append(transaction_helper(transaction))
    return transactions

# Add a new transaction into to the database
async def add_transaction(transaction_data: dict) -> dict:
    transaction = await transactions_collection.insert_one(transaction_data)
    new_transaction = await transactions_collection.find_one({"_id": transaction.inserted_id})
    return transaction_helper(new_transaction)

# Retrieve a transaction with a matching ID
async def retrieve_transaction(id: str) -> dict:
    transaction = await transactions_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        return transaction_helper(transaction)

# Update a transaction with a matching ID
async def update_transaction(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    transaction = await transactions_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        updated_transaction = await transactions_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_transaction:
            return True
        return False

# Delete a transaction from the database
async def delete_transaction(id: str):
    transaction = await transactions_collection.find_one({"_id": ObjectId(id)})
    if transaction:
        await transactions_collection.delete_one({"_id": ObjectId(id)})
        return True

###
# CATEGORIES
###
def category_helper(category) -> dict:
    return {
        "id": str(category["_id"]),
        "name": category["name"]
    }

async def retrieve_categories() -> list:
    categories = []
    async for category in categories_collection.find():
        categories.append(category_helper(category))
    return categories

# Add a new category into to the database
async def add_category(category_data: dict) -> dict:
    category = await categories_collection.insert_one(category_data)
    new_category = await categories_collection.find_one({"_id": category.inserted_id})
    return category_helper(new_category)

# Retrieve a category with a matching ID
async def retrieve_category(id: str) -> dict:
    category = await categories_collection.find_one({"_id": ObjectId(id)})
    if category:
        return category_helper(category)

# Update a category with a matching ID
async def update_category(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    category = await categories_collection.find_one({"_id": ObjectId(id)})
    if category:
        updated_category = await categories_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_category:
            return True
        return False

# Delete a transaction from the database
async def delete_category(id: str):
    category = await categories_collection.find_one({"_id": ObjectId(id)})
    if category:
        await categories_collection.delete_one({"_id": ObjectId(id)})
        return True