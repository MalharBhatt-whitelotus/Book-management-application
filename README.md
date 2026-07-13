# Book Management System

A modern **Book Management System** built with **FastAPI**, featuring a professional **single-page HTML dashboard UI** for managing books with support for:

* Add Book
* Update Book
* Delete Book
* Search Book
* Paginated Book Inventory
* Book Statistics Dashboard
* Light / Dark Mode UI

---

# Features

## Backend Features

* Built with **FastAPI**
* REST API for complete book management
* CRUD operations for books
* Search books by text
* Paginated book listing
* Summary APIs for dashboard stats

## Frontend Features

* Single-page **HTML + CSS + JavaScript** dashboard
* Professional admin-style UI
* Light / Dark mode toggle
* Inventory table with pagination
* Search bar integrated with backend search
* Add Book collapsible form
* Update Book modal
* Delete confirmation modal
* Toast notifications for user feedback
* Responsive design

---

# Tech Stack

## Backend

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **Pydantic**
* **Uvicorn**

## Frontend

* **HTML**
* **CSS**
* **Vanilla JavaScript**

## Database

* SQLite / SQLAlchemy ORM-based database

---

# Project Structure

```bash
book_management/
│
├── main.py                 # FastAPI app entry point
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── database.py             # Database connection setup
├── logic.py                # Business logic layer
├── router/                 # API routes
│   └── book.py
│
├── templates/              # HTML templates (if used)
│   └── index.html
│
├── static/                 # Static assets (if used)
│
├── books.db                # SQLite database
├── requirements.txt
└── README.md
```

> Your actual folder names may differ slightly depending on how you organized the project.

---

# Book Schema

Each book record follows this structure:

```json
{
  "id": 1,
  "title": "Python Basics",
  "author": "John Smith",
  "price": 499,
  "book_type": "hardcopy"
}
```

## Fields

* `id` → Unique book ID
* `title` → Book title
* `author` → Author name
* `price` → Price of the book
* `book_type` → Type of book

## Allowed `book_type` values

* `hardcopy`
* `softcopy`

---

# API Endpoints

## 1. Get Paginated Books

Fetch books with pagination.

**Endpoint**

```http
GET /book/get_books?page=1&limit=10
```

### Example Response

```json
{
  "items": [
    {
      "id": 1,
      "title": "Python Basics",
      "author": "John Smith",
      "price": 499,
      "book_type": "hardcopy"
    }
  ],
  "page": 1,
  "limit": 10,
  "total_pages": 5,
  "total_items": 48
}
```

---

## 2. Add Book

Add a new book to inventory.

**Endpoint**

```http
POST /book/add_book
```

### Request Body

```json
{
  "title": "FastAPI Guide",
  "author": "Jane Doe",
  "price": 599,
  "book_type": "softcopy"
}
```

---

## 3. Update Book

Update an existing book.

**Endpoint**

```http
PUT /book/update/{book_id}
```

### Example

```http
PUT /book/update/1
```

### Request Body

```json
{
  "title": "Updated Book Title",
  "author": "Updated Author",
  "price": 699,
  "book_type": "hardcopy"
}
```

---

## 4. Delete Book

Delete a book from inventory.

**Endpoint**

```http
DELETE /book/delete/{book_id}
```

### Example

```http
DELETE /book/delete/1
```

---

## 5. Search Book

Search books from the backend.

**Endpoint**

```http
GET /book/search_book/{search_text}
```

### Example

```http
GET /book/search_book/python
```

---

## 6. Get Total Books

Returns total number of books in inventory.

**Endpoint**

```http
GET /book/get_total_books
```

---

## 7. Get Hard Copy Count

Returns total hardcopy books.

**Endpoint**

```http
GET /book/get_hard_copies
```

---

## 8. Get Soft Copy Count

Returns total softcopy books.

**Endpoint**

```http
GET /book/get_soft_copies
```

---

# Frontend Dashboard Overview

The Book Management dashboard includes the following sections:

## 1. Header

* App branding / dashboard title
* Theme toggle for light/dark mode

## 2. Stats Cards

Displays:

* Total Books
* Hard Copies
* Soft Copies

## 3. Add Book Section

* Hidden/collapsible add book form
* Allows adding new books to inventory

## 4. Books Inventory Table

Displays:

* ID
* Title
* Author
* Price
* Type
* Actions

### Inventory Table Features

* Professional dashboard-style UI
* Backend pagination
* Search integration
* Edit / Delete actions
* Empty state handling

## 5. Update Modal

* Edit book details
* Save updates through backend API

## 6. Delete Confirmation Modal

* Confirm deletion before removing a book

## 7. Toast Notifications

* Success / error feedback for actions

---

# How to Run the Project

## 1. Clone the Repository

```bash
git clone <your-repo-url>
cd book_management
```

## 2. Create and Activate Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the FastAPI Server

```bash
uvicorn main:app --reload
```

## 5. Open in Browser

Visit:

```bash
http://127.0.0.1:8000/
```

or the route where your HTML dashboard is served.

---

# Example `requirements.txt`

```txt
fastapi
uvicorn
sqlalchemy
jinja2
pydantic
python-multipart
```

> Add/remove packages depending on your actual project setup.

---

# Pagination Behavior

The inventory table uses **backend pagination**.

## Normal Mode

When no search is active:

* Books load using:

  ```http
  GET /book/get_books?page=1&limit=10
  ```
* Pagination controls show:

  * Prev
  * Next
  * Page buttons
  * Ellipsis when needed
* Summary example:

  * `Showing 1–10 of 48 books`

## Search Mode

When search text is entered:

* Books load using:

  ```http
  GET /book/search_book/{search_text}
  ```
* Results are shown in the same inventory table
* Pagination controls are hidden or disabled
* Summary example:

  * `Found 4 matching books`

---

# Search Functionality

The inventory section includes backend-powered search.

## Search Behavior

* User enters text in the search bar
* Frontend calls:

  ```http
  /book/search_book/{search_text}
  ```
* Matching books are rendered in the same table
* Clearing the search restores normal paginated inventory mode

---

# CRUD Flow Summary

## Add Book

1. Click **Add Book**
2. Fill in title, author, price, and book type
3. Submit form
4. Book is added via backend API
5. Stats and table refresh

## Update Book

1. Click **Edit** on a book row
2. Update values in the modal
3. Save changes
4. Backend updates the record
5. Stats and table refresh

## Delete Book

1. Click **Delete**
2. Confirm deletion
3. Backend deletes the book
4. Stats and table refresh

---

# UI Highlights

* Clean admin dashboard layout
* Modern inventory table
* Search + pagination integration
* Responsive design
* Dark mode support
* Consistent buttons, modals, and forms
* Simple and professional styling

---

# Future Improvements

Possible enhancements for the project:

* Authentication / login system
* Role-based access (Admin / Staff)
* Book category support
* Sorting by price / title / author
* Export inventory to CSV / Excel
* Filter by book type
* Advanced search with multiple fields
* Book cover image support
* Better analytics dashboard

---

# Author

**Malhar Bhatt**

---

# License

This project is for learning / academic / portfolio use.
You can update the license section based on your preference, for example **MIT License**.
