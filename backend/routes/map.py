from flask import Blueprint
from middleware.auth import token_required
from controllers.mapController import (
    get_items_in_viewport, 
    get_nearby_items, 
    update_item_location, 
    get_nearby_matches_for_item
)

# 创建一个名为 'map' 的 Blueprint
map_bp = Blueprint('map_bp', __name__)

# GET /api/map/viewport - 获取地图视野内的物品标记点 (公开)
@map_bp.route('/map/items', methods=['GET'])
def route_get_items_in_viewport():
    return get_items_in_viewport()

# GET /api/map/nearby - 根据经纬度查询附近的物品 (公开)
@map_bp.route('/map/nearby', methods=['GET'])
def route_get_nearby_items():
    # This endpoint can be public or protected, depending on requirements.
    # If it needs to be protected, add @token_required and handle user_id.
    return get_nearby_items()

# 更新物品的地理位置 (这是一个示例，实际中可能并入物品更新的接口)
@map_bp.route('/map/items/<item_id>/location', methods=['PUT'])
@token_required
def route_update_item_location(user_id, item_id):
    # The controller function needs the full user object.
    from models.User import User
    current_user = User.objects.get(id=user_id)
    return update_item_location(current_user, item_id)

# 获取指定物品周边的匹配物品
@map_bp.route('/map/items/<item_id>/nearby-matches', methods=['GET'])
def route_get_nearby_matches_for_item(item_id):
    return get_nearby_matches_for_item(item_id) 