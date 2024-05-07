import sqlite3

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import  Optional

import uvicorn

app = FastAPI(
    description="Sample Assesmet contact={'name': 'AJAY CHEVULA  VADDE','Emain': 'cvajay69@gmail.com'} ",
    # title="Assessment Overview",
    summary="Assessment Overview of Book ",
    version="Python 3 ",
    contact={"name": "AJAY CHEVULA  VADDE",
                "Emain": "cvajay69@gmail.com"
             }    )

# Database setup
conn = sqlite3.connect('book_reviews.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    publication_year INTEGER
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY,
                    book_id INTEGER,
                    text TEXT,
                    rating INTEGER,
                    FOREIGN KEY(book_id) REFERENCES books(id)
                )''')


class Book(BaseModel):
    title: str
    author: str
    publication_year: int

class Review(BaseModel):
    book_id: int
    text: str
    rating: int


@app.get('/')
def homemongo():
    return {'msg': True}
# Endpoint to add a new book
@app.post("/books/")
def add_book(book: Book):
    cursor.execute('''INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)''', 
                   (book.title, book.author, book.publication_year))
    conn.commit()
    return {"message": "Book added successfully"}

# Endpoint to submit a review for a book
@app.post("/books/{book_id}/reviews/")
def submit_review(book_id: int, review: Review, background_tasks: BackgroundTasks):
    if book_id <= 0 or not cursor.execute("SELECT 1 FROM books WHERE id = ?", (book_id,)).fetchone():
        raise HTTPException(status_code=404, detail="Book not found")

    cursor.execute('''INSERT INTO reviews (book_id, text, rating) VALUES (?, ?, ?)''',
                   (book_id, review.text, review.rating))
    conn.commit()

    # Simulated background task to send confirmation email
    background_tasks.add_task(send_confirmation_email, book_id, review.text)
    
    return {"message": "Review added successfully"}

# Endpoint to retrieve all books with optional filters
@app.get("/books/")
def get_books(author: Optional[str] = None, publication_year: Optional[int] = None):
    query = "SELECT * FROM books"
    params = []
    if author:
        query += " WHERE author = ?"
        params.append(author)
    if publication_year:
        if not author:
            query += " WHERE"
        else:
            query += " AND"
        query += " publication_year = ?"
        params.append(publication_year)

    books = cursor.execute(query, params).fetchall()
    return books

# Endpoint to retrieve all reviews for a specific book
@app.get("/books/{book_id}/reviews/")
def get_reviews(book_id: int):
    if book_id <= 0 or not cursor.execute("SELECT 1 FROM books WHERE id = ?", (book_id,)).fetchone():
        raise HTTPException(status_code=404, detail="Book not found")
    
    reviews = cursor.execute("SELECT * FROM reviews WHERE book_id = ?", (book_id,)).fetchall()
    return reviews

# Background task to simulate sending confirmation email
def send_confirmation_email(book_id: int, review_text: str):
    # Simulated action
    print(f"Sending confirmation email for review '{review_text}' on book ID {book_id}")

# Part 3: Advanced Features and Testing

from fastapi.testclient import TestClient

client = TestClient(app)

def test_add_book():
    response = client.post("/books/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2022})
    assert response.status_code == 200
    assert response.json() == {"message": "Book added successfully"}

def test_get_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Part 4: Theoretical Questions and Evaluation Criteria


# Close the database connection when the application shuts down
@app.on_event("shutdown")
def shutdown_event():
    conn.close()




if __name__ == '__main__':
    uvicorn.run(app='over_view_of_book:app', 
                host='localhost',
                port=8000, 
                reload=True,
                use_colors=True
                )

