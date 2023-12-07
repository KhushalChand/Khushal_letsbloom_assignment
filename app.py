from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)

# Create tables
db.create_all()

# Seed the database with mock data
if not Book.query.first():
    db.session.add(Book(title="Book 1", author="Author 1"))
    db.session.add(Book(title="Book 2", author="Author 2"))
    db.session.commit()

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = [{"id": book.id, "title": book.title, "author": book.author} for book in books]
    return jsonify(book_list)

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"id": new_book.id, "title": new_book.title, "author": new_book.author})

# Endpoint 3: Update Book Details
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    db.session.commit()

    return jsonify({"id": book.id, "title": book.title, "author": book.author})

if __name__ == '__main__':
    app.run(debug=True)
