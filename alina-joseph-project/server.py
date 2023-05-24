from flask_app import app 
import flask_app.controllers.index
import flask_app.controllers.users
import flask_app.controllers.concerns

if __name__ == "__main__":
    app.run(debug=True, port=5002)

