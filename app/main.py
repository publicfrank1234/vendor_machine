import uvicorn
from fastapi import FastAPI

from .routers import products, transactions, users

app = FastAPI(title="Vending Machine API")


@app.get("/")
async def root():
    return {"message": "Welcome to the Vending Machine API!"}


app.include_router(users.router)
app.include_router(products.router)
app.include_router(transactions.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
