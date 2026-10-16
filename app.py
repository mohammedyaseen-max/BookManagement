
import os
import time

import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, redirect, render_template_string, request, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://bookuser:bookpass@localhost:5432/bookdb"
)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Book Management System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 850px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f4f6f8;
            color: #222;
        }

        h1 {
            color: #234;
        }

        form, .book {
            background: white;
            padding: 16px;
            margin: 12px 0;
            border-radius: 8px;
        }

        input {
            display: block;
            box-sizing: border-box;
            padding: 10px;
            margin: 8px 0;
            width: 100%;
        }

        button {
            padding: 10px 16px;
            border: 0;
            border-radius: 5px;
            cursor: pointer;
        }

        .add {
            background: #176b45;
            color: white;
        }

        .delete {
            background: #b42318;
            color: white;
        }

        .book {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }

        .book p {
            margin: 6px 0;
        }
    </style>
</head>
<body>
    <h1>Book Management System</h1>
    <p>Add, view, and delete books using PostgreSQL.</p>

    <form action="/add" method="post">
        <h2>Add a Book</h2>

        <input
            name="title"
            placeholder="Book title"
            required
            maxlength="200"
        >

        <input
            name="author"
            placeholder="Author name"
            required
            maxlength="150"
        >

        <button class="add" type="submit">Add Book</button>
    </form>

    <h2>Book List ({{ books|length }})</h2>

    {% for book in books %}
        <div class="book">
            <div>
                <p><strong>{{ book.title }}</strong></p>
                <p>Author: {{ book.author }}</p>
            </div>

            <form action="/delete/{{ book.id }}" method="post">
                <button class="delete" type="submit">Delete</button>
            </form>
        </div>
    {% else %}
        <p>No books yet. Add your first book above.</p>
    {% endfor %}
</body>
</html>
"""


def get_connection():
    return psycopg2.connect(
        DATABASE_URL,
        connect_timeout=5
    )


def initialize_database():
    last_error = None

    for attempt in range(10):
        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS books (
                            id SERIAL PRIMARY KEY,
                            title VARCHAR(200) NOT NULL,
                            author VARCHAR(150) NOT NULL
                        )
                    """)

            print("Database initialized successfully.")
            return

        except psycopg2.OperationalError as error:
            last_error = error

            print(
                f"Waiting for database "
                f"({attempt + 1}/10)..."
            )

            time.sleep(3)

    raise RuntimeError(
        "Could not connect to PostgreSQL after multiple attempts."
    ) from last_error


# Initialize the database once when the application is loaded.
# This also runs when Gunicorn imports this module.
initialize_database()


@app.route("/")
def index():
    with get_connection() as connection:
        with connection.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:
            cursor.execute("""
                SELECT id, title, author
                FROM books
                ORDER BY id DESC
            """)

            books = cursor.fetchall()

    return render_template_string(
        HTML_PAGE,
        books=books
    )


@app.route("/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()

    if title and author:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO books (title, author)
                    VALUES (%s, %s)
                    """,
                    (title, author)
                )

    return redirect(url_for("index"))


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete_book(book_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM books WHERE id = %s",
                (book_id,)
            )

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
