from django.shortcuts import redirect
from django.http import JsonResponse

def login_required(f):
    def decorated_function(request, *args, **kwargs):
        if "current_user" in request.session:
            if request.session["current_user"] is not None:
                pass
            else:
                return redirect(f'/login?then={request.path}')
        else:
             return redirect(f'/login?then={request.path}')
        return f(request, *args, **kwargs)

    return decorated_function

def login_required_json_response(f):
    def decorated_function_for_login_required_json_response(request, *args, **kwargs):
        if "current_user" in request.session:
            if request.session["current_user"] is not None:
                pass
            else:
                return JsonResponse({"status": "error", "message":"user not logged in"}, status=403)
        else:
             return JsonResponse({"status": "error", "message":"user not logged in"}, status=403)
        return f(request, *args, **kwargs)

    return decorated_function_for_login_required_json_response