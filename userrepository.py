from user import User

class UserRepository:
    def __init__(self, connection):
        self._connection = connection
    
    def create_user(self, user):
        self._connection.execute("INSERT INTO users (username, password) VALUES (%s, %s)", [user.username, user.password])
        return None
    
    def find(self, username):
        try:
            user_details = self._connection.execute("SELECT * FROM users WHERE username = (%s)", [username])[0]
        except IndexError:
            print("User not found")
            return None
        
        user = User(user_details["username"], user_details["password"], user_details["id"])

        return user



        