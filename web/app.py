from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]


def check_credentials(username, password):
    assert username is not None, "Please enter a username"
    assert password is not None, "Please enter a password"

    if users.find({"Username": username}).count() > 0:
        hashed_pw = users.find({"Username": username})[0]["Password"]
        return bcrypt.hashpw(password.encode("utf-8"), hashed_pw) == hashed_pw
    else:
        return False


def check_credits(username):
    return users.find({"Username": username})[0]["Credits"]


class Register(Resource):
    """Handle registration of a new user."""

    def post(self):
        posted_data = request.get_json(force=True)

        # Get credentials and hash password
        username = posted_data.get("username", None)
        password = posted_data.get("password", None)
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if users.find({"Username": username}).count() == 0:
            # Store credentials in database
            users.insert_one({"Username": username,
                              "Password": hashed_pw,
                              "Sentence": "",
                              "Credits": 5})
        else:
            return make_response(("Username already exists!", 302))

        return jsonify(message="Successfully signed up !")


class Store(Resource):
    """Authenticate user and save the user sentence."""

    def post(self):
        posted_data = request.get_json(force=True)

        # Get data
        username = posted_data.get("username", None)
        password = posted_data.get("password", None)
        sentence = posted_data.get("sentence", None)

        # Check credentials
        correct_credentials = check_credentials(username, password)
        if not correct_credentials:
            return make_response(("Incorrect credentials !", 302))

        # Check user credits
        num_credits = check_credits(username)
        if num_credits <= 0:
            return make_response(("Not enough credits !", 302))

        # Update database
        users.update_many(
            {"Username": username},
            {"$set": {"Sentence": sentence, "Credits": num_credits-1}}
        )

        return jsonify(message="Sentence saved successfully !")


class Get(Resource):
    """Authenticate and get the user sentence."""

    def post(self):
        posted_data = request.get_json(force=True)

        # Get data
        username = posted_data.get("username", None)
        password = posted_data.get("password", None)

        # Check credentials
        correct_credentials = check_credentials(username, password)
        if not correct_credentials:
            return make_response(("Incorrect credentials !", 302))

        # Check user credits
        num_credits = check_credits(username)
        if num_credits <= 0:
            return make_response(("Not enough credits !", 302))

        # Update database
        users.update_many({"Username": username},
                          {"$set": {"Credits": num_credits-1}})

        # Get stored sentence by the user
        sentence = users.find({"Username": username})[0]["Sentence"]
        return jsonify(sentence=sentence)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
