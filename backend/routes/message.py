from flask import Blueprint, request, jsonify
from middleware.auth import token_required
from controllers.messageController import (
    send_message,
    send_claim_request,
    handle_claim_response,
    get_conversations,
    get_messages_with_user,
    get_system_notifications,
    get_claim_requests,
    get_unread_count,
    mark_messages_as_read
)

# 创建一个名为 'message_bp' 的 Blueprint
message_bp = Blueprint('message_bp', __name__)

# 发送私信
@message_bp.route('/messages', methods=['POST'])
@token_required
def route_send_message(current_user):
    return send_message(current_user)

# 发送认领申请
@message_bp.route('/messages/claim-request', methods=['POST'])
@token_required
def route_send_claim_request(current_user):
    return send_claim_request(current_user)

# 处理认领申请响应
@message_bp.route('/messages/claim-response', methods=['POST'])
@token_required
def route_handle_claim_response(current_user):
    return handle_claim_response(current_user)

# 获取当前用户的所有对话列表
@message_bp.route('/messages/conversations', methods=['GET'])
@token_required
def route_get_conversations(current_user):
    return get_conversations(current_user)

# 获取与指定用户的消息历史
@message_bp.route('/messages/conversations/<other_user_id>', methods=['GET'])
@token_required
def route_get_messages_with_user(current_user, other_user_id):
    return get_messages_with_user(current_user, other_user_id)

# 获取系统通知
@message_bp.route('/messages/notifications', methods=['GET'])
@token_required
def route_get_system_notifications(current_user):
    return get_system_notifications(current_user)

# 获取认领申请列表
@message_bp.route('/messages/claim-requests', methods=['GET'])
@token_required
def route_get_claim_requests(current_user):
    return get_claim_requests(current_user)

# 获取未读消息数量
@message_bp.route('/messages/unread-count', methods=['GET'])
@token_required
def route_get_unread_count(current_user):
    return get_unread_count(current_user)

# 标记消息为已读
@message_bp.route('/messages/mark-read', methods=['POST'])
@token_required
def route_mark_messages_as_read(current_user):
    return mark_messages_as_read(current_user)

 