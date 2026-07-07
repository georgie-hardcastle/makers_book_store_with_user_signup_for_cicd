from flask import Flask, render_template, request, redirect
from databaseconnection import DatabaseConnection
from bookrepository import BookRepository
from book import Book
from userrepository import UserRepository
from user import User

# instantiate a Flask app object
app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/books_json', methods=['GET'])
def get_books_json():
    return [
        {
        "title": "The Gruffalo",
        "author": "Julia Donaldson"
        },
        {
        "title": "Ada Twist, Scientist",
        "author": "Andrea Beaty"
        },
        {
        "title": "The Girl Who Drank the Moon",
        "author": "Kelly Barnhill"
        },
        {
        "title": "Dragons in a Bag",
        "author": "Zetta Elliott"
        }
    ]

@app.route('/authors_json', methods=['GET'])
def get_authors_json():
    return [
    {
        "name": "Julia Donaldson",
        "dob": "1948-09-16"
    },
    {
        "name": "Andrea Beaty",
        "dob": "1961-10-08"
    },
    {
        "name": "Kelly Barnhill",
        "dob": "1973-01-01"
    },
    {
        "name": "Zetta Elliott",
        "dob": "1979-11-11"
    }
    ]


@app.route('/books', methods=['GET'])
def get_books_page():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)

    books = book_repository.all()
    print(books)

    return render_template("books.html", books=books)

@app.route("/books", methods=['POST'])
def add_new_book():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)

    new_book = request.form
    book = Book(title=new_book["title"], author=new_book["author"])

    book_repository.create_book(book)

    return redirect("/books")

@app.route("/users/new", methods=["GET"])
def get_signup_page():
    return render_template("signup_form.html")

@app.route("/thanks", methods=["GET"])
def get_thanks_page():
    return render_template("thanks.html")

@app.route("/users", methods=["POST"])
def add_new_user():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)

    new_user = request.form
    user = User(username=new_user["username"], password=new_user["password"])

    user_repository.create_user(user)

    return redirect("/thanks")



# @app.route('/team', methods=['GET'])
# def get_team_names():
#     team = ["Buffy", "Willow", "Xander", "Spike", "Anya"]

#     return render_template("team.html", team=team)



# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
