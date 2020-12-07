from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager

import models
from resources.dogs import dog
from resources.users import user

login_manager = LoginManager()

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.secret_key = "asdfasdfasdfasdfasdfasdf"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  try:
    return models.Users.get(models.Users.id == userid)
  except models.DoesNotExist:
    return None

# Logic for our database connection
@app.before_request
def before_request():
  """Connect to the database before each request."""
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  """Close the db connection after each requewst."""
  g.db.close()
  return response

CORS(dog, origins='*', supports_credentials=True)
CORS(user, origins='*', supports_credentials=True)

app.register_blueprint(dog, url_prefix='/api/v1/dogs')
app.register_blueprint(user, url_prefix='/user')

# The default URL ends in / ("website-url/").
@app.route('/')
def index():
  my_list = ["Hey", "check", "this", "out"]
  return my_list[0]

@app.route('/sayhi/<username>')
def hello(username):
  return "Hello {}".format(username)

# Run the app when the program starts!
if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)