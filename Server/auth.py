import datetime
import random
import ssl
import smtplib
import bcrypt
from email.message import EmailMessage
import shutil

import pymongo
from bson import ObjectId


class AuthHandler:
    def __init__(self, db):
        self.db = db
        self.users = self.db["users"]
        self.scores = self.db["scores"]

    def login(self, data):
        print("DATA", data)
        user = self.users.find_one({"username": data["userName"]})
        if user is not None:
            if bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
                del user["password"]
                user['_id'] = str(user['_id'])
                return {"status": "success", "user": user}
            else:
                return {"status": "error", "message": "Wrong password"}
        else:
            return {"status": "error", "message": "User not found"}

    def register(self, data, file=None):
        # user = list(self.users.find({"$or": [{"name": data["userName"]}, {"email": data["email"]}]}))
        user = []
        print(data)

        if "@" not in data["email"]:
            print("Invalid email")
            return {"status": "error", "message": "Invalid email"}

        if len(user) == 0:

            user = {
                'email': data["email"],
                'username': data["username"],
                'password': bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()),
            }

            self.users.insert_one(user)
            user = self.users.find_one({"username": data["username"]})
            del user['password']
            user['_id'] = str(user['_id'])
            return {"status": "success", "user": user}
        else:
            print("USER EXITS email")

            return {"status": "error", "message": "User already exists"}

    def save_score(self, data):
        user = self.users.find_one({"username": data["userName"]})
        if user is None:
            return {"status": "error", "message": "User not found"}
        else:
            self.scores.insert_one({
                "userId": user["_id"],
                "score": data["score"],
                "username": data["userName"],
                'timestamp': datetime.datetime.utcnow()
            })
            return {"status": "success"}

    def get_leaderboard(self, username=""):
        scores = list(self.scores.find({"username": {"$regex": username, "$options": "x"}}).sort("score", -1))
        for score in scores:
            score["_id"] = str(score["_id"])
        return {"status": "success", "scores": scores}

    def get_user_scores(self, username):
        userData = self.users.find_one({"_id": ObjectId(username)})
        scores = self.scores.find({"username": userData['username']}).sort("score", -1).limit(10)
        del userData["password"]
        userData["_id"] = str(userData["_id"])
        scores = list(scores)
        for score in scores:
            score["_id"] = str(score["_id"])
        return {"status": "success", "scores": scores, "user": userData}

    def update_user_data(self, user_data, file):
        userData = self.users.find_one({"_id": ObjectId(user_data["_id"])})
        if userData is None:
            return {"status": "error", "message": "User not found"}
        else:
            if file is not None:
                if userData["avatar"] != "default.png":
                    shutil.rmtree("images/" + userData["avatar"])
            userAvatar = userData['avatar']
            if file is not None:
                userAvatar = file
            elif user_data["avatar"] is not None:
                userAvatar = user_data["avatar"]
            if user_data["password"] == "":
                userPassword = userData['password']
            else:
                userPassword = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt())
            self.users.update_one({"_id": ObjectId(user_data["_id"])}, {
                "$set": {
                    "username": user_data["username"] if user_data["username"] != "" else userData["username"],
                    "email": user_data["email"] if user_data["email"] != "" else userData["email"],
                    "avatar": userAvatar,
                    "password": userPassword
                }
            })
            userData = self.users.find_one({"_id": ObjectId(user_data["_id"])})
            del userData["password"]
            userData["_id"] = str(userData["_id"])
            return {"status": "success", "user": userData}
