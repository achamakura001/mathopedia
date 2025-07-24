from flask_jwt_extended import get_jwt_identity

def get_current_user_id():
    """Helper function to get and validate current user ID from JWT"""
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return None
    try:
        return int(current_user_id)
    except (TypeError, ValueError):
        return None
