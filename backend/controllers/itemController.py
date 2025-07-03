from flask import request, jsonify
from models.Item import Item, Comment
from models.User import User
from bson import ObjectId
import datetime
import sys
import os
import json
from werkzeug.utils import secure_filename
import math
import re

# --- 配置上传文件 ---
# 定义上传文件夹的相对路径
UPLOAD_FOLDER = os.path.join('backend', 'static', 'uploads')
# 确保这个目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_distance(coord1, coord2):
    """计算两个坐标点之间的欧几里得距离"""
    if not coord1 or not coord2 or len(coord1) < 2 or len(coord2) < 2:
        return float('inf')
    
    x1, y1 = coord1[0], coord1[1]
    x2, y2 = coord2[0], coord2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def fuzzy_match(query, text):
    """
    改进的模糊匹配算法
    支持：完全匹配、部分匹配、字符包含、顺序匹配、中文分词
    返回值：0-100的匹配分数
    """
    if not query or not text:
        return 0
    
    query = query.lower().strip()
    text = text.lower().strip()
    
    # 1. 完全匹配 - 最高分
    if query == text:
        return 100
    
    # 2. 完整包含匹配 - 高分
    if query in text:
        # 根据匹配长度比例给分
        match_ratio = len(query) / len(text)
        return min(95, 80 + match_ratio * 15)
    
    # 3. 单词/词汇匹配
    query_words = [w for w in re.split(r'[\s\u3000]+', query) if w]  # 支持中文空格
    text_words = [w for w in re.split(r'[\s\u3000]+', text) if w]
    
    if not query_words:
        return 0
    
    word_matches = 0
    total_word_score = 0
    
    for q_word in query_words:
        best_match = 0
        for t_word in text_words:
            if q_word == t_word:
                best_match = max(best_match, 100)  # 完全匹配的词
            elif q_word in t_word or t_word in q_word:
                # 计算包含匹配的比例
                if len(q_word) <= len(t_word):
                    ratio = len(q_word) / len(t_word)
                else:
                    ratio = len(t_word) / len(q_word)
                best_match = max(best_match, 60 + ratio * 30)
            elif len(q_word) >= 2 and len(t_word) >= 2:
                # 计算字符相似度
                common_chars = len(set(q_word) & set(t_word))
                char_ratio = common_chars / max(len(q_word), len(t_word))
                if char_ratio >= 0.5:  # 至少50%字符相同
                    best_match = max(best_match, char_ratio * 50)
        
        total_word_score += best_match
        if best_match > 0:
            word_matches += 1
    
    word_score = total_word_score / len(query_words) if query_words else 0
    
    # 4. 字符级别匹配
    common_chars = len(set(query) & set(text))
    char_score = (common_chars / len(query)) * 40 if len(query) > 0 else 0
    
    # 5. 顺序匹配（检查查询字符是否按顺序出现在文本中）
    sequence_score = 0
    if len(query) >= 2:
        i, j = 0, 0
        while i < len(query) and j < len(text):
            if query[i] == text[j]:
                i += 1
            j += 1
        if i == len(query):  # 所有查询字符都按顺序找到
            sequence_score = 30
    
    # 返回最高分数
    final_score = max(word_score, char_score, sequence_score)
    return min(final_score, 100)

