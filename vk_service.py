from api_client import call_vk_api, VKAPIException
from typing import Dict, List, Optional, Any


def fetch_user_profile(identifier: str) -> Optional[Dict[str, Any]]:
    try:
        response = call_vk_api('users.get', {
            'user_ids': identifier,
            'fields': 'deactivated'
        })
        return response[0] if response else None
    except VKAPIException as e:
        if e.code not in [113, 18]:
            print(f"ERROR: Profile fetch error: {e.message}")
        return None

def fetch_friends(user_id: int, count: int = 100) -> Dict[str, Any]:
    try:
        return call_vk_api('friends.get', {
            'user_id': user_id,
            'count': count,
            'fields': 'first_name,last_name,deactivated'
        })
    except VKAPIException as e:
        if e.code in [15, 30, 18]:
            return {'count': 0, 'items': []}
        raise

def fetch_albums(user_id: int) -> List[Dict[str, Any]]:
    try:
        response = call_vk_api('photos.getAlbums', {
            'owner_id': user_id,
            'need_system': 1
        })
        return response.get('items', [])
    except VKAPIException as e:
        if e.code in [15, 18, 30, 200]:
            return []
        raise