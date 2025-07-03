from mongoengine import Document, StringField, EmailField, DateTimeField
import datetime

# 使用 MongoEngine 定义用户的数据库模型结构 (Document)
class User(Document):
    """
    用户模型定义
    """
    # 用户名，作为登录凭证，必须唯一
    username = StringField(unique=True)
    
    # 姓名
    name = StringField(required=True)
    
    # 学号，必须唯一
    studentId = StringField(required=True, unique=True)
    
    # 邮箱，必须唯一
    email = EmailField(required=True, unique=True)
    
    # 密码 - 存储的是哈希后的密码
    password = StringField(required=True)
    
    # 电话 (可选)
    phone = StringField()
    
    # 微信号 (可选)
    wechat = StringField()
    
    # 头像URL (可选)
    avatar = StringField()
    
    # meta 字典用于配置模型的元数据
    meta = {
        'collection': 'users',  # 明确指定在数据库中的集合名称为 'users'
        'timestamps': True      # 自动管理 createdAt 和 updatedAt 字段
    }

    def to_json(self, *args, **kwargs):
        """
        重写 to_json 方法以自定义输出。
        这个版本更健壮，能处理可能缺少时间戳字段的旧数据。
        """
        # 使用 hasattr 检查属性是否存在，然后再访问
        created_at_iso = self.created_at.isoformat() if hasattr(self, 'created_at') and self.created_at else None
        updated_at_iso = self.updated_at.isoformat() if hasattr(self, 'updated_at') and self.updated_at else None

        return {
            "id": str(self.id),
            "username": self.username,
            "name": self.name,
            "studentId": self.studentId,
            "email": self.email,
            "phone": self.phone,
            "wechat": self.wechat,
            "avatar": getattr(self, 'avatar', None),
            "createdAt": created_at_iso,
            "updatedAt": updated_at_iso
        }
