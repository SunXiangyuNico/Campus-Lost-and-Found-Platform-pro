from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mail import Mail
import os

# 在创建app实例和导入其他模块之前，最先加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

from config.db import initialize_db
from routes.auth import auth_bp
from routes.item import item_bp
from routes.message import message_bp
from routes.map import map_bp
from routes.health import health_bp

# 初始化 Flask 应用
app = Flask(__name__)

# 为CORS提供更健壮的配置，包括静态文件访问
CORS(
    app, 
    resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type", "Accept"],
            "supports_credentials": True
        },
        r"/static/*": {
            "origins": ["http://localhost:5173", "http://127.0.0.1:5173"]
        }
    }, 
    supports_credentials=True
)

# 配置静态文件路由，确保上传的文件可以被访问
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    return send_from_directory(upload_folder, filename)

# 配置头像静态文件路由
@app.route('/static/avatars/<filename>')
def avatar_file(filename):
    avatar_folder = os.path.join(os.path.dirname(__file__), 'static', 'avatars')
    return send_from_directory(avatar_folder, filename)

# --- 标准的 Flask 配置方法 ---
# 1. 从环境变量加载敏感配置
MONGO_URI_FROM_ENV = os.environ.get('MONGO_URI')
if not MONGO_URI_FROM_ENV:
    raise ValueError("No MONGO_URI set for Flask application")

# 2. 将配置设置到 app.config 对象中
app.config['MONGO_URI'] = MONGO_URI_FROM_ENV

# 初始化数据库 (现在它会从 app.config 读取)
initialize_db(app)

# 初始化邮件服务
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True').lower() in ['true', '1', 't']
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'False').lower() in ['true', '1', 't']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)

# 注册蓝图，并统一添加 /api 前缀
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(item_bp, url_prefix='/api')
app.register_blueprint(message_bp, url_prefix='/api')
app.register_blueprint(map_bp, url_prefix='/api')
app.register_blueprint(health_bp, url_prefix='/api')

# 全局错误处理
@app.errorhandler(404)
def not_found(e):
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    app.run(debug=True)