def calculate_search_score(item, query, search_coord=None):
    """
    改进的搜索匹配分数计算
    权重：物品名称(40%) > 描述内容(30%) > 地点(20%) > 时间(10%)
    """
    if not query:
        return 0
    
    total_score = 0
    
    # 1. 物品名称匹配 (权重: 40%)
    name = getattr(item, 'name', '')
    if name:
        name_match = fuzzy_match(query, name)
        total_score += (name_match / 100) * 40
        # 调试信息
        if name_match > 0:
            print(f"[DEBUG] Name '{name}' matches '{query}' with score {name_match}", file=sys.stderr)
    
    # 2. 描述内容匹配 (权重: 30%)
    description = getattr(item, 'description', '')
    if description:
        desc_match = fuzzy_match(query, description)
        total_score += (desc_match / 100) * 30
        # 调试信息
        if desc_match > 0:
            print(f"[DEBUG] Description '{description}' matches '{query}' with score {desc_match}", file=sys.stderr)
    
    # 3. 地点匹配 (权重: 20%)
    location = getattr(item, 'location', '')
    if location:
        loc_match = fuzzy_match(query, location)
        total_score += (loc_match / 100) * 20
        # 调试信息
        if loc_match > 0:
            print(f"[DEBUG] Location '{location}' matches '{query}' with score {loc_match}", file=sys.stderr)
    
    # 4. 类别匹配 (额外加分)
    category = getattr(item, 'category', '')
    category_map = {
        'id': ['证件', '身份证', '学生证', '卡', '工作证', '银行卡'],
        'electronics': ['电子', '手机', '电脑', '耳机', '充电器', '数码', '平板', '相机', '键盘', '鼠标'],
        'book': ['书', '教材', '笔记本', '资料', '文具', '笔', '本子'],
        'clothes': ['衣服', '衣物', '鞋子', '帽子', '包', '背包', '钱包', '手套', '围巾'],
        'key': ['钥匙', '门卡', '卡片', '钥匙扣'],
        'other': ['其他', '杂物']
    }
    
    for cat_key, cat_words in category_map.items():
        if category == cat_key:
            for cat_word in cat_words:
                if fuzzy_match(query, cat_word) > 60:
                    total_score += 8  # 类别匹配额外加分
                    break
    
    # 5. 坐标匹配 (如果提供了搜索坐标)
    if search_coord:
        item_coord = getattr(item, 'mapCoord', [])
        if item_coord and len(item_coord) >= 2:
            distance = calculate_distance(search_coord, item_coord)
            # 距离越近分数越高，最大额外加分15分
            if distance <= 30:
                total_score += 15
            elif distance <= 50:
                total_score += 12
            elif distance <= 100:
                total_score += 8
            elif distance <= 200:
                total_score += 5
            elif distance <= 300:
                total_score += 2
    
    # 6. 时间新旧程度 (权重: 10%)
    created_at = getattr(item, 'created_at', None)
    if created_at:
        days_ago = (datetime.datetime.now() - created_at).days
        if days_ago <= 1:
            total_score += 10
        elif days_ago <= 3:
            total_score += 8
        elif days_ago <= 7:
            total_score += 6
        elif days_ago <= 30:
            total_score += 4
        else:
            total_score += 1
    
    # 调试信息
    if total_score > 0:
        print(f"[DEBUG] Item '{name}' total score: {total_score}", file=sys.stderr)
    
    return min(total_score, 100)

