from .models import get_user_role

def role(request):
    """Context processor to add role to every template"""
    if request.user.is_authenticated:
        role = get_user_role(request.user)
    else:
        role = None
    return {'role': role}