from models.Item import Item
from models.User import User
from models.Message import Message
import json
import math
from datetime import datetime, timedelta

def calculate_distance(coord1, coord2):
    """
    计算两个地图坐标之间的距离（使用欧几里得距离）
    coord1, coord2: [x, y] 格式的坐标列表
    返回距离值（像素单位）
    """
    if not coord1 or not coord2 or len(coord1) < 2 or len(coord2) < 2:
        return float('inf')
    
    try:
        x1, y1 = coord1[0], coord1[1]
        x2, y2 = coord2[0], coord2[1]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance
    except (TypeError, ValueError, IndexError):
        return float('inf')

def check_content_similarity(content1, content2):
    """
    简单的内容相似度检查
    基于关键词匹配来判断物品描述的相似度
    """
    if not content1 or not content2:
        return 0
    
    # 转换为小写并分词
    words1 = set(content1.lower().split())
    words2 = set(content2.lower().split())
    
    # 计算交集和并集
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    # 计算相似度（Jaccard相似度）
    if len(union) == 0:
        return 0
    
    similarity = len(intersection) / len(union)
    return similarity

def find_matching_lost_items(found_item):
    """
    为拾到的物品寻找匹配的失物帖子
    返回匹配的失物帖子列表
    """
    if found_item.status != 'found':
        return []
    
    # 查找所有未被认领的失物帖子
    lost_items = Item.objects(
        status='lost',
        is_claimed=False
    )
    
    matches = []
    max_distance = 100  # 最大匹配距离（像素）
    min_similarity = 0.2  # 最小内容相似度
    
    for lost_item in lost_items:
        # 跳过同一用户发布的帖子
        try:
            if str(lost_item.user.id) == str(found_item.user.id):
                continue
        except Exception as e:
            # 如果用户引用无效，跳过这个物品
            print(f"[WARNING] 跳过无效物品 {lost_item.id}，用户引用错误: {e}")
            continue
        
        # 计算地理距离
        distance = calculate_distance(found_item.mapCoord, lost_item.mapCoord)
        
        # 计算内容相似度
        # 比较物品名称和描述
        name_similarity = check_content_similarity(found_item.name, lost_item.name)
        desc_similarity = check_content_similarity(found_item.description, lost_item.description)
        content_similarity = max(name_similarity, desc_similarity)
        
        # 类别匹配加分
        category_match = 1.0 if found_item.category == lost_item.category else 0.0
        
        # 综合匹配分数
        if distance <= max_distance and (content_similarity >= min_similarity or category_match > 0):
            match_score = (
                (max_distance - distance) / max_distance * 0.4 +  # 距离权重40%
                content_similarity * 0.4 +  # 内容相似度权重40%
                category_match * 0.2  # 类别匹配权重20%
            )
            
            matches.append({
                'lost_item': lost_item,
                'score': match_score,
                'distance': distance,
                'content_similarity': content_similarity,
                'category_match': category_match
            })
    
    # 按匹配分数排序，返回前5个最佳匹配
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:5]

def send_matching_notifications(found_item):
    """
    为新发布的拾物帖子发送匹配通知
    """
    try:
        matches = find_matching_lost_items(found_item)
        
        if not matches:
            print(f"没有为拾物帖子 {found_item.name} 找到匹配的失物帖子")
            return
        
        for match in matches:
            lost_item = match['lost_item']
            
            # 构造通知内容
            notification_content = (
                f"系统检测到可能有人捡到了您丢失的物品！\n"
                f"拾到物品：{found_item.name}\n"
                f"物品描述：{found_item.description[:100]}...\n"
                f"拾到地点：距离您丢失地点约 {int(match['distance'])} 像素\n"
                f"匹配度：{match['score']:.2f}\n"
                f"建议您查看详情并联系拾到者确认。"
            )
            
            # 构造通知数据
            notification_data = {
                'found_item_id': str(found_item.id),
                'lost_item_id': str(lost_item.id),
                'match_score': match['score'],
                'distance': match['distance'],
                'content_similarity': match['content_similarity'],
                'category_match': match['category_match']
            }
            
            # 创建系统通知消息
            try:
                notification = Message(
                    message_type='system_notification',
                    sender_id='system',  # 系统发送
                    receiver_id=str(lost_item.user.id),
                    item_id=str(found_item.id),  # 关联到拾物帖子
                    content=notification_content,
                    notification_data=json.dumps(notification_data)
                )
                notification.save()
                
                print(f"已为用户 {lost_item.user.name} 发送匹配通知，匹配拾物帖子：{found_item.name}")
            except Exception as e:
                print(f"[WARNING] 发送通知失败，用户引用错误: {e}")
        
        print(f"成功为拾物帖子 {found_item.name} 发送了 {len(matches)} 条匹配通知")
        
    except Exception as e:
        print(f"发送匹配通知时出错: {e}")

def process_new_found_item(item_id):
    """
    处理新发布的拾物帖子，发送匹配通知
    这个函数可以在物品发布时调用
    """
    try:
        found_item = Item.objects(id=item_id).first()
        if not found_item:
            print(f"未找到物品 ID: {item_id}")
            return
        
        if found_item.status == 'found':
            send_matching_notifications(found_item)
        else:
            print(f"物品 {found_item.name} 不是拾物帖子，跳过匹配")
            
    except Exception as e:
        print(f"处理新拾物帖子时出错: {e}")

