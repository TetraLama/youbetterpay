from fastapi import FastAPI
from server.routes.accounts import router as AccountsRouter
from server.routes.transactions import router as TransactionsRouter
from server.routes.categories import router as CategoriesRouter
from server.routes.types import router as TypesRouter

app = FastAPI()

app.include_router(AccountsRouter, tags=["Accounts"], prefix="/api/v1/accounts")
app.include_router(
    TransactionsRouter, tags=["Transactions"], prefix="/api/v1/transactions"
)
app.include_router(CategoriesRouter, tags=["Categories"], prefix="/api/v1/categories")
app.include_router(TypesRouter, tags=["Types"], prefix="/api/v1/types")


@app.get("/api/v1/healthcheck", tags=["Root"])
async def read_root():
    return {"message": "All Good!"}
