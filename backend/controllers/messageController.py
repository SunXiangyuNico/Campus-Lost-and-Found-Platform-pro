from flask import request, jsonify
from models.Message import Message
from models.User import User
from models.Item import Item
from mongoengine import Q
import json
import sys
from datetime import datetime

def send_message(current_user):
    """
    发送私信
    POST /api/messages/
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['recipientId', 'content']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # 检查收件人是否存在
        recipient = User.objects(id=data['recipientId']).first()
        if not recipient:
            return jsonify({'message': 'Recipient not found'}), 404

        # 检查关联物品是否存在（可选）
        item = None
        if data.get('itemId'):
            item = Item.objects(id=data['itemId']).first()
            if not item:
                return jsonify({'message': 'Item not found'}), 404
        
        # 不能给自己发消息
        if str(current_user.id) == data['recipientId']:
            return jsonify({'message': 'You cannot send a message to yourself'}), 400

        # 创建私信记录
        new_message = Message(
            message_type='private_message',
            sender_id=str(current_user.id),
            receiver_id=data['recipientId'],
            item_id=data.get('itemId'),
            content=data['content']
        )
        new_message.save()

        return jsonify(new_message.to_json(current_user_id=str(current_user.id))), 201

    except Exception as e:
        return jsonify({'message': 'Failed to send message', 'error': str(e)}), 500

def send_claim_request(current_user):
    """
    发送认领申请
    POST /api/messages/claim-request
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['itemId', 'content']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # 检查物品是否存在
        item = Item.objects(id=data['itemId']).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404

        # 检查是否已经被认领
        if item.is_claimed:
            return jsonify({'message': 'Item has already been claimed'}), 400

        # 不能认领自己发布的物品
        if str(item.user.id) == str(current_user.id):
            return jsonify({'message': 'You cannot claim your own item'}), 400

        # 检查是否已经发送过认领申请
        existing_claim = Message.objects(
            message_type='claim_request',
            sender_id=str(current_user.id),
            receiver_id=str(item.user.id),
            item_id=data['itemId'],
            claim_status='pending'
        ).first()
        
        if existing_claim:
            return jsonify({'message': 'You have already sent a claim request for this item'}), 400

        # 创建认领申请消息
        new_message = Message(
            message_type='claim_request',
            sender_id=str(current_user.id),
            receiver_id=str(item.user.id),
            item_id=data['itemId'],
            content=data['content'],
            claim_status='pending'
        )
        new_message.save()

        return jsonify(new_message.to_json(current_user_id=str(current_user.id))), 201

    except Exception as e:
        return jsonify({'message': 'Failed to send claim request', 'error': str(e)}), 500