def cleanup_old_notifications():
    """
    清理30天前的系统通知
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        
        old_notifications = Message.objects(
            message_type='system_notification',
            created_at__lt=cutoff_date
        )
        
        count = old_notifications.count()
        old_notifications.delete()
        
        print(f"已清理 {count} 条30天前的系统通知")
        
    except Exception as e:
        print(f"清理旧通知时出错: {e}")

def get_match_statistics():
    """
    获取匹配统计信息（用于管理和调试）
    """
    try:
        total_notifications = Message.objects(message_type='system_notification').count()
        recent_notifications = Message.objects(
            message_type='system_notification',
            created_at__gte=datetime.utcnow() - timedelta(days=7)
        ).count()
        
        return {
            'total_notifications': total_notifications,
            'recent_notifications': recent_notifications,
            'success_rate': 'N/A'  # 需要更复杂的逻辑来计算成功率
        }
        
    except Exception as e:
        print(f"获取匹配统计信息时出错: {e}")
        return None

def find_matching_found_items(lost_item):
    """
    为丢失的物品寻找匹配的招领帖子
    返回匹配的招领帖子列表
    """
    if lost_item.status != 'lost':
        return []
    
    # 查找所有未被认领的招领帖子
    found_items = Item.objects(
        status='found',
        is_claimed=False
    )
    
    matches = []
    max_distance = 100  # 最大匹配距离（像素）
    min_similarity = 0.2  # 最小内容相似度
    
    for found_item in found_items:
        # 跳过同一用户发布的帖子
        try:
            if str(found_item.user.id) == str(lost_item.user.id):
                continue
        except Exception as e:
            # 如果用户引用无效，跳过这个物品
            print(f"[WARNING] 跳过无效物品 {found_item.id}，用户引用错误: {e}")
            continue
        
        # 计算地理距离
        distance = calculate_distance(lost_item.mapCoord, found_item.mapCoord)
        
        # 计算内容相似度
        # 比较物品名称和描述
        name_similarity = check_content_similarity(lost_item.name, found_item.name)
        desc_similarity = check_content_similarity(lost_item.description, found_item.description)
        content_similarity = max(name_similarity, desc_similarity)
        
        # 类别匹配加分
        category_match = 1.0 if lost_item.category == found_item.category else 0.0
        
        # 综合匹配分数
        if distance <= max_distance and (content_similarity >= min_similarity or category_match > 0):
            match_score = (
                (max_distance - distance) / max_distance * 0.4 +  # 距离权重40%
                content_similarity * 0.4 +  # 内容相似度权重40%
                category_match * 0.2  # 类别匹配权重20%
            )
            
            matches.append({
                'found_item': found_item,
                'score': match_score,
                'distance': distance,
                'content_similarity': content_similarity,
                'category_match': category_match
            })
    
    # 按匹配分数排序，返回前5个最佳匹配
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches[:5]

def send_lost_item_matching_notifications(lost_item):
    """
    为新发布的失物帖子发送匹配通知
    """
    try:
        print(f"[DEBUG] 开始为失物帖子 {lost_item.name} (ID: {lost_item.id}) 寻找匹配的招领帖子")
        matches = find_matching_found_items(lost_item)
        
        if not matches:
            print(f"[DEBUG] 没有为失物帖子 {lost_item.name} 找到匹配的招领帖子")
            return
        
        for match in matches:
            found_item = match['found_item']
            
            # 构造通知内容
            notification_content = (
                f"系统检测到可能有人捡到了您丢失的物品！\n"
                f"招领物品：{found_item.name}\n"
                f"物品描述：{found_item.description[:100]}{'...' if len(found_item.description) > 100 else ''}\n"
                f"招领地点：距离您丢失地点约 {int(match['distance'])} 像素\n"
                f"匹配度：{match['score']:.2f}\n"
                f"建议您查看详情并联系拾到者确认。"
            )
            
            # 构造通知数据
            notification_data = {
                'found_item_id': str(found_item.id),
                'lost_item_id': str(lost_item.id),
                'match_score': match['score'],
                'distance': match['distance'],
                'content_similarity': match['content_similarity'],
                'category_match': match['category_match']
            }
            
            # 创建系统通知消息
            try:
                notification = Message(
                    message_type='system_notification',
                    sender_id='system',  # 系统发送
                    receiver_id=str(lost_item.user.id),
                    item_id=str(found_item.id),  # 关联到招领帖子
                    content=notification_content,
                    notification_data=json.dumps(notification_data)
                )
                notification.save()
                
                print(f"已为用户 {lost_item.user.name} 发送匹配通知，匹配招领帖子：{found_item.name}")
            except Exception as e:
                print(f"[WARNING] 发送通知失败，用户引用错误: {e}")
        
        print(f"成功为失物帖子 {lost_item.name} 发送了 {len(matches)} 条匹配通知")
        
    except Exception as e:
        print(f"发送失物匹配通知时出错: {e}")

def process_new_lost_item(item_id):
    """
    处理新发布的失物帖子，发送匹配通知
    这个函数可以在物品发布时调用
    """
    try:
        print(f"[DEBUG] 处理新失物帖子，物品ID: {item_id}")
        lost_item = Item.objects(id=item_id).first()
        if not lost_item:
            print(f"[DEBUG] 未找到物品 ID: {item_id}")
            return
        
        print(f"[DEBUG] 找到物品: {lost_item.name}, 状态: {lost_item.status}")
        if lost_item.status == 'lost':
            send_lost_item_matching_notifications(lost_item)
        else:
            print(f"[DEBUG] 物品 {lost_item.name} 不是失物帖子，跳过匹配")
            
    except Exception as e:
        print(f"[DEBUG] 处理新失物帖子时出错: {e}")
        import traceback
        traceback.print_exc() 