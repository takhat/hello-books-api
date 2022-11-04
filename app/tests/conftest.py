import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING":True})
    #makes sure cache is cleared after every request is completed
    #so we are contacting db for the most up-to-date data for tests
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    #create & return tables within the app context
    with app.app_context():
        db.create_all()
        yield app
    
    #The test will use the tables created above
    #then the tables will be deleted:    
    
    #drop tables within the app context
    with app.app_context():
        db.drop_all()
    
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    #Arrange
    ocean_book = Book(title="Ocean Book", description = "water 4 ever")

    mountain_book = Book(title="Mountain Book", description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()

    


# @pytest.fixture
# def empty_list():
#     return []

# def test_len_of_empty_list(empty_list):
#     assert isinstance(empty_list, list)
#     assert len(empty_list) == 0

# @pytest.fixture
# def one_item(empty_list):
#     empty_list.append("item")
#     return empty_list

# def test_len_of_unary_list(one_item):
#     assert isinstance(one_item, list)
#     assert len(one_item) == 1
#     assert one_item[0] == "item"
# class FancyObject:
#     def __init__(self):
#         self.fancy = True
#         print(f"\nFancyObject: {self.fancy}")

#     def or_is_it(self):
#         self.fancy = not self.fancy

#     def cleanup(self):
#         print(f"\ncleanup: {self.fancy}")

# @pytest.fixture
# def so_fancy():
#     fancy_object = FancyObject()

#     yield fancy_object

#     fancy_object.cleanup()

# def test_so_fancy(so_fancy):
#     assert so_fancy.fancy
#     so_fancy.or_is_it()
#     assert not so_fancy.fancy