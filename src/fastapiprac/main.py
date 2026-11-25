import json
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="FastAPIPractice",
    description="First FastAPI application",
    docs_url="/docs",
    redoc_url="/redoc"
)

with open("src/fastapiprac/data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    genre: str
    price: float
    in_stock: bool

def save_data():
    with open("src/fastapiprac/data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.get("/books", response_model=list[Book])
async def get_books():
    return data["books"]

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books", response_model=Book)
async def add_book(book: Book):
    for existing_book in data["books"]:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=409, detail="Book already exists")
    data["books"].append(book.model_dump())
    save_data()
    return book

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for book in data["books"]:
        if book["id"] == book_id:
            data["books"].remove(book)
            save_data()
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(data["books"]):
        if book["id"] == book_id:
            book_data = updated_book.model_dump()
            book_data["id"] = book_id
            data["books"][index] = book_data
            save_data()
            return book_data
    raise HTTPException(status_code=404, detail="Book not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)