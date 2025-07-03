from flask import Blueprint
from controllers.itemController import (
    create_item,
    get_all_items,
    get_item_by_id,
    update_item,
    delete_item,
    add_comment_to_item,
    search_items,
    get_my_claims
)
from middleware.auth import token_required

item_bp = Blueprint('item_bp', __name__)

@item_bp.route('/items', methods=['POST'])
@token_required
def create_item_route(current_user):
    return create_item(current_user)

@item_bp.route('/items', methods=['GET'])
def get_all_items_route():
    return get_all_items()

@item_bp.route('/items/search', methods=['GET'])
def search_items_route():
    return search_items()

@item_bp.route('/items/<item_id>', methods=['GET'])
def get_item_by_id_route(item_id):
    return get_item_by_id(item_id)

@item_bp.route('/items/<item_id>/comments', methods=['POST'])
@token_required
def add_comment_route(current_user, item_id):
    return add_comment_to_item(current_user, item_id)

@item_bp.route('/items/<item_id>', methods=['PUT'])
@token_required
def update_item_route(current_user, item_id):
    return update_item(current_user, item_id)

@item_bp.route('/items/<item_id>', methods=['DELETE'])
@token_required
def delete_item_route(current_user, item_id):
    return delete_item(current_user, item_id)