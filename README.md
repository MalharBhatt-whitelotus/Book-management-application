# 📚 Book Management System

A modern, production-ready **Book Management System** built using **FastAPI**, **Async SQLAlchemy**, and **JWT Authentication** with a clean architecture following the **Repository-Service pattern**.

The application allows administrators to manage book inventory while enabling users to browse and purchase books. It also supports bill generation, inventory updates, advanced filtering, sorting, file uploads, and automated testing.

---

# ✨ Features

## 🔐 Authentication

- JWT Authentication
- User Registration
- User Login
- Password Hashing using bcrypt
- Protected APIs with Bearer Token

---

## 📚 Book Management

- Add New Book
- Update Book
- Delete Book
- Get Book by ID
- Get All Books
- Search Books
- Advanced Filtering
- Dynamic Sorting
- Inventory Management

---

## 🧾 Billing System

- Checkout Multiple Books
- Generate Bills
- Automatic Inventory Reduction
- View Bills
- View User Purchase History
- Order Group Generation

---

## 📂 File Upload

- Upload Book Cover Image
- Upload PDF Documents
- File Type Validation
- Local Storage
- Upload Logging
- Background Tasks

---

## 📊 Dashboard

- Total Books
- Available Books
- Hardcopy Books
- Softcopy Books
- Inventory Overview

---

## 🧪 Testing

- Async Pytest
- HTTPX Test Client
- Authentication Tests
- CRUD Tests
- Checkout Tests
- Filtering Tests
- Sorting Tests

---

# 🚀 Tech Stack

## Backend

- Python 3.14+
- FastAPI
- SQLAlchemy (Async ORM)
- SQLite
- Pydantic v2
- JWT Authentication
- Passlib (bcrypt)
- Python Multipart
- Uvicorn

---

## Frontend

- HTML5
- CSS3
- Vanilla JavaScript

---

## Database

- SQLite

---

## Testing

- Pytest
- pytest-asyncio
- HTTPX

---

# 📁 Project Structure

```text
Book-management-application/
│
├── config.py
├── database.py
├── main.py
├── requirements.txt
├── .env
│
├── models/
│   ├── book.py
│   ├── bill.py
│   └── user.py
│
├── schemas/
│   ├── book_schema.py
│   ├── bill_schema.py
│   └── user_schema.py
│
├── repository/
│   ├── book_repo.py
│   ├── bills_repo.py
│   └── user_repo.py
│
├── services/
│   ├── book_services.py
│   ├── bills_services.py
│   ├── user_services.py
│   └── security.py
│
├── routes/
│   ├── book_routes.py
│   ├── bills_routes.py
│   └── user_routes.py
│
├── templates/
│
├── static/
│
├── uploads/
│   ├── covers/
│   └── documents/
│
├── tests/
│   ├── conftest.py
│   ├── test_books.py
│   ├── test_users.py
│   └── test_bills.py
│
└── README.md
```

---

# 🏗️ Architecture

```
Client
   │
   ▼
Routes
   │
   ▼
Services
   │
   ▼
Repositories
   │
   ▼
Database
```

The project follows the **Repository-Service Pattern**, separating API routes, business logic, and database operations for better maintainability.

---

# 📖 Book Model

| Field | Type |
|--------|------|
| id | Integer |
| title | String |
| author | String |
| category | String |
| price | Float |
| quantity | Integer |
| description | Text |
| book_type | hardcopy / softcopy |
| created_at | DateTime |

---

# 👤 User Model

| Field | Type |
|--------|------|
| id | Integer |
| name | String |
| email | String |
| password | String (Hashed) |
| role | Admin/User |

---

# 🧾 Bill Model

| Field | Type |
|--------|------|
| id | Integer |
| order_group | String |
| user_id | Integer |
| book_id | Integer |
| customer_name | String |
| book_title | String |
| quantity | Integer |
| unit_price | Float |
| line_total | Float |
| purchased_at | DateTime |

---

# 🔗 API Endpoints

## Authentication

| Method | Endpoint | Description |
|----------|----------------------|----------------|
| POST | `/users/register` | Register User |
| POST | `/users/login` | Login User |

---

## Books

| Method | Endpoint | Description |
|----------|----------------------------|----------------|
| GET | `/books` | Get All Books |
| GET | `/books/{id}` | Get Book by ID |
| POST | `/books` | Add Book |
| PUT | `/books/{id}` | Update Book |
| DELETE | `/books/{id}` | Delete Book |
| GET | `/books/search/{keyword}` | Search Books |
| GET | `/books/filter` | Advanced Filtering & Sorting |

---

### Filtering Parameters

| Parameter | Description |
|------------|-------------|
| category | Filter by category |
| author | Filter by author |
| book_type | hardcopy / softcopy |
| min_price | Minimum price |
| max_price | Maximum price |
| available | Quantity > 0 |

---

### Sorting Parameters

| Parameter | Values |
|------------|--------|
| sort_by | id,title,author,category,price,quantity,created_at |
| order | asc / desc |

---

### Example

```
GET /books/filter?
category=Programming&
author=Robert C. Martin&
book_type=hardcopy&
min_price=300&
max_price=1000&
available=true&
sort_by=price&
order=asc
```

---

## Bills

| Method | Endpoint | Description |
|----------|----------------------------|----------------|
| POST | `/bills/checkout` | Checkout Books |
| GET | `/bills/{bill_id}` | Get Bill |
| GET | `/bills` | Get All Bills |
| GET | `/bills/user` | User Purchase History |
| GET | `/bills/order/{order_group}` | Order Summary |

---

# 🔄 Checkout Flow

```
User Login
      │
      ▼
Select Books
      │
      ▼
Validate Stock
      │
      ▼
Generate Bill
      │
      ▼
Reduce Inventory
      │
      ▼
Commit Transaction
      │
      ▼
Return Bill Summary
```

---

# 🖼️ File Upload

Supported uploads:

- Book Cover Images
- PDF Documents

Features

- File validation
- Local storage
- Upload logging
- Background tasks

---

# 🔐 Security

- JWT Authentication
- Password Hashing
- Protected Routes
- Bearer Authentication
- OAuth2 Password Flow

---

# 🧪 Automated Testing

Implemented using

- pytest
- pytest-asyncio
- HTTPX Async Client

### Test Coverage

- User Registration
- User Login
- Add Book
- Update Book
- Delete Book
- Search Book
- Filter Books
- Sort Books
- Checkout Books
- Bill Generation
- Authentication

Run tests:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone <repository-url>

cd Book-management-application
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create a `.env` file.

Example:

```env
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

DATABASE_URL=sqlite+aiosqlite:///./books.db

UPLOAD_FOLDER=uploads
```

---

## Run Application

```bash
uvicorn main:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```
http://127.0.0.1:8000/redoc
```

---

# 📦 Dependencies

```text
fastapi
uvicorn
sqlalchemy
aiosqlite
pydantic
pydantic-settings
python-jose
passlib
bcrypt
python-multipart
jinja2
pytest
pytest-asyncio
httpx
```

---

# 📈 Future Improvements

- PostgreSQL Support
- Docker Deployment
- Redis Caching
- Email Notifications
- Role-Based Access Control
- Payment Gateway Integration
- Inventory Analytics Dashboard
- Book Recommendation System
- Export Bills to PDF
- Email Invoice Generation

---

# 👨‍💻 Author

**Malhar Bhatt**

GitHub: *Add your GitHub profile here*

---

# 📄 License

This project is released for educational and portfolio purposes.

You may choose to license it under the **MIT License** if you intend to make it open source.
