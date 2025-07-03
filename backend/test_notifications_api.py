#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.Message import Message
from models.User import User
import mongoengine
from dotenv import load_dotenv
import certifi
import json

# 加载环境变量
load_dotenv()

print("测试系统通知API...")

try:
    # 连接数据库
    MONGO_URI = os.environ.get('MONGO_URI')
    ca = certifi.where()
    mongoengine.connect(
        host=MONGO_URI, 
        alias='default', 
        serverSelectionTimeoutMS=30000,
        tlsCAFile=ca
    )
    print("✓ 数据库连接成功")

    # 查看系统通知
    notifications = Message.objects(message_type='system_notification').order_by('-created_at')
    print(f"系统通知总数: {len(notifications)}")
    
    if len(notifications) > 0:
        print("\n最近的系统通知:")
        for i, notif in enumerate(notifications[:3]):
            print(f"\n=== 通知 {i+1} ===")
            print(f"ID: {notif.id}")
            print(f"接收者ID: {notif.receiver_id}")
            print(f"发送者ID: {notif.sender_id}")
            print(f"关联物品ID: {notif.item_id}")
            print(f"是否已读: {notif.is_read}")
            
            # 尝试获取创建时间
            timestamp = None
            for field_name in ['created_at', 'createdAt', 'timestamp']:
                if hasattr(notif, field_name):
                    timestamp = getattr(notif, field_name)
                    break
            print(f"创建时间: {timestamp}")
            
            print(f"内容: {notif.content[:100]}...")
            
            # 检查关联的用户是否存在
            try:
                user = User.objects(id=notif.receiver_id).first()
                if user:
                    print(f"接收者: {user.name} ({user.email})")
                else:
                    print(f"⚠️  接收者不存在: {notif.receiver_id}")
            except Exception as e:
                print(f"❌ 检查接收者失败: {e}")
            
            # 检查通知数据格式
            if notif.notification_data:
                try:
                    data = json.loads(notif.notification_data)
                    print(f"通知数据: {data}")
                except Exception as e:
                    print(f"⚠️  通知数据格式错误: {e}")
    
    # 检查特定用户的通知
    print("\n=== 按用户分组的通知 ===")
    user_notifications = {}
    for notif in notifications:
        user_id = notif.receiver_id
        if user_id not in user_notifications:
            user_notifications[user_id] = []
        user_notifications[user_id].append(notif)
    
    for user_id, user_notifs in user_notifications.items():
        try:
            user = User.objects(id=user_id).first()
            user_name = user.name if user else "未知用户"
            print(f"用户 {user_name} ({user_id}): {len(user_notifs)} 条通知")
        except:
            print(f"用户 {user_id}: {len(user_notifs)} 条通知 (用户信息获取失败)")

    print("\n✅ 检查完成!")

except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc() 