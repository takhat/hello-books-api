from app.models.book import Book
import pytest

# get all books and return no records
def test_get_all_books_with_empty_db(client):
    response = client.get('/books')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

# get all books and return no records
def test_get_one_book_with_empty_db_returns_404(client):
    response = client.get('/books/1')
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'message': "book 1 not found"}
#get one book by id

def test_get_one_book_by_id(client, two_saved_books):
    response = client.get('/books/1')
    response_body = response.get_json()

    #Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "water 4 ever"
    }
#create one book
def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book successfully created with id: 1"

#update book
def test_update_one_book_with_populated_db(client, two_saved_books):
    response = client.put("/books/1", json={
        "title": "Updated Book",
        "description": "Updated Book description!"
    })
    response_body = response.get_json()
    book = Book.query.get(1)
    # Assert
    assert response.status_code == 200
    assert response_body == "book # 1 successfully updated"
    assert book.title== "Updated Book"
    assert book.description == "Updated Book description!"

#delete book
def test_delete_one_book_with_populated_db(client, two_saved_books):
    response = client.delete("/books/1")
    response_body = response.get_json()
    book = Book.query.get(1)
    # Assert
    assert response.status_code == 200
    assert response_body == "book # 1 successfully deleted"
    assert book == None
def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act & Assert
    with pytest.raises(KeyError, match='title'):
        response = client.post("/books", json=test_data)

def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        response = client.post("/books", json=test_data)

def test_create_one_book_with_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book successfully created with id: 3"

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Book(id = 1,
                    title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_id():
    # Arrange
    test_data = Book(title="Ocean Book",
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Ocean Book"
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_title():
    # Arrange
    test_data = Book(id=1,
                    description="watr 4evr")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "watr 4evr"

def test_to_dict_missing_description():
    # Arrange
    test_data = Book(id = 1,
                    title="Ocean Book")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Ocean Book"
    assert result["description"] is None