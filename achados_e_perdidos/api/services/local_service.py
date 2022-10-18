from ..models import Local


def get_local_by_user_id(user_id):
    return Local.objects.get(user_id=user_id)