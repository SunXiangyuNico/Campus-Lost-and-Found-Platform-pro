from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime

class Message(Document):
    """
    消息模型 - 支持私信、系统通知、认领申请等多种消息类型
    """
    # 消息类型：private_message(私信), system_notification(系统通知), claim_request(认领申请), claim_response(认领回复)
    message_type = StringField(required=True, choices=['private_message', 'system_notification', 'claim_request', 'claim_response'], default='private_message')
    
    # 内容字段
    content = StringField(required=True, max_length=1000)  # 限制消息长度
    is_read = BooleanField(default=False)  # 对应API的已读状态

    # 关联字段
    sender_id = StringField(required=True)  # 发送者User.id，系统通知时可为"system"
    receiver_id = StringField(required=True)  # 接收者User.id
    item_id = StringField()  # 关联Item.id，可选字段

    # 认领相关字段
    claim_status = StringField(choices=['pending', 'approved', 'rejected'], default=None)  # 认领申请状态
    
    # 系统通知相关字段
    notification_data = StringField()  # 存储系统通知的额外数据（JSON格式）

    # 元数据
    meta = {
        'collection': 'messages',
        'indexes': [
            'sender_id',
            'receiver_id',
            'item_id',
            'message_type',
            'is_read',
            ('sender_id', 'receiver_id'),  # 复合索引加速对话查询
            ('receiver_id', 'is_read'),    # 复合索引加速未读消息查询
            ('receiver_id', 'message_type') # 复合索引加速按类型查询消息
        ],
        'timestamps': True  # 自动时间戳
    }

    def to_json(self, *args, **kwargs):
        """返回消息的JSON格式"""
        try:
            timestamp = self.created_at.isoformat() if self.created_at else None
        except AttributeError:
            timestamp = datetime.utcnow().isoformat()
            
        return {
            "id": str(self.id),
            "messageType": self.message_type,
            "content": self.content,
            "isRead": self.is_read,
            "senderId": self.sender_id,
            "receiverId": self.receiver_id,
            "itemId": self.item_id,
            "claimStatus": self.claim_status,
            "notificationData": self.notification_data,
            "timestamp": timestamp,
            # 以下为API文档6.3接口需要的字段
            "sender": "me" if kwargs.get('current_user_id') == self.sender_id else "them"
        } 