def handle_claim_response(current_user):
    """
    处理认领申请响应
    POST /api/messages/claim-response
    """
    try:
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['claimRequestId', 'response']  # response: 'approved' or 'rejected'
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # 检查认领申请是否存在
        claim_request = Message.objects(id=data['claimRequestId']).first()
        if not claim_request:
            return jsonify({'message': 'Claim request not found'}), 404

        # 检查权限（只有物品发布者可以处理认领申请）
        if claim_request.receiver_id != str(current_user.id):
            return jsonify({'message': 'Permission denied'}), 403

        # 检查申请状态
        if claim_request.claim_status != 'pending':
            return jsonify({'message': 'Claim request has already been processed'}), 400

        # 更新认领申请状态
        response = data['response']
        if response not in ['approved', 'rejected']:
            return jsonify({'message': 'Invalid response'}), 400

        claim_request.claim_status = response
        claim_request.save()

        # 如果批准，更新物品状态
        if response == 'approved':
            item = Item.objects(id=claim_request.item_id).first()
            if item:
                item.is_claimed = True
                item.claimed_by = User.objects(id=claim_request.sender_id).first()
                item.claimed_at = datetime.utcnow()
                item.save()

        # 发送回复消息给申请者
        response_content = data.get('content', 
            f"您的认领申请已被{'批准' if response == 'approved' else '拒绝'}")
        
        response_message = Message(
            message_type='claim_response',
            sender_id=str(current_user.id),
            receiver_id=claim_request.sender_id,
            item_id=claim_request.item_id,
            content=response_content,
            claim_status=response
        )
        response_message.save()

        return jsonify({'message': 'Claim request processed successfully'}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to process claim request', 'error': str(e)}), 500

def get_conversations(current_user):
    """
    获取当前用户的所有对话列表（仅私信）- 修复版本
    GET /api/messages/conversations
    """
    try:
        current_user_id = str(current_user.id)
        
        # 使用更简单且正确的方法获取对话列表
        # 1. 先获取所有涉及当前用户的私信
        all_messages = Message.objects(
            message_type='private_message'
        ).filter(
            Q(sender_id=current_user_id) | Q(receiver_id=current_user_id)
        ).order_by('-created_at')
        
        # 2. 按对话伙伴分组处理
        conversations_dict = {}
        
        for message in all_messages:
            # 确定对话伙伴的ID
            other_user_id = message.receiver_id if message.sender_id == current_user_id else message.sender_id
            
            # 如果这个对话还没有记录，则创建记录
            if other_user_id not in conversations_dict:
                conversations_dict[other_user_id] = {
                    'other_user_id': other_user_id,
                    'last_message': message,
                    'unread_count': 0
                }
        
        # 3. 计算每个对话的未读消息数量
        for other_user_id in conversations_dict.keys():
            unread_count = Message.objects(
                message_type='private_message',
                sender_id=other_user_id,
                receiver_id=current_user_id,
                is_read=False
            ).count()
            conversations_dict[other_user_id]['unread_count'] = unread_count
        
        # 4. 构建返回数据
        conversations = []
        for other_user_id, conv_data in conversations_dict.items():
            # 获取对话伙伴用户信息
            other_user = User.objects(id=other_user_id).first()
            if not other_user:
                continue
            
            last_message = conv_data['last_message']
            
            # 获取关联物品信息
            item_info = None
            if last_message.item_id:
                item = Item.objects(id=last_message.item_id).first()
                if item:
                    item_info = {
                        'id': str(item.id),
                        'name': item.name
                    }
            
            # 安全地获取时间戳
            try:
                timestamp = last_message.created_at.isoformat() if last_message.created_at else datetime.utcnow().isoformat()
            except (AttributeError, KeyError):
                timestamp = datetime.utcnow().isoformat()
            
            conversations.append({
                'withUser': {
                    'id': str(other_user.id),
                    'username': other_user.username,
                    'name': other_user.name,
                    'avatar': other_user.avatar
                },
                'item': item_info,
                'lastMessage': last_message.content[:50] if last_message.content else '',  # 预览
                'timestamp': timestamp,
                'unreadCount': conv_data['unread_count']
            })
        
        # 5. 按最后消息时间排序
        conversations.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify(conversations), 200

    except Exception as e:
        return jsonify({'message': 'Failed to get conversations', 'error': str(e)}), 500

def get_messages_with_user(current_user, other_user_id):
    """
    获取与指定用户的消息历史（仅私信）
    GET /api/messages/<other_user_id>
    """
    try:
        current_user_id = str(current_user.id)
        
        # 验证对方用户是否存在
        other_user = User.objects(id=other_user_id).first()
        if not other_user:
            return jsonify({'message': 'User not found'}), 404
        
        # 查询私信记录
        messages = Message.objects(
            message_type='private_message'
        ).filter(
            Q(sender_id=current_user_id, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver_id=current_user_id)
        ).order_by('created_at')  # 按时间升序排列

        # 将发给当前用户的未读消息标记为已读
        Message.objects(
            message_type='private_message',
            sender_id=other_user_id, 
            receiver_id=current_user_id, 
            is_read=False
        ).update(set__is_read=True)

        # 返回格式调整为前端期望的格式
        return jsonify({
            'messages': [msg.to_json(current_user_id=current_user_id) for msg in messages]
        }), 200

    except Exception as e:
        return jsonify({'message': 'Failed to retrieve messages', 'error': str(e)}), 500

def get_system_notifications(current_user):
    """
    获取系统通知
    GET /api/messages/notifications
    """
    try:
        current_user_id = str(current_user.id)
        print(f"[DEBUG] 获取用户 {current_user_id} 的系统通知", file=sys.stderr)
        
        # 查询系统通知
        notifications = Message.objects(
            message_type='system_notification',
            receiver_id=current_user_id
        ).order_by('-created_at')

        print(f"[DEBUG] 找到 {len(notifications)} 个系统通知", file=sys.stderr)
        
        result = []
        for notification in notifications:
            try:
                # 安全地解析通知数据
                notification_data = {}
                if hasattr(notification, 'notification_data') and notification.notification_data:
                    try:
                        notification_data = json.loads(notification.notification_data)
                    except Exception as e:
                        print(f"[DEBUG] 解析通知数据失败: {e}", file=sys.stderr)
                        notification_data = {}
                
                # 安全地获取关联物品信息
                item_info = None
                if hasattr(notification, 'item_id') and notification.item_id:
                    try:
                        item = Item.objects(id=notification.item_id).first()
                        if item:
                            item_info = {
                                'id': str(item.id),
                                'name': getattr(item, 'name', '未知物品'),
                                'description': (getattr(item, 'description', '') or '')[:100]
                            }
                    except Exception as e:
                        print(f"[DEBUG] 获取关联物品信息失败: {e}", file=sys.stderr)
                        item_info = None
                
                # 安全地获取所有字段
                notification_id = str(notification.id) if hasattr(notification, 'id') else ''
                content = getattr(notification, 'content', '') or ''
                is_read = getattr(notification, 'is_read', False)
                item_id = getattr(notification, 'item_id', None)
                
                # 安全地处理时间戳
                timestamp = datetime.utcnow().isoformat()
                if hasattr(notification, 'created_at') and notification.created_at:
                    try:
                        timestamp = notification.created_at.isoformat()
                    except Exception as e:
                        print(f"[DEBUG] 时间戳处理失败: {e}", file=sys.stderr)
                
                result.append({
                    'id': notification_id,
                    'content': content,
                    'isRead': is_read,
                    'timestamp': timestamp,
                    'itemId': item_id,
                    'item': item_info,
                    'data': notification_data
                })
                
                print(f"[DEBUG] 成功处理通知: {notification_id}", file=sys.stderr)
                
            except Exception as e:
                print(f"[DEBUG] 处理单个通知失败: {e}", file=sys.stderr)
                # 跳过这个通知，继续处理下一个
                continue

        print(f"[DEBUG] 返回 {len(result)} 个有效通知", file=sys.stderr)
        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR] get_system_notifications 函数执行失败: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({'message': 'Failed to get notifications', 'error': str(e)}), 500

