from flask import Blueprint, request, jsonify
from controllers.authController import (
    register_user, login_user, get_user_profile, 
    change_password, update_avatar, delete_account, get_my_posts,
    get_me, update_me
)
from controllers.itemController import get_my_claims
from middleware.auth import token_required
from models.User import User

# 创建一个名为 'auth' 的蓝图 (Blueprint)
# 蓝图用于组织一组相关的路由，使其模块化
auth_bp = Blueprint('auth_bp', __name__)

# @route   POST /api/auth/register
# @desc    注册新用户
# @access  Public
@auth_bp.route('/auth/register', methods=['POST'])
def register():
    return register_user(request)

# @route   POST /api/auth/login
# @desc    用户登录并获取 token
# @access  Public
@auth_bp.route('/auth/login', methods=['POST'])
def login():
    return login_user(request)

# @route   GET /api/auth/me
# @desc    获取当前登录用户的信息
# @access  Private
@auth_bp.route('/auth/me', methods=['GET'])
@token_required
def me(current_user):
    return get_me(current_user)

# @route   PUT /api/auth/me
# @desc    更新当前用户信息
# @access  Private
@auth_bp.route('/auth/me', methods=['PUT'])
@token_required
def update_profile(current_user):
    return update_me(current_user)

# @route   POST /api/auth/change-password
# @desc    修改密码
# @access  Private
@auth_bp.route('/auth/change-password', methods=['POST'])
@token_required
def change_user_password(current_user):
    return change_password(current_user)

# @route   POST /api/auth/update-avatar
# @desc    更新头像
# @access  Private
@auth_bp.route('/auth/update-avatar', methods=['POST'])
@token_required
def update_user_avatar(current_user):
    return update_avatar(current_user)

# @route   DELETE /api/auth/account
# @desc    注销用户账户
# @access  Private
@auth_bp.route('/auth/account', methods=['DELETE'])
@token_required
def delete_user_account(current_user):
    return delete_account(current_user)

# @route   GET /api/auth/my-posts
# @desc    获取当前用户的所有帖子
# @access  Private
@auth_bp.route('/auth/my-posts', methods=['GET'])
@token_required
def my_posts(current_user):
    return get_my_posts(current_user)

# @route   GET /api/auth/my-claims
# @desc    获取当前用户的所有认领
# @access  Private
@auth_bp.route('/auth/my-claims', methods=['GET'])
@token_required
def my_claims(current_user):
    return get_my_claims(current_user)

# 获取用户列表（用于测试）
@auth_bp.route('/users', methods=['GET'])
@token_required
def get_users_list(current_user):
    """
    获取用户列表（用于私信测试）
    GET /api/users
    """
    try:
        # 获取除当前用户外的前10个用户
        users = User.objects(id__ne=current_user.id).limit(10)
        
        user_list = []
        for user in users:
            user_list.append({
                'id': str(user.id),
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'avatar': user.avatar
            })
        
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get users', 'error': str(e)}), 500 