from functools import wraps
from flask import request, jsonify
import jwt
from config.db import JWT_SECRET
from models.User import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # 确保以 'Bearer ' 开头
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'msg': '授权令牌缺失 (Token is missing)!'}), 401

        try:
            # 解码 token，获取用户ID
            data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = data.get('user', {}).get('id')
            if not user_id:
                raise jwt.InvalidTokenError("Token payload is invalid.")

            # 使用ID从数据库中获取完整的、存在的用户对象
            current_user = User.objects.get(id=user_id)

        except jwt.ExpiredSignatureError:
            return jsonify({'msg': '授权令牌已过期 (Token has expired)!'}), 401
        except jwt.InvalidTokenError as e:
            return jsonify({'msg': f'授权令牌无效 (Token is invalid): {e}'}), 401
        except User.DoesNotExist:
            return jsonify({'msg': '授权令牌对应的用户不存在 (User not found)!'}), 401
        except Exception as e:
            # 捕获其他所有潜在错误
            return jsonify({'msg': f'授权验证时发生未知错误: {e}'}), 500
            
        # 核心修复：将查询到的完整用户对象，作为第一个位置参数，传递给被装饰的函数
        return f(current_user, *args, **kwargs)

    return decorated