def search_items():
    """
    智能搜索物品
    支持文本搜索和坐标匹配，带权重排序
    """
    try:
        query = request.args.get('q', '').strip()
        coord_x = request.args.get('x', type=int)
        coord_y = request.args.get('y', type=int)
        min_score = request.args.get('min_score', 5, type=float)  # 降低最低匹配分数
        
        print(f"[DEBUG] Search query: '{query}', min_score: {min_score}", file=sys.stderr)
        
        if not query and (coord_x is None or coord_y is None):
            return jsonify({"msg": "请提供搜索关键词或坐标"}), 400
        
        # 获取所有物品
        all_items = Item.objects.all()
        print(f"[DEBUG] Total items in database: {len(all_items)}", file=sys.stderr)
        
        # 准备搜索坐标
        search_coord = None
        if coord_x is not None and coord_y is not None:
            search_coord = [coord_x, coord_y]
        
        # 计算每个物品的匹配分数
        scored_items = []
        for item in all_items:
            score = calculate_search_score(item, query, search_coord)
            if score >= min_score:  # 只包含达到最低分数的物品
                scored_items.append((item, score))
        
        print(f"[DEBUG] Items matching criteria: {len(scored_items)}", file=sys.stderr)
        
        # 按分数排序（降序）
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # 序列化结果
        result = []
        for item, score in scored_items:
            try:
                item_data = item.to_json()
                item_data['_searchScore'] = round(score, 2)  # 保留2位小数
                result.append(item_data)
            except Exception as e:
                print(f"Failed to serialize item {item.id}: {e}", file=sys.stderr)
                continue
        
        return jsonify({
            "results": result,
            "total": len(result),
            "query": query,
            "searchCoord": search_coord,
            "minScore": min_score
        }), 200
        
    except Exception as e:
        print(f"!!! EXCEPTION in search_items: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({"msg": "搜索时发生错误", "error": str(e)}), 500

def delete_item(current_user, item_id):
    """
    删除帖子 - 只有发布者可以删除自己的帖子
    """
    try:
        print(f"[DEBUG] delete_item called with item_id: {item_id}", file=sys.stderr)
        print(f"[DEBUG] current_user: {current_user}", file=sys.stderr)
        print(f"[DEBUG] current_user.id: {current_user.id}", file=sys.stderr)
        
        # 检查item_id格式是否有效  
        if not ObjectId.is_valid(item_id):
            print(f"[DEBUG] Invalid ObjectId format: {item_id}", file=sys.stderr)
            return jsonify({"msg": "Invalid item ID format"}), 400
            
        # 根据ID查找物品
        item = Item.objects(id=item_id).first()
        if not item:
            print(f"[DEBUG] Item not found: {item_id}", file=sys.stderr)
            return jsonify({"msg": "物品不存在"}), 404
        
        print(f"[DEBUG] Found item: {item}", file=sys.stderr)
        print(f"[DEBUG] item.user: {item.user}", file=sys.stderr)
        print(f"[DEBUG] item.user.id: {item.user.id}", file=sys.stderr)
        print(f"[DEBUG] Comparing: {str(item.user.id)} vs {str(current_user.id)}", file=sys.stderr)
        
        # 检查权限 - 只有发布者可以删除
        if str(item.user.id) != str(current_user.id):
            print(f"[DEBUG] Permission denied: item owner {str(item.user.id)} != current user {str(current_user.id)}", file=sys.stderr)
            return jsonify({"msg": "无权限删除此物品"}), 403
        
        # 删除关联的图片文件
        if hasattr(item, 'image_urls') and item.image_urls:
            for image_url in item.image_urls:
                if image_url.startswith('/static/uploads/'):
                    filename = image_url.replace('/static/uploads/', '')
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            print(f"[INFO] Deleted image file: {file_path}")
                        except Exception as e:
                            print(f"[WARNING] Failed to delete image file {file_path}: {e}")
        
        # 删除物品记录
        item.delete()
        
        return jsonify({"msg": "物品删除成功"}), 200
        
    except Exception as e:
        print(f"Error in delete_item: {e}", file=sys.stderr)
        return jsonify({"msg": "删除失败", "error": str(e)}), 500

def create_item(current_user):
    """
    创建新的失物或招领物品，包含图片上传 (最终简化版本)
    """
    try:
        data = request.form
        files = request.files.getlist('images')

        image_urls = []
        if files:
            for file in files:
                if file and file.filename:
                    filename = f"{datetime.datetime.now().timestamp()}_{secure_filename(file.filename)}"
                    save_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(save_path)
                    image_urls.append(f"/static/uploads/{filename}")

        item_date = None
        raw_date = data.get('date')
        if raw_date:
            item_date = datetime.datetime.fromisoformat(raw_date.replace('Z', '+00:00'))

        item_map_coord = None
        raw_map_coord = data.get('mapCoord')
        if raw_map_coord:
            item_map_coord = json.loads(raw_map_coord)

        new_item = Item(
            user=current_user,
            username=current_user.name,
            name=data.get('name'),
            description=data.get('description'),
            category=data.get('category'),
            status=data.get('status'),
            date=item_date,
            contact=data.get('contact'),
            mapCoord=item_map_coord,
            location=data.get('location', ''),  # 添加地点描述字段
            image_urls=image_urls,
            comments=[]  # 初始化空评论列表
        )
        
        new_item.save() # MongoEngine 会在这里执行基于模型的验证
        
        # 如果是拾物帖子，触发匹配通知
        if new_item.status == 'found':
            try:
                from services.matchingService import process_new_found_item
                process_new_found_item(str(new_item.id))
            except Exception as e:
                print(f"Failed to process matching notifications: {e}", file=sys.stderr)
                # 匹配通知失败不影响物品发布成功
        
        # 如果是失物帖子，也触发匹配通知
        if new_item.status == 'lost':
            try:
                print(f"[DEBUG] 触发失物帖子匹配，物品: {new_item.name}, ID: {new_item.id}", file=sys.stderr)
                from services.matchingService import process_new_lost_item
                process_new_lost_item(str(new_item.id))
            except Exception as e:
                print(f"Failed to process lost item matching notifications: {e}", file=sys.stderr)
                # 匹配通知失败不影响物品发布成功
        
        return jsonify(new_item.to_json()), 201

    except Exception as e:
        print(f"!!! EXCEPTION in create_item: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        # 将数据库验证错误更清晰地返回给前端
        if 'ValidationError' in str(type(e)):
            return jsonify({"msg": f"发布失败，请检查填写内容: {str(e)}"}), 400
        return jsonify({"msg": "服务器内部错误，创建失败", "error": str(e)}), 500

def get_all_items():
    """
    获取所有物品 (最终健壮版本)
    """
    try:
        items = Item.objects.order_by('-created_at').all()
        
        result = []
        for item in items:
            try:
                result.append(item.to_json())
            except Exception as e:
                print(f"!!! FAILED to serialize item with ID: {item.id}. Error: {e}", file=sys.stderr)
                continue
                
        return jsonify(result), 200
        
    except Exception as e:
        print(f"!!! EXCEPTION in get_all_items: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({"msg": "获取物品列表时发生严重错误", "error": str(e)}), 500

def get_item_by_id(item_id):
    try:
        if not ObjectId.is_valid(item_id):
            return jsonify({"msg": "Invalid item ID format"}), 400
            
        item = Item.objects.get(id=item_id)
        return jsonify(item.to_json()), 200
    except Item.DoesNotExist:
        return jsonify({"msg": "Item not found"}), 404
    except Exception as e:
        return jsonify({"msg": "Could not retrieve item", "error": str(e)}), 500

def add_comment_to_item(current_user, item_id):
    """
    为指定物品添加评论
    """
    try:
        if not ObjectId.is_valid(item_id):
            return jsonify({"msg": "Invalid item ID format"}), 400
            
        data = request.get_json()
        content = data.get('content', '').strip()
        
        if not content:
            return jsonify({"msg": "评论内容不能为空"}), 400
            
        if len(content) > 500:
            return jsonify({"msg": "评论内容不能超过500字"}), 400
            
        item = Item.objects.get(id=item_id)
        
        # 创建新评论
        new_comment = Comment(
            author_id=str(current_user.id),
            author_name=current_user.name,
            content=content,
            created_at=datetime.datetime.now()
        )
        
        # 添加到物品的评论列表
        item.comments.append(new_comment)
        item.save()
        
        return jsonify({
            "msg": "评论添加成功",
            "comment": {
                "nickname": new_comment.author_name,
                "content": new_comment.content,
                "time": new_comment.created_at.isoformat(),
                "avatar": None
            }
        }), 201
        
    except Item.DoesNotExist:
        return jsonify({"msg": "物品不存在"}), 404
    except Exception as e:
        print(f"!!! EXCEPTION in add_comment_to_item: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return jsonify({"msg": "添加评论失败", "error": str(e)}), 500

def update_item(current_user, item_id):
    try:
        print(f"[DEBUG] update_item called with item_id: {item_id}", file=sys.stderr)
        print(f"[DEBUG] current_user: {current_user}", file=sys.stderr)
        print(f"[DEBUG] current_user.id: {current_user.id}", file=sys.stderr)
        
        if not ObjectId.is_valid(item_id):
            return jsonify({"msg": "Invalid item ID format"}), 400

        data = request.get_json()
        item = Item.objects.get(id=item_id)
        
        print(f"[DEBUG] Found item: {item}", file=sys.stderr)
        print(f"[DEBUG] item.user: {item.user}", file=sys.stderr)
        print(f"[DEBUG] item.user.id: {item.user.id}", file=sys.stderr)
        print(f"[DEBUG] Comparing: {str(item.user.id)} vs {str(current_user.id)}", file=sys.stderr)

        if str(item.user.id) != str(current_user.id):
            print(f"[DEBUG] Permission denied: item owner {str(item.user.id)} != current user {str(current_user.id)}", file=sys.stderr)
            return jsonify({"msg": "Unauthorized"}), 403

        # 处理允许更新的字段
        allowed_fields = ['name', 'description', 'category', 'status', 'location', 'contact']
        
        for key, value in data.items():
            if key in allowed_fields and hasattr(item, key):
                setattr(item, key, value)
        
        # 特殊处理日期字段
        if 'date' in data and data['date']:
            try:
                from datetime import datetime
                # 解析ISO格式的日期字符串
                item.date = datetime.fromisoformat(data['date'].replace('Z', '+00:00'))
            except Exception as e:
                print(f"Date parsing error: {e}", file=sys.stderr)
                # 如果日期解析失败，使用当前时间
                item.date = datetime.datetime.now()
        
        item.save()
        return jsonify({"msg": "帖子更新成功", "item": item.to_json()}), 200
    except Item.DoesNotExist:
        return jsonify({"msg": "帖子不存在"}), 404
    except Exception as e:
        print(f"Error in update_item: {e}", file=sys.stderr)
        return jsonify({"msg": "帖子更新失败", "error": str(e)}), 500

def get_my_claims(current_user):
    """
    获取用户认领的物品列表
    """
    try:
        claimed_items = Item.objects(claimed_by=current_user)
        return jsonify([item.to_json() for item in claimed_items]), 200
    except Exception as e:
        print(f"Error in get_my_claims: {e}")
        return jsonify({'msg': f'获取认领列表失败: {str(e)}'}), 500