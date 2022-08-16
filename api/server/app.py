from fastapi import FastAPI
from server.routes.accounts import router as AccountsRouter
from server.routes.transactions import router as TransactionsRouter
from server.routes.categories import router as CategoriesRouter

app = FastAPI()

app.include_router(AccountsRouter, tags=["Accounts"], prefix="/v1/accounts")
app.include_router(TransactionsRouter, tags=["Transactions"], prefix="/v1/transactions")
app.include_router(CategoriesRouter, tags=["Categories"], prefix="/v1/categories")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}