def get_claim_requests(current_user):
    """
    获取认领申请列表（我收到的申请）
    GET /api/messages/claim-requests
    """
    try:
        current_user_id = str(current_user.id)
        print(f"[DEBUG] 获取用户 {current_user_id} 的认领申请")
        
        # 查询收到的认领申请
        claim_requests = Message.objects(
            message_type='claim_request',
            receiver_id=current_user_id
        ).order_by('-created_at')

        print(f"[DEBUG] 找到 {len(claim_requests)} 个认领申请")
        
        result = []
        for request in claim_requests:
            try:
                print(f"[DEBUG] 处理认领申请 ID: {request.id}")
                
                # 安全地获取申请者信息
                requester = None
                if request.sender_id:
                    try:
                        requester = User.objects(id=request.sender_id).first()
                        print(f"[DEBUG] 申请者: {requester.name if requester else 'None'}")
                    except Exception as e:
                        print(f"[ERROR] 获取申请者信息失败: {e}")
                
                # 安全地获取物品信息
                item = None
                if request.item_id:
                    try:
                        item = Item.objects(id=request.item_id).first()
                        print(f"[DEBUG] 物品: {item.name if item else 'None'}")
                    except Exception as e:
                        print(f"[ERROR] 获取物品信息失败: {e}")
                
                # 安全地获取时间戳
                try:
                    timestamp = request.created_at.isoformat() if hasattr(request, 'created_at') and request.created_at else datetime.utcnow().isoformat()
                except Exception as e:
                    print(f"[ERROR] 时间戳转换失败: {e}")
                    timestamp = datetime.utcnow().isoformat()
                
                # 只有当申请者和物品都存在时才添加到结果中
                if requester and item:
                    try:
                        result.append({
                            'id': str(request.id),
                            'content': getattr(request, 'content', ''),
                            'status': getattr(request, 'claim_status', 'pending'),
                            'isRead': getattr(request, 'is_read', False),
                            'timestamp': timestamp,
                            'requester': {
                                'id': str(requester.id),
                                'name': getattr(requester, 'name', '未知用户'),
                                'avatar': getattr(requester, 'avatar', None)
                            },
                            'item': {
                                'id': str(item.id),
                                'name': getattr(item, 'name', '未知物品'),
                                'description': (getattr(item, 'description', '') or '')[:100],
                                'status': getattr(item, 'status', 'unknown')
                            }
                        })
                        print(f"[DEBUG] 成功添加认领申请到结果")
                    except Exception as e:
                        print(f"[ERROR] 构建结果对象失败: {e}")
                else:
                    print(f"[WARNING] 跳过认领申请 {request.id}: requester={bool(requester)}, item={bool(item)}")
                    
            except Exception as e:
                print(f"[ERROR] 处理单个认领申请失败 {request.id}: {e}")
                continue

        print(f"[DEBUG] 返回 {len(result)} 个有效的认领申请")
        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR] get_claim_requests 函数执行失败: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Failed to get claim requests', 'error': str(e)}), 500

