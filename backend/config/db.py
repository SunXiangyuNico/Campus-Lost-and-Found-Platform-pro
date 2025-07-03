from mongoengine import connect
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get('MONGO_URI')
JWT_SECRET = os.environ.get('JWT_SECRET')

def initialize_db(app):
    """
    初始化数据库连接。
    从 Flask app.config 中获取 URI。
    """
    if not MONGO_URI:
        raise ValueError("No MONGO_URI set for Flask application")

    try:
        ca = certifi.where()
        connect(
            host=MONGO_URI, 
            alias='default', 
            serverSelectionTimeoutMS=30000,
            tlsCAFile=ca
        )
        print("MongoDB (Python) Connected...")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")