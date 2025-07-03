from flask import request, jsonify
from models.User import User
# 导入邮件发送服务
from services.notificationService import send_email
import bcrypt
import jwt
import json
import datetime
import os
from werkzeug.utils import secure_filename
from config.db import JWT_SECRET # 从中央配置导入

# 配置头像上传目录
AVATAR_UPLOAD_FOLDER = os.path.join('backend', 'static', 'avatars')
os.makedirs(AVATAR_UPLOAD_FOLDER, exist_ok=True)

# 直接从环境变量中获取 JWT 密钥
# JWT_SECRET = os.environ.get('JWT_SECRET')

def register_user(request):
    """
    Controller: 注册新用户 (根据新规范)
    """
    try:
        # 支持表单数据（用于文件上传）和JSON数据
        if request.content_type and 'multipart/form-data' in request.content_type:
            data = request.form
            avatar_file = request.files.get('avatar')
        else:
            data = request.get_json()
            avatar_file = None
        
        # 增加详细的日志，便于调试
        print(f"收到的注册请求数据: {data}")

        name = data.get('name')
        studentId = data.get('studentId')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        wechat = data.get('wechat')

        # 1. 验证所有必需字段是否存在
        if not name:
            return jsonify({"msg": "姓名是必填项"}), 400
        if not studentId:
            return jsonify({"msg": "学号是必填项"}), 400
        if not email:
            return jsonify({"msg": "邮箱是必填项"}), 400
        if not password:
            return jsonify({"msg": "密码是必填项"}), 400
        
        # 2. 检查学号或邮箱是否已被占用
        if User.objects(studentId=studentId).first():
            return jsonify({"msg": "该学号已被注册"}), 400
        if User.objects(email=email).first():
            return jsonify({"msg": "该邮箱已被注册"}), 400

        # 3. 密码强度检查
        if len(password) < 6:
            return jsonify({"msg": "密码长度不能少于6位"}), 400

        # 4. 对密码进行哈希加密
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 5. 处理头像上传
        avatar_url = None
        if avatar_file and avatar_file.filename:
            try:
                filename = f"{datetime.datetime.now().timestamp()}_{secure_filename(avatar_file.filename)}"
                save_path = os.path.join(AVATAR_UPLOAD_FOLDER, filename)
                avatar_file.save(save_path)
                avatar_url = f"/static/avatars/{filename}"
            except Exception as e:
                print(f"头像上传失败: {e}")
                # 头像上传失败不影响注册，继续使用默认头像

        # 6. 创建新用户实例，使用学号作为默认用户名
        new_user = User(
            username=studentId, # 使用学号作为唯一的登录用户名
            name=name,
            studentId=studentId,
            email=email,
            password=hashed_password.decode('utf-8'),
            phone=phone,
            wechat=wechat,
            avatar=avatar_url
        )
        new_user.save()

        # 注册成功后，也立即为用户生成 token，实现自动登录
        payload = {
            'user': {
                'id': str(new_user.id)
            },
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

        return jsonify({"token": token, "user": new_user.to_json()}), 201

    except Exception as e:
        print(f"Error in register_user: {e}")
        return jsonify({"msg": "服务器内部错误"}), 500


def login_user(request):
    """
    Controller: 用户登录 (根据新规范)
    """
    try:
        data = request.get_json()
        username = data.get('username') # 使用用户名登录
        password = data.get('password')

        if not all([username, password]):
            return jsonify({"msg": "用户名和密码不能为空"}), 400

        # 2. 根据用户名查找用户
        user = User.objects(username=username).first()
        if not user:
            return jsonify({"msg": "用户名或密码错误"}), 401 # 401 Unauthorized 更符合语义

        # 3. 比较密码
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # 4. 创建 JWT payload
            payload = {
                'user': {
                    'id': str(user.id)
                },
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)
            }

            # 5. 签名并生成 JWT
            token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
            
            # 登录成功时，返回token和用户信息
            return jsonify({"token": token, "user": user.to_json()}), 200
        else:
            return jsonify({"msg": "用户名或密码错误"}), 401

    except Exception as e:
        print(f"Error in login_user: {e}")
        return jsonify({"msg": "服务器内部错误"}), 500


def get_user_profile(user_id):
    """
    Controller: 根据用户ID获取用户信息
    """
    try:
        user = User.objects.get(id=user_id)
        return jsonify(user.to_json()), 200
    except User.DoesNotExist:
        return jsonify({"msg": "User not found"}), 404
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        return jsonify({"msg": "Server Error"}), 500

