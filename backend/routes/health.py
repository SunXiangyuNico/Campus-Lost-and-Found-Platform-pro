from flask import Blueprint, jsonify
from middleware.auth import token_required

health_bp = Blueprint('health_bp', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    一个简单的健康检查端点
    """
    return jsonify({"status": "UP"}), 200

# 添加数据库连接测试
@health_bp.route('/health/db', methods=['GET'])
def db_check():
    try:
        from models.User import User
        from models.Message import Message
        
        # 测试数据库连接
        user_count = User.objects.count()
        message_count = Message.objects.count()
        
        return jsonify({
            "database": "Connected",
            "users_count": user_count,
            "messages_count": message_count,
            "status": "OK"
        }), 200
    except Exception as e:
        return jsonify({
            "database": "Error",
            "error": str(e),
            "status": "FAILED"
        }), 500

# 用户认证测试
@health_bp.route('/health/auth', methods=['GET'])
@token_required
def auth_check(current_user):
    try:
        return jsonify({
            "auth": "Valid",
            "user": {
                "id": str(current_user.id),
                "username": current_user.username,
                "name": current_user.name
            },
            "status": "OK"
        }), 200
    except Exception as e:
        return jsonify({
            "auth": "Error",
            "error": str(e),
            "status": "FAILED"
        }), 500 