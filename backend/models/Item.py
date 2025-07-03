from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField, IntField, EmbeddedDocument, EmbeddedDocumentField, BooleanField
from models.User import User

class Comment(EmbeddedDocument):
    """评论嵌入文档"""
    author_id = StringField(required=True)
    author_name = StringField(required=True)
    content = StringField(required=True, max_length=500)
    created_at = DateTimeField()
    
    meta = {
        'timestamps': True
    }

class Item(Document):
    user = ReferenceField(User, required=True)
    username = StringField(required=True)
    name = StringField(required=True, max_length=120)
    description = StringField(required=True)
    category = StringField(required=True)
    status = StringField(required=True, choices=('lost', 'found'))
    date = DateTimeField()
    contact = StringField()
    mapCoord = ListField(IntField())
    image_urls = ListField(StringField())
    comments = ListField(EmbeddedDocumentField(Comment))
    # location 字段是历史遗留，设为非必需，确保旧数据兼容
    location = StringField() 
    # 认领相关字段
    is_claimed = BooleanField(default=False)
    claimed_by = ReferenceField(User, null=True)
    claimed_at = DateTimeField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    meta = {
        'collection': 'items',
        'timestamps': True,
        'ordering': ['-created_at']
    }

    def to_json(self):
        """
        一个绝对健壮的序列化方法，可以处理任何历史遗留的脏数据。
        """
        # 安全地获取 date, 因为旧数据可能没有
        date_val = getattr(self, 'date', None)
        
        # 安全地获取 user 对象, 因为它可能在数据库层面断开连接
        user_info = {"id": None, "name": "未知用户", "avatar": None, "email": None}
        try:
            if self.user:
                user_info = {
                    "id": str(self.user.id), 
                    "name": self.user.name,
                    "avatar": getattr(self.user, 'avatar', None),
                    "email": getattr(self.user, 'email', None)
                }
        except Exception:
            # 如果 self.user 引用已失效, 则保持默认的"未知用户"
            pass

        # 处理地图坐标，生成地点文本描述
        map_coord = getattr(self, 'mapCoord', [])
        user_location = getattr(self, 'location', '').strip()
        
        # 优先使用用户输入的地点描述，如果没有则使用坐标信息
        if user_location:
            location_text = user_location
        elif map_coord and len(map_coord) >= 2:
            location_text = f"校园地图坐标 ({map_coord[0]}, {map_coord[1]})"
        else:
            location_text = "未指定地点"

        # 处理评论数据
        comments_data = []
        for comment in getattr(self, 'comments', []):
            try:
                # 获取评论作者的头像信息
                comment_avatar = None
                try:
                    if comment.author_id:
                        # 查询评论作者的用户信息
                        from bson import ObjectId
                        author = User.objects(id=ObjectId(comment.author_id)).first()
                        if author:
                            comment_avatar = getattr(author, 'avatar', None)
                except Exception:
                    # 如果查询失败，保持avatar为None
                    pass
                
                comments_data.append({
                    "nickname": comment.author_name,
                    "content": comment.content,
                    "time": comment.created_at.isoformat() if comment.created_at else None,
                    "avatar": comment_avatar  # 使用查询到的用户头像
                })
            except Exception:
                continue

        # 处理认领者信息
        claimed_by_info = None
        try:
            if getattr(self, 'claimed_by', None):
                claimed_by_info = {
                    "id": str(self.claimed_by.id),
                    "name": self.claimed_by.name,
                    "username": getattr(self.claimed_by, 'username', None),
                    "avatar": getattr(self.claimed_by, 'avatar', None),
                    "email": getattr(self.claimed_by, 'email', None)
                }
        except Exception:
            # 如果认领者引用失效，保持None
            pass

        return {
            "id": str(self.id),
            "name": getattr(self, 'name', '无标题'),
            "desc": getattr(self, 'description', ''),  # 前端期望的是desc字段
            "category": getattr(self, 'category', 'other'),
            "status": getattr(self, 'status', 'lost'),
            "type": getattr(self, 'status', 'lost'),  # 前端也期望type字段
            "location": getattr(self, 'location', ''),
            "locationText": location_text,  # 前端期望的地点文本
            "locationCoord": map_coord,  # 前端期望的坐标字段名
            "date": date_val.isoformat() if date_val else None,
            "time": self.created_at.isoformat() if self.created_at else None,  # 前端期望的时间字段
            "contact": getattr(self, 'contact', '无联系方式'),
            "images": [f"http://localhost:5000{url}" for url in getattr(self, 'image_urls', [])],  # 添加完整的URL前缀
            "comments": comments_data,  # 前端期望的评论字段
            "claimed": getattr(self, 'is_claimed', False),  # 前端期望的认领状态字段
            "is_claimed": getattr(self, 'is_claimed', False),  # 保持兼容性
            "claimedBy": claimed_by_info,  # 返回完整的认领者信息对象
            "claimed_by": claimed_by_info,  # 保持兼容性
            "claimedAt": self.claimed_at.isoformat() if getattr(self, 'claimed_at', None) else None,
            "claimed_at": self.claimed_at.isoformat() if getattr(self, 'claimed_at', None) else None,  # 保持兼容性
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user": user_info,
            "username": getattr(self, 'username', '未知用户'),
            "nickname": getattr(self, 'username', '未知用户'),  # 前端期望的昵称字段
            "avatar": user_info.get('avatar', None)  # 使用用户的头像信息
        }