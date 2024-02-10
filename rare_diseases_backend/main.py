from flask import Flask
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import colors as co
import os
app = Flask(__name__)

load_dotenv()

client = MongoClient(os.getenv("ATLAS_URI"), server_api=ServerApi('1'))

def mongo_connect_test(log: bool = True) -> bool:
    # Send a ping to confirm a successful connection
    try:
        if log: print("\033[33mAttempting to connect to MongoDB...  \033[0m", end='')
        client.admin.command('ping')
        if log: print("\033[32mSuccessfully connected to Atlas instance.\033[0m")
        return True
    except Exception as e:
        print("\033[31mFailed to connect.\033[0m")
        print(e)
        return False

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    mongo_connect_test()
    app.run()