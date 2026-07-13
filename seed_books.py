import sqlite3
from datetime import datetime, timedelta
import random

DB_NAME = "book_management.db"


def create_books_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            description TEXT,
            book_type TEXT DEFAULT 'hardcopy',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()


def generate_books_dataset():
    """
    Returns a list of dictionaries matching the schema:
        id, title, author, category, price, quantity, description, book_type, created_at
    """

    base_books = [
        # Self Help / Productivity / Finance / Business
        ("Atomic Habits", "James Clear", "Self Help", 499, "A practical guide to building good habits, breaking bad ones, and improving daily systems."),
        ("Deep Work", "Cal Newport", "Productivity", 450, "A book about focused success in a distracted world and how to produce better results through concentration."),
        ("The Psychology of Money", "Morgan Housel", "Finance", 520, "Explains how behavior, emotion, and psychology shape financial decisions and long-term wealth."),
        ("Rich Dad Poor Dad", "Robert Kiyosaki", "Finance", 400, "A classic personal finance book about financial literacy, assets, and building wealth."),
        ("Think and Grow Rich", "Napoleon Hill", "Motivation", 380, "A motivational classic about mindset, desire, persistence, and achievement."),
        ("Ikigai", "Francesc Miralles", "Self Help", 320, "A book exploring purpose, happiness, longevity, and meaningful living through Japanese philosophy."),
        ("Zero to One", "Peter Thiel", "Business", 410, "A startup and innovation book about building unique businesses that create new value."),
        ("The Lean Startup", "Eric Ries", "Business", 460, "A guide to building startups through experimentation, customer feedback, and iterative product development."),
        ("Start With Why", "Simon Sinek", "Business", 430, "Explains why purpose-driven leadership inspires teams, customers, and long-term trust."),
        ("The 7 Habits of Highly Effective People", "Stephen R. Covey", "Self Help", 540, "A personal development classic focused on principles, effectiveness, and character-based growth."),

        # Programming / CS / AI / Data
        ("Clean Code", "Robert C. Martin", "Programming", 650, "A software engineering classic about writing readable, maintainable, and high-quality code."),
        ("The Pragmatic Programmer", "Andrew Hunt", "Programming", 750, "A practical guide to software craftsmanship, habits, tools, and engineering discipline."),
        ("Python Crash Course", "Eric Matthes", "Programming", 700, "A beginner-friendly Python book covering fundamentals, exercises, and practical projects."),
        ("Fluent Python", "Luciano Ramalho", "Programming", 980, "An advanced Python book covering idiomatic Python, data models, and language internals."),
        ("Effective Python", "Brett Slatkin", "Programming", 820, "A collection of practical Python best practices for writing better production code."),
        ("Introduction to Algorithms", "Thomas H. Cormen", "Computer Science", 1200, "A comprehensive textbook on algorithms, data structures, and computational problem solving."),
        ("Grokking Algorithms", "Aditya Bhargava", "Computer Science", 680, "An illustrated introduction to algorithms with intuitive examples and visual explanations."),
        ("Designing Data-Intensive Applications", "Martin Kleppmann", "System Design", 1100, "A deep dive into scalable systems, databases, streams, consistency, and reliability."),
        ("Hands-On Machine Learning", "Aurélien Géron", "AI/ML", 950, "A practical machine learning guide using Python, Scikit-Learn, Keras, and TensorFlow."),
        ("Deep Learning", "Ian Goodfellow", "AI/ML", 1350, "A foundational textbook covering neural networks, deep learning theory, and modern ML concepts."),

        # Fiction / Fantasy / Dystopian / Literature
        ("The Alchemist", "Paulo Coelho", "Fiction", 350, "A philosophical novel about dreams, destiny, and the pursuit of one’s personal legend."),
        ("1984", "George Orwell", "Dystopian", 360, "A dystopian novel about surveillance, authoritarianism, and the manipulation of truth."),
        ("Animal Farm", "George Orwell", "Satire", 250, "A political allegory about power, corruption, and revolution through a farmyard tale."),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 480, "A fantasy adventure following Bilbo Baggins on a quest involving dwarves, treasure, and dragons."),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 550, "The first Harry Potter novel introducing Hogwarts, friendship, and the wizarding world."),
        ("Harry Potter and the Chamber of Secrets", "J.K. Rowling", "Fantasy", 570, "The second Harry Potter adventure featuring hidden secrets, danger, and magic at Hogwarts."),
        ("To Kill a Mockingbird", "Harper Lee", "Classic", 390, "A classic novel about justice, morality, prejudice, and childhood in the American South."),
        ("Pride and Prejudice", "Jane Austen", "Classic", 340, "A timeless novel of manners, love, class, and social expectations."),
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 330, "A novel about wealth, desire, illusion, and the American dream."),
        ("The Catcher in the Rye", "J.D. Salinger", "Classic", 370, "A coming-of-age novel exploring alienation, identity, and adolescence."),

        # More Programming / Tech / Security / Data
        ("Refactoring", "Martin Fowler", "Programming", 890, "A guide to improving existing code structure without changing its behavior."),
        ("Code Complete", "Steve McConnell", "Programming", 990, "A detailed handbook of software construction practices, design, debugging, and quality."),
        ("Cracking the Coding Interview", "Gayle Laakmann McDowell", "Interview Prep", 850, "A popular interview preparation book with coding questions and explanations."),
        ("Computer Networking: A Top-Down Approach", "James Kurose", "Networking", 920, "A networking textbook explaining protocols, architecture, and internet systems."),
        ("Operating System Concepts", "Abraham Silberschatz", "Computer Science", 1180, "A standard OS textbook covering processes, memory, concurrency, and scheduling."),
        ("Database System Concepts", "Abraham Silberschatz", "Database", 1050, "A foundational database systems book covering design, SQL, transactions, and architecture."),
        ("Head First Design Patterns", "Eric Freeman", "Programming", 780, "An accessible guide to software design patterns using practical object-oriented examples."),
        ("System Design Interview", "Alex Xu", "System Design", 860, "A practical guide to common large-scale system design problems and tradeoffs."),
        ("Python for Data Analysis", "Wes McKinney", "Data Science", 880, "A practical guide to data wrangling, pandas, NumPy, and exploratory analysis in Python."),
        ("Data Science from Scratch", "Joel Grus", "Data Science", 760, "Introduces data science concepts by implementing core techniques from the ground up."),

        # More business / productivity / biographies
        ("Can't Hurt Me", "David Goggins", "Biography", 530, "A memoir and mindset book about discipline, resilience, and mental toughness."),
        ("Shoe Dog", "Phil Knight", "Biography", 520, "The memoir of Nike’s founder about entrepreneurship, risk, and building a global brand."),
        ("Steve Jobs", "Walter Isaacson", "Biography", 690, "A detailed biography of Steve Jobs, his leadership, products, and impact on technology."),
        ("Elon Musk", "Walter Isaacson", "Biography", 720, "A biography covering Elon Musk’s companies, ambitions, and high-risk decision making."),
        ("The Hard Thing About Hard Things", "Ben Horowitz", "Business", 610, "A startup leadership book about managing hard decisions, pressure, and uncertainty."),
        ("Measure What Matters", "John Doerr", "Business", 590, "Explains OKRs and how goal-setting frameworks can improve focus and execution."),
        ("Make Time", "Jake Knapp", "Productivity", 430, "A practical productivity book about focusing on what matters and reclaiming time."),
        ("Essentialism", "Greg McKeown", "Self Help", 410, "A book about doing less but better through clarity, focus, and disciplined prioritization."),
        ("The Power of Now", "Eckhart Tolle", "Self Help", 390, "A spiritual self-help book about mindfulness, presence, and inner peace."),
        ("Man's Search for Meaning", "Viktor E. Frankl", "Psychology", 440, "A profound book about suffering, meaning, and human resilience."),

        # More fiction / literature / fantasy / thrillers
        ("The Silent Patient", "Alex Michaelides", "Thriller", 480, "A psychological thriller about trauma, silence, obsession, and hidden truths."),
        ("Gone Girl", "Gillian Flynn", "Thriller", 500, "A suspense novel about marriage, manipulation, media narratives, and deception."),
        ("The Da Vinci Code", "Dan Brown", "Thriller", 470, "A fast-paced mystery thriller involving symbols, secrets, and religious conspiracies."),
        ("The Kite Runner", "Khaled Hosseini", "Fiction", 420, "A moving novel about friendship, guilt, redemption, and the impact of history."),
        ("A Thousand Splendid Suns", "Khaled Hosseini", "Fiction", 440, "A powerful story about love, sacrifice, and survival in Afghanistan."),
        ("The Book Thief", "Markus Zusak", "Historical Fiction", 460, "A novel set during World War II narrated through loss, books, and courage."),
        ("Dune", "Frank Herbert", "Science Fiction", 620, "An epic science fiction novel about politics, prophecy, ecology, and power."),
        ("The Name of the Wind", "Patrick Rothfuss", "Fantasy", 590, "A fantasy novel following the life, legend, and education of Kvothe."),
        ("Mistborn", "Brandon Sanderson", "Fantasy", 560, "A fantasy novel featuring rebellion, magic systems, and a world ruled by oppression."),
        ("The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 1250, "An epic fantasy saga about friendship, sacrifice, evil, and the fate of Middle-earth."),
    ]

    # We want 100 rows total. We'll make 50 unique titles * 2 variants each (hardcopy + softcopy).
    # base_books above contains 60 books. We'll use the first 50 to create exactly 100 records.
    selected_books = base_books[:50]

    books = []
    current_id = 1
    now = datetime.utcnow()

    for i, (title, author, category, hardcopy_price, description) in enumerate(selected_books):
        # hardcopy row
        books.append({
            "id": current_id,
            "title": title,
            "author": author,
            "category": category,
            "price": float(hardcopy_price),
            "quantity": random.randint(8, 35),
            "description": description,
            "book_type": "hardcopy",
            "created_at": (now - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        })
        current_id += 1

        # softcopy row
        softcopy_price = round(hardcopy_price * random.uniform(0.35, 0.55), 2)
        books.append({
            "id": current_id,
            "title": title,
            "author": author,
            "category": category,
            "price": float(softcopy_price),
            "quantity": random.randint(40, 150),
            "description": f"Digital edition of {title}. {description}",
            "book_type": "softcopy",
            "created_at": (now - timedelta(days=i)).strftime("%Y-%m-%d %H:%M:%S")
        })
        current_id += 1

    return books


def book_exists(cursor, title, author, book_type):
    cursor.execute(
        """
        SELECT id
        FROM books
        WHERE title = ? AND author = ? AND book_type = ?
        LIMIT 1
        """,
        (title, author, book_type)
    )
    return cursor.fetchone() is not None


def seed_books(conn: sqlite3.Connection, books_data):
    cursor = conn.cursor()
    inserted = 0
    skipped = 0

    for book in books_data:
        if book_exists(cursor, book["title"], book["author"], book["book_type"]):
            skipped += 1
            continue

        cursor.execute("""
            INSERT INTO books (
                id,
                title,
                author,
                category,
                price,
                quantity,
                description,
                book_type,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            book["id"],
            book["title"],
            book["author"],
            book["category"],
            book["price"],
            book["quantity"],
            book["description"],
            book["book_type"],
            book["created_at"]
        ))
        inserted += 1

    conn.commit()
    print(f"Inserted: {inserted} books")
    print(f"Skipped : {skipped} duplicate books")


def show_books_preview(conn: sqlite3.Connection, limit: int = 20):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, author, category, price, quantity, book_type, created_at
        FROM books
        ORDER BY id
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()

    print(f"\nShowing first {limit} books:")
    print("-" * 140)
    for row in rows:
        print(row)


def count_books(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    total = cursor.fetchone()[0]
    print(f"\nTotal books in database: {total}")


def main():
    conn = sqlite3.connect(DB_NAME)

    try:
        create_books_table(conn)
        books_data = generate_books_dataset()
        seed_books(conn, books_data)
        count_books(conn)
        show_books_preview(conn, limit=20)
    finally:
        conn.close()


if __name__ == "__main__":
    main()