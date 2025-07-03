from flask import request, jsonify
from models.Item import Item

# 注意：MongoEngine的PointField存储格式为 [经度(longitude), 纬度(latitude)]

def get_items_in_viewport():
    """
    获取地图视野内的物品标记点
    GET /api/map/items?ne_lng=xx&ne_lat=xx&sw_lng=xx&sw_lat=xx
    """
    try:
        # 验证并获取坐标参数
        ne_lat = float(request.args.get('ne_lat'))
        ne_lng = float(request.args.get('ne_lng'))
        sw_lat = float(request.args.get('sw_lat'))
        sw_lng = float(request.args.get('sw_lng'))

        # 定义地图边界框
        box = [[sw_lng, sw_lat], [ne_lng, ne_lat]]

        # 使用 MongoEngine 的 apatial queries (地理空间查询)
        # 'coordinates__within_box' 查找 'coordinates' 字段在 'box' 定义的矩形内的所有文档
        items = Item.objects(coordinates__within_box=box).limit(100) # 限制返回100条

        result = [{
            'id': str(item.id),
            'name': item.name,
            'status': item.status,
            'category': item.category,
            'coordinates': {
                'longitude': item.coordinates['coordinates'][0],
                'latitude': item.coordinates['coordinates'][1]
            }
        } for item in items]

        return jsonify(result)

    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid or missing coordinate parameters'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve items', 'error': str(e)}), 500

def update_item_location(current_user, item_id):
    """
    更新物品的地理位置
    PUT /api/items/<item_id>/location
    """
    try:
        item = Item.objects(id=item_id).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        
        # 验证是否是物品的发布者
        if item.user.id != current_user.id:
            return jsonify({'message': 'Unauthorized to modify this item'}), 403

        data = request.get_json()
        if 'longitude' not in data or 'latitude' not in data:
            return jsonify({'message': 'Missing longitude or latitude'}), 400

        lng = float(data['longitude'])
        lat = float(data['latitude'])

        # 更新坐标
        item.coordinates = [lng, lat]
        item.save()
        
        return jsonify({'message': 'Location updated successfully'}), 200

    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid coordinate format'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to update location', 'error': str(e)}), 500

def get_nearby_items():
    """
    根据经纬度查询附近的物品
    GET /api/map/nearby?lng=xx&lat=xx&radius_km=xx
    """
    try:
        lng = float(request.args.get('lng'))
        lat = float(request.args.get('lat'))
        # 将半径从公里转换为米
        radius_m = float(request.args.get('radius_km', 1)) * 1000 

        # 使用 'coordinates__near' 进行查询
        # 它会返回按距离中心点从近到远排序的文档
        point = [lng, lat]
        items = Item.objects(coordinates__near=point, coordinates__max_distance=radius_m).limit(50)

        result = [{
            'id': str(item.id),
            'name': item.name,
            'status': item.status,
            'category': item.category,
            'location': item.location,
            'coordinates': {
                'longitude': item.coordinates['coordinates'][0],
                'latitude': item.coordinates['coordinates'][1]
            }
        } for item in items]

        return jsonify(result)

    except (ValueError, TypeError):
        return jsonify({'message': 'Invalid or missing coordinate parameters'}), 400
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve nearby items', 'error': str(e)}), 500

def get_nearby_matches_for_item(item_id):
    """
    为一个指定ID的物品，查找其周边一定范围内的、状态相反的物品。
    GET /api/map/items/<item_id>/nearby-matches
    """
    try:
        # 1. 查找作为查询中心的物品
        center_item = Item.objects(id=item_id).first()
        if not center_item:
            return jsonify({'message': 'Center item not found'}), 404
            
        # 2. 检查该物品是否有坐标
        if not center_item.coordinates:
            return jsonify({'message': 'Center item does not have location data'}), 400

        # 3. 确定目标状态和搜索参数
        target_status = 'found' if center_item.status == 'lost' else 'lost'
        center_point = center_item.coordinates['coordinates'] # [lng, lat]
        search_radius_m = 2000 # 默认搜索半径为2000米

        # 4. 执行地理空间查询
        nearby_matches = Item.objects(
            status=target_status,
            coordinates__near=center_point,
            coordinates__max_distance=search_radius_m
        ).limit(50) # 最多返回50个匹配项

        # 5. 格式化并返回结果
        result = [{
            'id': str(item.id),
            'name': item.name,
            'status': item.status,
            'location': item.location,
            'coordinates': {
                'longitude': item.coordinates['coordinates'][0],
                'latitude': item.coordinates['coordinates'][1]
            }
        } for item in nearby_matches if item.coordinates]

        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'message': 'Failed to get nearby matches', 'error': str(e)}), 500 