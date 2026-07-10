from playwright.sync_api import Page, expect
from databaseconnection import DatabaseConnection

def test_books_page_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    h1 = page.locator("h1")

    expect(h1).to_have_text("Books in stock")

"""
Test that the books page lists all the books.
"""
def test_books_page_lists_all_books(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/books.sql")

    page.goto("http://127.0.0.1:5001/books")

    books_list = page.get_by_role("listitem")

    expect(books_list).to_have_text(["The Gruffalo by Julia Donaldson",
                                    "Ada Twist, Scientist by Andrea Beaty",
                                    "The Girl Who Drank the Moon by Kelly Barnhill",
                                    "Dragons in a Bag by Zetta Elliott"])
    

"""
Test that a new book can be created with the
form on the books page.
"""
def test_add_book_form_creates_new_book(page: Page):
    connection = DatabaseConnection()
    connection.connect()

    # first, create a test user so that Playwright can log in
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) VALUES ('testuser', '1234');")

    # make playwright log in to the site using the testuser account
    page.goto("http://127.0.0.1:5001/sessions/new")
    page.get_by_placeholder("Enter your username").fill("testuser")
    page.get_by_placeholder("Enter your password").fill("1234")
    page.get_by_role("button").click()


    # try to create a new book
    page.goto("http://127.0.0.1:5001/books")
    page.get_by_placeholder("Title").fill("One Hundred Years of Solitude")
    page.get_by_placeholder("Author").fill("Gabriel Garcia Marquez")
    page.get_by_role("button", name="Submit").click()

    new_book = page.get_by_text("One Hundred Years of Solitude")

    expect(new_book).to_be_visible()

