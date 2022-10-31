from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.book import Book
'''
class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Book1", "Book1 description"),
    Book(2, "Book2", "Book2 description"),
    Book(3, "Book3", "Book3 description")
]
'''
books_bp = Blueprint("book", __name__, url_prefix="/books")
@books_bp.route("", methods=["GET"])
def read_all_books():

    books = Book.query.all()
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_response)

@books_bp.route("", methods=["POST"])
def create_book():
        request_body = request.get_json()
        if "title" not in request_body:
            return make_response("invalid request", 400)
        new_book = Book(
            title = request_body["title"],
            description = request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()
        return f"Book {new_book.title} created with id: {new_book.id}", 201
    
# @books_bp.route('', methods=['GET'])
# def get_all_books():
#     """converts a list of objects into a list of dictionaries"""
#     result = []
#     for item in books:
#         item_dict = {"id": item.id, 
#         "title": item.title,
#         "description":item.description}
#         result.append(item_dict)
#     return jsonify(result), 200

# @books_bp.route('/<book_id>', methods=['GET'])
# def get_one_book(book_id):
    
#     try:
#         book_id = int(book_id)
#     except ValueError:
#         return jsonify({"msg": f"invalid data type: {book_id}"}), 400
#     chosen_book = None
#     for item in books:
#         if item.id == book_id:
#             chosen_book = item
#     if chosen_book is None:
#         return({"msg": f"could not find book item with id: {book_id}"}), 404
#     result = {
#         'id': chosen_book.id,
#         "title": chosen_book.title,
#         "description": chosen_book.description,
#     } 
    
#     return jsonify(result), 200