def get_unread_count(current_user):
    """
    获取未读消息数量
    GET /api/messages/unread-count
    """
    try:
        current_user_id = str(current_user.id)
        
        # 统计各类型未读消息
        private_messages = Message.objects(
            message_type='private_message',
            receiver_id=current_user_id,
            is_read=False
        ).count()
        
        notifications = Message.objects(
            message_type='system_notification',
            receiver_id=current_user_id,
            is_read=False
        ).count()
        
        claim_requests = Message.objects(
            message_type='claim_request',
            receiver_id=current_user_id,
            is_read=False
        ).count()
        
        claim_responses = Message.objects(
            message_type='claim_response',
            receiver_id=current_user_id,
            is_read=False
        ).count()

        total = private_messages + notifications + claim_requests + claim_responses

        return jsonify({
            'total': total,
            'privateMessages': private_messages,
            'notifications': notifications,
            'claimRequests': claim_requests,
            'claimResponses': claim_responses
        }), 200

    except Exception as e:
        return jsonify({'message': 'Failed to get unread count', 'error': str(e)}), 500

def mark_messages_as_read(current_user):
    """
    标记消息为已读
    POST /api/messages/mark-read
    """
    try:
        data = request.get_json() or {}
        message_ids = data.get('messageIds', [])
        message_type = data.get('messageType')  # 可选，标记特定类型的所有消息为已读
        other_user_id = data.get('otherUserId')  # 可选，标记与特定用户的所有私信为已读
        
        current_user_id = str(current_user.id)
        
        if message_ids:
            # 标记指定消息为已读
            Message.objects(
                id__in=message_ids,
                receiver_id=current_user_id
            ).update(set__is_read=True)
        elif message_type and other_user_id:
            # 标记与特定用户的特定类型消息为已读
            Message.objects(
                message_type=message_type,
                sender_id=other_user_id,
                receiver_id=current_user_id,
                is_read=False
            ).update(set__is_read=True)
        elif message_type:
            # 标记特定类型的所有消息为已读
            Message.objects(
                message_type=message_type,
                receiver_id=current_user_id,
                is_read=False
            ).update(set__is_read=True)
        else:
            return jsonify({'message': 'No messageIds, messageType, or otherUserId provided'}), 400

        return jsonify({'message': 'Messages marked as read'}), 200

    except Exception as e:
        return jsonify({'message': 'Failed to mark messages as read', 'error': str(e)}), 500 