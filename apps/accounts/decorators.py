from functools import wraps
from django.http import JsonResponse

def duke_only(view_func):
    """
    Decorator to restrict access to users with nobility <= 3 (Dukes or higher).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.nobility > 3:  
            return JsonResponse({"error": "Permission denied. Must be Duke or higher."}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