def get_me(current_user):
    """
    Controller: 获取当前登录用户的信息
    (需要 auth 中间件注入用户信息)
    """
    try:
        # user 对象由 token_required 装饰器直接传入
        user = current_user
        
        if not user:
             return jsonify({"msg": "User not found"}), 404
        
        # 使用我们之前在 User 模型中定义的 to_json 方法来序列化
        return jsonify(user.to_json()), 200

    except Exception as e:
        print(f"Error in get_me: {e}")
        return jsonify({"msg": "Server Error"}), 500

def update_me(current_user):
    """
    Controller: 更新当前登录用户的信息
    (例如: 用户名, 姓名, 电话, 微信)
    """
    try:
        # 1. user 对象由 token_required 装饰器直接传入
        user = current_user

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # 2. 获取请求体中的 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({"msg": "Request body must be JSON"}), 400

        # 3. 更新允许修改的字段
        if 'name' in data:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'wechat' in data:
            user.wechat = data['wechat']
        
        # 不允许通过此接口更新用户名(学号)、邮箱或密码

        # 4. 保存更新后的用户对象
        user.save()

        # 5. 返回更新后的用户信息
        return jsonify(user.to_json()), 200

    except Exception as e:
        print(f"Error in update_me: {e}")
        return jsonify({"msg": "Server Error"}), 500

def change_password(current_user):
    """
    Controller: 修改密码
    """
    try:
        user = current_user
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json()
        old_password = data.get('oldPassword')
        new_password = data.get('newPassword')

        if not old_password or not new_password:
            return jsonify({"msg": "旧密码和新密码不能为空"}), 400

        # 验证旧密码
        if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"msg": "旧密码错误"}), 400

        # 验证新密码强度
        if len(new_password) < 6:
            return jsonify({"msg": "新密码长度不能少于6位"}), 400

        # 加密新密码并保存
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user.password = hashed_password.decode('utf-8')
        user.save()

        return jsonify({"msg": "密码修改成功"}), 200

    except Exception as e:
        print(f"Error in change_password: {e}")
        return jsonify({"msg": "Server Error"}), 500

def update_avatar(current_user):
    """
    Controller: 更新头像
    """
    try:
        user = current_user
        if not user:
            return jsonify({"msg": "User not found"}), 404

        avatar_file = request.files.get('avatar')
        if not avatar_file or not avatar_file.filename:
            return jsonify({"msg": "请选择头像文件"}), 400

        try:
            # 删除旧头像文件（如果存在）
            if user.avatar and user.avatar.startswith('/static/avatars/'):
                old_filename = user.avatar.replace('/static/avatars/', '')
                old_path = os.path.join(AVATAR_UPLOAD_FOLDER, old_filename)
                if os.path.exists(old_path):
                    os.remove(old_path)

            # 保存新头像
            filename = f"{datetime.datetime.now().timestamp()}_{secure_filename(avatar_file.filename)}"
            save_path = os.path.join(AVATAR_UPLOAD_FOLDER, filename)
            avatar_file.save(save_path)
            avatar_url = f"/static/avatars/{filename}"

            # 更新用户头像URL
            user.avatar = avatar_url
            user.save()

            return jsonify({"msg": "头像更新成功", "avatar": f"http://localhost:5000{avatar_url}"}), 200

        except Exception as e:
            print(f"头像上传失败: {e}")
            return jsonify({"msg": "头像上传失败"}), 500

    except Exception as e:
        print(f"Error in update_avatar: {e}")
        return jsonify({"msg": "Server Error"}), 500

def delete_account(current_user):
    """
    Controller: 注销用户（删除账户）
    """
    try:
        user = current_user
        if not user:
            return jsonify({"msg": "User not found"}), 404

        data = request.get_json()
        password = data.get('password')

        if not password:
            return jsonify({"msg": "请输入密码确认注销"}), 400

        # 验证密码
        if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return jsonify({"msg": "密码错误"}), 400

        # 删除用户头像文件（如果存在）
        if user.avatar and user.avatar.startswith('/static/avatars/'):
            filename = user.avatar.replace('/static/avatars/', '')
            file_path = os.path.join(AVATAR_UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        # 删除用户账户
        user.delete()

        return jsonify({"msg": "账户注销成功"}), 200

    except Exception as e:
        print(f"Error in delete_account: {e}")
        return jsonify({"msg": "Server Error"}), 500

def get_my_posts(current_user):
    """
    Controller: 获取当前用户的所有帖子
    """
    try:
        from models.Item import Item
        
        user = current_user
        if not user:
            return jsonify({"msg": "User not found"}), 404

        # 获取用户的所有帖子
        items = Item.objects(user=user).order_by('-created_at')
        
        result = []
        for item in items:
            try:
                result.append(item.to_json())
            except Exception as e:
                print(f"Failed to serialize item {item.id}: {e}")
                continue

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in get_my_posts: {e}")
        return jsonify({"msg": "Server Error"}), 500