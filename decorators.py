from django.shortcuts import redirect

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