from flask import Blueprint, jsonify

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
book_bp = Blueprint("book", __name__, url_prefix="/book")


@book_bp.route('', methods=['GET'])
def get_all_books():
    """converts a list of objects into a list of dictionaries"""
    result = []
    for item in books:
        item_dict = {"id": item.id, 
        "title": item.title,
        "description":item.description}
        result.append(item_dict)
    return jsonify(result), 200

@book_bp.route('/<book_id>', methods=['GET'])
def get_one_book(book_id):
    
    try:
        book_id = int(book_id)
    except ValueError:
        return jsonify({"msg": f"invalid data type: {book_id}"}), 400
    chosen_book = None
    for item in books:
        if item.id == book_id:
            chosen_book = item
    if chosen_book is None:
        return({"msg": f"could not find book item with id: {book_id}"}), 404
    result = {
        'id': chosen_book.id,
        "title": chosen_book.title,
        "description": chosen_book.description,
    } 
    
    return jsonify(result), 200